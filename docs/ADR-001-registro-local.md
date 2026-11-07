# ADR 001 Registro local del primer incremento

Fecha: 2026-11-07. Estado: decisión técnica adoptada para la entrega de Semana 5.

## Contexto

HU-01 exige conservar descripción, fecha y operación y rechazar una descripción vacía sin crear un registro. El material disponible de Semana 3 no define una tecnología de almacenamiento. No se recibió un diseño de Semana 4; esta decisión se formula ahora y no se presenta como una aprobación anterior del cliente.

## Decisión

Usar Python y SQLite de la librería estándar, con una función principal `registrar_reporte` que reciba la ruta del archivo. El esquema mínimo contiene una clave numérica, descripción, fecha ISO y operación. La salida muestra la clave como REP-001, REP-002 y así sucesivamente.

Limpiar los espacios exteriores, validar tipos y requerir una operación no vacía. La fecha es explícita. No imponer un máximo de texto ni prohibir duplicados o fechas futuras sin una necesidad confirmada. Cada escritura es una transacción y utiliza parámetros SQL.

## Alternativas

- Lista en memoria: simple, pero pierde los datos al cerrar el programa.
- Archivo JSON: suficiente para un ejercicio, aunque obliga a reescribir el conjunto para agregar un reporte.
- Servicio o servidor de base de datos: agrega instalación, credenciales y administración que este incremento no necesita.

## Consecuencias

La entrega se ejecuta sin servicio externo y demuestra persistencia real. Se limita al registro local secuencial; no promete seguridad multiusuario, integración con producción ni clasificación por IA. Las decisiones de validación adicionales necesitan revisión de negocio antes de extender el proyecto.
