from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StockMovement(BaseModel):
    id_movement: int
    hospital_id: int
    id_inputs: int
    id_work_order: Optional[int] = None
    movement_type: str  # 'salida_orden' | 'salida_directa' | 'ingreso_compra' | 'ajuste_inventario'
    id_reason: Optional[int] = None
    quantity: int
    destination_service: Optional[str] = None
    id_user_requested: Optional[int] = None
    id_user_dispatched: Optional[int] = None
    movement_date: datetime
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
