#!/bin/bash

# Navigate to the infra directory and start the Docker containers
cd ../infra
docker-compose up -d

# Wait for services to start
sleep 10

# Optionally, you can run tests or any other commands here
# For example, you could run integration tests if they are set up
# cd ../tests/integration
# ./run_tests.sh

echo "All services are up and running."