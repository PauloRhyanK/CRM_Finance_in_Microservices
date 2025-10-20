# Product Service

This is the Product Service of the TCC microservices architecture. It is responsible for managing product-related operations.

## Structure

The Product Service follows a microservices architecture and is structured as follows:

- **app/**: Contains the main application code.
  - **main.py**: Entry point for the Product Service. Initializes the Flask application and sets up routes.
  - **models.py**: Defines the data models used in the Product Service.
  - **routes.py**: Contains the route definitions for the Product Service.

## Docker

The Product Service is containerized using Docker. The `Dockerfile` in this directory contains the instructions for building the Docker image.

## Requirements

The `requirements.txt` file lists all the Python dependencies required for the Product Service. Make sure to install these dependencies before running the service.

## Running the Service

To run the Product Service, you can use the provided scripts or Docker commands. Refer to the main project documentation for more details on how to set up and run the entire microservices architecture.