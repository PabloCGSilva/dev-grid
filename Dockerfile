FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y tini && apt-get clean
RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["python", "app.py"]
