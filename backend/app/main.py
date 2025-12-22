from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routes import router
from .database import SessionLocal
from .models import Product
from .schemas import ProductIn
from .scoring import (
    calculate_demand,
    calculate_competition,
    calculate_risk,
    calculate_viability
)

app = FastAPI(title="AI Dropshipping Agent")
app.include_router(router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products")
def ingest_product(product: ProductIn, db: Session = Depends(get_db)):
    demand = calculate_demand(product.review_count)
    competition = calculate_competition(product.review_count)
    risk = calculate_risk(product.shipping_time_days)
    viability = calculate_viability(demand, competition, risk)

    db_product = Product(
        **product.dict(),
        demand_score=demand,
        competition_score=competition,
        risk_score=risk,
        viability_score=viability
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return {"id": db_product.id, "viability_score": viability}
