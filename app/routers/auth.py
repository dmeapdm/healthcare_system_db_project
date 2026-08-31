from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.user import Token, UserLogin
from app.services.auth_service import autenticar_usuario, registrar_auditoria

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token)
def login(credenciales: UserLogin, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, credenciales.username, credenciales.password)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos, o el usuario está inactivo.",
        )

    token = create_access_token(data={
        "sub": usuario["username"],
        "id_user": usuario["id_user"],
        "role_name": usuario["role_name"],
        "hospital_id": usuario["hospital_id"],
    })

    registrar_auditoria(
        db, usuario["id_user"], "LOGIN", "users", usuario["id_user"],
        {"username": usuario["username"]}
    )

    return Token(access_token=token)
