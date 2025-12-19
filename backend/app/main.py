from fastapi import FastAPI
from .database import engine
from .models import Base

app = FastAPI(title="AI Dropshipping Agent")

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "ok"}
