from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StockConsumptionItem(BaseModel):
    """Un insumo consumido dentro de la OT (referenciado por id_inputs)."""
    id_inputs: int
    quantity_used: int = Field(gt=0)


class WorkOrderCreate(BaseModel):
    id_equipment: int
    date_work_start: datetime
    date_work_finish: Optional[datetime] = None
    type_maintenance: str  # 'corrective' | 'preventive'
    description_fault: str
    description_work_done: str
    destination_service: Optional[str] = None  # para la bitácora de stock_movements
    insumos_consumidos: List[StockConsumptionItem] = []

    @field_validator("type_maintenance")
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        if v not in ("corrective", "preventive"):
            raise ValueError("type_maintenance debe ser 'corrective' o 'preventive'.")
        return v

    @field_validator("date_work_finish")
    @classmethod
    def validar_fechas(cls, v, info):
        inicio = info.data.get("date_work_start")
        if v is not None and inicio is not None and v < inicio:
            raise ValueError("date_work_finish no puede ser anterior a date_work_start.")
        return v


class WorkOrderResponse(BaseModel):
    id_work_order: int
    hospital_id: int
    id_equipment: int
    date_work_start: datetime
    date_work_finish: Optional[datetime] = None
    type_maintenance: str
    description_fault: Optional[str] = None
    description_work_done: Optional[str] = None
    id_user_responsible: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
