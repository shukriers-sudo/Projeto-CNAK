# ARGOS Security - Módulo 1: Controle Inteligente de Acesso

Sistema base da plataforma ARGOS Segurança.

## Rodar o projeto

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Depois acesse:

http://127.0.0.1:8000/docs

## Login padrão

E-mail: admin@argos.com  
Senha: Argos@123

## Módulo 1 inclui

- CRUD de usuários
- CRUD de perfis
- CRUD de módulos
- CRUD de ambientes
- Banco JSON
- Login com JWT
- Senha com hash
- Permissões por perfil
- Logs básicos de auditoria
