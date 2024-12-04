FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-dev

COPY . .

# Run the data loading script with unbuffered output
RUN python -u load_at_docker_stage.py

EXPOSE 8050

CMD ["python", "app.py"]
