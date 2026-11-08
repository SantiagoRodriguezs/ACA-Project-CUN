# Guion para el Video Pitch (Máximo 5 Minutos - YouTube)

**Duración estimada:** 4 minutos con 15 segundos  
**Recomendación:** Usa OBS Studio, Loom o la grabadora de pantalla de Windows (`Win + G`) mostrando primero el documento/código en tu editor, luego la terminal corriendo las pruebas y finalmente el navegador con `/docs`.

---

## Minuto 0:00 - 0:45 | 1. Presentación e Introducción
* **En pantalla:** Portada del informe y repositorio de GitHub (`SantiagoRodriguezs/ACA-Project-CUN`).
* **Qué decir:**
  > "Hola a todos, mi nombre es Santiago Rodríguez. En este video presentaremos el desarrollo de la Actividad de Construcción Aplicada (ACA) para la asignatura de Aseguramiento de la Calidad de Software de la CUN.  
  > Para este proyecto desarrollamos **EduTasks API**, un sistema de información para la gestión de tareas académicas construido en **Python 3.14 con FastAPI**, aplicando **Clean Architecture**, principios **SOLID** y pruebas automatizadas con **Pytest**."

---

## Minuto 0:45 - 1:45 | 2. Arquitectura del Sistema y Demostración en Vivo
* **En pantalla:** Estructura de carpetas en el IDE (`app/domain`, `app/services`, `app/repositories`, `app/api`) y la ventana del navegador en `http://127.0.0.1:8000/docs` (Swagger UI).
* **Qué decir:**
  > "El sistema se estructuró desacoplando las entidades del dominio, los casos de uso en `TaskService`, la persistencia en memoria y los controladores HTTP.  
  > Como vemos aquí en la interfaz Swagger UI de FastAPI, contamos con un endpoint público de salud (`/health`) y los endpoints protegidos de tareas (`/api/v1/tasks`), los cuales están resguardados mediante autenticación por cabecera `X-API-KEY`."

---

## Minuto 1:45 - 3:00 | 3. Explicación y Ejecución de las Dos Pruebas de Software
* **En pantalla:** Archivos `tests/test_functional_tasks.py` y `tests/test_security_auth.py`, seguido de la ejecución en consola de `pytest --cov=app --cov-report=term-missing`.
* **Qué decir:**
  > "Siguiendo la guía de actividades, diseñamos dos tipos diferentes de pruebas bajo el patrón *Arrange, Act, Assert (AAA)*:  
  > 1. **Prueba Funcional (`test_functional_tasks.py`):** Evaluamos dos casos principales: primero, la creación exitosa de una tarea válida verificando el código `201 Created`; y segundo, una prueba parametrizada que envía datos incompletos o fuera de rango para comprobar que el sistema rechace la petición con `422 Unprocessable Entity`.  
  > 2. **Prueba de Seguridad (`test_security_auth.py`):** Evaluamos el control de acceso en dos escenarios: peticiones anónimas sin cabecera `X-API-KEY` y peticiones con credenciales falsas o vectores de inyección SQL y XSS, confirmando que en todos los casos el sistema bloquea el acceso con `401 Unauthorized`.  
  > Al ejecutar `pytest` en nuestra terminal, observamos que los 13 casos de prueba parametrizados pasan exitosamente."

---

## Minuto 3:00 - 3:45 | 4. Tres Métricas de Calidad del Software
* **En pantalla:** Ejecutar en la terminal `python -m scripts.collect_metrics` y mostrar la tabla impresa en consola.
* **Qué decir:**
  > "Para valorar objetivamente la calidad del software ejecutamos nuestro script de métricas:  
  > - **Primera métrica (Cobertura de Código):** Obtuvimos un **100 % de cobertura**, garantizando que todas las líneas de negocio y seguridad fueron probadas.  
  > - **Segunda métrica (Efectividad o Tasa de Éxito de Pruebas):** Logramos un **100 % de casos exitosos** (13 de 13 pruebas aprobadas).  
  > - **Tercera métrica (Tiempo Medio de Respuesta):** Tras simular 100 transacciones consecutivas, el tiempo promedio de respuesta fue de apenas **1 a 2 milisegundos**, muy por debajo del umbral máximo de 50 ms."

---

## Minuto 3:45 - 4:15 | 5. Análisis Crítico y Conclusiones
* **En pantalla:** Sección de Análisis Crítico y Conclusiones del informe APA 7.0.
* **Qué decir:**
  > "Como análisis crítico, identificamos que aunque la validación y la arquitectura limpia cumplen altos estándares, el paso previo a producción requeriría migrar el repositorio en memoria hacia una base de datos persistente como PostgreSQL (lo cual es inmediato gracias a la inversión de dependencias aplicada) y evolucionar la API Key estática hacia tokens dinámicos JWT con limitación de peticiones (*Rate Limiting*).  
  > En conclusión, este proceso demuestra cómo las pruebas automatizadas previenen fallos críticos y aseguran la calidad antes de la implementación final. ¡Muchas gracias!"
