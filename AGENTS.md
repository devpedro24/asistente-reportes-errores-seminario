# Reglas del proyecto

- Incremento HU-01: registro de reportes de Semana 5 y revisión de Semana 6. No ampliar a otras historias.
- Python 3.11 o posterior; pruebas con pytest.
- Implementación solo con librería estándar y SQLite local; ver docs/ADR-001-registro-local.md.
- Nombres, docstrings y mensajes del dominio en español. Tipos explícitos en funciones públicas.
- Respetar la firma y los criterios del README.
- Escribir y ejecutar las pruebas antes de implementar; guardar rojo, verde y refactor en commits distintos.
- No cambiar ni borrar pruebas para hacer pasar el código. Una corrección de prueba requiere commit separado y explicación.
- No escribir claves ni archivos .env. Usar consultas SQL con parámetros.
- Registrar las sugerencias de IA aceptadas, ajustadas y rechazadas con evidencia real.
- Revisión de Semana 6: ejecutar pytest, Ruff (E,F,B,S) y pip-audit; justificar excepciones del linter.
- Un agente que corrija código trabaja en una rama propia y su diff se revisa antes de integrar.
- Mantener README con ocho secciones e informe revision_seguridad.md breve y verificable.
