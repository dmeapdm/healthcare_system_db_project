"""
Pruebas de POST /work-orders: autorización, creación exitosa, descuento
transaccional de stock y rollback ante stock insuficiente.
"""

from datetime import datetime, timezone

from app.core import models


def _payload_ot(id_equipment: int, tipo="preventive", insumos=None):
    return {
        "id_equipment": id_equipment,
        "date_work_start": datetime.now(timezone.utc).isoformat(),
        "type_maintenance": tipo,
        "description_fault": "Falla simulada para test automatizado.",
        "description_work_done": "Reparación simulada para test automatizado.",
        "destination_service": "UCI",
        "insumos_consumidos": insumos or [],
    }


def test_create_work_order_success(client, auth_headers, seed_equipment):
    payload = _payload_ot(seed_equipment.id_equipment, tipo="preventive")

    response = client.post("/work-orders", json=payload, headers=auth_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["type_maintenance"] == "preventive"
    assert body["id_equipment"] == seed_equipment.id_equipment
    assert body["id_work_order"] is not None


def test_unauthorized_access(client, seed_equipment):
    payload = _payload_ot(seed_equipment.id_equipment)

    response = client.post("/work-orders", json=payload)  # sin header Authorization

    assert response.status_code == 401


def test_stock_consumption_and_movement(client, auth_headers, db_session, seed_equipment, seed_input_stock):
    stock_inicial = seed_input_stock.stock
    cantidad_consumida = 3

    payload = _payload_ot(
        seed_equipment.id_equipment,
        insumos=[{"id_inputs": seed_input_stock.id_inputs, "quantity_used": cantidad_consumida}],
    )

    response = client.post("/work-orders", json=payload, headers=auth_headers)
    assert response.status_code == 201
    id_work_order = response.json()["id_work_order"]

    # 1. El stock en `inputs` debe haber disminuido exactamente lo consumido
    db_session.refresh(seed_input_stock)
    assert seed_input_stock.stock == stock_inicial - cantidad_consumida

    # 2. Debe existir la fila correspondiente en `stock_movements`
    movimiento = (
        db_session.query(models.StockMovement)
        .filter_by(id_work_order=id_work_order, id_inputs=seed_input_stock.id_inputs)
        .first()
    )
    assert movimiento is not None
    assert movimiento.movement_type == "salida_orden"
    assert movimiento.quantity == cantidad_consumida


def test_insufficient_stock_rollback(client, auth_headers, db_session, seed_equipment, seed_input_stock):
    stock_inicial = seed_input_stock.stock
    cantidad_excesiva = stock_inicial + 100  # más de lo disponible

    payload = _payload_ot(
        seed_equipment.id_equipment,
        insumos=[{"id_inputs": seed_input_stock.id_inputs, "quantity_used": cantidad_excesiva}],
    )

    response = client.post("/work-orders", json=payload, headers=auth_headers)

    assert response.status_code == 400
    assert "stock" in response.json()["detail"].lower()

    # Rollback real: el stock NO debe haber cambiado...
    db_session.refresh(seed_input_stock)
    assert seed_input_stock.stock == stock_inicial

    # ...y tampoco debe haber quedado una Orden de Trabajo huérfana.
    ot_creadas = (
        db_session.query(models.WorkOrder)
        .filter_by(id_equipment=seed_equipment.id_equipment)
        .count()
    )
    assert ot_creadas == 0

    # ...ni un movimiento de stock a medio registrar.
    movimientos = (
        db_session.query(models.StockMovement)
        .filter_by(id_inputs=seed_input_stock.id_inputs)
        .count()
    )
    assert movimientos == 0
