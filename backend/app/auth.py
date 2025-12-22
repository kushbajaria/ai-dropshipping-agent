from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import APIKey


def verify_api_key(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    key = db.query(APIKey).filter(APIKey.key == x_api_key).first()
    if not key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return key
