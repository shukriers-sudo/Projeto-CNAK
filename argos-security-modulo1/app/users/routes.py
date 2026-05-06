from fastapi import APIRouter, HTTPException, Depends
from app.users.schemas import UserCreate, UserUpdate
from app.database.json_db import read_json, write_json
from app.security.password import hash_password
from app.auth.dependencies import require_roles, get_current_user
from app.utils.id_generator import generate_id
from app.utils.time import now_iso

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

def sanitize(user: dict):
    safe = user.copy()
    safe.pop("password_hash", None)
    return safe

@router.post("")
def create_user(data: UserCreate, current_user: dict = Depends(require_roles("ADMIN_GLOBAL", "GESTOR_SEGURANCA"))):
    users = read_json("users.json", [])
    if any(u["email"].lower() == data.email.lower() for u in users):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = {
        "id": generate_id("USR"),
        "full_name": data.full_name,
        "email": data.email,
        "document": data.document,
        "phone": data.phone,
        "password_hash": hash_password(data.password),
        "profile": data.profile,
        "status": "ATIVO",
        "risk_level": "BAIXO",
        "allowed_environments": data.allowed_environments,
        "mfa_enabled": False,
        "facial_biometric_ready": False,
        "voice_biometric_ready": False,
        "created_at": now_iso(),
        "updated_at": now_iso()
    }
    users.append(user)
    write_json("users.json", users)
    return {"status": "sucesso", "mensagem": "Usuário criado", "dados": sanitize(user)}

@router.get("")
def list_users(current_user: dict = Depends(get_current_user)):
    users = read_json("users.json", [])
    return {"status": "sucesso", "dados": [sanitize(u) for u in users]}

@router.get("/{user_id}")
def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    users = read_json("users.json", [])
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"status": "sucesso", "dados": sanitize(user)}

@router.put("/{user_id}")
def update_user(user_id: str, data: UserUpdate, current_user: dict = Depends(require_roles("ADMIN_GLOBAL", "GESTOR_SEGURANCA"))):
    users = read_json("users.json", [])
    for user in users:
        if user["id"] == user_id:
            update_data = data.model_dump(exclude_unset=True)
            user.update(update_data)
            user["updated_at"] = now_iso()
            write_json("users.json", users)
            return {"status": "sucesso", "mensagem": "Usuário atualizado", "dados": sanitize(user)}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@router.patch("/{user_id}/inativar")
def deactivate_user(user_id: str, current_user: dict = Depends(require_roles("ADMIN_GLOBAL"))):
    users = read_json("users.json", [])
    for user in users:
        if user["id"] == user_id:
            user["status"] = "INATIVO"
            user["updated_at"] = now_iso()
            write_json("users.json", users)
            return {"status": "sucesso", "mensagem": "Usuário inativado"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
