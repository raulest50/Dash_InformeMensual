FROM python:3.12-slim AS builder

WORKDIR /app

# Install openssh-client and poetry in a single layer
RUN apt-get update && \
    apt-get install -y openssh-client && \
    rm -rf /var/lib/apt/lists/* && \
    pip install poetry && \
    poetry self add poetry-plugin-export

COPY pyproject.toml poetry.lock ./

# Configure poetry and export dependencies to requirements.txt
RUN poetry config virtualenvs.create false && \
    poetry export --format requirements.txt --output requirements.txt

# Second stage: final image
FROM python:3.12-slim

WORKDIR /app

# Install dependencies in a single layer
RUN apt-get update && \
    apt-get install -y openssh-client && \
    rm -rf /var/lib/apt/lists/* && \
    pip install gunicorn

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8050

# Use environment variable to determine whether to use Gunicorn (production) or direct Python (development)
ENV APP_ENV=production
ENV DEBUG=False

# Use entrypoint script to decide between Gunicorn and direct Python execution
CMD ["sh", "-c", "if [ \"$APP_ENV\" = \"production\" ]; then gunicorn --bind 0.0.0.0:8050 app:server; else python app.py; fi"]
