# Build deps and venv in a separate stage to keep runtime small
FROM python:3.12-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN python -m venv "${VIRTUAL_ENV}" \
    && pip install --no-cache-dir "poetry==1.8.3" "poetry-plugin-export==1.7.1"

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry export --only main --format requirements.txt --output requirements.txt --without-hashes \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY entrypoint.sh /app/entrypoint.sh
COPY random_phrase_api.py /app/random_phrase_api.py
COPY phrases.txt /app/phrases.txt
COPY templates /app/templates

RUN chmod +x /app/entrypoint.sh

EXPOSE 7070

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "random_phrase_api.py"]
