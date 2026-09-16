FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD python manage.py migrate && python manage.py loaddata  user.json && gunicorn root.wsgi:application -c gunicorn.conf.py