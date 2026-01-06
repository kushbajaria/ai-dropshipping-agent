from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schema import ProductBatch
from app.ingestion import ingest_products
from app.auth import verify_api_key
from app.database import get_db
from app.schemas import ProductCreate, ProductRead
from app.models import Product

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/analyze-products")
def analyze_products(
    batch: ProductBatch,
    api_key=Depends(verify_api_key)
):
    results = ingest_products([p.dict() for p in batch.products])
    return {
        "owner": api_key["key"],
        "count": len(results),
        "results": results
    }


@router.get("/health", dependencies=[Depends(verify_api_key)])
def health_check():
    return {"status": "ok"}


@router.post(
    "/",
    response_model=list[ProductRead],
    dependencies=[Depends(verify_api_key)]
)
def create_products(
    products: list[ProductCreate],
    db: Session = Depends(get_db)
):
    db_products = []

    for product in products:
        db_product = Product(**product.dict())
        db.add(db_product)
        db_products.append(db_product)

    db.commit()

    for p in db_products:
        db.refresh(p)

    return db_products
