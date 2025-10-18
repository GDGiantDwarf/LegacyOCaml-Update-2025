from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import tempfile
import shutil
from geneweb.core.database import BaseManager

router = APIRouter(prefix="/api/bases", tags=["admin:backup"])

BACKUP_DIR = Path("./backups")

@router.post("/{name}/backup")
def backup_base(name: str, base_dir: str | None = None):
    db_path = BaseManager.base_path(name, base_dir)
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Base not found")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    out = BACKUP_DIR / f"{name}.zip"
    with ZipFile(out, "w", ZIP_DEFLATED) as z:
        z.write(db_path, arcname=f"{name}.db")
    return FileResponse(out, media_type="application/zip", filename=out.name)

@router.post("/restore")
async def restore_backup(
        file: UploadFile = File(...),
        target_name: str = Form(...),
        base_dir: str | None = None,
):
    BaseManager._validate_name(target_name)
    target = BaseManager.base_path(target_name, base_dir)
    if target.exists():
        raise HTTPException(status_code=409, detail="Target base already exists")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / file.filename
        with open(tmp, "wb") as f:
            f.write(await file.read())
        with ZipFile(tmp) as z:
            cand = next((m for m in z.namelist() if m.endswith(".db")), None)
            if not cand:
                raise HTTPException(status_code=400, detail="No .db file in archive")
            z.extract(cand, Path(td))
            shutil.move(Path(td) / cand, target)
    return {"status": "ok", "name": target_name}
