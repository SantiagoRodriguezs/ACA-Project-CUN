# EduTasks — Task Management System (API & Web UI)

Sistema web full-stack para la gestión y seguimiento de tareas, desarrollado con **FastAPI** y **Python 3.14**, estructurado bajo **Clean Architecture**, principios **S.O.L.I.D.** y estándares **PEP 8**. Incluye una interfaz gráfica interactiva, control de acceso por API Key, gestión de ciclo de vida de tareas con comentarios de seguimiento y una suite completa de pruebas automatizadas.

---

## Características Principales

* **Interfaz Web Interactiva:** Panel de control integrado para registrar, filtrar, comentar, completar, reabrir y eliminar tareas en tiempo real.
* **Seguridad por Cabecera (`X-API-KEY`):** Protección de endpoints privados contra accesos no autenticados o credenciales inválidas.
* **Validaciones en Lenguaje Natural:** Respuestas claras en español ante errores de validación de reglas de negocio (`HTTP 422`).
* **Ciclo de Vida de Tareas:** Estados dinámicos (`PENDIENTE`, `EN_PROGRESO`, `COMPLETADA`), historial de comentarios por tarea, bloqueo automático de comentarios al completar y reapertura de tareas.
* **Clean Architecture & S.O.L.I.D.:** Separación estricta entre entidades de dominio, contratos (`Protocol`), casos de uso, persistencia en memoria y controladores HTTP.

---

## Estructura del Proyecto

```text
ACA-Project-CUN/
├── app/
│   ├── api/
│   │   ├── dependencies.py              # Seguridad (X-API-KEY) e inyección de dependencias
│   │   └── routers.py                   # Controladores HTTP y entrega de interfaz web
│   ├── core/
│   │   └── config.py                    # Configuración central tipada
│   ├── domain/
│   │   ├── entities.py                  # Entidades y esquemas Pydantic
│   │   └── interfaces.py                # Contratos abstractos (DIP - SOLID)
│   ├── repositories/
│   │   └── in_memory_task_repository.py # Persistencia en memoria
│   ├── services/
│   │   └── task_service.py              # Casos de uso y reglas de negocio
│   ├── web/
│   │   └── index.html                   # Interfaz gráfica web (Frontend interactivo)
│   └── main.py                          # Punto de entrada de la aplicación y manejadores
├── tests/
│   ├── conftest.py                      # Fixtures aisladas para pruebas
│   ├── test_functional_tasks.py         # Suite de pruebas funcionales (AAA)
│   └── test_security_auth.py            # Suite de pruebas de seguridad (AAA)
├── scripts/
│   └── collect_metrics.py               # Medición automatizada de métricas de calidad
├── pyproject.toml                       # Configuración de pytest y coverage
└── requirements.txt                     # Dependencias del proyecto
```

---

## Instalación y Configuración Paso a Paso

### 1. Clonar el repositorio
```powershell
git clone https://github.com/SantiagoRodriguezs/ACA-Project-CUN.git
cd ACA-Project-CUN
```

### 2. Crear el entorno virtual
```powershell
python -m venv .venv
# O usando el lanzador de Python en Windows:
py -m venv .venv
```

### 3. Activar el entorno virtual
* **En PowerShell (Windows):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
* **En CMD (Windows):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
* **En Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 4. Instalar las dependencias
```powershell
pip install -r requirements.txt
```

---

## Ejecución del Proyecto

### Iniciar el servidor de desarrollo (Frontend + API)
```powershell
uvicorn app.main:app --reload
```
* **Aplicación Web (Frontend):** `http://127.0.0.1:8000`
* **Documentación Swagger UI:** `http://127.0.0.1:8000/docs`
* **API Key por defecto (`X-API-KEY`):** `CUN-CALIDAD-2026-SECRET`

---

## Ejecución de Pruebas y Métricas

### 1. Ejecutar las suites de pruebas y cobertura de código
```powershell
pytest --cov=app --cov-report=term-missing
```

### 2. Generar el reporte de métricas de rendimiento y calidad
```powershell
python -m scripts.collect_metrics
```
