# 1. environment with python pre-installed
FROM python:3.12-slim

WORKDIR /app

# 2. install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy application files
COPY . .

# 4. Run SQL migrations before starting the API
CMD ["sh", "-c", "python migrations.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
