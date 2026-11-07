"""Registro local de reportes para HU-01."""

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import sqlite3


@dataclass(frozen=True)
class Reporte:
    """Datos de un reporte que se conservarán en SQLite."""

    identificador: str
    descripcion: str
    fecha: date
    operacion: str


def _validar_y_limpiar_datos(
    descripcion: str,
    fecha: date,
    operacion: str,
) -> tuple[str, str]:
    """Validar los tipos y devolver los textos sin espacios exteriores."""
    if not isinstance(descripcion, str):
        raise TypeError("La descripción debe ser texto")
    if not isinstance(operacion, str):
        raise TypeError("La operación afectada debe ser texto")
    if type(fecha) is not date:
        raise TypeError("La fecha debe ser un objeto date")

    descripcion = descripcion.strip()
    operacion = operacion.strip()
    if not descripcion:
        raise ValueError("Falta la descripción")
    if not operacion:
        raise ValueError("Falta la operación afectada")
    return descripcion, operacion


def registrar_reporte(
    ruta_bd: str | Path,
    descripcion: str,
    fecha: date,
    operacion: str,
) -> Reporte:
    """Registrar y devolver el reporte según el contrato del README."""
    descripcion, operacion = _validar_y_limpiar_datos(descripcion, fecha, operacion)

    conexion = sqlite3.connect(ruta_bd)
    try:
        with conexion:
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS reportes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    operacion TEXT NOT NULL
                )
                """
            )
            cursor = conexion.execute(
                "INSERT INTO reportes (descripcion, fecha, operacion) VALUES (?, ?, ?)",
                (descripcion, fecha.isoformat(), operacion),
            )
            numero = cursor.lastrowid
    finally:
        conexion.close()

    return Reporte(f"REP-{numero:03d}", descripcion, fecha, operacion)
