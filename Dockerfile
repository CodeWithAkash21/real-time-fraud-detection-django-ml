FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (postgres client)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn fraud_backend.wsgi:application --bind 0.0.0.0:8000"]
