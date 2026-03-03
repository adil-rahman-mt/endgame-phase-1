FROM python:3.14-slim

WORKDIR /app

ENV REDIS_STORAGE_URI = os.environ.get('REDIS_STORAGE_URI')

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "--app", "run", "run"]