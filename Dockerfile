# # Use the official Python image
# FROM python:3.9-slim

# # Set the working directory
# WORKDIR /app

# # Copy the requirements file into the container
# COPY requirements.txt .

# # Install the dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . .

# # Expose the port the app runs on
# EXPOSE 5000

# # Command to run the application
# CMD ["python", "app.py"]

# Dockerfile

FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Command to run the application
CMD ["python", "app.py"]