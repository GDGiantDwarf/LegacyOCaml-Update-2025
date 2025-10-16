from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from geneweb.core import base_ops
from geneweb.web.admin.schemas import BaseCreate, BaseRename

router = APIRouter()


@router.get("", summary="List all existing bases")
def list_bases():
    """Retourne la liste des bases (.db) présentes dans le dossier /bases."""
    return {"bases": base_ops.list_bases()}


@router.post("", status_code=201, summary="Create a new base from scratch")
def create_base(payload: BaseCreate):
    """Crée une nouvelle base SQLite vide dans /bases."""
    try:
        base_ops.create_base(payload.name)
        return {"message": "created", "name": payload.name}
    except FileExistsError:
        raise HTTPException(status_code=409, detail="Base already exists")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/{name}/cleanup", summary="Clean up a base")
def cleanup_base(name: str):
    """Nettoie une base (VACUUM + OPTIMIZE)."""
    try:
        base_ops.cleanup_base(name)
        return {"message": "cleaned", "name": name}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Base not found")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.put("/{name}/rename", summary="Rename an existing base")
def rename_base(name: str, payload: BaseRename):
    """Renomme une base existante (ancien nom -> nouveau nom)."""
    try:
        base_ops.rename_base(name, payload.new_name)
        return {"message": "renamed", "from": name, "to": payload.new_name}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Base not found")
    except FileExistsError:
        raise HTTPException(status_code=409, detail="Target already exists")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{name}", status_code=204, summary="Delete a base")
def delete_base(name: str):
    """Supprime une base (.db)."""
    try:
        base_ops.delete_base(name)
        return JSONResponse(status_code=204, content=None)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Base not found")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
