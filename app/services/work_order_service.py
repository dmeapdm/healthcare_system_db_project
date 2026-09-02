"""
Servicio de Órdenes de Trabajo.

crear_orden_trabajo() es una operación transaccional de punta a punta:
  1. Valida que el equipo pertenezca al hospital del usuario autenticado.
  2. Inserta la OT, con id_user_responsible tomado del JWT (nunca del body:
     así nadie puede "firmar" una OT en nombre de otro usuario).
  3. Por cada insumo consumido: bloquea la fila de `inputs` (SELECT ... FOR
     UPDATE), valida stock suficiente, descuenta, inserta en
     `work_order_inputs` y registra el movimiento en `stock_movements`
     ('salida_orden').
  4. Registra la auditoría (WORK_ORDER_CLOSE).

Todo corre en la MISMA transacción de SQLAlchemy (la sesión que entrega
get_db mantiene autocommit=False). Si cualquier paso falla -incluido stock
insuficiente en cualquier insumo- se hace ROLLBACK completo: no queda ni la
OT ni ningún descuento de stock a medio guardar.
"""

import json
from typing import Optional

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.schemas.work_order import WorkOrderCreate


class EquipoNoEncontradoError(Exception):
    pass


class InsumoNoEncontradoError(Exception):
    pass


class StockInsuficienteError(Exception):
    def __init__(self, id_inputs: int, solicitado: int, disponible: int):
        self.id_inputs = id_inputs
        self.solicitado = solicitado
        self.disponible = disponible
        super().__init__(
            f"Stock insuficiente para el insumo id={id_inputs}: "
            f"solicitado {solicitado}, disponible {disponible}."
        )


def crear_orden_trabajo(db: Session, datos: WorkOrderCreate, current_user: dict) -> dict:
    hospital_id = current_user["hospital_id"]
    id_user_responsible = current_user["id_user"]
    id_work_order: Optional[int] = None

    try:
        # 1. El equipo debe existir y pertenecer al hospital del usuario
        equipo = db.execute(
            text("SELECT id_equipment FROM equipment WHERE id_equipment = :id AND hospital_id = :hospital_id;"),
            {"id": datos.id_equipment, "hospital_id": hospital_id},
        ).first()
        if equipo is None:
            raise EquipoNoEncontradoError(
                f"El equipo id={datos.id_equipment} no existe o no pertenece a tu hospital."
            )

        # 2. Insertar la Orden de Trabajo (id_user_responsible viene del JWT, no del body)
        result = db.execute(
            text("""
                INSERT INTO work_order (hospital_id, id_equipment, date_work_start, date_work_finish,
                                         type_maintenance, description_fault, description_work_done,
                                         id_user_responsible)
                VALUES (:hospital_id, :id_equipment, :date_work_start, :date_work_finish,
                        :type_maintenance, :description_fault, :description_work_done, :id_user_responsible);
            """),
            {
                "hospital_id": hospital_id,
                "id_equipment": datos.id_equipment,
                "date_work_start": datos.date_work_start,
                "date_work_finish": datos.date_work_finish,
                "type_maintenance": datos.type_maintenance,
                "description_fault": datos.description_fault,
                "description_work_done": datos.description_work_done,
                "id_user_responsible": id_user_responsible,
            },
        )
        id_work_order = result.lastrowid

        # 3. Descuento atómico de stock por cada insumo consumido
        # FOR UPDATE es sintaxis MySQL para bloquear la fila hasta el
        # commit/rollback de esta transacción (evita condiciones de carrera
        # si dos técnicos despachan el mismo insumo al mismo tiempo). SQLite
        # no soporta esa cláusula -y no la necesita, porque ya serializa
        # escrituras a nivel de base de datos- así que se omite en tests.
        usa_row_lock = db.bind.dialect.name == "mysql"
        clausula_lock = "FOR UPDATE" if usa_row_lock else ""

        for item in datos.insumos_consumidos:
            fila_stock = db.execute(
                text(f"""
                    SELECT stock FROM inputs
                    WHERE id_inputs = :id AND hospital_id = :hospital_id
                    {clausula_lock};
                """),
                {"id": item.id_inputs, "hospital_id": hospital_id},
            ).first()
            if fila_stock is None:
                raise InsumoNoEncontradoError(
                    f"El insumo id={item.id_inputs} no existe o no pertenece a tu hospital."
                )

            stock_actual = fila_stock[0]
            if stock_actual < item.quantity_used:
                raise StockInsuficienteError(item.id_inputs, item.quantity_used, stock_actual)

            db.execute(
                text("""
                    INSERT INTO work_order_inputs (id_work_order, id_inputs, quantity_used)
                    VALUES (:wo, :ins, :qty);
                """),
                {"wo": id_work_order, "ins": item.id_inputs, "qty": item.quantity_used},
            )
            db.execute(
                text("UPDATE inputs SET stock = stock - :qty WHERE id_inputs = :id;"),
                {"qty": item.quantity_used, "id": item.id_inputs},
            )
            db.execute(
                text("""
                    INSERT INTO stock_movements (hospital_id, id_inputs, id_work_order, movement_type,
                                                  quantity, destination_service, id_user_requested,
                                                  id_user_dispatched, notes)
                    VALUES (:hospital_id, :id_inputs, :id_wo, 'salida_orden', :qty, :destino,
                            :id_user, :id_user, :notas);
                """),
                {
                    "hospital_id": hospital_id,
                    "id_inputs": item.id_inputs,
                    "id_wo": id_work_order,
                    "qty": item.quantity_used,
                    "destino": datos.destination_service,
                    "id_user": id_user_responsible,
                    "notas": f"Consumido automáticamente en reparación bajo Orden de Trabajo N° {id_work_order}.",
                },
            )

        # 4. Auditoría — si algo de los pasos 2/3 falló, esto nunca se ejecuta
        db.execute(
            text("""
                INSERT INTO audit_logs (user_id, action_type, entity_affected, entity_id, details_json)
                VALUES (:user_id, 'WORK_ORDER_CLOSE', 'work_order', :entity_id, :details_json);
            """),
            {
                "user_id": id_user_responsible,
                "entity_id": id_work_order,
                "details_json": json.dumps(
                    {
                        "id_equipment": datos.id_equipment,
                        "type_maintenance": datos.type_maintenance,
                        "insumos_consumidos": [item.model_dump() for item in datos.insumos_consumidos],
                    },
                    default=str,
                ),
            },
        )

        db.commit()

    except (SQLAlchemyError, EquipoNoEncontradoError, InsumoNoEncontradoError, StockInsuficienteError):
        db.rollback()
        raise

    fila_final = db.execute(
        text("""
            SELECT id_work_order, hospital_id, id_equipment, date_work_start, date_work_finish,
                   type_maintenance, description_fault, description_work_done, id_user_responsible
            FROM work_order WHERE id_work_order = :id;
        """),
        {"id": id_work_order},
    ).mappings().first()
    return dict(fila_final)
