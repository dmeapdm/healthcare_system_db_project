"""
Configuración de pytest para la suite de la API.

Usa una base de datos SQLite en memoria, completamente aislada de
healthcare_system_db (MySQL) — ningún test toca la base de desarrollo.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core import models  # noqa: F401 - necesario para registrar las tablas en Base.metadata
from app.core.database import Base, get_db
from app.core.security import create_access_token, hash_password
from main import app

# =========================================================================
# Motor de pruebas: SQLite en memoria
# =========================================================================
# StaticPool es obligatorio acá: sin él, cada conexión nueva que pida el
# engine a "sqlite:///:memory:" abriría una base en memoria DISTINTA y
# vacía (así funciona SQLite in-memory por conexión). StaticPool fuerza a
# que todo el engine de test reutilice siempre la misma conexión física,
# para que las tablas creadas por Base.metadata.create_all() sean visibles
# en el resto del test.
TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="function")
def db_session():
    """Crea todas las tablas antes de cada test y las destruye después, para
    que ningún test dependa de datos dejados por otro."""
    Base.metadata.create_all(bind=engine_test)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def client(db_session):
    """TestClient con get_db sobreescrita (app.dependency_overrides) para
    que los endpoints usen la sesión SQLite de test en vez de conectarse a
    MySQL. Se reutiliza la MISMA sesión que ya sembró los fixtures, así los
    datos de seed son visibles para el request HTTP."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# =========================================================================
# Fixtures de datos base (hospital + rol)
# =========================================================================
@pytest.fixture
def seed_hospital_and_role(db_session):
    hospital = models.Hospital(
        id_hospital=1, name_hospital="Hospital Heller (Sede Principal)", is_active=True
    )
    role = models.Role(id_role=1, role_name="Ingeniero", description="Rol de prueba")
    db_session.add_all([hospital, role])
    db_session.commit()
    return {"hospital_id": hospital.id_hospital, "role_id": role.id_role}


# =========================================================================
# Fixtures de usuario autenticado
# =========================================================================
@pytest.fixture
def test_user(db_session, seed_hospital_and_role):
    """Crea un usuario real en la DB de prueba, con password_hash generado
    por el mismo bcrypt que usa la app (no un mock/fake hash)."""
    plain_password = "ClaveSegura123"
    usuario = models.User(
        username="tecnico_test",
        password_hash=hash_password(plain_password),
        full_name="Técnico de Prueba",
        role_id=seed_hospital_and_role["role_id"],
        hospital_id=seed_hospital_and_role["hospital_id"],
        is_active=True,
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return {"user": usuario, "plain_password": plain_password}


@pytest.fixture
def auth_token(test_user):
    """Token JWT válido, con las mismas claims que genera /auth/login
    (incluida 'sub', que dependencies.py usa como username)."""
    usuario = test_user["user"]
    return create_access_token(data={
        "sub": usuario.username,
        "id_user": usuario.id_user,
        "role_name": "Ingeniero",
        "hospital_id": usuario.hospital_id,
    })


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


# =========================================================================
# Fixtures de datos de negocio (equipo + insumo con stock conocido)
# =========================================================================
@pytest.fixture
def seed_equipment(db_session, seed_hospital_and_role):
    equipo = models.Equipment(
        hospital_id=seed_hospital_and_role["hospital_id"],
        serial_number_factory="SN-TEST-0001",
        type_device="Monitor de Signos Vitales",
        category="Soporte de Vida",
        brand="Mindray",
        model="UMEC 12",
        state="OK",
        location="Quirófano 1",
    )
    db_session.add(equipo)
    db_session.commit()
    db_session.refresh(equipo)
    return equipo


@pytest.fixture
def seed_input_stock(db_session, seed_hospital_and_role):
    """Insumo de prueba con stock inicial CONOCIDO (10 unidades), para poder
    verificar el descuento exacto tras crear una OT."""
    insumo = models.Inputs(
        hospital_id=seed_hospital_and_role["hospital_id"],
        internal_code="TEST-INS-0001",
        input_type="repuesto_tecnico",
        name_input="Batería 12V de prueba",
        unit_of_measure="unidad",
        stock=10,
        min_stock_alert=2,
    )
    db_session.add(insumo)
    db_session.commit()
    db_session.refresh(insumo)
    return insumo
