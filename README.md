# rs_lrnflask
## notes from the book
Mastering Flask Web Development Second Edition
by Daniel Gaspar, Jack Stouffer

- supporting tech
  - git
  - python/pip
  - virtualenv - best practic is to sandbox your dev away from any system python implementations
  - flask
    - flask-sqlalchemy (add-on) - flask-oriented abstractiont to tie ORM to flask models
    - flask-migrate (comes with) - handles db schema updates and rollbacks
      - alembic (comes with?) - used to manage db schema change files
  - sqlalchemy

- quick app
  - layout of files
    - requirements.txt - package dependencies for the virtualenv
    - main.py - the appliation
      - must set env var: `FLASK_APP=main.py`
        - windows: set; UNIX: export
      - also set: `FLASK_ENV=development` - suppresses a warning that the server is not meant for prod and set debug mode
      - expected default is app.py
    - config.py
    - manage.py - used to extend flask shell
    - dockerfile - for container based implementations
- `flask run` - runs the local server
  - make sure you're in the proj directory so main.py is available
- `flask shell` - start a python shell in app context - used for troubleshooting and management

## models
- managed with sqlalchemy ORM - abstracted further by flask-sqlalchemy package (makes some commands less verbose)
- database uri == connection string (varies by db type)
  - includes uswername and PW (caution)
- [datatypes](https://docs.sqlalchemy.org/en/14/core/type_basics.html) - support varies by bakcing DB (e.g. sqlite has no date types - just string)
  - String, Integer, and Float types take an extra argument for length limit
  - String/Text - both translate to varchar? ❓ no, Text usually becomes CLOB; string becomes varchar
  - Integer
  - Float
  - Boolean - becomes 0 or 1 if db has no boolean type
  - Date/DateTime/Time
- operations
  - create - assign model object instance to var and use `db.session.add(instance)` and `db.session.commit()`
  - read - `<parentclass>.qeury` e.g. for User table it would be `res = User.query.all()` - subcommends
    - order_by()
    - filter_by() - **requires exact value**
    - filter() - params accept boolean operations (e.g. id > 10)
      -  other booleans in `sqlalchemy.sql.expression` e.g.  not_, or_
      -  `None` is automatically translated to NULL
    - limit(n) - return top n rows
    - first() - return top 1 row
    - get() - retrieve by primary key
  - update - `<query result>.update({dict_of:'new_values'})` ... **then commit**
  - delete - `res = <dbquery>` then `res.delete()` ... **then commit**
- versions/migrations managed with alembic via flask-migrate
- dependency types: one-one, one-many, many-many (requires implicit lookup table)
  - lookup table extends db.Table (lower level than db.Model) 

- <span style='color:red;'>NOTE</span> migrate doesn't handle indexes - need to check logs to make sure indexes are updated as needed
- gotchas
    - render_pagination macro is called in the templates but never written out in the text
    - in some places ORM uses explicit sql text (e.g. in order_by statement of get_sidebar_data) which is not valid in current implementation and must be explictly placed in `text()` method from sqlalchemy.sql module.
    - <span style='color:red;font-weight:bold;'>NOTE</span> SQLite and MySQL/MyISAM engines do not enforce relationship constraints - by default - can be enabled but causes additional overhead
    - sqlite doesn't support foreign key contraints by default - has to be turned on (performance hit)
    ```python
        ...
        from sqlalchemy import func, event
        from sqlalchemy.engine import Engine
        ...
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        
    ```
    - sqlite doesn't suport alter command for alembic migrations - solution is to alter env.py in the migrations folder.  This needs to be set for both online and offline mgiration sectiosn (2 places).
        - if this was forgotten after running a migrate command go into the migrations/versions folder and delete the faulty migration py file. Then run migrate again.
    ```python
        context.configure(..., render_as_batch=True, ...)
    ```
## Templates
- managed with jinja package
- code blockes are `{{ }}`
  - some javascript frameworks also use this convention so need to escape the JS stuff with `{% raw %}` and end with `{% endraw %}`
- comments are `{# #}`
- flow control uses `{% %}` (e.g. if/for )
  - most blocks are closed with `end<keyword>` e.g. `{% endif %}` or `{% endfor %}`
- syntax is diff than python itself (but similar)
- filters - pipe a variable to a filter to change the formatting - example filters:
  - default - specify a default to use if the var is None; can also give default when var==False by setting 2nd param to True
  - escape - escape html (rather than rendering it) this appears to be the default per 'safe' filter below
  - float - convert to float representation
  - int - convert number to integer (truncate the decimal portion)
  - join - combine iterables into a single string using the specified separator
  - length - jinja version of python len (how long is the var)
  - round - round to specified digits - params: 'common', 'floor', 'ceiling'
  - safe - html is escaped by default - if you wante it rendered you have to specify that it is safe
  - title - present string in title case
  - tojson - convert the var (e.g. a dict) to json format
  - truncate - abbreviate long text and follow with ellipses; doesn't split a word unless True is passed as second param
  - custom - define your own custom functions with the decorator `@app.template_filter`
    - first param is assumed to be the var left of the pipe
    - add it to the filters dictionary of the **jinja_env** object in our _main.py_
- macros - convenience to re-use segments of the template (html/code) 
