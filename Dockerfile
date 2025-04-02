# Use official Python image with Debian Bullseye for better compatibility
FROM python:3.11-bullseye

# Environment variables to prevent .pyc files and enable real-time logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (compiler, PostgreSQL client libs, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev netcat && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies file and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Change to the Django app directory where manage.py is located
WORKDIR /app/library

# Default command: run pytest tests
CMD ["pytest"]
