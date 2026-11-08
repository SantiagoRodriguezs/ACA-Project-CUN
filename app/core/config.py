"""Configuración central de la aplicación."""

from pydantic import BaseModel

API_TITLE_DEFAULT: str = "ACA - Sistema de Gestión de Tareas (EduTasks API)"
API_VERSION_DEFAULT: str = "1.0.0"
API_SECRET_KEY_DEFAULT: str = "CUN-CALIDAD-2026-SECRET"
API_KEY_HEADER_DEFAULT: str = "X-API-KEY"


class AppConfig(BaseModel):
    """Configuración inmutable de la aplicación.

    Attributes:
        api_title: Nombre del sistema evaluado.
        api_version: Versión semántica del sistema.
        api_secret_key: Clave secreta para autenticación de rutas protegidas.
        api_key_header: Nombre de la cabecera HTTP de seguridad.
    """

    api_title: str = API_TITLE_DEFAULT
    api_version: str = API_VERSION_DEFAULT
    api_secret_key: str = API_SECRET_KEY_DEFAULT
    api_key_header: str = API_KEY_HEADER_DEFAULT


settings = AppConfig()

