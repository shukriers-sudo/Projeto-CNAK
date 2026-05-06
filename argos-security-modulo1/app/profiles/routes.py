from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.database.json_db import read_json, write_json
from app.auth.dependencies import require_roles, get_current_user
from app.utils.id_generator import generate_id
from app.utils.time import now_iso

router = APIRouter(prefix="/perfis", tags=["Perfis"])

class ProfileCreate(BaseModel):
    name: str
    description: str
    permissions: List[str] = []

@router.post("")
def create_profile(data: ProfileCreate, current_user: dict = Depends(require_roles("ADMIN_GLOBAL"))):
    profiles = read_json("profiles.json", [])
    if any(p["name"] == data.name for p in profiles):
        raise HTTPException(status_code=400, detail="Perfil já existe")
    profile = {
        "id": generate_id("PRF"),
        "name": data.name,
        "description": data.description,
        "permissions": data.permissions,
        "created_at": now_iso()
    }
    profiles.append(profile)
    write_json("profiles.json", profiles)
    return {"status": "sucesso", "dados": profile}

@router.get("")
def list_profiles(current_user: dict = Depends(get_current_user)):
    return {"status": "sucesso", "dados": read_json("profiles.json", [])}
