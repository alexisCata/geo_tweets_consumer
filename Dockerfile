FROM python:3.5

RUN apt-get update && apt-get install python3-pip -y

RUN mkdir -p /usr/local/twitter_consumer

COPY . /usr/local/twitter_consumer

WORKDIR /usr/local/twitter_consumer

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python3 web.py