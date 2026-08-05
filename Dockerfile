# AetherFlow Production Image
FROM python:3.12-slim AS builder

WORKDIR /build
COPY pyproject.toml requirements.txt ./
COPY src/ ./src/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir build && \
    python -m build --wheel

FROM python:3.12-slim

LABEL org.opencontainers.image.title="AetherFlow"
LABEL org.opencontainers.image.description="Enterprise Multi-Agent AI Automation Platform"
LABEL org.opencontainers.image.version="0.9.2"

RUN groupadd -r aether && useradd -r -g aether aether

WORKDIR /app

COPY --from=builder /build/dist/*.whl .
RUN pip install --no-cache-dir *.whl && rm *.whl

COPY configs/ ./configs/
COPY scripts/entrypoint.sh ./

RUN chmod +x entrypoint.sh && \
    chown -R aether:aether /app

USER aether

ENV AETHERFLOW_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 8080 9090

ENTRYPOINT ["./entrypoint.sh"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8080"]
