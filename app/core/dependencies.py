"""
Dependency de FastAPI para proteger endpoints con JWT.
El token trae embebidas las claims que /auth/login generó: 'sub' (estándar
JWT para el identificador del usuario, mapeado acá a username), id_user,
role_name y hospital_id. No volvemos a golpear la base de datos en cada
request protegido — solo se decodifica/valida el token.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    campos_requeridos = ("id_user", "role_name", "hospital_id")
    if username is None or not all(campo in payload for campo in campos_requeridos):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token con formato inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "username": username,
        "id_user": payload["id_user"],
        "role_name": payload["role_name"],
        "hospital_id": payload["hospital_id"],
    }
