# Use Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY gunicorn.conf.py .
COPY setup.py .

# Install the package in development mode
RUN pip install -e .

# Create logs directory with proper permissions
RUN mkdir -p logs && chmod 777 logs

# Set environment variables
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Run the application with Gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:create_app"]
