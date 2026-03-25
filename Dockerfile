# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables (FLASK_APP is helpful)
ENV FLASK_APP=app.py

# Run the application (Listening on 0.0.0.0 is critical for Docker)
CMD ["python", "app.py"]
