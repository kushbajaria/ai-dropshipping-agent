from fastapi import APIRouter, Depends
from app.schemas import ProductBatch
from app.ingestion import ingest_products
from app.auth import verify_api_key

router = APIRouter()


@router.post("/analyze-products")
def analyze_products(
    batch: ProductBatch,
    api_key=Depends(verify_api_key)
):
    results = ingest_products([p.dict() for p in batch.products])
    return {
        "owner": api_key.owner,
        "count": len(results),
        "results": results
    }
