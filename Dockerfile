FROM ubuntu:20.04

COPY src/* /app/src/

COPY assets/* /app/assets/

COPY requirements.txt /app/

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN pip3 install -r /app/requirements.txt

WORKDIR /app/src/

CMD ["gunicorn", "--worker-connections=3", "--bind=0.0.0.0:5000", "app:app"]

EXPOSE 5000