"""
Capa de seguridad de la API.

IMPORTANTE (nota de entorno): el hashing de contraseñas usa bcrypt.checkpw /
bcrypt.hashpw exactamente igual que 15_app_visual.py y 08_crear_usuario_admin.py.
Esto es intencional: los hashes ya guardados en la tabla `users` (generados
por bcrypt.hashpw + bcrypt.gensalt) siguen siendo válidos acá sin necesidad
de re-hashear nada al migrar de Streamlit a la API.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Equivalente directo al patrón bcrypt.checkpw() usado en la app Streamlit."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def hash_password(plain_password: str) -> str:
    """Equivalente directo al patrón de 08_crear_usuario_admin.py."""
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
