# Social Media Downloader

Web interface to download videos, audio, and images from YouTube, Facebook, TikTok, Bilibili, and Instagram....
Uses `yt-dlp` and `gallery-dl` under the hood.

## Features

- Modern UI with React + Vite
- FastAPI backend
- IPv6 Source Address Rotation (Useful for Oracle Cloud / lavalink style)
- Auto-cleanup of downloaded files
- Supports downloading TikTok slideshows and Instagram carousels

## Quick Start via Docker

1. Copy `.env.example` to `.env` and configure accordingly.
2. Run `docker-compose up -d --build`
3. Access at `http://localhost:8000`

## Developer Setup

### Backend

```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```
cd frontend
npm install
npm run dev
```
