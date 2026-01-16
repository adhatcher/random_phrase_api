# Use the official Python image as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install the required packages without dev dependencies
RUN poetry install --only main --no-root

# Copy the rest of the application code
COPY . .

# Expose port 7070 for the Flask API
EXPOSE 7070

#COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the application
CMD ["poetry", "run", "python", "random_phrase_api.py"]
