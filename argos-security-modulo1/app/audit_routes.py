from fastapi import APIRouter, Depends
from app.database.json_db import read_json
from app.auth.dependencies import require_roles

router = APIRouter(prefix="/auditoria-preview", tags=["Auditoria Preview"])

@router.get("")
def list_audit_preview(current_user: dict = Depends(require_roles("ADMIN_GLOBAL", "GESTOR_SEGURANCA", "AUDITOR"))):
    return {"status": "sucesso", "dados": read_json("audit_preview.json", [])}
