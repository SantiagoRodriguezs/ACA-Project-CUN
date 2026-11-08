"""Configuración global de fixtures para pytest."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_task_service
from app.core.config import settings
from app.main import app
from app.repositories.in_memory_task_repository import InMemoryTaskRepository
from app.services.task_service import TaskService


@pytest.fixture()
def isolated_task_service() -> Generator[TaskService, None, None]:
    """Provee un servicio de tareas aislado con repositorio limpio por cada test."""
    repository = InMemoryTaskRepository()
    service = TaskService(repository=repository)
    yield service
    service.reset_tasks()


@pytest.fixture()
def client(isolated_task_service: TaskService) -> Generator[TestClient, None, None]:
    """Provee un cliente HTTP de prueba con dependencias inyectadas y aisladas."""
    app.dependency_overrides[get_task_service] = lambda: isolated_task_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def valid_auth_headers() -> dict[str, str]:
    """Retorna las cabeceras HTTP con la credencial de seguridad válida."""
    return {settings.api_key_header: settings.api_secret_key}
