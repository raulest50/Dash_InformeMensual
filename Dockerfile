FROM python:3.12-slim

# Install system dependencies (if any are required)
# RUN apt-get update && apt-get install -y <your-dependencies>

# Install Poetry
RUN pip install poetry

WORKDIR /app

# Copy pyproject.toml and poetry.lock first (for caching)
COPY pyproject.toml poetry.lock ./

# Configure Poetry to install packages in the global environment
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the rest of your application code
COPY . .

# Expose the port your app runs on (if applicable)
# EXPOSE 8000

# Set the command to run your application
CMD ["python", "app.py"]
