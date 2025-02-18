# Use a suitable base image with Python
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's caching
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that your FastAPI app listens on (default is 80)
EXPOSE 80

# Define the command to run when the container starts
# Use Uvicorn to serve the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"] 
# app.main:app means the app instance is in the main.py file.
# --host 0.0.0.0 makes the server accessible from outside the container