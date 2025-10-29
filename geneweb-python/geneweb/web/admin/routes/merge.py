from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from geneweb.core.database import BaseManager

router = APIRouter(prefix="/api/bases", tags=["admin:merge"])


@router.post("/merge")
def merge_bases(
        base_a: str,
        base_b: str,
        target: str,
        base_dir: str | None = None):
    for n in (base_a, base_b, target):
        BaseManager._validate_name(n)
    if base_a == base_b:
        raise HTTPException(status_code=400,
                            detail="Source bases must be different")

    return JSONResponse(
        status_code=501, content={
            "detail": "Merge not implemented yet; endpoint stub in place."}, )
