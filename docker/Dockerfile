# Use python slim image
FROM python:3.11-slim

# Add security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create logs directory with proper permissions
RUN mkdir -p logs && chmod 777 logs

# Copy only necessary files
COPY app/ ./app/
COPY gunicorn.conf.py .
COPY setup.py .

# Install the package in development mode
RUN pip install -e .

# Set non-root user for security
RUN useradd -m myuser
USER myuser

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=production

# Run the application with Gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:create_app()"]