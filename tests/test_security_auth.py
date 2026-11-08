"""Pruebas de Seguridad (Tipo de Prueba 2) para control de acceso y autenticación."""

import pytest
from fastapi.testclient import TestClient


def test_access_protected_endpoint_without_api_key_returns_401_unauthorized(
    client: TestClient,
) -> None:
    """Caso de Prueba de Seguridad 1 (CP-SEG-01): Bloqueo de petición sin cabecera X-API-KEY."""
    # Arrange
    endpoint = "/api/v1/tasks"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 401
    assert "falta la cabecera X-API-KEY" in response.json()["detail"]


@pytest.mark.parametrize(
    "malicious_or_invalid_key",
    [
        "CLAVE-FALSA-123",
        "' OR '1'='1",
        "<script>alert(1)</script>",
        "   ",
    ],
)
def test_access_protected_endpoint_with_invalid_api_key_returns_401_unauthorized(
    client: TestClient,
    malicious_or_invalid_key: str,
) -> None:
    """Caso de Prueba de Seguridad 2 (CP-SEG-02): Rechazo de credenciales inválidas o maliciosas."""
    # Arrange
    headers = {"X-API-KEY": malicious_or_invalid_key}

    # Act
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Intento de intrusión"},
        headers=headers,
    )

    # Assert
    assert response.status_code == 401
    assert "inválida" in response.json()["detail"]

