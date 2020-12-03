release: python manage.py migrate --noinput
web: gunicorn -w 3 -k uvicorn.workers.UvicornWorker web.asgi:application
