FROM python:3.10-slim
ENV PYTHONPATH=/app
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY app/ ./app/
COPY utils/ ./utils/
COPY .env .
COPY config_sse_tools.yaml .
CMD ["python", "app/main.py"]
