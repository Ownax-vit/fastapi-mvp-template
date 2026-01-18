FROM python:3.13-slim as builder


ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup" \
    UV_HOME="/usr/local/bin" \
    VENV_PATH="/opt/pysetup"

WORKDIR /app

RUN pip install uv
WORKDIR $VENV_PATH
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --locked --no-dev

ENV PATH="$VENV_PATH/.venv/bin:$PATH"
# ======DEVELOPMENT======
FROM builder as runner-dev

ENV USER_UID=${USER_UID:-1500} \
    USER_GID=${USER_GID:-1500}

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

RUN groupadd -g ${USER_GID} app-user && \
    useradd -m -u ${USER_UID} -g app-user app-user

WORKDIR $VENV_PATH
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --locked

COPY --chown=app-user:app-user . /app

RUN mkdir -p /app/sqlite && chown -R app-user:app-user /app/sqlite

USER app-user

WORKDIR /app

EXPOSE 8000
ENTRYPOINT /entrypoint.sh $0 $@

ENV PYDEVD_DISABLE_FILE_VALIDATION=1
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

