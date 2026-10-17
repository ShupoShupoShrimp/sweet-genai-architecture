# ===== Creating the base =====
ARG PYTHON_IMAGE=python:3.13-slim-trixie@sha256:33f2ed6c37a2c8c66c7d9e1f2f9ca47d1ef89e2127e6c7a83f3d4eeab6c9bd8f
FROM ${PYTHON_IMAGE} AS base

# ===== Builder stage =====
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv /uv /bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential\
    libpq-dev\
    && rm -rf /var/lib/apt/lists/*

    WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

RUN uv sync --frozen --no-dev 

# ===== Final stage =====
FROM base AS final

WORKDIR /app

RUN groupadd --gid 10001 appgroup \
    && useradd --uid 10001 --gid appgroup --shell /usr/sbin/nologin --create-home appuser 

COPY --from=builder /app/.venv /app/.venv

COPY src/ ./src/
COPY alembic.ini ./
COPY migrations/ ./migrations/

ENV PATH="/app/.venv/bin:$PATH"

RUN chown -R appuser:appgroup /app
USER appuser

CMD ["uvicorn", "src.sugar.api.main", "--host", "0.0.0.0", "--port", "8000"]
