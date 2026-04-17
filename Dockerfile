# Multi-stage build
# Stage 1: Build React frontend
FROM node:20-slim AS frontend-build
WORKDIR /app/frontend
# Copy package.json and install deps
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy frontend source and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend + serve frontend
FROM python:3.12-slim
WORKDIR /app

# [CRITICAL TRICK TO PREVENT PARALLEL BUILD OOM ON WINDOWS]
# Copy compiled frontend FIRST. This forces Docker BuildKit to WAIT until
# the frontend build is 100% finished BEFORE starting `apt-get install ffmpeg`. 
# This prevents both stages from thrashing CPU/Memory in parallel and causing EOF errors.
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Install system dependencies (ffmpeg is crucial for yt-dlp)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create downloads directory
RUN mkdir -p /downloads

# Copy backend code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Set environment variables
ENV API_PORT=8000
ENV DOWNLOAD_DIR=/downloads
ENV PYTHONUNBUFFERED=1

# Change to backend directory to run uvicorn
WORKDIR /app/backend

# The command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
