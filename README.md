# Asistente para priorizar reportes de errores

Primera funcionalidad del proyecto final del seminario de IA aplicada al ciclo de vida del software.
Estudiante: Pedro José Ortiz Méndez. Entrega: Semana 5, 7 de noviembre de 2026.

Este incremento registra y conserva un reporte de error en una base SQLite local. Es una pieza pequeña del proyecto: todavía no clasifica severidad ni conecta con servicios de IA. La IA se utiliza como asistente durante el desarrollo.

## Funcionalidad de la semana 5

### Historia elegida de la Semana 3

**HU-01, prioridad Must.** Como persona que reporta un error, quiero registrar su descripción, fecha y operación afectada para conservar la información del incidente. Necesidad de origen: N-01.

**Criterios de aceptación originales**

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

Fuente: documento de requisitos de Semana 3, sección 4, HU-01. Los criterios se conservan; las decisiones adicionales de este incremento se distinguen en el contrato y en [ADR-001](docs/ADR-001-registro-local.md).

### Contrato de la función

```python
def registrar_reporte(
    ruta_bd: str | Path,
    descripcion: str,
    fecha: date,
    operacion: str,
) -> Reporte:
```

`Reporte` contiene `identificador: str`, `descripcion: str`, `fecha: date` y `operacion: str`.

| Entrada | Regla |
|---|---|
| `ruta_bd` | Ruta de un archivo SQLite. Su carpeta debe existir y permitir escritura. La función crea la tabla si hace falta. |
| `descripcion` | Texto. Se eliminan espacios al comienzo y al final; el contenido interno se conserva. Después de limpiar no puede quedar vacío. |
| `fecha` | Objeto `datetime.date`. No se aceptan cadenas ni `datetime.datetime`. No se agrega una regla sobre fechas futuras. |
| `operacion` | Texto no vacío después de limpiar espacios exteriores. Se guarda el nombre que reciba; no hay catálogo cerrado. |

**Salida y efectos.** Devuelve el reporte ya guardado. El primer identificador es `REP-001`; los siguientes usan el número persistido por SQLite, con al menos tres dígitos. Los registros anteriores se conservan al cerrar y volver a abrir el archivo. Cada llamada válida agrega un registro, incluso si sus datos coinciden con otro. No cambia los argumentos recibidos.

**Errores.** Descripción vacía o solo con espacios: `ValueError("Falta la descripción")`. Operación vacía: `ValueError("Falta la operación afectada")`. Descripción u operación que no sean texto, o fecha con tipo incorrecto: `TypeError`. La validación ocurre antes de abrir la base y no crea registros. Los errores de almacenamiento se propagan como excepciones de `sqlite3`; no se informa éxito cuando una escritura falla.

**Supuestos y límites.** Un archivo local, uso secuencial y esquema administrado por esta función. No se añaden límites arbitrarios de longitud, cuentas, red, interfaz gráfica, clasificación, búsqueda ni modificaciones de reportes. Se admiten descripciones de un carácter, fechas bisiestas y texto con apóstrofos. La fecha la proporciona quien llama. Estas son decisiones de diseño del incremento, pendientes de validación de negocio, no nuevas frases de un cliente.

### Ejemplos de entrada y salida

Cada ejemplo parte de una base nueva, salvo donde se indica.

| Descripción | Fecha | Operación | Resultado esperado |
|---|---|---|---|
| `No se confirma el pedido` | `date(2026, 10, 24)` | `confirmación` | `Reporte("REP-001", "No se confirma el pedido", date(2026, 10, 24), "confirmación")` |
| `Falla al abrir pedidos` | `date(2026, 11, 7)` | `consulta` | Después del primer ejemplo: `REP-002`, con los datos recibidos, sin perder REP-001. |
| ` x ` | `date(2024, 2, 29)` | ` vista ` | `Reporte("REP-001", "x", date(2024, 2, 29), "vista")` |
| `   ` | `date(2026, 11, 7)` | `confirmación` | `ValueError: Falta la descripción`; cero registros nuevos. |

## Ejecutar las pruebas

Requiere Python 3.11 o posterior. La implementación utiliza únicamente la librería estándar; `pytest` es una dependencia de desarrollo.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pytest
```

Si el entorno ya tiene las dependencias instaladas, el único comando de pruebas es `python -m pytest`. Las pruebas usan archivos temporales y no alteran los reportes de la demostración.

## Estructura

```text
reportes/             Modelo y función principal
tests/               Pruebas automatizadas
docs/                Decisión de diseño y explicación del código
evidencias/          Salidas reales de las pruebas y revisión del historial
README.md            Historia, contrato y ejecución
bitacora_ia.md       Sugerencias, decisiones, verificación y reflexión
```

## Demostración breve

```powershell
.venv\Scripts\python.exe demo.py
```

Guarda un ejemplo válido y muestra el mensaje al intentar guardar otro con la descripción vacía. Crea `reportes_demo.sqlite3`, un archivo local excluido de Git. Si se repite la demostración, conserva los datos anteriores y utiliza un identificador nuevo. También admite `--bd ruta/al/archivo.sqlite3` si la carpeta existe.

## Resultado y evidencia

Verificado el 7 de noviembre de 2026 con Python 3.12.14, SQLite y pytest 9.2.0 en Windows. Hay 12 funciones de prueba que generan **20 casos**: 3 normales, 3 de límite y 14 de error. El comportamiento de años bisiestos se comprueba junto con la limpieza de espacios.

| Etapa | Commit | Ejecución real |
|---|---|---|
| Contrato y pruebas antes de implementar | `587800f` | 20 fallos esperados por `NotImplementedError`; [salida roja](evidencias/01_pruebas_rojo.txt). |
| Implementación | `8dc816a` | 20 pruebas pasan; [salida verde](evidencias/03_pruebas_verde.txt). |
| Refactor de la validación | `49e4b51` | Las mismas 20 pruebas pasan; [salida posterior](evidencias/04_pruebas_refactor.txt). |

No se cambiaron las pruebas entre esas etapas. Su identificador de contenido Git es el mismo: `f178981bbb4a4ab0622245519007a1f064850100`.

La [bitácora](bitacora_ia.md) contiene cinco entradas con propuestas aceptadas, ajustadas y rechazadas. El [análisis de la alternativa en memoria](evidencias/alternativa_memoria.md) incluye la prueba deliberada que detectó pérdida de datos. Esa comparación no se incluye en las pruebas del producto, ya que el código rechazado no pertenece a la implementación final.

La [guía del código](docs/explicacion_codigo.md) explica el modelo, la validación, las transacciones y el refactor. La [revisión de entrega](docs/revision_entrega.md) relaciona los criterios de la tarea con sus evidencias. No se afirma haber validado nuevos requisitos con un cliente ni haber desarrollado las otras historias.

## Entrega y revisión del historial

La carpeta del proyecto se entrega en un ZIP con `.git` incluido, opción admitida por la guía cuando no se usa un repositorio en línea. Extrae la carpeta completa antes de abrirla en el editor; algunas aplicaciones ocultan `.git` al mostrar archivos.

```powershell
git log --oneline --reverse
git diff 587800f 49e4b51 -- tests/test_registro.py
git show 587800f:reportes/registro.py
```

El segundo comando no debe mostrar cambios: confirma que no se alteraron las pruebas para llegar al verde. El tercero muestra el contrato ejecutable todavía sin implementar. Para revisar las etapas sin cambiar la versión final, pueden crearse carpetas independientes con `git worktree add ../revision-rojo 587800f` y `git worktree add ../revision-verde 8dc816a`, y ejecutar allí las pruebas.
