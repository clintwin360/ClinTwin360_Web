release: python manage.py migrate --no-input
web: gunicorn clintwin.wsgi --timeout 2400 --log-file -