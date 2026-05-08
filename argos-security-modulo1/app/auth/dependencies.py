from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security.token import decode_token
from app.database.json_db import read_json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    users = read_json("users.json", [])
    user = next((u for u in users if u["id"] == payload.get("sub")), None)
    if not user or user.get("status") != "ATIVO":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário inválido ou inativo")
    return user

def require_roles(*allowed_roles: str):
    def checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("profile") not in allowed_roles:
            raise HTTPException(status_code=403, detail="Acesso negado para este perfil")
        return current_user
    return checker
