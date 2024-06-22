# Start with an appropriate Alpine Linux base image with Python
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV APP_PORT=5000

# Install dependencies
RUN apk update && \
    apk add --no-cache gcc musl-dev linux-headers

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the application port
EXPOSE ${APP_PORT}

# Define a volume for data persistence
VOLUME ["/app/data"]

# Run the application with Gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${APP_PORT} app:app"]
 
