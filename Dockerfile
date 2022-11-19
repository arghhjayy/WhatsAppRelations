FROM ubuntu:20.04

COPY src/* /app/src/

COPY assets/* /app/assets/

COPY requirements.txt /app/

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN pip3 install -r /app/requirements.txt

WORKDIR /app/src/

CMD ["python3", "app.py"]

EXPOSE 5000