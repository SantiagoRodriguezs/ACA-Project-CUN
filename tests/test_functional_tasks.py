"""Pruebas Funcionales (Tipo de Prueba 1) para el módulo de gestión de tareas."""

import pytest
from fastapi.testclient import TestClient


def test_health_check_returns_200_ok(client: TestClient) -> None:
    """Verifica que el endpoint de salud responda 200 OK y estado healthy."""
    # Arrange
    endpoint = "/health"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"


def test_create_task_valid_payload_returns_201_created(
    client: TestClient,
    valid_auth_headers: dict[str, str],
) -> None:
    """Caso de Prueba Funcional 1 (CP-FUN-01): Creación exitosa de tarea válida."""
    # Arrange
    payload = {
        "title": "Diseñar plan de pruebas de software",
        "description": "Documentar casos funcionales y de seguridad para el ACA",
        "priority": "ALTA",
        "status": "EN_PROGRESO",
    }

    # Act
    response = client.post(
        "/api/v1/tasks",
        json=payload,
        headers=valid_auth_headers,
    )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Diseñar plan de pruebas de software"
    assert data["priority"] == "ALTA"
    assert data["status"] == "EN_PROGRESO"
    assert "created_at" in data


@pytest.mark.parametrize(
    "invalid_payload",
    [
        {"title": "AB", "priority": "MEDIA"},  # Título menor a 3 caracteres
        {"title": "", "priority": "ALTA"},  # Título vacío
        {"title": "Tarea válida", "priority": "URGENTE"},  # Prioridad inexistente
        {"description": "Sin título obligatorio"},  # Falta campo requerido
    ],
)
def test_create_task_invalid_payload_returns_422_unprocessable_entity(
    client: TestClient,
    valid_auth_headers: dict[str, str],
    invalid_payload: dict[str, str],
) -> None:
    """Caso de Prueba Funcional 2 (CP-FUN-02): Rechazo de datos inválidos con HTTP 422."""
    # Arrange
    endpoint = "/api/v1/tasks"

    # Act
    response = client.post(
        endpoint,
        json=invalid_payload,
        headers=valid_auth_headers,
    )

    # Assert
    assert response.status_code == 422


def test_list_and_filter_tasks_returns_matching_items(
    client: TestClient,
    valid_auth_headers: dict[str, str],
) -> None:
    """Verifica el listado y filtrado de tareas por estado y prioridad."""
    # Arrange
    client.post(
        "/api/v1/tasks",
        json={"title": "Tarea 1", "priority": "ALTA", "status": "PENDIENTE"},
        headers=valid_auth_headers,
    )
    client.post(
        "/api/v1/tasks",
        json={"title": "Tarea 2", "priority": "BAJA", "status": "COMPLETADA"},
        headers=valid_auth_headers,
    )

    # Act
    response_all = client.get("/api/v1/tasks", headers=valid_auth_headers)
    response_filtered = client.get(
        "/api/v1/tasks?status_filter=COMPLETADA&priority_filter=BAJA",
        headers=valid_auth_headers,
    )

    # Assert
    assert response_all.status_code == 200
    assert len(response_all.json()) == 2
    assert response_filtered.status_code == 200
    filtered_items = response_filtered.json()
    assert len(filtered_items) == 1
    assert filtered_items[0]["title"] == "Tarea 2"


def test_get_and_delete_task_lifecycle_succeeds(
    client: TestClient,
    valid_auth_headers: dict[str, str],
) -> None:
    """Verifica la consulta por ID, eliminación y retorno 404 cuando no existe."""
    # Arrange
    created = client.post(
        "/api/v1/tasks",
        json={"title": "Tarea por eliminar"},
        headers=valid_auth_headers,
    ).json()
    task_id = created["id"]

    # Act
    get_res = client.get(f"/api/v1/tasks/{task_id}", headers=valid_auth_headers)
    del_res = client.delete(f"/api/v1/tasks/{task_id}", headers=valid_auth_headers)
    get_missing = client.get(f"/api/v1/tasks/{task_id}", headers=valid_auth_headers)
    del_missing = client.delete(f"/api/v1/tasks/{task_id}", headers=valid_auth_headers)

    # Assert
    assert get_res.status_code == 200
    assert del_res.status_code == 204
    assert get_missing.status_code == 404
    assert del_missing.status_code == 404

