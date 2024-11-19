# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.10-slim

WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code to the working directory
COPY . .

# Expose the port that the application will run on
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]