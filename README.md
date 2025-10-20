# CRM_Finance_in_Microservices
This repository is a migration for microservices from monolithic, for work graduation.

## Architecture

This project implements a microservices architecture for a CRM Finance system with the following services:

### Services

1. **API Gateway** (Nginx)
   - Entry point for all client requests
   - Routes requests to appropriate microservices
   - Runs on port 80

2. **Auth Service** (Python/FastAPI)
   - Handles user authentication and authorization
   - JWT token generation and validation
   - User registration and login
   - Internal port: 8001

3. **Customer Service** (Python/FastAPI)
   - Manages customer data and operations
   - CRUD operations for customer records
   - Internal port: 8002

4. **Product Service** (Python/FastAPI)
   - Manages product catalog
   - Product inventory management
   - Internal port: 8003

5. **Interaction Service** (Python/FastAPI)
   - Tracks customer interactions
   - Manages calls, emails, meetings, and notes
   - Internal port: 8004

## Project Structure

```
├── .git/                  # Git repository
├── docker-compose.yml     # Docker Compose orchestration
├── /api-gateway/
│   ├── Dockerfile
│   └── nginx.conf
├── /auth-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       └── main.py
├── /customer-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       └── main.py
├── /product-service/  
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       └── main.py
└── /interaction-service/ 
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── __init__.py
        └── main.py
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:
```bash
git clone https://github.com/PauloRhyanK/CRM_Finance_in_Microservices.git
cd CRM_Finance_in_Microservices
```

2. Build and start all services:
```bash
docker compose up --build
```

3. Access the services:
   - API Gateway: http://localhost
   - Auth Service: http://localhost/auth/
   - Customer Service: http://localhost/customers/
   - Product Service: http://localhost/products/
   - Interaction Service: http://localhost/interactions/

### API Documentation

Each service provides interactive API documentation via FastAPI:
- Auth Service: http://localhost/auth/docs
- Customer Service: http://localhost/customers/docs
- Product Service: http://localhost/products/docs
- Interaction Service: http://localhost/interactions/docs

### Stopping the Application

```bash
docker compose down
```

## Development

Each service is independently deployable and can be developed separately. The services communicate through HTTP REST APIs.

### Technology Stack

- **API Gateway**: Nginx
- **Backend Services**: Python 3.11, FastAPI, Uvicorn
- **Containerization**: Docker
- **Orchestration**: Docker Compose
