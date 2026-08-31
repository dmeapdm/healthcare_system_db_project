from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["Salud del sistema"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Gestión Biomédica API - Hospital Heller",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
