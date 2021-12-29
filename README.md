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
  - update - 
  - delete - 
- versions/migrations managed with alembic via flask-migrate
- dependency types: one-one, one-many, many-many (requires implicit lookup table)
  - lookup table extends db.Table (lower level than db.Model)
- <span style='color:red;font-weight:bold;'>NOTE</span> SQLite and MySQL/MyISAM engines do not enforce relationship constraints - by default - can be enabled but causes additional overhead
- <span style='color:red;'>NOTE</span> migrate doesn't handle indexes - need to check logs to make sure indexes are updated as needed

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
