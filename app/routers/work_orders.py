from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.work_order import WorkOrderCreate, WorkOrderResponse
from app.services.work_order_service import (
    EquipoNoEncontradoError,
    InsumoNoEncontradoError,
    StockInsuficienteError,
    crear_orden_trabajo,
)

router = APIRouter(prefix="/work-orders", tags=["Órdenes de Trabajo"])


@router.post("", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
def crear_work_order(
    datos: WorkOrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Crea una nueva Orden de Trabajo. id_user_responsible se toma del token
    JWT del usuario autenticado, nunca del body de la request.

    Si `insumos_consumidos` no está vacío, el descuento de stock y el
    registro en `stock_movements` ocurren dentro de la misma transacción
    que la OT: o se guarda todo, o no se guarda nada (ver work_order_service).
    """
    try:
        nueva_ot = crear_orden_trabajo(db, datos, current_user)
    except (StockInsuficienteError, EquipoNoEncontradoError, InsumoNoEncontradoError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return nueva_ot
