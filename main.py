from fastapi import FastAPI

from app.routers import auth, health

app = FastAPI(
    title="Gestión Biomédica API",
    description="API REST para el sistema de gestión de equipamiento biomédico - Hospital Heller",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(auth.router)
