FROM python:3.9-slim

WORKDIR /app

COPY ./common ./
COPY ./analyze .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV PYTHONUNBUFFERED=1 

CMD ["python3", "./analyze.py"]
