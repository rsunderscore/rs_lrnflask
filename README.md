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
      - must set env var: FLASK_APP=main.py
        - windows: set; UNIX: export
      - expected default is app.py
    - config.py
    - dockerfile - for container based implementations
- `flask run` - runs the local server
- `flask shell` - start a python shell in app context - used for troubleshooting and management

## models
- managed with sqlalchemy ORM - abstracted further by flask-sqlalchemy package (makes some commands less verbose)
- versions/migrations managed with alembic via flask-migrate
- dependency types: one-one, one-many, many-many (requires implicit lookup table)
  - lookup table extends db.Table (lower level than db.Model)
- SQLite and MySQL/MyISAM engines do not enforce relationship constraints - by default - can be enabled but causes additional overhead

## Templates
- managed with jinja package
- code blockes are {{ }}
- comments are {# #}
- flow control uses {% %} (e.g. if/for
- syntax is diff than python
