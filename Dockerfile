# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.12-slim

WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code to the working directory
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "--host", "127.0.0.1 ", "--port", "8000", "app.main:app", "--reload"]