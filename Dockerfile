# syntax=docker/dockerfile:1.4

FROM python:3.12-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:0.7.12 /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_CACHE_DIR=/opt/uv-cache/

WORKDIR /app

COPY pyproject.toml .

RUN --mount=type=cache,target=/opt/uv-cache/ \
    uv sync --no-install-project

ADD . /app

RUN --mount=type=cache,target=/opt/uv-cache/ \
    uv sync

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl", "-f", "http://localhost:8000" ]

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["uvicorn"]

CMD ["src.app:app", "--host", "0.0.0.0", "--port", "8000"]


