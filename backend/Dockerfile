FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM python:3.13-slim-bookworm

RUN groupadd --system --gid 10000 nonroot \
    && useradd --system --gid 10000 --uid 10000 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PYTHONPATH="/app/src" \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER nonroot

WORKDIR /app

CMD ["python", "-m", "mood_tracker.main"]