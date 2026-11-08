"""Contratos e interfaces del dominio (Principio de Inversión de Dependencias - DIP)."""

from typing import Protocol

from app.domain.entities import (
    TaskCreate,
    TaskEntity,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)


class TaskRepositoryProtocol(Protocol):
    """Interfaz abstracta para el repositorio de tareas."""

    def add(self, task_data: TaskCreate) -> TaskEntity:
        """Persiste una nueva tarea en el almacén de datos.

        Args:
            task_data: Datos validados para crear la tarea.

        Returns:
            La entidad creada con su identificador y marca de tiempo.
        """

    def get_by_id(self, task_id: int) -> TaskEntity | None:
        """Obtiene una tarea por su identificador único.

        Args:
            task_id: Identificador numérico de la tarea.

        Returns:
            La entidad encontrada o None si no existe.
        """

    def list_all(
        self,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
    ) -> list[TaskEntity]:
        """Lista todas las tareas con filtros opcionales.

        Args:
            status: Filtro opcional por estado.
            priority: Filtro opcional por prioridad.

        Returns:
            Lista de entidades que cumplen los criterios.
        """

    def update(self, task_id: int, task_update: TaskUpdate) -> TaskEntity | None:
        """Actualiza el estado, prioridad o comentarios de una tarea existente.

        Args:
            task_id: Identificador numérico de la tarea.
            task_update: Campos a modificar o comentario a anexar.

        Returns:
            La entidad actualizada o None si no existe.
        """

    def delete(self, task_id: int) -> bool:
        """Elimina una tarea por su identificador.

        Args:
            task_id: Identificador numérico de la tarea.

        Returns:
            True si fue eliminada, False si no existía.
        """

    def clear(self) -> None:
        """Limpia todas las tareas almacenadas."""

