# BlinkTask — full-stack portfolio platform

The original static HTML pages are preserved at the repository root during migration. The new React + TypeScript app lives in `frontend/`; FastAPI backend code lives in `backend/`.

## Stack
- React + TypeScript + Vite + React Router frontend
- Python FastAPI API
- SQLAlchemy database layer (SQLite local development; PostgreSQL recommended for production)
- Contact form API with validation and rate limiting
- Admin login with short-lived JWT tokens and a message inbox to change message status
- GitHub Pages frontend deployment via Actions

## Run locally

Backend (Python 3.11+):
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Copy .env.example to .env, then set strong unique ADMIN_PASSWORD and JWT_SECRET values.
uvicorn app.main:app --reload --port 8000
```

Frontend (second terminal):
```bash
cd frontend
npm install
# create .env.local containing VITE_API_URL=http://localhost:8000
npm run dev
```

## Deployment requirements

GitHub Pages can host the built frontend only. It cannot run FastAPI or a database. Deploy the backend and persistent PostgreSQL database separately, configure `APP_ENV=production`, `DATABASE_URL`, `ADMIN_PASSWORD`, `JWT_SECRET` (at least 32 random characters), and exact `CORS_ORIGINS`. Then add repository Actions variable `VITE_API_URL` pointing to the backend's HTTPS origin and rerun the Pages workflow.

The backend code is committed, but the API and database have **not** been deployed by this repository change. The contact form stores messages but does not send email notifications. Review hosting costs, persistent storage, backups, deletion/retention policy, and secrets before launch. Never commit real credentials.
