# Asistente para priorizar reportes de errores

Repositorio: https://github.com/devpedro24/asistente-reportes-errores-seminario

**Semana 6:** incremento revisado con 25 pruebas, linter de seguridad, auditoría de dependencias, informe y bitácora. El historial conserva Semana 5 y añade las correcciones organizadas de esta revisión.

## 1. Qué es

Proyecto pequeño del Seminario de Inteligencia Artificial Aplicada al Ciclo de Vida del Software. El primer incremento registra y conserva reportes de errores en SQLite local. En la Semana 6 se revisó su calidad y seguridad; todavía no clasifica severidad ni conecta con servicios de IA. La IA se utilizó como asistente de desarrollo y revisión.

### Funcionalidad de la semana 5 y cierre de la semana 6

**HU-01, prioridad Must.** Como persona que reporta un error, quiero registrar su descripción, fecha y operación afectada para conservar la información del incidente. Necesidad de origen: N-01, documento de requisitos de Semana 3.

Los dos criterios originales se conservan:

```gherkin
Escenario: Guardar el reporte
  Dado que el 24/10/2026 describo "No se confirma el pedido"
  Y marco "confirmación" como operación afectada
  Cuando guardo el reporte
  Entonces se muestran esos dos datos y la fecha en el registro REP-001

Escenario: Descripción vacía
  Dado que la descripción está vacía
  Cuando intento guardar el reporte
  Entonces se informa "Falta la descripción"
  Y no se crea un registro
```

### Contrato

```python
def registrar_reporte(
    ruta_bd: str | Path,
    descripcion: str,
    fecha: date,
    operacion: str,
) -> Reporte:
```

`Reporte` contiene identificador, descripción, fecha de tipo `date` y operación. La función devuelve el reporte después de confirmar la escritura y cerrar la conexión. Cada llamada válida agrega un registro, incluso si sus datos coinciden con otro; conserva los anteriores entre ejecuciones.

| Entrada | Regla |
|---|---|
| `ruta_bd` | Ruta de un archivo SQLite cuya carpeta ya existe y permite escritura. La tabla se crea si falta. Desde Semana 6 se rechazan `""` y `":memory:"` porque no conservan los reportes al cerrar. |
| `descripcion` | Texto no vacío después de quitar espacios exteriores; conserva los espacios internos. |
| `fecha` | Objeto `datetime.date` exacto; no se aceptan cadenas ni `datetime.datetime`. |
| `operacion` | Texto no vacío después de quitar espacios exteriores, sin catálogo cerrado. |

El primer identificador es `REP-001`; SQLite administra la secuencia y se muestran al menos tres dígitos. No se añaden límites arbitrarios de longitud ni restricciones de fechas futuras. Se aceptan un carácter, años bisiestos y apóstrofos. El uso es local y secuencial, con el esquema administrado por esta función; no incluye cuentas, red, búsqueda ni modificación de reportes.

Errores: `ValueError("Falta la descripción")`, `ValueError("Falta la operación afectada")` o, desde Semana 6, `ValueError("La base debe ser un archivo persistente")`. Los tipos incorrectos generan `TypeError`. SQLite puede rechazar rutas inválidas o propagar errores de apertura/escritura; no se informa éxito si falla la persistencia. Los datos se validan antes de abrir la base y los argumentos no se modifican.

Las decisiones técnicas adicionales se identifican en [ADR-001](docs/ADR-001-registro-local.md); no se atribuyen a una nueva entrevista con un cliente. La validación de rutas temporales protege el contrato existente de conservación.

### Ejemplos

Cada ejemplo parte de una base nueva, salvo el segundo.

| Descripción | Fecha | Operación | Salida |
|---|---|---|---|
| `No se confirma el pedido` | `date(2026, 10, 24)` | `confirmación` | `Reporte("REP-001", "No se confirma el pedido", date(2026, 10, 24), "confirmación")` |
| `Falla al abrir pedidos` | `date(2026, 11, 7)` | `consulta` | Tras el anterior: `REP-002`, con los datos recibidos y sin perder REP-001. |
| ` x ` | `date(2024, 2, 29)` | ` vista ` | `Reporte("REP-001", "x", date(2024, 2, 29), "vista")` |
| `   ` | `date(2026, 11, 7)` | `confirmación` | `ValueError: Falta la descripción`; ningún registro nuevo. |

## 2. Requisitos

Python 3.11 o posterior y Git para clonar. La aplicación usa solo la librería estándar (`sqlite3`, `datetime`, `dataclasses`, `pathlib` y `argparse`). No requiere servidor, credenciales ni servicios de pago.

`requirements-dev.txt` fija las herramientas de desarrollo: pytest 9.2.0, Ruff 0.17.5, pip-audit 2.10.1 y sus dependencias transitivas, incluido pip 26.3. Pytest comprueba comportamiento; Ruff revisa estilo, errores y seguridad; pip-audit consulta vulnerabilidades conocidas. Las dependencias transitivas sirven a estas herramientas, no se importan desde el producto. Los resultados se verificaron el 14/11/2026 y deben renovarse al actualizar versiones.

`.env.example` documenta que este incremento no consume variables de entorno. No contiene claves y la aplicación no lo carga. `.env`, las bases de datos y los entornos locales están excluidos de Git.

## 3. Instalación

En PowerShell, desde la carpeta donde quieras guardar el proyecto:

```powershell
git clone https://github.com/devpedro24/asistente-reportes-errores-seminario.git
cd asistente-reportes-errores-seminario
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Los comandos usan el ejecutable del entorno y no necesitan activar scripts de PowerShell. El entorno `.venv` se crea en cada equipo; no se copia desde Git. Si una actualización o desinstalación elimina el Python al que apuntaba un entorno local, vuelve a crearlo con el Python instalado.

La instalación y ejecución se comprobaron primero en una copia local limpia; su registro está en `evidencias/semana6/instalacion_limpia_local.txt`. El cierre de publicación añade una comprobación desde un clon limpio de GitHub en `evidencias/semana6/21_validacion_github.txt`.

## 4. Ejecución

```powershell
.\.venv\Scripts\python.exe demo.py
```

En una base nueva muestra REP-001, los datos guardados y `Registro vacío rechazado: Falta la descripción`. Crea `reportes_demo.sqlite3`, excluido de Git. Al repetir la demostración conserva los datos anteriores y usa otro identificador.

```powershell
.\.venv\Scripts\python.exe demo.py --help
.\.venv\Scripts\python.exe demo.py --bd otra_base.sqlite3
```

La carpeta de una ruta personalizada debe existir. La biblioteca también se puede llamar con la firma de la sección 1. No hay un servidor web que iniciar.

## 5. Pruebas y revisión

Ejecuta desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pip_audit -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip check
```

Resultado al cerrar Semana 6: **25 casos pasan**, Ruff sin avisos y auditoría sin vulnerabilidades conocidas en el conjunto fijado. La consulta no certifica que todo el programa sea seguro ni cubre vulnerabilidades futuras.

Las veinte pruebas de Semana 5 permanecen intactas. Se agregaron tres regresiones de almacenamiento temporal y dos casos de abuso: SQL en la operación y fallo de escritura sin pérdida del registro anterior. Las pruebas usan archivos temporales; no alteran la base de la demostración.

Ruff activa `E,F,B,S` en `pyproject.toml`. Solo se excluye `S101` en `tests/**`: las aserciones son la forma de comprobar resultados en pytest y no validan entradas en producción. Los demás avisos se corrigieron. El [informe de seguridad](revision_seguridad.md) contiene hallazgos, commits, revisión con IA y pendientes; la [guía del código](docs/explicacion_codigo.md) ayuda a preparar la exposición.

### Historial de pruebas primero

| Etapa de Semana 5 | Commit | Evidencia |
|---|---|---|
| Contrato y pruebas antes del código | `587800f` | 20 fallos esperados, `evidencias/01_pruebas_rojo.txt`. |
| Implementación | `8dc816a` | 20 pasan, `evidencias/03_pruebas_verde.txt`. |
| Refactor de validación | `49e4b51` | Las mismas 20 pasan, `evidencias/04_pruebas_refactor.txt`. |

```powershell
git log --oneline --graph --all
git diff 587800f HEAD -- tests/test_registro.py
```

El segundo comando no muestra cambios. Para la corrección de Semana 6 se conservó también el resultado previo de las nuevas regresiones: tres fallos y 22 casos en verde, antes del arreglo.

## 6. Estructura

```text
reportes/                 Modelo, validación y almacenamiento de HU-01
tests/test_registro.py    Veinte casos originales de Semana 5
tests/test_seguridad.py   Cinco casos nuevos de Semana 6
demo.py                   Demostración local con datos de ejemplo
pyproject.toml            Ruff con reglas E, F, B y S
requirements-dev.txt      Herramientas y versiones transitivas fijadas
.env.example              Ausencia de configuración secreta en este incremento
revision_seguridad.md     Informe breve de Semana 6
bitacora_ia.md            Registro de ambas semanas
docs/                     Decisiones, explicación y revisión de entrega
evidencias/semana6/       Resultados reales de herramientas y revisión
```

## 7. Uso de IA

Se utilizó Codex en modo agente para proponer pruebas, implementar HU-01 y revisar el código. La [bitácora](bitacora_ia.md) conserva las cinco entradas de Semana 5 y agrega las de Semana 6 con decisiones, razones y verificación. La [revisión de IA](evidencias/semana6/revision_ia.md) distingue hallazgos confirmados de sospechas y puntos no aplicables.

Las correcciones de agentes auxiliares se hicieron en ramas propias. Se leyó cada diff y se ejecutaron pruebas y Ruff antes de integrar. El informe relaciona cada corrección con su commit verificable; no se reescribió el historial de Semana 5 ni se modificaron sus pruebas para que pasaran.

Contraseñas y control por roles no aplican al alcance local sin usuarios. El acceso al archivo depende de los permisos del sistema operativo; el programa no se presenta como un servicio multiusuario. La revisión de código e historial no encontró claves expuestas. No se afirma una validación nueva con cliente ni una evaluación ya realizada de la explicación personal del estudiante.

## 8. Autor y licencia

Autor: **Pedro José Ortiz Méndez**. Seminario de Inteligencia Artificial Aplicada al Ciclo de Vida del Software, 2026.

Licencia: todos los derechos reservados; no se ha añadido una licencia de código abierto. La publicación permite la revisión académica del repositorio.

Entrega de Semana 6: pegar en Q10 **https://github.com/devpedro24/asistente-reportes-errores-seminario**. El repositorio público incluye código, pruebas, README, `revision_seguridad.md`, bitácora y el historial de commits. La rama del agente y su integración permiten revisar el trabajo supervisado. El primer incremento de HU-01 queda revisado; HU-05 sigue como trabajo posterior sujeto a confirmar sus reglas.
