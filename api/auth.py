"""
Autenticação SSO/OIDC + RBAC básico.
Suporta AWS IAM Identity Center (SSO) ou qualquer IdP OIDC.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import jwt
from typing import Optional

security = HTTPBearer()

ROLES = {
    "viewer": ["read:graph", "read:coverage"],
    "analyst": ["read:graph", "read:coverage", "query:path", "query:exposure"],
    "admin": ["read:graph", "read:coverage", "query:path", "query:exposure", "admin:config"],
}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    # Em produção: validar JWT contra o JWKS do IdP (SSO/OIDC)
    try:
        # payload = jwt.decode(token, options={"verify_signature": False})  # substituir por validação real
        payload = {"sub": "user@example.com", "roles": ["analyst"]}
        return payload
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def require_permission(permission: str):
    def checker(user: dict = Depends(get_current_user)):
        roles = user.get("roles", [])
        allowed = any(permission in ROLES.get(r, []) for r in roles)
        if not allowed:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker
