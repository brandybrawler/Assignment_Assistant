ARG VARIANT=3.11.2
FROM python:${VARIANT}-slim AS base

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

CMD ["python3", "main.py"]

# Expose port
EXPOSE 8000
