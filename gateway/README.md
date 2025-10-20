# API Gateway

This directory contains the implementation of the API Gateway for the TCC microservices project. The API Gateway acts as a single entry point for all client requests and routes them to the appropriate microservices.

## Structure

- **app/**: Contains the main application code for the API Gateway.
  - **main.py**: The entry point for the API Gateway service, initializing the application and setting up routing.
  - **routes/**: Contains route definitions that connect to various microservices.
    - **__init__.py**: Initializes the routes for the API Gateway.
  - **config.py**: Contains configuration settings such as service URLs and environment variables.

- **Dockerfile**: Instructions for building the Docker image for the API Gateway service.

- **requirements.txt**: Lists the Python dependencies required for the API Gateway service.

## Usage

To build and run the API Gateway, use the provided scripts in the `scripts/` directory or follow the instructions in the `infra/docker-compose.yml` file. Make sure to configure the necessary environment variables in the `.env` file.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Please ensure that your code adheres to the project's coding standards and includes appropriate tests.