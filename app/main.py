"""Punto de entrada principal de la aplicación FastAPI."""

from fastapi import FastAPI

from app.api.routers import health_router, tasks_router
from app.core.config import settings


def create_application() -> FastAPI:
    """Construye y configura la instancia de la aplicación FastAPI."""
    application = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=(
            "Sistema de información para la gestión de tareas académicas. "
            "Diseñado bajo Clean Architecture y principios SOLID para evaluación "
            "de pruebas de software y métricas de calidad (CUN)."
        ),
    )
    application.include_router(health_router)
    application.include_router(tasks_router)
    return application


app = create_application()
