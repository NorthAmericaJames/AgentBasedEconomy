# Base image for Evolutionary AI ecosystem
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir streamlit

# Default command runs simulation (placeholder)
CMD ["python", "-c", "print('Container for Evolutionary AI environment')"]
