# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install system dependencies if required
# RUN apt-get update && apt-get install -y <your-dependencies>

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock first (for caching)
COPY pyproject.toml poetry.lock ./

# Configure Poetry to install packages in the global environment
RUN poetry config virtualenvs.create false

# Install project dependencies without dev dependencies
RUN poetry install --no-interaction --no-ansi --no-dev

# Copy the rest of your application code
COPY . .

# Run the data loading script during the build
RUN python load_at_docker_stage.py

# Expose the port your app runs on (if applicable)
EXPOSE 8050

# Set the command to run your application
CMD ["python", "app.py"]
