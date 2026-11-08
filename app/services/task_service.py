"""Casos de uso y lógica de negocio para la gestión de tareas."""

from app.domain.entities import (
    TaskCreate,
    TaskEntity,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)
from app.domain.interfaces import TaskRepositoryProtocol


class TaskService:
    """Servicio de dominio que orquesta las operaciones sobre tareas."""

    def __init__(self, repository: TaskRepositoryProtocol) -> None:
        """Inicializa el servicio inyectando la abstracción del repositorio (DIP).

        Args:
            repository: Implementación que cumple con TaskRepositoryProtocol.
        """
        self._repository = repository

    def create_task(self, task_in: TaskCreate) -> TaskEntity:
        """Crea una nueva tarea aplicando validaciones de negocio.

        Args:
            task_in: Datos de entrada de la tarea.

        Returns:
            La entidad de tarea creada.
        """
        normalized_data = TaskCreate(
            title=task_in.title.strip(),
            description=task_in.description.strip() if task_in.description else None,
            priority=task_in.priority,
            status=task_in.status,
        )
        return self._repository.add(normalized_data)

    def get_task(self, task_id: int) -> TaskEntity | None:
        """Obtiene una tarea por su identificador."""
        return self._repository.get_by_id(task_id)

    def list_tasks(
        self,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
    ) -> list[TaskEntity]:
        """Lista las tareas aplicando filtros opcionales."""
        return self._repository.list_all(status=status, priority=priority)

    def update_task(self, task_id: int, task_in: TaskUpdate) -> TaskEntity | None:
        """Actualiza el estado, prioridad o agrega un comentario a una tarea."""
        return self._repository.update(task_id, task_in)

    def delete_task(self, task_id: int) -> bool:
        """Elimina una tarea por su identificador."""
        return self._repository.delete(task_id)

    def reset_tasks(self) -> None:
        """Limpia todas las tareas registradas."""
        self._repository.clear()

