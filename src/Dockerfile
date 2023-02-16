FROM python:3.11-slim

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN set -x \
    && groupadd -g "${GID}" app \
    && useradd \
        --create-home \
        --no-log-init \
        -u "${UID}" \
        -g "${GID}" \
        app \
    && chown app:app -R /app

USER app

COPY --chown=app:app requirements.txt .
RUN pip install \
        --no-cache-dir \
        --no-warn-script-location \
        --user \
        -r requirements.txt

COPY --chown=app:app . .

ARG FLASK_DEBUG="false"
ENV FLASK_DEBUG="${FLASK_DEBUG}" \
    FLASK_APP="app" \
    FLASK_SKIP_DOTENV="true" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/app/.local/bin" \
    USER="app"

CMD ["gunicorn", "-c", "python:config.gunicorn", "app.app:create_app()"]
