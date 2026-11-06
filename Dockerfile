# Production Dockerfile for Guppy - Clinical Pharmacy & Fornas 2025 Helper
FROM python:3.11-slim

# Prevent Python from writing .pyc and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first for build cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source and assets
COPY . .

# Expose standard Streamlit port
EXPOSE 8501

# Healthcheck probe for cloud orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Launch application listening on all network interfaces
ENTRYPOINT ["streamlit", "run", "guppy/frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
