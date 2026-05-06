from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database.json_db import read_json, write_json
from app.auth.dependencies import require_roles, get_current_user
from app.utils.id_generator import generate_id
from app.utils.time import now_iso

router = APIRouter(prefix="/ambientes", tags=["Ambientes"])

class EnvironmentCreate(BaseModel):
    name: str
    type: str
    location: str
    capacity: int = 0
    risk_level: str = "BAIXO"
    status: str = "ATIVO"
    observations: Optional[str] = None

class EnvironmentUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    risk_level: Optional[str] = None
    status: Optional[str] = None
    observations: Optional[str] = None

@router.post("")
def create_environment(data: EnvironmentCreate, current_user: dict = Depends(require_roles("ADMIN_GLOBAL", "GESTOR_SEGURANCA"))):
    environments = read_json("environments.json", [])
    environment = {
        "id": generate_id("ENV"),
        **data.model_dump(),
        "created_at": now_iso(),
        "updated_at": now_iso()
    }
    environments.append(environment)
    write_json("environments.json", environments)
    return {"status": "sucesso", "dados": environment}

@router.get("")
def list_environments(current_user: dict = Depends(get_current_user)):
    return {"status": "sucesso", "dados": read_json("environments.json", [])}

@router.put("/{environment_id}")
def update_environment(environment_id: str, data: EnvironmentUpdate, current_user: dict = Depends(require_roles("ADMIN_GLOBAL", "GESTOR_SEGURANCA"))):
    environments = read_json("environments.json", [])
    for environment in environments:
        if environment["id"] == environment_id:
            environment.update(data.model_dump(exclude_unset=True))
            environment["updated_at"] = now_iso()
            write_json("environments.json", environments)
            return {"status": "sucesso", "dados": environment}
    raise HTTPException(status_code=404, detail="Ambiente não encontrado")
