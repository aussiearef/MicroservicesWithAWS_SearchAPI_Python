# Use the official Python image as the parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
pip3 install --upgrade pip

pip3 install typing
pip3 install fastapi
pip3 install fastapi.responses
pip3 install elasticsearch
pip3 install elasticsearch_dsl
pip3 install elasticsearch.exceptions


# Make port 8080 available to the world outside this container
EXPOSE 80

# Run the command to start the application
CMD [ "python", "SearchApi.py" ]
