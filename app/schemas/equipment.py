from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EquipmentResponse(BaseModel):
    id_equipment: int
    hospital_id: int
    serial_number_factory: Optional[str] = None
    type_device: str
    category: str
    brand: Optional[str] = None
    model: Optional[str] = None
    year_manufactured: Optional[int] = None
    state: str
    location: Optional[str] = None
    power_requirements: Optional[str] = None
    date_inventory_updated: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class WorkOrderHistoryItem(BaseModel):
    """Un ítem del historial de intervenciones de un equipo (incluye tanto las
    OT nuevas como las importadas de la Agenda Elomed vía 16_import_elomed_data.py)."""
    id_work_order: int
    type_maintenance: str
    date_work_start: datetime
    date_work_finish: Optional[datetime] = None
    description_fault: Optional[str] = None
    description_work_done: Optional[str] = None
    technical_responsible: Optional[str] = None  # resuelto: usuario real o legacy

    model_config = ConfigDict(from_attributes=True)
