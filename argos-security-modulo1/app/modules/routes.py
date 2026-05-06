from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database.json_db import read_json, write_json
from app.auth.dependencies import require_roles, get_current_user
from app.utils.id_generator import generate_id
from app.utils.time import now_iso

router = APIRouter(prefix="/modulos", tags=["Módulos"])

class ModuleCreate(BaseModel):
    name: str
    description: str
    criticality: str = "MEDIA"
    requires_mfa: bool = False

class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    criticality: Optional[str] = None
    requires_mfa: Optional[bool] = None
    status: Optional[str] = None

@router.post("")
def create_module(data: ModuleCreate, current_user: dict = Depends(require_roles("ADMIN_GLOBAL"))):
    modules = read_json("modules.json", [])
    module = {
        "id": generate_id("MOD"),
        "name": data.name,
        "description": data.description,
        "criticality": data.criticality,
        "requires_mfa": data.requires_mfa,
        "status": "ATIVO",
        "created_at": now_iso(),
        "updated_at": now_iso()
    }
    modules.append(module)
    write_json("modules.json", modules)
    return {"status": "sucesso", "dados": module}

@router.get("")
def list_modules(current_user: dict = Depends(get_current_user)):
    return {"status": "sucesso", "dados": read_json("modules.json", [])}

@router.put("/{module_id}")
def update_module(module_id: str, data: ModuleUpdate, current_user: dict = Depends(require_roles("ADMIN_GLOBAL"))):
    modules = read_json("modules.json", [])
    for module in modules:
        if module["id"] == module_id:
            module.update(data.model_dump(exclude_unset=True))
            module["updated_at"] = now_iso()
            write_json("modules.json", modules)
            return {"status": "sucesso", "dados": module}
    raise HTTPException(status_code=404, detail="Módulo não encontrado")
