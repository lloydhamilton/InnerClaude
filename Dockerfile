FROM python:3.11-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:0.4.18 /uv /uvx /bin/

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Set the working directory
WORKDIR /app

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy the project
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

FROM python:3.11-slim-bookworm AS runner
COPY --from=builder --chown=app:app /app /app

WORKDIR app

# Expose port 8501 for Streamlit
EXPOSE 8501

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
CMD ["streamlit", "run", "InnerClaude/app/main.py"]