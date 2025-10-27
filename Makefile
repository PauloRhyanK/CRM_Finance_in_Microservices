# Makefile

# --- Comandos Docker Compose Básicos ---
up:
	docker-compose up --build -d

down:
	docker-compose down -v

logs:
	docker-compose logs -f $(filter-out $@,$(MAKECMDGOALS))

# --- ALVO PARA A CONFIGURAÇÃO INICIAL COMPLETA ---
setup: down up wait-for-dbs migrate-all

# --- Alvo para esperar os bancos estarem prontos ---
# (Pode precisar ajustar o sleep ou usar waits mais robustos)
wait-for-dbs:
	@echo "Aguardando bancos de dados estarem prontos..."
	@sleep 15 

# --- Alvo para rodar TODAS as migrações iniciais ---
migrate-all: migrate-auth migrate-customer migrate-product migrate-interaction

# --- Alvos individuais para migrações (primeira vez) ---
migrate-auth:
	@echo "Executando migrações para auth-service..."
	docker-compose exec auth-service python manage.py db init || true 
	docker-compose exec auth-service python manage.py db migrate -m "Init auth schema" || true
	docker-compose exec auth-service python manage.py db upgrade

migrate-customer:
	@echo "Executando migrações para customer-service..."
	docker-compose exec customer-service python manage.py db init || true
	docker-compose exec customer-service python manage.py db migrate -m "Init customer schema" || true
	docker-compose exec customer-service python manage.py db upgrade

migrate-product:
	@echo "Executando migrações para product-service..."
	docker-compose exec product-service python manage.py db init || true
	docker-compose exec product-service python manage.py db migrate -m "Init product schema" || true
	docker-compose exec product-service python manage.py db upgrade

migrate-interaction:
	@echo "Executando migrações para interaction-service..."
	docker-compose exec interaction-service python manage.py db init || true
	docker-compose exec interaction-service python manage.py db migrate -m "Init interaction schema" || true
	docker-compose exec interaction-service python manage.py db upgrade
# --- Alvo para gerar NOVAS migrações (quando você alterar models.py) ---
# Uso: make migrate service=customer-service m="Sua mensagem aqui"
migrate: check-args
	@echo "Gerando nova migração para $(service)..."
	docker-compose exec $(service) python manage.py db migrate -m "$(m)"

# --- Alvo para APLICAR novas migrações (ou todas) ---
# Uso: make upgrade service=customer-service  (ou make upgrade-all)
upgrade: check-service
	@echo "Aplicando migrações para $(service)..."
	docker-compose exec $(service) python manage.py db upgrade

upgrade-all:
	@echo "Aplicando migrações para todos os serviços..."
	docker-compose exec auth-service python manage.py db upgrade
	docker-compose exec customer-service python manage.py db upgrade
	docker-compose exec product-service python manage.py db upgrade
	docker-compose exec interaction-service python manage.py db upgrade


# --- Verificações ---
check-args:
ifndef service
	$(error service is undefined. Usage: make migrate service=<service_name> m="<message>")
endif
ifndef m
	$(error m is undefined. Usage: make migrate service=<service_name> m="<message>")
endif

check-service:
ifndef service
	$(error service is undefined. Usage: make upgrade service=<service_name>)
endif

.PHONY: up down logs setup wait-for-dbs migrate-all migrate-auth migrate-customer migrate-product migrate-interaction migrate upgrade upgrade-all check-args check-service