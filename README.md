# TCC Microservices Project

This project is a microservices architecture for a TCC (Trabalho de Conclusão de Curso) application. It consists of multiple services, including an API gateway and several microservices, each responsible for different functionalities.

## Project Structure

```
tcc-microservices
├── gateway
│   ├── app
│   │   ├── main.py          # Entry point for the API gateway service
│   │   ├── routes
│   │   │   └── __init__.py  # Route definitions for the API gateway
│   │   └── config.py        # Configuration settings for the API gateway
│   ├── Dockerfile            # Dockerfile for the API gateway service
│   ├── requirements.txt      # Python dependencies for the API gateway service
│   └── README.md             # Documentation for the API gateway service
├── services
│   ├── auth-service
│   │   ├── app
│   │   │   ├── main.py      # Entry point for the authentication service
│   │   │   ├── models.py    # Data models for the authentication service
│   │   │   └── routes.py    # Route definitions for the authentication service
│   │   ├── Dockerfile        # Dockerfile for the authentication service
│   │   ├── requirements.txt  # Python dependencies for the authentication service
│   │   └── README.md         # Documentation for the authentication service
│   ├── user-service
│   │   ├── app
│   │   │   ├── main.py      # Entry point for the user service
│   │   │   ├── models.py    # Data models for the user service
│   │   │   └── routes.py    # Route definitions for the user service
│   │   ├── Dockerfile        # Dockerfile for the user service
│   │   ├── requirements.txt  # Python dependencies for the user service
│   │   └── README.md         # Documentation for the user service
│   ├── product-service
│   │   ├── app
│   │   │   ├── main.py      # Entry point for the product service
│   │   │   ├── models.py    # Data models for the product service
│   │   │   └── routes.py    # Route definitions for the product service
│   │   ├── Dockerfile        # Dockerfile for the product service
│   │   ├── requirements.txt  # Python dependencies for the product service
│   │   └── README.md         # Documentation for the product service
│   └── order-service
│       ├── app
│       │   ├── main.py      # Entry point for the order service
│       │   ├── models.py    # Data models for the order service
│       │   └── routes.py    # Route definitions for the order service
│       ├── Dockerfile        # Dockerfile for the order service
│       ├── requirements.txt  # Python dependencies for the order service
│       └── README.md         # Documentation for the order service
├── infra
│   ├── docker-compose.yml    # Docker Compose setup for the project
│   ├── nginx
│   │   └── nginx.conf        # Nginx configuration for reverse proxy
│   └── env
│       └── .env.example      # Example environment variables
├── scripts
│   ├── build.sh              # Script to build Docker images
│   └── run.sh                # Script to run Docker containers
├── tests
│   └── integration
│       └── README.md         # Documentation for integration tests
├── Makefile                  # Commands for building and managing the project
└── README.md                 # Overall documentation for the project
```

## Getting Started

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd tcc-microservices
   ```

2. **Build the Docker images**:
   ```
   ./scripts/build.sh
   ```

3. **Run the services**:
   ```
   ./scripts/run.sh
   ```

## Services Overview

- **API Gateway**: Acts as a single entry point for all client requests and routes them to the appropriate microservices.
- **Auth Service**: Handles user authentication and authorization.
- **User Service**: Manages user-related operations.
- **Product Service**: Manages product-related operations.
- **Order Service**: Handles order processing and management.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.