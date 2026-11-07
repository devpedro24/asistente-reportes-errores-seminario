"""Demostración de HU-01 con datos de ejemplo, sin servicios externos."""

import argparse
from datetime import date
from pathlib import Path

from reportes import registrar_reporte


def main() -> None:
    """Guardar un ejemplo y mostrar el rechazo de una descripción vacía."""
    argumentos = argparse.ArgumentParser(description="Demostración del registro de reportes")
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
