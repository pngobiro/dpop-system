# Use Python 3.9 base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV OPENAI_API_KEY=your_openai_api_key_here

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    ffmpeg \
    postgresql-client \
    netcat-openbsd \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy static files first
COPY static/ /code/static/

# Copy the rest of the project files
COPY . /code/

# Create necessary directories and collect static files
RUN mkdir -p /code/data/db && \
    mkdir -p /code/staticfiles && \
    mkdir -p /code/static/assets/img/brand

# Set permissions as root
RUN chmod +x /code/entrypoint.sh && \
    chmod -R 755 /code && \
    chmod -R 777 /code/data && \
    chmod -R 755 /code/staticfiles && \
    chmod -R 755 /code/static

# Command to run
CMD ["/bin/bash", "/code/entrypoint.sh"]