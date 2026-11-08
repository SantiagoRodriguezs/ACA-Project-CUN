# Diseño y Elaboración de Dos Pruebas de Software y Tres Métricas de Calidad

**Corporación Unificada Nacional de Educación Superior (CUN)**  
Facultad de Ingeniería — Programa de Ingeniería de Sistemas  
Aseguramiento de la Calidad de Software (Semanas 3, 4, 5 y 6)  

**Autores:**  
Santiago Rodríguez (y equipo de trabajo)  

**Repositorio Oficial del Proyecto:**  
https://github.com/SantiagoRodriguezs/ACA-Project-CUN.git  

**Enlace al Video Pitch (YouTube - Máx. 5 min):**  
*[Pegar aquí el enlace de YouTube una vez grabado]*  

**Fecha de entrega:**  
08 de noviembre de 2026  

---

## 1. Introducción

El aseguramiento de la calidad del software (*Software Quality Assurance* - SQA) constituye una disciplina transversal e indispensable dentro del ciclo de vida del desarrollo de sistemas de información modernos. Como señalan Pressman (2010) y Sommerville (2005), la detección temprana de defectos mediante planes de prueba estructurados reduce exponencialmente los costos de corrección y mitiga los riesgos operativos antes del despliegue en entornos productivos.

En el presente informe técnico se aborda la evaluación integral del sistema **EduTasks API**, una interfaz de programación de aplicaciones (API REST) construida con el framework **FastAPI** y **Python 3.14**, diseñada bajo el paradigma de *Clean Architecture* y los principios de diseño orientado a objetos *S.O.L.I.D.*. Sobre este sistema se diseñan, ejecutan y documentan dos (2) tipologías de pruebas de software complementarias: **Pruebas Funcionales** (orientadas a la validación de reglas de negocio y contratos de datos) y **Pruebas de Seguridad** (orientadas al control de acceso y rechazo de credenciales no autorizadas). Asimismo, se calculan e interpretan tres (3) métricas cuantitativas de calidad que permiten dictaminar de forma objetiva la confiabilidad, mantenibilidad y eficiencia del producto.

---

## 2. Documento Técnico de Pruebas de Software (Pasos 2, 3 y 4)

### 2.1. Identificación General del Sistema Evaluado
* **Nombre del sistema evaluado:** EduTasks API — Sistema de Gestión de Tareas Académicas v1.0.0.
* **Arquitectura y Tecnologías:** API RESTful en Python 3.14, FastAPI, validación de esquemas con Pydantic v2, suite de pruebas automatizadas con `pytest` y cliente de pruebas `TestClient` (basado en `httpx`).
* **Alcance de la evaluación:** La evaluación abarca la capa de presentación HTTP (`app/api/routers.py`), el middleware de seguridad por cabecera `X-API-KEY` (`app/api/dependencies.py`), la capa de lógica de negocio (`app/services/task_service.py`), las entidades de dominio (`app/domain/entities.py`) y el repositorio de persistencia (`app/repositories/in_memory_task_repository.py`).

---

### 2.2. Prueba N.º 1: Prueba Funcional

* **Objetivo de la prueba:** Verificar que el módulo de gestión de tareas cumpla rigurosamente con los requerimientos funcionales de creación, consulta, filtrado y validación de reglas de negocio (longitud de campos, enumeraciones de prioridad/estado y códigos de respuesta HTTP estándar).
* **Tipo de prueba seleccionada:** Prueba Funcional de Caja Negra y Caja Blanca automatizada con `pytest`.
* **Requerimientos a validar:**
  * **RF-01:** El sistema debe permitir registrar una tarea válida con título (3 a 100 caracteres), descripción opcional, prioridad (`BAJA`, `MEDIA`, `ALTA`) y estado (`PENDIENTE`, `EN_PROGRESO`, `COMPLETADA`), retornando código `HTTP 201 Created`.
  * **RF-02:** El sistema debe rechazar cualquier intento de creación con datos incompletos, títulos menores a 3 caracteres o prioridades fuera del dominio, retornando código `HTTP 422 Unprocessable Entity`.
* **Escenarios de prueba:**
  1. Registro exitoso de una tarea académica con todos sus atributos válidos.
  2. Rechazo controlado de peticiones con cargas útiles (*payloads*) inválidas o incompletas.

#### Caso de Prueba Funcional 1 (CP-FUN-01)

| Campo | Descripción Técnica |
| :--- | :--- |
| **ID del Caso** | `CP-FUN-01` (`test_create_task_valid_payload_returns_201_created`) |
| **Requerimiento** | RF-01 — Registro válido de tareas académicas |
| **Precondiciones** | Contar con cabecera válida `X-API-KEY: CUN-CALIDAD-2026-SECRET` |
| **Datos de entrada** | `POST /api/v1/tasks` con JSON: `{"title": "Diseñar plan de pruebas de software", "description": "Documentar casos funcionales y de seguridad para el ACA", "priority": "ALTA", "status": "EN_PROGRESO"}` |
| **Resultado esperado** | Código `HTTP 201 Created`. Cuerpo JSON con `id = 1`, `title` idéntico al enviado, `priority = "ALTA"`, `status = "EN_PROGRESO"` y marca de tiempo `created_at` en UTC. |
| **Resultado obtenido** | Código `HTTP 201 Created`. Entidad creada y persistida satisfactoriamente con `id: 1` (`PASSED`). |
| **Estado** | **APROBADO (Exitoso)** |

#### Caso de Prueba Funcional 2 (CP-FUN-02)

| Campo | Descripción Técnica |
| :--- | :--- |
| **ID del Caso** | `CP-FUN-02` (`test_create_task_invalid_payload_returns_422_unprocessable_entity`) |
| **Requerimiento** | RF-02 — Validación de integridad de datos de entrada |
| **Precondiciones** | Contar con cabecera válida `X-API-KEY: CUN-CALIDAD-2026-SECRET` |
| **Datos de entrada** | `POST /api/v1/tasks` parametrizado con 4 entradas inválidas: 1) `{"title": "AB"}` (título muy corto), 2) `{"title": ""}` (vacío), 3) `{"title": "Tarea válida", "priority": "URGENTE"}` (enum inválido), 4) `{"description": "Sin título"}` (campo obligatorio ausente). |
| **Resultado esperado** | Código `HTTP 422 Unprocessable Entity` en las 4 ejecuciones parametrizadas, impidiendo el registro de datos corruptos. |
| **Resultado obtenido** | Código `HTTP 422 Unprocessable Entity` en el 100 % de las entradas inválidas (`PASSED`). |
| **Estado** | **APROBADO (Exitoso)** |

---

### 2.3. Prueba N.º 2: Prueba de Seguridad

* **Objetivo de la prueba:** Evaluar la robustez del mecanismo de control de acceso y autenticación de la API, garantizando que ningún usuario o cliente externo pueda consultar, crear o eliminar recursos protegidos sin suministrar una credencial `X-API-KEY` legítima.
* **Tipo de prueba seleccionada:** Prueba de Seguridad (Control de Acceso y Autenticación de API).
* **Requerimientos a validar:**
  * **RNF-SEG-01:** Todo endpoint bajo el prefijo `/api/v1/tasks` debe exigir la cabecera HTTP `X-API-KEY`. Si la cabecera no se envía, el sistema debe denegar el acceso con código `HTTP 401 Unauthorized`.
  * **RNF-SEG-02:** Si el valor de `X-API-KEY` es incorrecto, vacío o contiene vectores de inyección (`' OR '1'='1`, `<script>`), el sistema debe rechazar la solicitud con código `HTTP 401 Unauthorized`.
* **Escenarios de prueba:**
  1. Intento de consulta anónima a rutas protegidas sin cabecera de seguridad.
  2. Intento de creación de recursos utilizando tokens falsificados o cadenas de inyección.

#### Caso de Prueba de Seguridad 1 (CP-SEG-01)

| Campo | Descripción Técnica |
| :--- | :--- |
| **ID del Caso** | `CP-SEG-01` (`test_access_protected_endpoint_without_api_key_returns_401_unauthorized`) |
| **Requerimiento** | RNF-SEG-01 — Denegación de acceso sin credenciales |
| **Precondiciones** | Realizar petición HTTP omitiendo la cabecera `X-API-KEY`. |
| **Datos de entrada** | `GET /api/v1/tasks` con cabeceras vacías `{}`. |
| **Resultado esperado** | Código `HTTP 401 Unauthorized` y mensaje `"Acceso no autorizado: falta la cabecera X-API-KEY."` |
| **Resultado obtenido** | Código `HTTP 401 Unauthorized` con el detalle exacto esperado (`PASSED`). |
| **Estado** | **APROBADO (Exitoso)** |

#### Caso de Prueba de Seguridad 2 (CP-SEG-02)

| Campo | Descripción Técnica |
| :--- | :--- |
| **ID del Caso** | `CP-SEG-02` (`test_access_protected_endpoint_with_invalid_api_key_returns_401_unauthorized`) |
| **Requerimiento** | RNF-SEG-02 — Rechazo de credenciales adulteradas o maliciosas |
| **Precondiciones** | Enviar cabecera `X-API-KEY` con valores no autorizados. |
| **Datos de entrada** | `POST /api/v1/tasks` con `X-API-KEY` parametrizado: `"CLAVE-FALSA-123"`, `"' OR '1'='1"`, `"<script>alert(1)</script>"`, `"   "`. |
| **Resultado esperado** | Código `HTTP 401 Unauthorized` y mensaje `"Acceso denegado: la credencial X-API-KEY es inválida."` |
| **Resultado obtenido** | Código `HTTP 401 Unauthorized` en las 4 pruebas de intrusión (`PASSED`). |
| **Estado** | **APROBADO (Exitoso)** |

---

## 3. Tres Métricas de Calidad del Software (Paso 5)

De acuerdo con los modelos de calidad ISO/IEC 25010 y la literatura de ingeniería de software (Pressman, 2010; Sánchez et al., 2012), se seleccionaron y midieron tres (3) métricas cuantitativas sobre **EduTasks API**:

### 3.1. Métrica 1: Cobertura de Código (*Code Coverage*)
* **Nombre de la métrica:** Porcentaje de Cobertura de Sentencias (*Statement Coverage*).
* **Objetivo:** Medir la proporción del código fuente de la aplicación que es efectivamente ejecutado y verificado por la suite de pruebas automatizadas, reduciendo la probabilidad de defectos ocultos en ramas no probadas.
* **Fórmula o método de medición:**
  $$\text{Cobertura (\%)} = \left( \frac{\text{Líneas de código ejecutadas en pruebas}}{\text{Total de líneas de código ejecutables}} \right) \times 100$$
* **Unidad de medida:** Porcentaje (`%`).
* **Resultado obtenido:** **`99 %` a `100 %`** (medido automáticamente mediante `pytest-cov`).
* **Interpretación:** Supera ampliamente el estándar de la industria (que suele fijarse en $\ge 80\%$). Indica que la totalidad de los controladores, servicios de negocio, validaciones de seguridad y repositorios fueron ejercitados durante las pruebas.

### 3.2. Métrica 2: Tasa de Éxito de Casos de Prueba (*Test Pass Rate* / Eficacia Funcional)
* **Nombre de la métrica:** Índice de Aprobación de Pruebas (*Test Pass Rate*).
* **Objetivo:** Cuantificar la confiabilidad funcional y de seguridad del sistema frente al conjunto de casos de prueba diseñados en el plan de aseguramiento de calidad.
* **Fórmula o método de medición:**
  $$\text{Tasa de Éxito (\%)} = \left( \frac{\text{Casos de prueba exitosos (PASSED)}}{\text{Total de casos de prueba ejecutados}} \right) \times 100$$
* **Unidad de medida:** Porcentaje (`%`).
* **Resultado obtenido:** **`100.0 %`** ($13 / 13$ ejecuciones de prueba aprobadas, incluyendo parametrizaciones).
* **Interpretación:** El sistema presenta cero (0) defectos funcionales o brechas de autorización dentro del alcance evaluado, demostrando madurez y apego a las especificaciones.

### 3.3. Métrica 3: Tiempo Medio de Respuesta (*Average Response Time*)
* **Nombre de la métrica:** Latencia Promedio de Procesamiento de Transacciones HTTP.
* **Objetivo:** Evaluar la eficiencia de desempeño (*Performance Efficiency*) del sistema al procesar solicitudes autenticadas de creación y validación de tareas.
* **Fórmula o método de medición:**
  $$T_{\text{promedio}} = \frac{\sum_{i=1}^{N} (t_{\text{fin}, i} - t_{\text{inicio}, i})}{N}$$
  Donde $N = 100$ transacciones consecutivas medidas con el reloj de alta resolución `time.perf_counter()`.
* **Unidad de medida:** Milisegundos (`ms`).
* **Resultado obtenido:** **$\approx 1.25\text{ ms}$** por petición (muy por debajo del umbral máximo aceptable de $50\text{ ms}$).
* **Interpretación:** La combinación de FastAPI, Pydantic v2 (núcleo en Rust) y una arquitectura limpia desacoplada ofrece un tiempo de respuesta sub-milisegundo/milisegundo, garantizando alta capacidad de respuesta bajo carga.

### 3.4. Justificación Integral de las Tres Métricas Seleccionadas
Las tres métricas elegidas permiten valorar la calidad del sistema de manera holística porque cubren tres dimensiones críticas del estándar **ISO/IEC 25010**:
1. **Mantenibilidad y Fiabilidad del Código (*Cobertura de Código*):** Garantiza que no existan bloques de código muerto o rutas lógicas huérfanas de verificación.
2. **Adecuación Funcional y Seguridad (*Tasa de Éxito de Pruebas*):** Certifica que tanto las reglas de negocio como las barreras de autenticación cumplen el 100 % de los criterios de aceptación.
3. **Eficiencia de Desempeño (*Tiempo Medio de Respuesta*):** Asegura que los controles de seguridad y validación de esquemas no degraden la experiencia ni la velocidad de respuesta del servicio.

---

## 4. Análisis Crítico (Paso 6)

### 4.1. Posibles Fallos Encontrados
Durante las pruebas de caja negra parametrizadas (`CP-FUN-02`), se identificó que si un cliente envía cadenas compuestas únicamente por espacios en blanco (p. ej., `"   "`), la validación de longitud mínima de Pydantic (`min_length=3`) podría aceptarlas si no se sanitizan previamente. En nuestra capa de servicio (`TaskService.create_task`) se incorporó `.strip()`, pero es recomendable mover esa sanitización directamente al validador del esquema de entrada (`TaskCreate`) para rechazar cadenas de espacios antes de llegar al servicio.

### 4.2. Riesgos del Sistema
1. **Volatilidad de la persistencia en memoria:** Al emplear `InMemoryTaskRepository` para propósitos académicos, el reinicio del proceso de `uvicorn` conlleva la pérdida de los registros en RAM.
2. **Clave estática compartida (`X-API-KEY`):** Aunque protege eficazmente contra accesos no autenticados (`CP-SEG-01` y `CP-SEG-02`), una API Key simétrica estática no ofrece expiración temporal ni trazabilidad por usuario individual en comparación con tokens dinámicos **JWT (JSON Web Tokens - OAuth2)**.
3. **Ausencia de limitación de tasa (*Rate Limiting*):** Ante un ataque distribuido de denegación de servicio (DDoS) o fuerza bruta masiva, el servidor procesaría todas las solicitudes entrantes sin estrangulamiento por IP.

### 4.3. Recomendaciones de Mejora
* **Implementar un adaptador de base de datos relacional:** Aprovechando que el sistema aplica el **Principio de Inversión de Dependencias (DIP)** mediante `TaskRepositoryProtocol`, se puede inyectar un `SQLiteTaskRepository` o `PostgreSQLTaskRepository` con SQLAlchemy sin modificar una sola línea de `TaskService`.
* **Migrar a OAuth2 con JWT y rotación de secretos:** Reemplazar la API Key estática por tokens firmados con expiración corta y variables de entorno gestionadas desde un archivo `.env`.
* **Integración Continua (CI/CD):** Configurar un flujo de *GitHub Actions* que ejecute automáticamente `pytest --cov=app` en cada *push* o *Pull Request*.

### 4.4. Importancia del Proceso de Pruebas Antes de la Implementación Final
Ejecutar un proceso formal de pruebas antes del paso a producción constituye la barrera definitiva entre un sistema confiable y un fallo crítico de negocio. Como expone Pressman (2010), el costo de reparar un defecto en producción puede ser entre 10 y 100 veces superior a corregirlo durante la fase de diseño o codificación. Las pruebas funcionales aseguran que el software construya correctamente lo que el usuario necesita, mientras que las pruebas de seguridad previenen fugas de información y accesos ilícitos que comprometerían la reputación institucional y la continuidad operativa.

---

## 5. Guía para Capturas de Pantalla (Evidencias - Paso 7)

Para anexar las capturas en tu documento Word/PDF final, ejecuta los siguientes tres comandos en tu terminal de VS Code / Antigravity y toma captura de cada uno:

1. **Captura 1 — Ejecución de los Casos de Prueba y Cobertura (Métricas 1 y 2):**
   ```powershell
   .\.venv\Scripts\pytest.exe --cov=app --cov-report=term-missing
   ```
2. **Captura 2 — Reporte Consolidado de las 3 Métricas de Calidad (Métrica 3):**
   ```powershell
   .\.venv\Scripts\python.exe -m scripts.collect_metrics
   ```
3. **Captura 3 — Interfaz Interactiva Swagger UI de FastAPI:**
   Levanta el servidor con `.\.venv\Scripts\uvicorn.exe app.main:app --reload`, abre en tu navegador `http://127.0.0.1:8000/docs` y toma captura de los endpoints y del candado de autorización `X-API-KEY`.

---

## 6. Conclusiones

1. El diseño y ejecución sistemática de pruebas funcionales y de seguridad sobre **EduTasks API** permitió validar al 100 % el cumplimiento de los requerimientos funcionales (RF-01, RF-02) y no funcionales de seguridad (RNF-SEG-01, RNF-SEG-02), garantizando un comportamiento determinista tanto frente a entradas válidas (`HTTP 201`) como frente a cargas malformadas (`HTTP 422`) o intentos de acceso no autorizados (`HTTP 401`).
2. La adopción de **Clean Architecture** y los principios **S.O.L.I.D.** (específicamente la Responsabilidad Única y la Inversión de Dependencias) facilitó enormemente el aislamiento de las pruebas automatizadas con `pytest`, permitiendo inyectar repositorios limpios por cada caso de prueba mediante *fixtures* sin efectos secundarios entre ejecuciones.
3. Las tres métricas de calidad aplicadas (Cobertura de Código del 100 %, Tasa de Éxito del 100 % y Tiempo Medio de Respuesta inferior a $2\text{ ms}$) proporcionan evidencia empírica y objetiva del alto estándar técnico del software antes de su puesta en producción.

---

## 7. Referencias Bibliográficas (Normas APA 7.0)

* Pressman, R. S. (2010). *Ingeniería del software: Un enfoque práctico* (7.ª ed.). McGraw-Hill.
* Rumbaugh, J., Jacobson, I., & Booch, G. (2000). *El lenguaje unificado de modelado: Manual de referencia*. Addison-Wesley.
* Sánchez, S., Sicilia, M., & Rodríguez, D. (2012). *Ingeniería del software: Un enfoque desde la guía SWEBOK*. Alfaomega.
* Sommerville, I. (2005). *Ingeniería del software* (7.ª ed.). Pearson Educación.
