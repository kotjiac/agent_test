FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir fastapi fastapi_mcp uvicorn
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${GREETER_PORT}"]
