from sqlalchemy.orm import Session
from .models import ApiUsage
from .database import SessionLocal

def log_api_usage(api_key: str, endpoint: str) -> None:
    db: Session = SessionLocal()
    try:
        usage = ApiUsage(
            api_key=api_key,
            endpoint=endpoint
        )
        db.add(usage)
        db.commit()
    finally:
        db.close()
