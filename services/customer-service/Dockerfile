# /customer-service/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app/
COPY config.py .
COPY run.py .
COPY manage.py .
EXPOSE 5000
CMD ["python", "run.py"]