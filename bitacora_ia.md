# Bitácora de uso de IA

Proyecto: Asistente para priorizar reportes de errores  
Estudiante: Pedro José Ortiz Méndez  
Funcionalidad: HU-01 Registrar un reporte de error, prioridad Must  
Asistente usado: Codex, modo agente en el entorno local, con agentes auxiliares de revisión, pruebas e implementación.  
Fecha de trabajo: 2026-11-07.

Esta bitácora registra propuestas efectivamente producidas y verificaciones ejecutadas durante esta entrega. Las decisiones describen lo incorporado en el repositorio por el flujo asistido; no afirman una revisión personal del estudiante que no se haya observado. Las respuestas citadas son extractos literales o resúmenes identificados como tales. No se inventa una entrevista con cliente ni resultados de pruebas.

## Entradas

### Entrada 1 Seleccionar la historia y fijar el contrato

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia:** Se pidió revisar la guía y las historias Must del documento de Semana 3 y recomendar un contrato pequeño para registrar y conservar reportes con SQLite.
- **Respuesta del asistente, extracto:** «La selección adecuada es HU-01, prioridad Must» y «SQLite permite demostrar conservación reabriendo la base». Propuso `registrar_reporte(ruta_bd, descripcion, fecha, operacion) -> Reporte` y separar las nuevas decisiones técnicas de los criterios originales.
- **Decisión:** Aceptada.
- **Por qué:** HU-01 tiene un resultado observable y acotado. La persistencia local permite demostrar que se conserva el incidente sin servidor ni credenciales. No agrega la clasificación de severidad de HU-05.
- **Verificación:** Se comprobó HU-01 y su prioridad en el Word de Semana 3. El README conserva ambos criterios originales, documenta firma, entradas, salida, errores y cuatro ejemplos. ADR-001 declara expresamente que la elección técnica se toma ahora.
- **Commit relacionado:** `587800f`, contrato y pruebas en rojo.

### Entrada 2 Proponer y revisar las pruebas antes del código

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia, extracto literal:** «Escribe solo tests/test_registro.py (no implementación, no cambios al contrato y no commits). Usa pytest y tmp_path. Cubre los dos criterios originales de HU-01».
- **Respuesta del asistente, resumen:** Escribió 12 funciones con 20 casos parametrizados. Comprobó el objeto devuelto, los registros persistidos mediante una conexión nueva, valores vacíos, tipos y caracteres con aspecto de SQL. La propuesta inicial abría conexiones de lectura con `with sqlite3.connect(...)`.
- **Decisión:** Aceptada con cambios.
- **Por qué:** Se incorporó `contextlib.closing` a las conexiones de lectura antes de congelar las pruebas. El contexto de SQLite controla la transacción, pero no cierra la conexión. El ajuste evita dejar archivos abiertos en Windows; no cambia resultados esperados ni reduce la cobertura.
- **Verificación:** Se ejecutaron las 20 pruebas antes de implementar y todas fallaron por `NotImplementedError`, no por problemas de importación. El resultado está en `evidencias/01_pruebas_rojo.txt`. Ese archivo de pruebas quedó guardado en el primer commit y no cambió después.
- **Commit relacionado:** `587800f`.

### Entrada 3 Evaluar y rechazar almacenamiento en memoria

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia:** Se pidió comparar una lista en memoria con SQLite mediante un fragmento candidato y una prueba observable.
- **Respuesta del asistente, extracto:** «Guardar los reportes en una lista en memoria y asignar REP-{len(reportes)+1:03d} para reducir el código». También advirtió que una ejecución nueva empieza sin los registros.
- **Decisión:** Rechazada.
- **Por qué:** La lista solo conserva reportes durante la vida del proceso. No cumple el contrato de conservación entre ejecuciones fijado para este incremento.
- **Verificación:** Se ejecutó una prueba aislada con dos procesos: el primero agregó REP-001 y el segundo inició una lista nueva. Falló con `AssertionError: La alternativa en memoria pierde el reporte al comenzar otra ejecución`. El código de la comparación y su explicación están en `evidencias/alternativa_memoria.md`; la salida real está en `evidencias/02_alternativa_rechazada.txt`.
- **Commit relacionado:** `docs: completa bitácora y evidencias de entrega de Semana 5`.
- **Alcance de la evidencia:** Es una comparación deliberada de alternativas, no un fallo accidental atribuido a la versión SQLite ni una validación del cliente.

### Entrada 4 Implementar el contrato con el asistente

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia, extracto literal:** «Ya se ejecutaron 20 pruebas en rojo y se guardaron en commit 587800f75444fb33ed801bb9a0da6f38d42cb285. Modifica solo reportes/registro.py. No cambies pruebas, contrato, firma ni hagas commits».
- **Respuesta del asistente, resumen:** Generó validación inline antes de abrir la base, creación del esquema, inserción parametrizada, transacción, cierre explícito y devolución de `Reporte`. No añadió dependencias ni modificó las pruebas.
- **Decisión:** Aceptada.
- **Por qué:** Cumple el contrato pequeño de HU-01 y respeta la separación entre datos y SQL. La función devuelve el registro después de confirmar la escritura.
- **Verificación:** `python -m pytest -q --tb=short` produjo `20 passed in 0.22s`. El diff de pruebas estaba vacío. La salida está en `evidencias/03_pruebas_verde.txt`.
- **Commit relacionado:** `8dc816a`, implementación en verde.

### Entrada 5 Refactorizar sin modificar el comportamiento

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia, extracto literal:** «Extrae la validación y limpieza de descripción/operación a un helper privado con tipos y docstring para que la función principal se lea como validar, guardar y devolver. Preserva exactamente firma pública, orden de errores, transacción, salida y comportamiento».
- **Respuesta del asistente, extracto:** «Extraje _validar_y_limpiar_datos(...) -> tuple[str, str]». Incluyó la comprobación de fecha en el helper para conservar el orden de los errores.
- **Decisión:** Aceptada.
- **Por qué:** Hace más legible la función principal y separa la validación del almacenamiento sin incorporar capas ni nuevas reglas.
- **Verificación:** La misma suite produjo `20 passed in 0.19s`; salida en `evidencias/04_pruebas_refactor.txt`. El identificador Git del archivo de pruebas coincide en rojo, verde y refactor: `f178981bbb4a4ab0622245519007a1f064850100`.
- **Commit relacionado:** `49e4b51`, extracción del helper de validación.

## Resumen

| Decisión | Cantidad |
|---|---:|
| Aceptadas | 3 |
| Aceptadas con cambios | 1 |
| Rechazadas | 1 |
| Total | 5 |

## Errores que atraparon las pruebas

El estado rojo detectó que el contrato ejecutable aún no estaba implementado: las 20 pruebas fallaron por `NotImplementedError`. Se conserva el commit anterior al código funcional como evidencia real del orden del trabajo.

La prueba de conservación entre procesos detectó un defecto concreto en la alternativa generada de lista en memoria: el resultado de la segunda ejecución era `[]` y debía conservar REP-001. Se rechazó ese almacenamiento y se eligió SQLite, cuyas pruebas verifican los datos con conexiones nuevas. La implementación SQLite pasó sus 20 casos en la primera ejecución; no se inventa un error accidental adicional para la bitácora.

El ajuste a `closing` se realizó durante la revisión de pruebas, antes del primer commit. Después del rojo no se eliminó ni modificó ninguna prueba para alcanzar el verde o hacer el refactor.

## Reflexión final

El asistente ayudó a convertir una historia pequeña en un contrato ejecutable.  
Las pruebas previas hicieron explícitos el dato vacío y la conservación de reportes.  
La comparación con memoria mostró que devolver datos correctos no garantiza conservarlos.  
El código SQLite pasó los casos y permitió revisar cada operación sin dependencias externas.  
El refactor mejoró la lectura sin cambiar el archivo de pruebas.  
En el próximo incremento conviene validar las reglas de severidad antes de programar HU-05.  
La explicación del código y sus límites debe revisarse antes de la exposición del estudiante.
