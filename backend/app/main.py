from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from .config import settings
from .database import Base, engine, get_db
from .models import ContactMessage
from .schemas import AdminLogin, ContactCreate, ContactOut, StatusUpdate, TokenOut
from .security import issue_token, require_admin_token, verify_admin_password

@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.app_env == "production":
        if len(settings.jwt_secret) < 32 or not settings.admin_password:
            raise RuntimeError("Set strong JWT_SECRET and ADMIN_PASSWORD environment variables before production startup.")
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="BlinkTask API", version="1.0.0", lifespan=lifespan, docs_url="/api/docs" if settings.app_env != "production" else None, redoc_url=None)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=False, allow_methods=["GET", "POST", "PATCH", "OPTIONS"], allow_headers=["Authorization", "Content-Type"])
limiter = Limiter(key_func=get_remote_address, default_limits=[])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "blinktask-api"}

@app.post("/api/contact", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
def create_contact(payload: ContactCreate, request: Request, db: Session = Depends(get_db)):
    message = ContactMessage(name=payload.name.strip(), email=str(payload.email).lower(), subject=payload.subject.strip(), message=payload.message.strip())
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"id": message.id, "status": "received"}

@app.post("/api/admin/login", response_model=TokenOut)
@limiter.limit("5/15minutes")
def admin_login(payload: AdminLogin, request: Request):
    if not verify_admin_password(payload.password):
        raise HTTPException(status_code=401, detail="Incorrect admin password.")
    if len(settings.jwt_secret) < 32:
        raise HTTPException(status_code=503, detail="Admin authentication is not configured securely.")
    return TokenOut(access_token=issue_token())

def authenticated_admin(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Admin sign-in required.")
    require_admin_token(authorization[7:])

@app.get("/api/admin/messages", response_model=list[ContactOut], dependencies=[Depends(authenticated_admin)])
def list_messages(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    limit = max(1, min(limit, 100))
    return list(db.scalars(select(ContactMessage).order_by(ContactMessage.created_at.desc()).offset(max(offset, 0)).limit(limit)))

@app.patch("/api/admin/messages/{message_id}", response_model=ContactOut, dependencies=[Depends(authenticated_admin)])
def update_message(message_id: int, payload: StatusUpdate, db: Session = Depends(get_db)):
    message = db.get(ContactMessage, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found.")
    message.status = payload.status
    db.commit()
    db.refresh(message)
    return message
