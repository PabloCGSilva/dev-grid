#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Print each command before executing it (for debugging)
set -x

# Define environment variables
export OPEN_WEATHER_API_KEY=1d48d72ff11b7280f11e0faa87b2b3f9

# Build the Docker image for testing
docker build -t app_python_tests .

# Stop and remove any existing container with the same name
docker stop weather_data_collector || true
docker rm weather_data_collector || true

# Run the Docker container in detached mode
docker run -d -p 5000:5000 --name weather_data_collector app_python_tests

# Wait for the Flask app to start inside the container
sleep 5

# Run the tests inside the Docker container
docker exec weather_data_collector sh -c "pytest"

# Clean up: stop and remove the container after tests
docker stop weather_data_collector
docker rm weather_data_collector
