# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container to /app
RUN mkdir -p /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./Source/* /app/

# Install Python packages
RUN pip install --no-cache-dir -r requirements
