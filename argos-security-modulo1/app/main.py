from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.profiles.routes import router as profiles_router
from app.modules.routes import router as modules_router
from app.environments.routes import router as environments_router
from app.audit_routes import router as audit_router
from app.database.json_db import read_json, write_json
from app.utils.time import now_iso

app = FastAPI(
    title="ARGOS Security - Controle Inteligente de Acesso",
    description="Módulo 1 da plataforma ARGOS Segurança: identidade, usuários, perfis, módulos, ambientes e autenticação.",
    version="1.0.0"
)


@app.on_event("startup")
def seed_database():
    users = read_json("users.json", [])

    if not users:
        users.append({
            "id": "USR-ADMIN-001",
            "full_name": "Administrador ARGOS",
            "email": "admin@argos.com",
            "document": None,
            "phone": None,
            "password_hash": "admin123",
            "profile": "ADMIN_GLOBAL",
            "status": "ATIVO",
            "risk_level": "BAIXO",
            "allowed_environments": ["ALL"],
            "mfa_enabled": False,
            "facial_biometric_ready": False,
            "voice_biometric_ready": False,
            "created_at": now_iso(),
            "updated_at": now_iso()
        })
        write_json("users.json", users)

    if not read_json("profiles.json", []):
        write_json("profiles.json", [
            {
                "id": "PRF-001",
                "name": "ADMIN_GLOBAL",
                "description": "Acesso total ao sistema ARGOS",
                "permissions": ["*"]
            },
            {
                "id": "PRF-002",
                "name": "GESTOR_SEGURANCA",
                "description": "Gestão operacional de segurança",
                "permissions": [
                    "usuarios:read",
                    "ambientes:*",
                    "modulos:read",
                    "auditoria:read"
                ]
            },
            {
                "id": "PRF-003",
                "name": "OPERADOR",
                "description": "Operação diária do sistema",
                "permissions": [
                    "usuarios:read",
                    "ambientes:read",
                    "modulos:read"
                ]
            },
            {
                "id": "PRF-004",
                "name": "AUDITOR",
                "description": "Consulta e auditoria",
                "permissions": [
                    "audit:read",
                    "usuarios:read",
                    "ambientes:read"
                ]
            },
            {
                "id": "PRF-005",
                "name": "VISITANTE",
                "description": "Acesso limitado e temporário",
                "permissions": []
            }
        ])

    if not read_json("modules.json", []):
        write_json("modules.json", [
            {
                "id": "MOD-001",
                "name": "Controle de Acesso",
                "description": "Identidade, usuários, perfis, permissões e ambientes",
                "criticality": "CRITICA",
                "requires_mfa": True,
                "status": "ATIVO"
            },
            {
                "id": "MOD-002",
                "name": "Gerenciamento de Equipamentos",
                "description": "Gestão de câmeras, catracas, cancelas, sensores e totens",
                "criticality": "ALTA",
                "requires_mfa": True,
                "status": "PLANEJADO"
            },
            {
                "id": "MOD-003",
                "name": "Monitoramento de Ambientes",
                "description": "Monitoramento dos prédios, estacionamento, fluxo e alertas",
                "criticality": "CRITICA",
                "requires_mfa": True,
                "status": "PLANEJADO"
            },
            {
                "id": "MOD-004",
                "name": "Auditoria",
                "description": "Registros, rastreabilidade, relatórios e conformidade",
                "criticality": "CRITICA",
                "requires_mfa": True,
                "status": "PLANEJADO"
            },
            {
                "id": "MOD-005",
                "name": "Análise / Mapa de Calor",
                "description": "BI, heatmap, análise de fluxo e inteligência comercial",
                "criticality": "ALTA",
                "requires_mfa": True,
                "status": "PLANEJADO"
            }
        ])

    if not read_json("environments.json", []):
        write_json("environments.json", [
            {
                "id": "ENV-001",
                "name": "CNAK Prédio 01",
                "type": "PREDIO",
                "location": "Complexo CNAK",
                "capacity": 2500,
                "risk_level": "ALTO",
                "status": "ATIVO",
                "observations": "Unidade piloto do projeto ARGOS"
            },
            {
                "id": "ENV-002",
                "name": "CNAK Prédio 02",
                "type": "PREDIO",
                "location": "Complexo CNAK",
                "capacity": 2500,
                "risk_level": "ALTO",
                "status": "ATIVO",
                "observations": "Unidade preparada para expansão"
            },
            {
                "id": "ENV-003",
                "name": "Estacionamento CNAK",
                "type": "ESTACIONAMENTO",
                "location": "Área externa",
                "capacity": 800,
                "risk_level": "MEDIO",
                "status": "ATIVO",
                "observations": "Preparado para LPR futuro"
            },
            {
                "id": "ENV-004",
                "name": "CCO - Central de Controle Operacional",
                "type": "AREA_RESTRITA",
                "location": "Administração CNAK",
                "capacity": 30,
                "risk_level": "CRITICO",
                "status": "ATIVO",
                "observations": "Ambiente de acesso restrito"
            }
        ])

    read_json("sessions.json", [])
    read_json("audit_preview.json", [])
    read_json("permissions.json", [])
    read_json("access_rules.json", [])


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(profiles_router)
app.include_router(modules_router)
app.include_router(environments_router)
app.include_router(audit_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "projeto": "ARGOS Security",
        "cliente": "CNAK",
        "modulo": "Módulo 1 - Controle Inteligente de Acesso",
        "docs": "/docs"
    }