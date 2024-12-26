# Stage 1: Build the application
FROM python:3.12-slim AS build

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir

# Stage 2: Runtime environment
FROM python:3.12-slim AS runtime

# Set environment variables (optional: can be overridden via docker-compose)
ENV BG_COLOR "#f0f0f0"

# Create necessary directories for logs (optional)
RUN mkdir -p /var/log/flask /var/log/gunicorn
RUN chmod -R 755 /var/log/flask /var/log/gunicorn

# Set working directory
WORKDIR /app

# Copy dependencies from the build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy the application code (excluding any unnecessary files like tests, etc.)
COPY . .

# Expose the port for your Flask app (adjust to match your Flask configuration)
EXPOSE 5000

# Start the Flask application
CMD ["python", "consumer.py"]
