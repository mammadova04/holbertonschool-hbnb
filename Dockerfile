FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

VOLUME /app/data

ENV PORT 5000

EXPOSE $PORT

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
