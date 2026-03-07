# NAS Super-App

> The ultimate self-hosted, modular digital cloud system. LAN-accelerated transfers, AI indexing, metadata streaming, and more.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- (Optional) Go 1.23+ for Sync Client

### 1. Run in Production
```bash
# Start all services with production optimizations
docker compose -f docker-compose.prod.yml up -d --build
```
Access the dashboard at **http://localhost:3000** (or your server IP).

### 2. Environment Variables
Create a `.env` file for security (recommended):
```env
POSTGRES_PASSWORD=secure_password
SECRET_KEY=very_long_random_string
MINIO_ROOT_PASSWORD=another_secure_password
```

---

## Architecture

The system follows a **Hybrid Microkernel** architecture:

1.  **Core (Python/FastAPI)**: The brain. Handles Authentication, Database, AI Indexing, Transcoding, and Module logic.
2.  **Transfer Engine (Go)**: The brawn. A raw UDP/QUIC server dedicated to moving files at maximum LAN speeds.
3.  **Frontend (Next.js)**: The face. A modern, responsive React application.

---

## Modules (Addons)

| Module | URL | Description |
| :--- | :--- | :--- |
| **Files** | `/dashboard/files` | Drive-like file management. Upload, organize, share. |
| **Media** | `/dashboard/media` | Video gallery with FFmpeg HLS transcoding & streaming. |
| **Chat** | `/dashboard/chat` | Real-time WebSocket chat room. |
| **Notes** | `/dashboard/notes` | Collaborative Markdown editor (Google Docs style). |
| **AI** | *Background* | Auto-indexes text & images for Semantic Search. |

---

## Sync Client

A native Go client is included to sync local folders to the NAS automatically.

```bash
cd transfer-engine
go build -o sync-client ./client/main.go
./sync-client /path/to/watch
```

## Security

-   **JWT Auth**: Secure session and transfer tokens.
-   **Public Sharing**: Generate expiring links for files.
-   **Isolation**: Services run in isolated Docker containers.

