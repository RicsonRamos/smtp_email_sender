# Use a lightweight Python image
FROM python:3.11-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from generating .pyc files and enable real-time logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first (optimizes Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Create necessary folders if they don't exist (security)
RUN mkdir -p logs data attachments templates

# Command to run the script
CMD ["python", "runner.py"]