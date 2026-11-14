# Segunda revisión con IA de Semana 6

Fecha: 2026-11-14. Asistente: Codex, agente auxiliar de revisión de solo lectura. Commit examinado: `65f2ce4e886e98b3712516bf4f16d72bd55f61c2`.

## Prompt enviado

Actúa como revisor de código y seguridad para la Semana 6. SOLO lectura. Lee AGENTS.md, reportes/registro.py, demo.py, tests y configuración/README. Revisa corrección, casos límite, diseño, legibilidad, consultas parametrizadas, secretos, contraseñas, acceso y dependencias. Devuelve tabla ID | archivo:línea baseline | hallazgo | severidad | evidencia | seguro o sospecha | cómo verificar. Separa problemas confirmados, sospechas y puntos no aplicables; no inventes vulnerabilidades ni asumas web/roles que no existen. Considera incumplimientos reales del contrato de conservar reportes. NO ejecutes linter ni pip-audit, no edites ni hagas commits. Tu respuesta se conservará para contrastarla con comprobaciones independientes.

## Respuesta recibida y contraste

La tabla siguiente resume fielmente los cinco hallazgos recibidos; las líneas corresponden al commit revisado, no a la numeración después de los docstrings.

| ID | Localización | Respuesta de la IA | Estado inicial | Verificación independiente |
|---|---|---|---|---|
| IA-01 | registro.py:50 | Acepta nombres de base vacíos o :memory:, devuelve éxito y pierde reportes al cerrar. Media, integridad; no es inyección. | Confirmado por dos llamadas a cada ruta. | Real: tres regresiones fallaron antes de la corrección; las 25 pruebas pasan después. H-01 del informe. |
| IA-02 | .gitignore:6 y plantilla ausente | Falta .env.example y .env.* la ignoraría. Baja. | Confirmado con árbol Git y check-ignore. | Real: se versionó la plantilla y su excepción en 7048e43, conservando .env ignorado. H-02. |
| IA-03 | registro.py:24,47; demo.py:11 | Docstrings de una línea sin contrato completo. Baja. | Confirmado por lectura. | Real: se compararon los nuevos Args, Returns y Raises con el código; ramas propias y pruebas antes de integrar. H-03. |
| IA-04 | README.md:71-118 | Faltan la organización en ocho secciones y autor/licencia explícitos. Baja. | Confirmado por títulos. | Real: ocho secciones explícitas y comandos comprobados en una copia local limpia. H-04. |
| IA-05 | requirements-dev.txt:1 | Se fija pytest pero no el cierre transitivo. Sin auditoría no puede afirmarse ausencia de vulnerabilidades. Baja. | Fijación incompleta confirmada; vulnerabilidades por verificar. | Real en reproducibilidad: se fijaron herramientas y transitivas. El pytest inicial no presentó avisos; la auditoría del entorno sí detectó pip antiguo. H-05. |

No se emitieron falsos positivos como hallazgos de esa tabla. La propia revisión descartó dos alertas genéricas: que no se cierra SQLite (hay finally) y que faltan roles web (no hay usuarios ni servicio web). Se conserva esta distinción, sin atribuir a la IA una vulnerabilidad que no afirmó.

## Lo que la revisión de IA no encontró

El agente no ejecutó la auditoría por instrucción. La comprobación independiente de pip-audit detectó seis identificadores únicos de avisos en pip 25.0.1 del entorno, reflejados como doce entradas en la salida del servicio. No son doce vulnerabilidades diferentes ni fallos remotos de HU-01. Se actualizó a pip 26.3 y se auditó nuevamente el entorno y el archivo de versiones: cero avisos conocidos. También se detectó antes de la revisión un entorno virtual que apuntaba a un intérprete de Codex ya retirado; se reconstruyó y se repitió la instalación en una copia local limpia.

## Material de práctica

Se leyó codigo_practica_s6/LEEME.md, tienda.py, tests y pyproject.toml como referencia de la lista de seguridad. Ese ejercicio declara vulnerabilidades sembradas y una clave ficticia; no se copió al proyecto ni se atribuyeron sus defectos a HU-01.
