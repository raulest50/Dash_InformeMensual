FROM python:3.12-slim

WORKDIR /app

# Install openssh-client and Cleans up the local repository of retrieved package files to reduce the image size
RUN apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-dev

COPY . .

EXPOSE 8050

CMD ["python", "app.py"]
