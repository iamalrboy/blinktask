from datetime import datetime, timedelta, timezone
import hmac
import jwt
from fastapi import HTTPException, status
from .config import settings

def issue_token() -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": "admin", "iat": now, "exp": now + timedelta(minutes=settings.admin_token_minutes)}, settings.jwt_secret, algorithm="HS256")

def verify_admin_password(candidate: str) -> bool:
    return bool(settings.admin_password and hmac.compare_digest(candidate, settings.admin_password))

def require_admin_token(token: str) -> None:
    if not settings.jwt_secret or len(settings.jwt_secret) < 32:
        raise HTTPException(status_code=503, detail="Admin authentication is not configured securely.")
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        if payload.get("sub") != "admin":
            raise ValueError("invalid subject")
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired admin session.") from None
