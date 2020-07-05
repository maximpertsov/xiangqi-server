release: python manage.py migrate --noinput
web: bin/start-pgbouncer-stunnel gunicorn web.wsgi --log-file -
