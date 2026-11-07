# Revisión de la entrega de Semana 5

Revisión del 7 de noviembre de 2026. Esta tabla localiza evidencias de los siete criterios de la guía. La calificación y la comprobación de que el estudiante puede explicar el código corresponden al docente.

| Criterio | Evidencia entregada | Comprobación |
|---|---|---|
| Contrato | README, HU-01 Must, dos criterios originales, firma con tipos, entradas, salida, errores, supuestos, límites y cuatro ejemplos. | Revisado contra la guía y el Word de Semana 3. |
| Pruebas | 12 funciones y 20 casos: 3 normales, 3 límites y 14 errores. | `python -m pytest` pasa; errores incluyen descripción vacía y ningún registro nuevo. |
| Implementación | Función principal `registrar_reporte`, dataclass y helper privado. | SQLite conserva el dato; prueba de reapertura, validación y texto parametrizado. |
| Pruebas primero | Commits `587800f`, `8dc816a` y `49e4b51`. | Primer estado: 20 fallos por función pendiente. Estados siguientes: 20 casos en verde. |
| Refactor | Extracción de `_validar_y_limpiar_datos`. | Archivo de pruebas sin cambios; mismo identificador Git en las tres etapas. |
| Bitácora | Cinco entradas, 3 aceptadas, 1 ajustada y 1 rechazada; razones, respuestas, verificación y reflexión de siete líneas. | Referencias a salidas reales y commits. |
| Uso responsable | `.gitignore`, SQL parametrizado, código sin credenciales; guía para explicar los bloques. | Pruebas intactas después del rojo. La explicación personal del estudiante se prepara con la guía y no se declara como una evaluación ya realizada. |

La entrega se publica en https://github.com/devpedro24/asistente-reportes-errores-seminario y se envía su URL en Q10. El repositorio es público para permitir la revisión del docente mediante el enlace. El ZIP con `.git` se conserva como respaldo de la entrega inicial, modalidad también admitida por la página 2 de la tarea.

## Avance del proyecto

HU-01 pasa de especificación a implementación verificada. El siguiente incremento es HU-05: sugerir severidad con reglas confirmadas. Siguen fuera de este incremento la clasificación, la integración con un modelo externo, cuentas de usuarios y el despliegue.
