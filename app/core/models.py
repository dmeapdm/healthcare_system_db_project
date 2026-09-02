"""
Modelos SQLAlchemy declarativos.

NOTA ARQUITECTÓNICA: la capa de servicios (equipment_service.py,
work_order_service.py, auth_service.py) usa SQL crudo parametrizado con
sqlalchemy.text() en vez de estos modelos, a propósito — nos da control
total sobre CHECK constraints, row-locking MySQL-específico y la estructura
exacta ya definida en 01/04/05/06/07_*.sql. Estos modelos declarativos
existen ÚNICAMENTE para poder generar el esquema en la base de datos de
pruebas SQLite in-memory con Base.metadata.create_all() (ver
tests/conftest.py) — no se usan en el código de producción contra MySQL.

Por eso este archivo NO incluye los triggers de inmutabilidad de audit_logs
(BEFORE UPDATE/DELETE con SIGNAL SQLSTATE) ni la tabla reposition_reasons:
son sintaxis específica de MySQL / no están ejercitadas por los tests
actuales. Si más adelante se agregan tests de Almacén (salida directa con
motivo obligatorio), habrá que sumar el modelo RepositionReason acá.
"""

from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer,
    Numeric, String, Text,
)
from sqlalchemy.sql import func

from app.core.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id_hospital = Column(Integer, primary_key=True, autoincrement=True)
    name_hospital = Column(String(150), nullable=False)
    address = Column(String(255))
    is_active = Column(Boolean, default=True)


class Role(Base):
    __tablename__ = "roles"

    id_role = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id_role"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id_hospital"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class Equipment(Base):
    __tablename__ = "equipment"

    id_equipment = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id_hospital"), nullable=False)
    serial_number_factory = Column(String(50), unique=True)
    type_device = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    year_manufactured = Column(Integer)
    state = Column(String(50), default="OK")
    location = Column(String(100))
    power_requirements = Column(String(100), default="220V / Batería interna")
    id_supplier = Column(Integer, nullable=True)
    date_inventory_updated = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("state IN ('OK','MAINTENANCE','OUT_OF_SERVICE','DISPOSED')", name="chk_equipment_state"),
    )


class WorkOrder(Base):
    __tablename__ = "work_order"

    id_work_order = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id_hospital"), nullable=False)
    id_equipment = Column(Integer, ForeignKey("equipment.id_equipment"), nullable=False)
    date_work_start = Column(DateTime, nullable=False)
    date_work_finish = Column(DateTime)
    type_maintenance = Column(String(50), nullable=False)
    description_fault = Column(Text)
    description_work_done = Column(Text)
    technical_responsible_legacy = Column(String(100))
    id_user_responsible = Column(Integer, ForeignKey("users.id_user"))

    __table_args__ = (
        CheckConstraint("type_maintenance IN ('corrective','preventive')", name="chk_work_order_type"),
    )


class WorkOrderInputs(Base):
    __tablename__ = "work_order_inputs"

    id_work_order = Column(Integer, ForeignKey("work_order.id_work_order"), primary_key=True)
    id_inputs = Column(Integer, ForeignKey("inputs.id_inputs"), primary_key=True)
    quantity_used = Column(Integer, nullable=False, default=1)


class Inputs(Base):
    __tablename__ = "inputs"

    id_inputs = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id_hospital"), nullable=False)
    internal_code = Column(String(50), unique=True)
    input_type = Column(String(30), nullable=False)
    input_category = Column(String(100))
    brand = Column(String(100), default="GENERICO")
    model_ref = Column(String(100))
    name_input = Column(Text, nullable=False)
    unit_of_measure = Column(String(20), nullable=False, default="unidad")
    cabinet_space = Column(String(100))
    drawer_location = Column(String(100))
    stock = Column(Integer, nullable=False, default=0)
    min_stock_alert = Column(Integer, nullable=False, default=5)
    unit_price = Column(Numeric(10, 2))
    id_supplier = Column(Integer, nullable=True)
    compatible_equipment = Column(String(150))
    procurement_notes = Column(String(255))
    is_active = Column(Boolean, default=True)


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id_movement = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id_hospital"), nullable=False)
    id_inputs = Column(Integer, ForeignKey("inputs.id_inputs"), nullable=False)
    id_work_order = Column(Integer, ForeignKey("work_order.id_work_order"))
    movement_type = Column(String(20), nullable=False)
    id_reason = Column(Integer, nullable=True)  # ver nota del módulo: sin FK a reposition_reasons acá
    quantity = Column(Integer, nullable=False)
    destination_service = Column(String(100))
    requested_by_legacy = Column(String(100))
    dispatched_by_legacy = Column(String(100))
    id_user_requested = Column(Integer, ForeignKey("users.id_user"))
    id_user_dispatched = Column(Integer, ForeignKey("users.id_user"))
    movement_date = Column(DateTime, server_default=func.now())
    notes = Column(Text)

    __table_args__ = (
        CheckConstraint(
            "movement_type IN ('salida_orden','salida_directa','ingreso_compra','ajuste_inventario')",
            name="chk_stock_movement_type",
        ),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id_log = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id_user"), nullable=True)
    action_type = Column(String(50), nullable=False)
    entity_affected = Column(String(50), nullable=False)
    entity_id = Column(Integer)
    action_timestamp = Column(DateTime, server_default=func.now())
    details_json = Column(Text)  # SQLite no tiene tipo JSON nativo; se guarda como texto (igual que MySQL vía json.dumps())
