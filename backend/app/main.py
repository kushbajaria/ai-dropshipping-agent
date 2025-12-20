from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Product
from .schemas import ProductIn
from .scoring import (
    compute_demand_score,
    compute_competition_score,
    compute_risk_score,
    compute_viability_score
)

app = FastAPI(title="AI Dropshipping Agent")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products")
def ingest_product(product: ProductIn, db: Session = Depends(get_db)):
    demand = compute_demand_score(product.review_count)
    competition = compute_competition_score(product.review_count)
    risk = compute_risk_score(product.shipping_time_days)
    viability = compute_viability_score(demand, competition, risk)

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
