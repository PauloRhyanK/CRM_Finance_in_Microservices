.PHONY: help build up down logs clean restart ps

help:
	@echo "Available commands:"
	@echo "  make build    - Build all Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - View logs from all services"
	@echo "  make clean    - Remove all containers, images, and volumes"
	@echo "  make restart  - Restart all services"
	@echo "  make ps       - Show running containers"

build:
	docker compose build

up:
	docker compose up -d
	@echo "Services are starting..."
	@echo "API Gateway available at http://localhost"

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker compose down -v --rmi all

restart: down up

ps:
	docker compose ps
