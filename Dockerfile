# Use Python 3.9 base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    ffmpeg \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

# Create data directory
RUN mkdir -p /code/data/db

# Set permissions as root
RUN chmod +x /code/entrypoint.sh && \
    chmod -R 755 /code && \
    chmod -R 777 /code/data

# Command to run
CMD ["/bin/bash", "/code/entrypoint.sh"]