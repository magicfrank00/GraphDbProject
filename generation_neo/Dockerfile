FROM neo4j:latest

WORKDIR /app

COPY ./common ./
COPY ./generation_neo .

EXPOSE 80

ENV PYTHONUNBUFFERED=1 

RUN mkdir dataset

RUN chmod +x ingest.sh
RUN chmod +x wait.sh

RUN chmod -R 777 /app


CMD ["./wait.sh", "30", "./ingest.sh"]

