# Base image
FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirement.txt


# Expose port 5000 for the Flask app to listen on
EXPOSE 5000


# Start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
