"""Contrato inicial de HU-01; implementación pendiente del estado rojo."""

from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Reporte:
    """Datos de un reporte que se conservarán en SQLite."""

    identificador: str
    descripcion: str
    fecha: date
    operacion: str


def registrar_reporte(
    ruta_bd: str | Path,
    descripcion: str,
    fecha: date,
    operacion: str,
) -> Reporte:
    """Registrar y devolver el reporte según el contrato del README."""
    raise NotImplementedError("HU-01 pendiente de implementación")
