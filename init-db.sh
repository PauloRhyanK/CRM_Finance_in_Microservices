#!/bin/bash
set -e

# Executa o psql como o superusuário 'postgres'
# ${POSTGRES_USER} e ${POSTGRES_PASSWORD} são fornecidos pelo Docker Compose
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $AUTH_DB_NAME;
    CREATE DATABASE $CUSTOMER_DB_NAME;
    CREATE DATABASE $PRODUCT_DB_NAME;
    CREATE DATABASE $INTERACTION_DB_NAME;
EOSQL