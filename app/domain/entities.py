"""Entidades del dominio para la gestión de tareas."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TaskPriority(str, Enum):
    """Niveles de prioridad permitidos para una tarea."""

    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"


class TaskStatus(str, Enum):
    """Estados permitidos en el ciclo de vida de una tarea."""

    PENDIENTE = "PENDIENTE"
    EN_PROGRESO = "EN_PROGRESO"
    COMPLETADA = "COMPLETADA"


class TaskCreate(BaseModel):
    """Esquema de entrada para la creación de una tarea.

    Attributes:
        title: Título de la tarea (entre 3 y 100 caracteres).
        description: Descripción opcional (máximo 500 caracteres).
        priority: Prioridad asignada a la tarea.
        status: Estado inicial de la tarea.
    """

    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Título descriptivo de la tarea académica.",
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Descripción detallada de la tarea.",
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIA,
        description="Prioridad de la tarea.",
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDIENTE,
        description="Estado actual de la tarea.",
    )


class TaskEntity(TaskCreate):
    """Entidad completa de una tarea registrada en el sistema.

    Attributes:
        id: Identificador único incremental.
        created_at: Fecha y hora de creación en UTC.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Identificador único numérico.")
    created_at: datetime = Field(..., description="Fecha de creación en UTC.")
