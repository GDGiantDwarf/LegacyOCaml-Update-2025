from fastapi import (
    APIRouter, HTTPException, UploadFile, File, Form,
)
from fastapi.responses import JSONResponse
from pathlib import Path
from zipfile import ZipFile
import shutil
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geneweb.core.database import BaseManager
from geneweb.core.models.alchemyBase import Base
from geneweb.core.services.gedcom_converter import (
    import_from_gedcom,
)

router = APIRouter(prefix="/api/bases", tags=["admin:import"])


@router.post("/import")
async def import_base(
    file: UploadFile = File(...),
    name: str = Form(...),
    format: str = Form("sqlite"),
    base_dir: str | None = None,
):
    BaseManager._validate_name(name)

    bases_dir = BaseManager.bases_dir(base_dir)
    target = bases_dir / f"{name}.db"
    if target.exists():
        raise HTTPException(
            status_code=409,
            detail="Target base already exists",
        )

    with tempfile.TemporaryDirectory() as td:
        tmp_path = Path(td) / file.filename
        with open(tmp_path, "wb") as f:
            f.write(await file.read())

        if format == "sqlite":
            shutil.copy(tmp_path, target)
            return {"status": "ok", "name": name}

        if format == "zip":
            with ZipFile(tmp_path) as z:
                cand = next(
                    (
                        m for m in z.namelist()
                        if m.endswith(".db")
                    ),
                    None,
                )
                if not cand:
                    raise HTTPException(
                        status_code=400,
                        detail="No .db file in archive",
                    )
                z.extract(cand, Path(td))
                shutil.move(Path(td) / cand, target)
            return {"status": "ok", "name": name}

        if format == "gedcom":
            content = tmp_path.read_text(
                encoding="utf-8"
            )
            engine = create_engine(
                f"sqlite:///{target}",
                connect_args={
                    "check_same_thread": False,
                },
            )
            Base.metadata.create_all(bind=engine)
            session_factory = sessionmaker(bind=engine)
            session = session_factory()
            try:
                result = import_from_gedcom(
                    content, session
                )
            except Exception as exc:
                session.rollback()
                if target.exists():
                    target.unlink()
                raise HTTPException(
                    status_code=400,
                    detail=f"GEDCOM parse error: {exc}",
                ) from exc
            finally:
                session.close()
                engine.dispose()
            return {
                "status": "ok",
                "name": name,
                **result,
            }

    return JSONResponse(
        status_code=501,
        content={
            "detail": (
                f"Import format '{format}' "
                "not implemented yet."
            ),
        },
    )
