# Use the official Python image as the parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --upgrade pip

RUN pip3 install typing
RUN pip3 install requests
RUN pip3 install fastapi
RUN pip3 install fastapi.responses
RUN pip3 install uvicorn
RUN pip3 install elasticsearch
RUN pip3 install elasticsearch_dsl

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y curl

# Make port 8080 available to the world outside this container
EXPOSE 80

# Set Environment Variables

ENV host=https://hotels.es.us-central1.gcp.cloud.es.io:443
ENV userName=elastic
ENV password=Jx6IFj52PlDIujxrXLMaVTtP
ENV indexName=hotels

# Run the command to start the application
CMD [ "python", "SearchApi.py" ]
