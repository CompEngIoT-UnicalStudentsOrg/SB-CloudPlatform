FROM python:3.8-slim-buster

COPY . .
RUN pip3 install -r requirements.txt


CMD ["gunicorn", "-b", ":80", "app:app"]
