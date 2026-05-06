from fastapi import APIRouter, HTTPException
from app.auth.schemas import LoginRequest
from app.database.json_db import read_json, write_json
from app.security.token import create_access_token
from app.utils.time import now_iso

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login")
def login(data: LoginRequest):
    users = read_json("users.json", [])
    user = next((u for u in users if u["email"].lower() == data.email.lower()), None)

    if not user or data.password != user["password_hash"]:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

    if user.get("status") != "ATIVO":
        raise HTTPException(status_code=403, detail="Usuário inativo, suspenso ou bloqueado")

    token = create_access_token({
        "sub": user["id"],
        "profile": user["profile"]
    })

    sessions = read_json("sessions.json", [])
    sessions.append({
        "user_id": user["id"],
        "email": user["email"],
        "login_at": now_iso()
    })
    write_json("sessions.json", sessions)

    safe_user = user.copy()
    safe_user.pop("password_hash", None)

    return {
        "status": "sucesso",
        "mensagem": "Login realizado com sucesso",
        "access_token": token,
        "token_type": "bearer",
        "usuario": safe_user
    }
