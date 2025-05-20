FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc python3-dev musl-dev linux-headers

ENV UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

RUN playwright install --with-deps

EXPOSE 8000

RUN chmod +x init.sh

ENTRYPOINT [ "./init.sh" ]