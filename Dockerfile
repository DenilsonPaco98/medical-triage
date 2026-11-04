# Multi-stage Dockerfile for Medical Review Sentiment Analysis API
# Stage 1: Base - Python runtime
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# =====================================================================
# Stage 2: Builder - Install Python dependencies
FROM base as builder

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv pip install --python /usr/local/bin/python -r <(uv pip compile -o - --no-dev)

# =====================================================================
# Stage 3: Runtime - Minimal production image
FROM base as runtime

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data/models /app/logs /app/mlruns && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser src/ src/
COPY --chown=appuser:appuser pyproject.toml .
COPY --chown=appuser:appuser .env.example .env

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Switch to non-root user
USER appuser

# Expose ports
EXPOSE 8000 5000 8501 9090 4200

# Default command: start FastAPI server
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# =====================================================================
# Stage 4: Development image (includes dev tools)
FROM runtime as dev

USER root

# Install development tools
RUN pip install -e ".[dev,lint,ml,ui]"

USER appuser

# Start with interactive shell
CMD ["/bin/bash"]
