FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy backend code
COPY backend/ ./backend/

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory to backend app
WORKDIR /app/backend

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
