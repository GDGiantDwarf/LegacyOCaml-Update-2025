from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse, Response
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geneweb.core.database import BaseManager
from geneweb.core.services.gedcom_converter import (
    export_to_gedcom,
)

router = APIRouter(prefix="/api/bases", tags=["admin:export"])

EXPORT_DIR = Path("./exports")


@router.post("/{name}/export")
def export_base(
    name: str,
    format: str = Query(
        "sqlite",
        pattern="^(sqlite|zip|gedcom|geneweb)$",
    ),
    base_dir: str | None = None,
):
    db_path = BaseManager.base_path(name, base_dir)
    if not db_path.exists():
        raise HTTPException(
            status_code=404, detail="Base not found"
        )

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    if format == "sqlite":
        out = EXPORT_DIR / f"{name}.db"
        out.write_bytes(db_path.read_bytes())
        return FileResponse(
            out,
            media_type="application/octet-stream",
            filename=out.name,
        )

    if format == "zip":
        out = EXPORT_DIR / f"{name}.zip"
        with ZipFile(out, "w", ZIP_DEFLATED) as z:
            z.write(db_path, arcname=f"{name}.db")
        return FileResponse(
            out,
            media_type="application/zip",
            filename=out.name,
        )

    if format == "gedcom":
        engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
        )
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        try:
            content = export_to_gedcom(session)
        finally:
            session.close()
            engine.dispose()
        return Response(
            content=content,
            media_type="text/plain",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="{name}.ged"'
                ),
            },
        )

    return JSONResponse(
        status_code=501,
        content={
            "detail": (
                f"Export format '{format}' "
                "not implemented yet."
            ),
        },
    )
