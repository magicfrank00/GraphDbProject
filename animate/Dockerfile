FROM python:3.9-slim

WORKDIR /app

COPY ./common ./
COPY ./animate ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1 
EXPOSE 5000

CMD ["python", "animate.py"]
