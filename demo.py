"""Demostración de HU-01 con datos de ejemplo, sin servicios externos."""

import argparse
from datetime import date
from pathlib import Path

from reportes import registrar_reporte


def main() -> None:
    """Ejecutar una demostración de registro y mostrar sus resultados.

    Lee --bd desde los argumentos de consola; por defecto utiliza el archivo
    reportes_demo.sqlite3 en la carpeta actual. Guarda un reporte de ejemplo y
    muestra el ValueError esperado al intentar otro con la descripción vacía.

    Returns:
        None. Imprime los datos guardados, el rechazo y la ruta de la base.

    Raises:
        ValueError: Si la ruta del primer registro indica una base temporal.
        sqlite3.Error: Si no puede abrir o escribir el archivo SQLite.
        SystemExit: Si argparse muestra la ayuda o rechaza los argumentos.
    """
    argumentos = argparse.ArgumentParser(
        description="Demostración del registro de reportes"
    )
    argumentos.add_argument("--bd", type=Path, default=Path("reportes_demo.sqlite3"))
    ruta_bd = argumentos.parse_args().bd
    reporte = registrar_reporte(
        ruta_bd, "No se confirma el pedido", date(2026, 10, 24), "confirmación"
    )
    print(f"Guardado {reporte.identificador}")
    print(f"Descripción: {reporte.descripcion}")
    print(f"Fecha: {reporte.fecha.isoformat()} | Operación: {reporte.operacion}")
    try:
        registrar_reporte(ruta_bd, "", date(2026, 10, 24), "confirmación")
    except ValueError as error:
        print(f"Registro vacío rechazado: {error}")
    print(f"Base local: {ruta_bd.resolve()}")


if __name__ == "__main__":
    main()
