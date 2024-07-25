FROM python:3.9-slim as PY


WORKDIR /app

COPY ./common ./
COPY ./generation .
COPY ./generation/ingest.sh ./dataset_ingest/ingest.sh 

#COPY ./dataset/offers.csv ./dataset/offers.csv

RUN apt-get update && apt-get install -y netcat-openbsd 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV PYTHONUNBUFFERED=1 

# RUN mkdir dataset

RUN chmod +x generation.sh
RUN chmod +x wait.sh


CMD ["./generation.sh"]

