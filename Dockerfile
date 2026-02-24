# Stage 1: Build the Angular app
FROM node:20-alpine AS frontend-build
WORKDIR /frontend

# Install deps first (better layer caching)
COPY frontend/package*.json ./
RUN npm ci

# Build
COPY frontend/ ./
RUN npm run build


# Stage 2: Build the FastAPI runtime image
FROM python:3.11-slim AS runtime
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps (optional, but useful for health/debug)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Python deps
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# App code
COPY backend/app /app/app
COPY backend/alembic /app/alembic
COPY backend/alembic.ini /app/alembic.ini

# Ensure data directory exists (mount a volume here for persistence)
RUN mkdir -p /app/data

# Copy built Angular assets into FastAPI static directory
COPY --from=frontend-build /frontend/dist /app/app/static

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]