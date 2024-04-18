# Dockerfile
FROM python:3.10.11

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all application files
COPY . .

# Command to run the main application
CMD ["python", "main.py"]

# You might want to add a secondary command to handle jobs, or manage it within your Python application
