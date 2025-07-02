# Use Python 3.9 base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install system dependencies (this layer will be cached)
RUN apt-get update

# Step 2: Install packages and clean up. This layer will be rebuilt only if packages change.
RUN apt-get install -y --no-install-recommends     apt-utils     ffmpeg     postgresql-client     netcat-openbsd     poppler-utils     && rm -rf /var/lib/apt/lists/*     && apt-get clean

# Copy and install Python dependencies first (separate layer for better caching)
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories for static files
RUN mkdir -p /code/staticfiles \
    /code/static/assets/img/brand \
    /code/DCRT

# Copy entrypoint script and make it executable
COPY entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh

# Copy static files (if they don't change often)
COPY static/ /code/static/

# Copy the rest of the application code (this should be last)
COPY . /code/

# Set final permissions (simplified)
RUN chmod -R 755 /code/staticfiles && \
    chmod -R 755 /code/static

# Command to run
CMD ["/bin/bash", "/code/entrypoint.sh"]