# Makefile for TCC Microservices Project

.PHONY: build run clean

build:
	docker-compose build

run:
	docker-compose up

clean:
	docker-compose down --volumes --remove-orphans

test:
	@echo "Running integration tests..."
	# Add commands to run your tests here

help:
	@echo "Makefile commands:"
	@echo "  build   - Build the Docker images"
	@echo "  run     - Start the services"
	@echo "  clean   - Stop and remove containers, networks, images, and volumes"
	@echo "  test    - Run integration tests"
	@echo "  help    - Show this help message"