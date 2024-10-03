# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    pkg-config \
    libmariadb-dev \
    gcc && \
    rm -rf /var/lib/apt/lists/*

# Verify that pkg-config is installed
RUN pkg-config --version

# Set work directory
WORKDIR /code

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# set permission
RUN chmod +x ./entrypoint.sh

# entrypoint
ENTRYPOINT ["./entrypoint.sh"]