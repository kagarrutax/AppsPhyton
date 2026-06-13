FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads/products uploads/payments uploads/invoices uploads/tickets

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && python -m app.seeders.run_seeders && uvicorn main:app --host 0.0.0.0 --port 8000"]
