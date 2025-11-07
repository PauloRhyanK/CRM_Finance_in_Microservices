# CRM Finance - API (Arquitetura de Microserviços)

Este repositório contém o código-fonte da API backend para o sistema CRM Finance, reimplementada como uma arquitetura de microserviços. O projeto original (um monólito) foi decomposto em serviços independentes baseados em domínios de negócio, cada um com sua própria responsabilidade e banco de dados.

## 🎯 Objetivo

O objetivo principal deste projeto (e TCC) é demonstrar a transição de uma aplicação monolítica para uma arquitetura de microserviços, utilizando a estratégia de **Bifurcação Baseada em Componentes**. A aplicação visa fornecer funcionalidades básicas de CRM, incluindo gerenciamento de clientes, produtos/serviços e registro de interações.

## ⚙️ Stack de Tecnologias

A arquitetura utiliza as seguintes tecnologias e bibliotecas principais:

-   **Backend (Microserviços):**
    -   **Flask:** Micro-framework web Python usado para construir cada serviço e o API Gateway.
    -   **Flask-SQLAlchemy:** Integração com SQLAlchemy para ORM (Mapeamento Objeto-Relacional).
    -   **Flask-Migrate:** Gerenciamento de migrações de esquema do banco de dados (Alembic).
    -   **Flask-Marshmallow / Marshmallow-SQLAlchemy:** Validação de dados de entrada e serialização de dados de saída da API.
    -   **Flask-JWT-Extended:** Implementação de autenticação baseada em tokens JWT (JSON Web Tokens).
-   **Banco de Dados:**
    -   **PostgreSQL:** Banco de dados relacional robusto, utilizado individualmente por cada microserviço.
    -   **Psycopg2:** Driver Python para PostgreSQL.
-   **Comunicação:**
    -   **Requests:** Biblioteca Python usada para comunicação síncrona (HTTP) entre serviços (ex: Interaction Service -> Customer Service).
-   **Ambiente e Orquestração:**
    -   **Docker & Docker Compose:** Containerização de todos os serviços e bancos de dados para um ambiente consistente e isolado.
    -   **Python-dotenv:** Gerenciamento de variáveis de ambiente.
-   **Estrutura:**
    -   **Monorepo:** Todo o código-fonte reside em um único repositório Git para facilitar o gerenciamento e a orquestração.

## 🏛️ Arquitetura Overview

A aplicação segue uma arquitetura de microserviços, com os seguintes componentes principais:

1.  **API Gateway (Flask):** A porta de entrada única para todas as requisições externas. Responsável por:
    * **Roteamento:** Encaminha as requisições para o microserviço apropriado com base no path da URL (ex: `/api/customers/*` -> Customer Service).
    * **Autenticação:** Verifica a validade do token JWT em rotas protegidas usando `Flask-JWT-Extended`.
    * **Injeção de Dados:** Insere informações relevantes (como `X-User-Id`) nos headers antes de encaminhar a requisição.
2.  **Serviços de Domínio (Flask):** Quatro microserviços independentes, cada um responsável por um domínio de negócio específico:
    * **Auth Service:** Gerencia usuários (registro, login) e a emissão de tokens JWT.
    * **Customer Service:** Gerencia o cadastro completo de clientes (CRUD, busca, ativação/desativação).
    * **Product Service:** Gerencia o catálogo de produtos e serviços (CRUD).
    * **Interaction Service:** Gerencia o histórico de interações com clientes e também as transações financeiras. Este serviço demonstra a comunicação síncrona, consultando o Customer Service para validar a existência de clientes.
3.  **Bancos de Dados (PostgreSQL):** Cada serviço possui seu próprio banco de dados PostgreSQL isolado, garantindo o desacoplamento e a autonomia dos dados.
4.  **Rede Docker:** Todos os contêineres rodam em uma rede Docker privada (`crm_network`), permitindo que se comuniquem uns com os outros usando os nomes dos serviços como hostnames (ex: `http://customer-service:5000`).

### Diagrama Conceitual

```

```
                      [ Cliente (Navegador/App/Insomnia) ]
                                     | (Porta 8080)
                                     V
```

\+------------------------------ [ API Gateway (Flask) ] ------------------------------+
| (Roteamento: /auth/*, /api/customers/*, etc. | Validação JWT | Injeção X-User-Id)   |
\+-----------------------------------|-------------------|-----------------------------+
| (http://auth-service:5000) |                   | (http://interaction-service:5000)
|                      | (http://customer-service:5000) |
V                      V                   V                      V
\+-------------------------+  +-------------------------+  +-------------------------+  +-----------------------------+
| [ Auth Service (Flask) ] |  | [ Customer Service (Flask)] |  | [ Product Service (Flask)] |  | [ Interaction Service (Flask)] |
| (Users, JWT Tokens)     |  | (Customers CRUD, Search)|  | (Products CRUD)         |  | (Interactions, Transactions)|
\+-------------------------+  +-------------------------+  +-------------------------+  +-----------------------------+
|                      |                   |                      |
V                      V                   V                      V
[ Auth\_DB (PG) ]       [ Customer\_DB (PG) ]     [ Product\_DB (PG) ]    [ Interaction\_DB (PG) ]
(Tabela: user)          (Tabela: customer)       (Tabela: product)      (Tabelas: interaction,
transaction)

````
*(Nota: Setas de comunicação síncrona existem do API Gateway para Auth e Customer, e do Interaction Service para Customer via API Gateway ou diretamente).*

## 📁 Estrutura do Projeto (Monorepo)

O código está organizado em um Monorepo com a seguinte estrutura:

```bash
/
├── .git/
├── docker-compose.yml     # Orquestrador principal
├── .env                   # Variáveis de ambiente (ignorado pelo Git)
├── .env.example           # Exemplo de variáveis de ambiente
├── .gitignore
├── Makefile               # (Opcional) Atalhos para comandos Docker
├── README.md              # Esta documentação
│
├── /gateway/              # Código do API Gateway (Flask)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── config.py
│   └── app.py
│
└── /services/             # Contém todos os microserviços de domínio
    ├── /auth-service/     # Serviço de Autenticação
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── config.py
    │   ├── manage.py        # Para migrações
    │   └── app/             # Código Flask do serviço
    │
    ├── /customer-service/ # Serviço de Clientes (estrutura similar)
    │   └── ...
    │
    ├── /interaction-service/ # Serviço de Interações (estrutura similar)
    │   └── ...
    │
    └── /product-service/  # Serviço de Produtos (estrutura similar)
        └── ...
````

## ▶️ Como Executar o Projeto

Pré-requisitos: **Docker** e **Docker Compose** instalados.

1.  **Clone o repositório:**

    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2.  **Crie o ficheiro de ambiente:**
    Copie o ficheiro de exemplo `.env.example` para `.env`.

    ```bash
    cp .env.example .env
    ```

    ⚠️ **Importante:** Revise o ficheiro `.env` e defina valores seguros para `SECRET_KEY` e `JWT_SECRET_KEY`. As outras variáveis (nomes de DB, user, password) podem ser mantidas como estão para desenvolvimento.


3.  **Primeira vez no projeto (ou depois de apagar tudo):**

    ```bash
    make setup
    ```

    *(Este comando faz tudo, do início ao fim. Depois dele, sua aplicação estará 100% funcional com os bancos de dados prontos).*


## MakeFile
  * **`make up`**: Inicia tudo (equivalente a `docker-compose up --build -d`).
  * **`make down`**: Para e remove tudo, incluindo volumes (`docker-compose down -v`).
  * **`make setup`**: **Este é o comando mágico para a primeira vez\!** Ele faz tudo:
    1.  `down`: Garante que tudo está parado e limpo.
    2.  `up`: Constrói e inicia todos os contêineres.
    3.  `wait-for-dbs`: Espera um pouco para os bancos de dados iniciarem (ajuste o `sleep` se necessário).
    4.  `migrate-all`: Executa `init`, `migrate` e `upgrade` para **todos** os seus serviços automaticamente. O `|| true` ignora erros se a pasta `migrations` já existir (no `init`) ou se não houver mudanças (no `migrate`).
  * **`make migrate service=<nome> m="msg"`**: Atalho para gerar uma *nova* migração depois que você alterar um modelo (ex: `make migrate service=customer-service m="Adiciona campo NIF"`).
  * **`make upgrade service=<nome>`**: Atalho para aplicar as migrações pendentes num serviço específico.
  * **`make upgrade-all`**: Aplica migrações pendentes em *todos* os serviços.

**Fluxo de Trabalho:**

1.  **Primeira vez no projeto (ou depois de apagar tudo):**

    ```bash
    make setup
    ```

    *(Este comando faz tudo, do início ao fim. Depois dele, sua aplicação estará 100% funcional com os bancos de dados prontos).*

2.  **Para iniciar o trabalho num dia normal:**

    ```bash
    make up
    ```

    *(Apenas inicia os contêineres. O banco de dados já estará pronto da vez anterior).*

3.  **Para parar tudo:**

    ```bash
    make down
    ```

4.  **Quando você alterar um `models.py`:**

    ```bash
    make migrate service=nome-do-servico m="Sua mensagem descritiva"
    make upgrade service=nome-do-servico
    ```

**Pronto\!** A API estará disponível através do API Gateway no endereço **`http://localhost:8080`**.

## 🚀 Endpoints da API

Todas as requisições devem ser feitas para o API Gateway (`http://localhost:8080`). O Gateway cuidará do roteamento e da autenticação. Rotas que não são de `auth` exigem um token JWT válido no header `Authorization: Bearer <token>`.

### Autenticação (`/auth`)

| Método | Rota        | Descrição                | Corpo (JSON)                                       | Resposta de Sucesso (200/201)                          |
| :----- | :---------- | :----------------------- | :------------------------------------------------- | :---------------------------------------------------- |
| `POST` | `/register` | Registra um novo usuário. | `{ "ds_user": "Nome", "ds_user_email": "...", "password": "..." }` | `{ "message": "...", "user": {...} }`                 |
| `POST` | `/login`    | Autentica e gera token.  | `{ "ds_user_email": "...", "password": "..." }`       | `{ "message": "...", "access_token": "...", "user": {...} }` |

### Clientes (`/api/customers`)

| Método | Rota                      | Descrição                                         | Corpo/Parâmetros                                     | Resposta de Sucesso (200/201)                                 |
| :----- | :------------------------ | :------------------------------------------------ | :--------------------------------------------------- | :---------------------------------------------------------- |
| `POST` | `/`                       | Cria um novo cliente.                             | **Corpo (JSON):** Dados do cliente.                  | `{ "message": "...", "customer": {...} }`     |
| `GET`  | `/`                       | Lista clientes com paginação e busca.             | **Query:** `page`, `per_page`, `active_only`, `search` | `{ "customers": [...], "total": ..., "pages": ... }`        |
| `GET`  | `/<customer_id>`          | Obtém detalhes de um cliente.                     | -                                                    | `{ "customer": {...} }`                                      |
| `PUT`  | `/<customer_id>`          | Atualiza dados de um cliente.                     | **Corpo (JSON):** Dados (parciais ou completos).     | `{ "message": "...", "customer": {...} }` |
| `DELETE` | `/<customer_id>`        | Desativa (soft delete) ou remove um cliente.      | **Query:** `hard_delete=true` (opcional)             | `{ "message": "..." }`                                      |
| `PATCH`  | `/<customer_id>/activate` | Reativa um cliente desativado.                    | -                                                    | `{ "message": "...", "customer": {...} }`                     |

### Produtos (`/api/products`)

| Método | Rota             | Descrição                                         | Corpo/Parâmetros                                     | Resposta de Sucesso (200/201)                               |
| :----- | :--------------- | :------------------------------------------------ | :--------------------------------------------------- | :-------------------------------------------------------- |
| `POST` | `/`              | Cria um novo produto/serviço.                     | **Corpo (JSON):** Dados do produto.                  | `{ "message": "...", "product": {...} }`    |
| `GET`  | `/`              | Lista produtos com paginação.                     | **Query:** `page`, `per_page`                        | `{ "products": [...], "total": ..., "pages": ... }`       |
| `GET`  | `/<product_id>`  | Obtém detalhes de um produto.                     | -                                                    | `{ "product": {...} }`                                    |
| `PUT`  | `/<product_id>`  | Atualiza dados de um produto.                     | **Corpo (JSON):** Dados (parciais ou completos).     | `{ "message": "...", "product": {...} }` |
| `DELETE`| `/<product_id>` | Desativa (soft delete) ou remove um produto.      | **Query:** `hard_delete=true` (opcional)             | `{ "message": "..." }`                                      |

### Interações (`/api/customers/<customer_id>/interactions`)

| Método | Rota                      | Descrição                                         | Corpo/Parâmetros                                     | Resposta de Sucesso (200/201)                                     |
| :----- | :------------------------ | :------------------------------------------------ | :--------------------------------------------------- | :-------------------------------------------------------------- |
| `POST` | `/`                       | Registra uma nova interação para o cliente.       | **Corpo (JSON):** `{ "ds_notes": "...", "id_interaction_type": "..." }` | `{ "message": "...", "interaction": {...} }` |
| `GET`  | `/`                       | Lista interações do cliente com paginação.        | **Query:** `page`, `per_page`                        | `{ "interactions": [...], "total": ..., "pages": ... }`           |

*(Nota: Os endpoints para `Transaction` não foram implementados nesta versão, mas a estrutura está pronta no `interaction-service` para adicioná-los futuramente).*

```bash
# Da primeira vez (Execute um de cada vez)
docker compose exec auth-service flask db init
docker compose exec auth-service flask db migrate -m "Init auth schema"

docker compose exec customer-service flask db init
docker compose exec customer-service flask db migrate -m "Init customer schema"
docker compose exec product-service flask db init
docker compose exec product-service flask db migrate -m "Init product schema"
docker compose exec interaction-service flask db init
docker compose exec interaction-service flask db migrate -m "Init interaction/transaction schema"

# Pra rodar
chmod +x init-db.sh
docker-compose down -v
docker-compose up --build -d
# 1. Cria a tabela 'user' no 'auth-db'
docker compose exec auth-service flask db upgrade

# 2. Cria a tabela 'customer' no 'customer-db'
docker compose exec customer-service flask db upgrade

# 3. Cria a tabela 'product' no 'product-db'
docker compose exec product-service flask db upgrade

# 4. Cria as tabelas 'interaction' e 'transaction' no 'interaction-db'
docker compose exec interaction-service flask db upgrade

```