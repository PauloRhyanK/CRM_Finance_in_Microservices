#!/bin/bash

# Build Docker images for all services and the API gateway

# Navigate to the gateway directory and build the Docker image
echo "Building API Gateway..."
cd gateway
docker build -t tcc-gateway .

# Navigate to each service directory and build their Docker images
for service in auth-service user-service product-service order-service; do
    echo "Building $service..."
    cd services/$service
    docker build -t tcc-$service .
    cd ../../..
done

echo "All services and API Gateway have been built successfully."