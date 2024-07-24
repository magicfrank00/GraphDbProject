FROM python:3.9-slim

WORKDIR /app

COPY ./common ./
COPY ./dequeue .

RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV PYTHONUNBUFFERED=1 

RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "neo4j", "7474", "python", "dequeue.py"]
