"""Controladores y endpoints HTTP de la API."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse

from app.api.dependencies import get_task_service, verify_api_key
from app.core.config import settings
from app.domain.entities import (
    TaskCreate,
    TaskEntity,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)
from app.services.task_service import TaskService

FRONTEND_HTML_PATH = Path(__file__).resolve().parent.parent / "web" / "index.html"

health_router = APIRouter(tags=["Health"])
tasks_router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    dependencies=[Depends(verify_api_key)],
)


@health_router.get(
    "/",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def serve_frontend() -> HTMLResponse:
    """Sirve la interfaz gráfica web (Frontend) del sistema EduTasks."""
    html_content = FRONTEND_HTML_PATH.read_text(encoding="utf-8")
    return HTMLResponse(content=html_content)




@health_router.get(
    "/health",
    summary="Verificar estado del servicio",
)
async def health_check() -> dict[str, str]:
    """Retorna el estado operativo del servicio (endpoint público)."""
    return {
        "status": "healthy",
        "system": settings.api_title,
        "version": settings.api_version,
    }


@tasks_router.post(
    "",
    response_model=TaskEntity,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva tarea académica",
)
async def create_task_endpoint(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskEntity:
    """Registra una nueva tarea validando los campos de entrada."""
    return service.create_task(payload)


@tasks_router.get(
    "",
    response_model=list[TaskEntity],
    summary="Listar tareas registradas",
)
async def list_tasks_endpoint(
    status_filter: TaskStatus | None = None,
    priority_filter: TaskPriority | None = None,
    service: TaskService = Depends(get_task_service),
) -> list[TaskEntity]:
    """Obtiene la lista de tareas con filtros opcionales."""
    return service.list_tasks(status=status_filter, priority=priority_filter)


@tasks_router.get(
    "/{task_id}",
    response_model=TaskEntity,
    summary="Obtener tarea por ID",
)
async def get_task_endpoint(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskEntity:
    """Busca una tarea específica por su identificador único."""
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La tarea con ID {task_id} no existe.",
        )
    return task


@tasks_router.patch(
    "/{task_id}",
    response_model=TaskEntity,
    summary="Actualizar estado, prioridad o agregar comentario",
)
async def update_task_endpoint(
    task_id: int,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskEntity:
    """Actualiza el estado, prioridad o anexa un comentario a una tarea existente."""
    updated = service.update_task(task_id, payload)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La tarea con ID {task_id} no existe.",
        )
    return updated


@tasks_router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar tarea por ID",
)
async def delete_task_endpoint(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Elimina una tarea existente por su identificador único."""
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La tarea con ID {task_id} no existe.",
        )

