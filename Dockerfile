# AetherFlow — simple production-ish image
# (full wheel build is overkill for now; this keeps CI green)
FROM python:3.12-slim

LABEL org.opencontainers.image.title="AetherFlow"
LABEL org.opencontainers.image.description="Enterprise Multi-Agent AI Automation Platform"
LABEL org.opencontainers.image.version="0.9.2"

RUN groupadd -r aether && useradd -r -g aether aether

WORKDIR /app

# deps first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# source
COPY src/ ./src/
COPY configs/ ./configs/
COPY scripts/entrypoint.sh ./
COPY pyproject.toml .

RUN chmod +x entrypoint.sh && \
    chown -R aether:aether /app

USER aether

ENV AETHERFLOW_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

EXPOSE 8080 9090

ENTRYPOINT ["./entrypoint.sh"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8080"]
