"""
Lógica de negocio de autenticación, portada 1:1 desde verificar_login() y
registrar_auditoria() de 15_app_visual.py, ahora sobre SQLAlchemy Core (text())
en lugar de mysql.connector.
"""

import json
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import verify_password


def autenticar_usuario(db: Session, username: str, password: str) -> Optional[dict]:
    query = text(
        """
        SELECT u.id_user, u.username, u.password_hash, u.full_name, u.is_active,
               r.role_name, u.hospital_id, h.name_hospital
        FROM users u
        JOIN roles r ON u.role_id = r.id_role
        JOIN hospitals h ON u.hospital_id = h.id_hospital
        WHERE u.username = :username;
        """
    )
    fila = db.execute(query, {"username": username}).mappings().first()

    if fila is None or not fila["is_active"]:
        return None
    if not verify_password(password, fila["password_hash"]):
        return None
    return dict(fila)


def registrar_auditoria(db: Session, id_user: int, action_type: str, entity_affected: str,
                         entity_id: int, detalles: dict) -> None:
    query = text(
        """
        INSERT INTO audit_logs (user_id, action_type, entity_affected, entity_id, details_json)
        VALUES (:user_id, :action_type, :entity_affected, :entity_id, :details_json);
        """
    )
    db.execute(query, {
        "user_id": id_user,
        "action_type": action_type,
        "entity_affected": entity_affected,
        "entity_id": entity_id,
        "details_json": json.dumps(detalles, default=str),
    })
    db.commit()
