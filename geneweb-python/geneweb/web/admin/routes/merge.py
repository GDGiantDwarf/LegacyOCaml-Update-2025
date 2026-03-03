from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from geneweb.core.database import BaseManager

router = APIRouter(
    prefix="/api/bases", tags=["admin:merge"]
)


@router.post("/merge")
def merge_bases(
    base_a: str,
    base_b: str,
    target: str,
    base_dir: str | None = None,
):
    for n in (base_a, base_b, target):
        BaseManager._validate_name(n)
    if base_a == base_b:
        raise HTTPException(
            status_code=400,
            detail="Source bases must be different",
        )
    try:
        BaseManager.merge_bases(
            base_a, base_b, target, base_dir
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404, detail=str(exc)
        )
    except FileExistsError as exc:
        raise HTTPException(
            status_code=409, detail=str(exc)
        )
    return JSONResponse(
        status_code=200,
        content={
            "detail": (
                f"Merged '{base_a}' and '{base_b}' "
                f"into '{target}'"
            )
        },
    )
