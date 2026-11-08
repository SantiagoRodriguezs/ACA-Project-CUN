# EduTasks API — Proyecto ACA (Pruebas de Software y Métricas de Calidad)

Sistema de gestión de tareas académicas desarrollado con **FastAPI** y **Python 3.14**, estructurado bajo **Clean Architecture**, principios **S.O.L.I.D.** y estándares **PEP 8**. Diseñado específicamente para el desarrollo de la Actividad de Construcción Aplicada (ACA) de la **Corporación Unificada Nacional de Educación Superior (CUN)**.

---

## Arquitectura del Proyecto

```text
ACA-Project-CUN/
├── app/
│   ├── api/
│   │   ├── dependencies.py           # Seguridad (X-API-KEY) e inyección de dependencias
│   │   └── routers.py                # Controladores HTTP (FastAPI)
│   ├── core/
│   │   └── config.py                 # Configuración central tipada
│   ├── domain/
│   │   ├── entities.py               # Entidades y esquemas Pydantic
│   │   └── interfaces.py             # Contratos abstractos (DIP - SOLID)
│   ├── repositories/
│   │   └── in_memory_task_repository.py # Persistencia en memoria
│   ├── services/
│   │   └── task_service.py           # Casos de uso y reglas de negocio
│   └── main.py                       # Punto de entrada de la aplicación
├── tests/
│   ├── conftest.py                   # Fixtures aisladas para pruebas
│   ├── test_functional_tasks.py      # Prueba 1: Pruebas Funcionales (AAA)
│   └── test_security_auth.py         # Prueba 2: Pruebas de Seguridad (AAA)
├── scripts/
│   └── collect_metrics.py            # Medición automatizada de las 3 métricas
├── pyproject.toml                    # Configuración de pytest y coverage
└── requirements.txt                  # Dependencias del proyecto
```

---

## Requisitos y Ejecución Rápida

### 1. Activar el entorno virtual
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Iniciar el servidor de desarrollo (Swagger UI)
```powershell
uvicorn app.main:app --reload
```
- **Swagger UI interactivo:** `http://127.0.0.1:8000/docs`
- **Credencial de prueba (`X-API-KEY`):** `CUN-CALIDAD-2026-SECRET`

### 3. Ejecutar las pruebas de software y medir cobertura
```powershell
pytest --cov=app --cov-report=term-missing
```

### 4. Ejecutar el reporte de las 3 métricas de calidad
```powershell
python -m scripts.collect_metrics
```
