FROM python:3.11
COPY . /

RUN pip3 install --upgrade pip

RUN pip3 install requests
RUN pip3 install fastapi
RUN pip3 install fastapi_responses
RUN pip3 install uvicorn
RUN pip3 install elasticsearch
RUN pip install elasticsearch_dsl

RUN apt update -y
RUN apt upgrade -y
RUN apt install curl -y

EXPOSE 80

ENV host=https://hotels.es.us-central1.gcp.cloud.es.io:443
ENV userName=elastic
ENV password=Jx6IFj52PlDIujxrXLMaVTtP
ENV indexName=hotels

ENTRYPOINT [ "python" ,"SearchApi.py"]
