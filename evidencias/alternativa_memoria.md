# Comparación deliberada de almacenamiento

Fecha: 2026-11-07. Sugerencia evaluada: usar una lista en memoria para reducir código. Fue propuesta como alternativa de comparación y rechazada por pérdida de datos entre procesos; no se presenta como un error accidental de la implementación SQLite.

La prueba aislada produjo un fallo real: el segundo proceso devolvió una lista vacía. La salida está en `02_alternativa_rechazada.txt`. El código rechazado no se instala en el producto.

## Código candidato

Para reproducir la comparación, guarda este bloque en `s5_alternativa_memoria.py` dentro de una carpeta temporal.

```python
"""Alternativa propuesta por IA para comparar; no pertenece al producto."""

from datetime import date


def registrar_en_memoria(reportes, descripcion, fecha, operacion):
    if not descripcion.strip():
        raise ValueError("Falta la descripción")
    reporte = {
        "identificador": f"REP-{len(reportes) + 1:03d}",
        "descripcion": descripcion,
        "fecha": fecha.isoformat(),
        "operacion": operacion,
    }
    reportes.append(reporte)
    return reporte

```

## Prueba de conservación

En la misma carpeta guarda `s5_alternativa_memoria_test.py` con este contenido. Ejecuta `python -m pytest s5_alternativa_memoria_test.py -q`. El fallo es el resultado esperado de evaluar esta alternativa, no de la suite del producto.

```python
"""Comparación deliberada de una alternativa de almacenamiento con el contrato."""

import json
import subprocess
import sys
from pathlib import Path


def test_alternativa_en_memoria_conserva_reportes_entre_procesos():
    carpeta = Path(__file__).parent
    primera = subprocess.run(
        [sys.executable, "-c", "from s5_alternativa_memoria import registrar_en_memoria; from datetime import date; import json; reportes=[]; registrar_en_memoria(reportes, 'No se confirma el pedido', date(2026,10,24), 'confirmación'); print(json.dumps(reportes))"],
        cwd=carpeta, capture_output=True, text=True, encoding="utf-8", check=True,
    )
    segunda = subprocess.run(
        [sys.executable, "-c", "import json; reportes=[]; print(json.dumps(reportes))"],
        cwd=carpeta, capture_output=True, text=True, encoding="utf-8", check=True,
    )
    assert json.loads(segunda.stdout) == json.loads(primera.stdout), (
        "La alternativa en memoria pierde el reporte al comenzar otra ejecución"
    )

```

## Decisión

Rechazada. La función final usa SQLite y comprueba sus datos desde conexiones nuevas. Todas las pruebas del producto pasan con `python -m pytest`.
