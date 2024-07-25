FROM python:3.9-slim

WORKDIR /app

COPY ./common ./
COPY ./orchestrator .
COPY ./dataset/offers.csv ./dataset/offers.csv

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV PYTHONUNBUFFERED=1 

RUN chmod +x wait.sh


CMD ["./wait.sh", "30", "python", "orchestrator.py"]
