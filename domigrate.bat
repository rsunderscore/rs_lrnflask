set FLASK_APP=main.py
set FLASK_ENV=development 
@rem or flask run
@rem or flask shell
flask migrate
@rem or flask db init
@rem or flask db migrate -m "message for migration"
@rem or flask db upgrade (apply the migration)
@rem or flask db upgrade --sql (to show sql)
@rem or flask db history (to show prior versions)
@rem or flask db downgrade <version>