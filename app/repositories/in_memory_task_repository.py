"""Implementación en memoria del repositorio de tareas."""

from datetime import datetime, timezone

from app.domain.entities import (
    TaskCreate,
    TaskEntity,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)


class InMemoryTaskRepository:
    """Repositorio concreto en memoria que implementa TaskRepositoryProtocol."""

    def __init__(self) -> None:
        """Inicializa el almacén en memoria y el contador de identificadores."""
        self._storage: dict[int, TaskEntity] = {}
        self._next_id: int = 1

    def add(self, task_data: TaskCreate) -> TaskEntity:
        """Guarda una nueva tarea en el diccionario en memoria."""
        entity = TaskEntity(
            id=self._next_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            status=task_data.status,
            created_at=datetime.now(timezone.utc),
        )
        self._storage[self._next_id] = entity
        self._next_id += 1
        return entity

    def get_by_id(self, task_id: int) -> TaskEntity | None:
        """Busca y retorna una tarea por su ID."""
        return self._storage.get(task_id)

    def list_all(
        self,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
    ) -> list[TaskEntity]:
        """Retorna las tareas filtradas por estado y/o prioridad."""
        items = list(self._storage.values())
        if status is not None:
            items = [item for item in items if item.status == status]
        if priority is not None:
            items = [item for item in items if item.priority == priority]
        return items

    def update(self, task_id: int, task_update: TaskUpdate) -> TaskEntity | None:
        """Actualiza estado, prioridad y/o agrega comentario a una tarea existente."""
        current = self._storage.get(task_id)
        if current is None:
            return None

        updated_comments = list(current.comments)
        if task_update.comment:
            updated_comments.append(task_update.comment.strip())

        updated_entity = TaskEntity(
            id=current.id,
            title=current.title,
            description=current.description,
            priority=task_update.priority if task_update.priority else current.priority,
            status=task_update.status if task_update.status else current.status,
            created_at=current.created_at,
            comments=updated_comments,
        )
        self._storage[task_id] = updated_entity
        return updated_entity

    def delete(self, task_id: int) -> bool:
        """Elimina una tarea si existe en el almacén."""
        if task_id in self._storage:
            del self._storage[task_id]
            return True
        return False

    def clear(self) -> None:
        """Reinicia el almacén en memoria."""
        self._storage.clear()
        self._next_id = 1

