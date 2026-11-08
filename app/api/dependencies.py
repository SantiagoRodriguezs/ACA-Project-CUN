"""Dependencias de la capa de presentación (autenticación e inyección de servicios)."""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings
from app.repositories.in_memory_task_repository import InMemoryTaskRepository
from app.services.task_service import TaskService

api_key_header_scheme = APIKeyHeader(
    name=settings.api_key_header,
    auto_error=False,
)

_default_repository = InMemoryTaskRepository()
_default_task_service = TaskService(repository=_default_repository)


def get_task_service() -> TaskService:
    """Provee la instancia del servicio de tareas para inyección de dependencias."""
    return _default_task_service


async def verify_api_key(
    api_key: str | None = Security(api_key_header_scheme),
) -> str:
    """Valida la presencia y exactitud de la cabecera de seguridad X-API-KEY.

    Args:
        api_key: Valor extraído de la cabecera HTTP.

    Returns:
        La clave validada si es correcta.

    Raises:
        HTTPException: Con código 401 si falta la clave o no coincide.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso no autorizado: falta la cabecera X-API-KEY.",
        )
    if api_key != settings.api_secret_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado: la credencial X-API-KEY es inválida.",
        )
    return api_key
