FROM python:3.11-slim 

# Environent Varaible 
ENV PYTHONUNBUFFERED=1

# Define work directory
WORKDIR /finance-pipeline

# Copy
COPY . . 

# Install poetry
RUN pip install poetry

# Install all dependencies
RUN poetry config virtualenv.create false \
    && poetry install --without-dev --no-root --no-interaction --no-ansi
