from fastapi import FastAPI

from app.routers import auth, equipments, health, work_orders

app = FastAPI(
    title="Gestión Biomédica API",
    description="API REST para el sistema de gestión de equipamiento biomédico - Hospital Heller",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(equipments.router)
app.include_router(work_orders.router)
