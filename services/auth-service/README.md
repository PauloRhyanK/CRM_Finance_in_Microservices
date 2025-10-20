# Authentication Service

This is the authentication service for the TCC microservices project. It is responsible for handling user authentication, including login, registration, and token management.

## Project Structure

```
auth-service/
├── app/
│   ├── main.py        # Entry point for the authentication service
│   ├── models.py      # Data models for the authentication service
│   └── routes.py      # Route definitions for the authentication service
├── Dockerfile          # Dockerfile for building the authentication service image
├── requirements.txt    # Python dependencies for the authentication service
└── README.md           # Documentation for the authentication service
```

## Getting Started

To get started with the authentication service, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd tcc-microservices/services/auth-service
   ```

2. **Install dependencies**:
   Make sure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the service**:
   You can run the service locally using:
   ```bash
   python app/main.py
   ```

4. **Build and run with Docker**:
   To build and run the service using Docker, execute:
   ```bash
   docker build -t auth-service .
   docker run -p 5000:5000 auth-service
   ```

## API Endpoints

- **POST /login**: Authenticate a user and return a token.
- **POST /register**: Register a new user.
- **GET /user**: Retrieve user information (requires authentication).

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.