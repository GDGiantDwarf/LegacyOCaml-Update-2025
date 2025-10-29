from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from geneweb.core.database import BaseManager

router = APIRouter(prefix="/api/bases", tags=["admin:export"])

EXPORT_DIR = Path("./exports")


@router.post("/{name}/export")
def export_base(
    name: str,
    format: str = Query("sqlite", pattern="^(sqlite|zip|gedcom|geneweb)$"),
    base_dir: str | None = None,
):
    db_path = BaseManager.base_path(name, base_dir)
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Base not found")

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    if format == "sqlite":
        out = EXPORT_DIR / f"{name}.db"
        out.write_bytes(db_path.read_bytes())
        return FileResponse(
            out, media_type="application/octet-stream", filename=out.name
        )

    if format == "zip":
        out = EXPORT_DIR / f"{name}.zip"
        with ZipFile(out, "w", ZIP_DEFLATED) as z:
            z.write(db_path, arcname=f"{name}.db")
        return FileResponse(
            out,
            media_type="application/zip",
            filename=out.name)

    return JSONResponse(
        status_code=501,
        content={"detail": f"Export format '{format}' not implemented yet."},
    )
