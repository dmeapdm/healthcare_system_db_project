"""
Servicio de Equipos. Todas las consultas filtran por hospital_id (aislamiento
multi-tenant): un usuario nunca puede ver ni vincular equipos de otro hospital,
aunque conozca su id_equipment.
"""

from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

_CAMPOS_EQUIPMENT = """
    id_equipment, hospital_id, serial_number_factory, type_device, category,
    brand, model, year_manufactured, state, location, power_requirements,
    date_inventory_updated
"""


def obtener_equipo_por_serie(db: Session, hospital_id: int, serial: str) -> Optional[dict]:
    query = text(f"""
        SELECT {_CAMPOS_EQUIPMENT}
        FROM equipment
        WHERE hospital_id = :hospital_id AND serial_number_factory = :serial;
    """)
    fila = db.execute(query, {"hospital_id": hospital_id, "serial": serial}).mappings().first()
    return dict(fila) if fila else None


def obtener_equipo_por_id(db: Session, hospital_id: int, id_equipment: int) -> Optional[dict]:
    query = text(f"""
        SELECT {_CAMPOS_EQUIPMENT}
        FROM equipment
        WHERE hospital_id = :hospital_id AND id_equipment = :id_equipment;
    """)
    fila = db.execute(query, {"hospital_id": hospital_id, "id_equipment": id_equipment}).mappings().first()
    return dict(fila) if fila else None


def obtener_historial_equipo(db: Session, hospital_id: int, id_equipment: int) -> List[dict]:
    """Historial de intervenciones de un equipo: incluye tanto las OT nuevas
    (creadas vía API, con id_user_responsible) como las históricas importadas
    de la Agenda Elomed (con technical_responsible_legacy). COALESCE resuelve
    cuál mostrar sin que el consumidor de la API tenga que saber la diferencia."""
    query = text("""
        SELECT
            w.id_work_order, w.type_maintenance, w.date_work_start, w.date_work_finish,
            w.description_fault, w.description_work_done,
            COALESCE(u.full_name, w.technical_responsible_legacy, 'Sin registrar') AS technical_responsible
        FROM work_order w
        LEFT JOIN users u ON w.id_user_responsible = u.id_user
        WHERE w.hospital_id = :hospital_id AND w.id_equipment = :id_equipment
        ORDER BY w.date_work_start DESC;
    """)
    filas = db.execute(query, {"hospital_id": hospital_id, "id_equipment": id_equipment}).mappings().all()
    return [dict(f) for f in filas]
