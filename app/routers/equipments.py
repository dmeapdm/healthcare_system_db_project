from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.equipment import EquipmentResponse, WorkOrderHistoryItem
from app.services.equipment_service import (
    obtener_equipo_por_id,
    obtener_equipo_por_serie,
    obtener_historial_equipo,
)

router = APIRouter(prefix="/equipments", tags=["Equipos"])


@router.get("/serial/{serial_number}", response_model=EquipmentResponse)
def buscar_por_serie(
    serial_number: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Búsqueda por número de serie de fábrica (para el flujo de escaneo/QR)."""
    equipo = obtener_equipo_por_serie(db, current_user["hospital_id"], serial_number)
    if equipo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado en tu hospital.")
    return equipo


@router.get("/{id_equipment}", response_model=EquipmentResponse)
def obtener_equipo(
    id_equipment: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    equipo = obtener_equipo_por_id(db, current_user["hospital_id"], id_equipment)
    if equipo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado en tu hospital.")
    return equipo


@router.get("/{id_equipment}/history", response_model=List[WorkOrderHistoryItem])
def historial_equipo(
    id_equipment: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Historial completo de intervenciones (incluye las importadas de la
    Agenda Elomed vía 16_import_elomed_data.py, ya resueltas por técnico)."""
    equipo = obtener_equipo_por_id(db, current_user["hospital_id"], id_equipment)
    if equipo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado en tu hospital.")
    return obtener_historial_equipo(db, current_user["hospital_id"], id_equipment)
