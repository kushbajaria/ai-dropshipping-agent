from fastapi import APIRouter
from app.schemas import ProductBatch
from app.ingestion import ingest_products

router = APIRouter()


@router.post("/analyze-products")
def analyze_products(batch: ProductBatch):
    results = ingest_products([p.dict() for p in batch.products])
    return {
        "count": len(results),
        "results": results
    }
