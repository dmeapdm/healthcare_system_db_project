"""
Configuración centralizada de la app, leída desde variables de entorno (.env).
No usamos pydantic-settings a propósito: no fue parte de las dependencias
pedidas, y esta clase simple con os.getenv cubre lo que necesitamos hoy.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- Base de datos ---
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "tecnico_biomedica")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "healthcare_system_db")

    # --- Seguridad / JWT ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CAMBIAR_EN_PRODUCCION")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


settings = Settings()
