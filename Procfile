release: python manage.py migrate --noinput
web: bin/start-pgbouncer-stunnel gunicorn -w 3 -k uvicorn.workers.UvicornWorker web.asgi:application
