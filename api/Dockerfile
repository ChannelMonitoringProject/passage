FROM python:3.13
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . ./api
CMD ["gunicorn", "--conf", "api/gunicorn_conf.py", "--bind", "0.0.0.0:80", "api.main:app"]
