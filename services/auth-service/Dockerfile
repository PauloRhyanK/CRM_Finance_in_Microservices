# /auth-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copia apenas o que este serviço precisa
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o código-fonte deste serviço
COPY app/ ./app/
COPY config.py .
COPY app.py .
COPY manage.py .

EXPOSE 5000

# O comando para iniciar o servidor
CMD ["python", "app.py"]