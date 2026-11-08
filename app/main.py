"""Punto de entrada principal de la aplicación FastAPI."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routers import health_router, tasks_router
from app.core.config import settings

FIELD_LABELS: dict[str, str] = {
    "title": "Título de la tarea",
    "description": "Descripción",
    "priority": "Prioridad",
    "status": "Estado",
    "comment": "Comentario",
}


def format_validation_error(exc: RequestValidationError) -> str:
    """Convierte los errores técnicos de Pydantic en mensajes en lenguaje natural."""
    messages: list[str] = []
    for err in exc.errors():
        loc = err.get("loc", ())
        field_key = str(loc[-1]) if loc else "campo"
        field_name = FIELD_LABELS.get(field_key, field_key)
        err_type = err.get("type", "")
        user_input = err.get("input", "")

        if err_type == "missing" or (err_type == "string_too_short" and not user_input):
            messages.append(
                f"El campo '{field_name}' es obligatorio y no puede estar vacío."
            )
        elif err_type == "string_too_short":
            min_len = err.get("ctx", {}).get("min_length", 3)
            messages.append(
                f"El campo '{field_name}' es demasiado corto: debe tener al menos {min_len} caracteres."
            )
        elif err_type == "string_too_long":
            max_len = err.get("ctx", {}).get("max_length", 100)
            messages.append(
                f"El campo '{field_name}' supera el límite máximo de {max_len} caracteres."
            )
        elif err_type == "enum":
            messages.append(
                f"El valor enviado en '{field_name}' no es válido dentro de las opciones permitidas."
            )
        else:
            messages.append(f"Datos inválidos en '{field_name}'.")

    return " ".join(messages)


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

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Retorna errores de validación HTTP 422 explicados en lenguaje natural."""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": format_validation_error(exc)},
        )

    application.include_router(health_router)
    application.include_router(tasks_router)
    return application


app = create_application()


