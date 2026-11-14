"""Registro local de reportes para HU-01."""

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import sqlite3


@dataclass(frozen=True)
class Reporte:
    """Datos confirmados de un reporte, sin permitir reasignar sus atributos.

    Contiene el identificador visible, la descripción, la fecha sin hora y la
    operación afectada. No conserva una conexión abierta a SQLite.
    """

    identificador: str
    descripcion: str
    fecha: date
    operacion: str


def _validar_y_limpiar_datos(
    descripcion: str,
    fecha: date,
    operacion: str,
) -> tuple[str, str]:
    """Validar los datos del incidente y limpiar los textos exteriores.

    Args:
        descripcion: Texto del error; no puede quedar vacío tras limpiar.
        fecha: Fecha de tipo date exacto, sin aceptar datetime ni cadenas.
        operacion: Nombre de la operación; no puede quedar vacío tras limpiar.

    Returns:
        Tupla con descripción y operación sin espacios exteriores. Los espacios
        interiores se conservan y no se modifica la fecha recibida.

    Raises:
        TypeError: Si los textos o la fecha no tienen los tipos admitidos.
        ValueError: Si la descripción o la operación quedan vacías.
    """
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


def _guardar_en_sqlite(
    ruta_bd: str | Path,
    descripcion: str,
    fecha: date,
    operacion: str,
) -> int:
    """Guardar los datos ya validados y devolver la clave de la inserción.

    Args:
        ruta_bd: Ruta del archivo SQLite que se abrirá.
        descripcion: Descripción ya validada y sin espacios exteriores.
        fecha: Fecha validada que se almacenará en formato ISO.
        operacion: Operación ya validada y sin espacios exteriores.

    Returns:
        Clave numérica asignada por SQLite, después de confirmar la escritura
        y cerrar la conexión. Crea el esquema mínimo si todavía no existe.

    Raises:
        TypeError: Si SQLite no admite el tipo de ruta recibido.
        ValueError: Si SQLite rechaza una ruta con caracteres nulos.
        sqlite3.Error: Si falla la apertura, el esquema o la escritura. El error
            se propaga y la conexión abierta se cierra en todos los casos.
    """
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
    return numero


def registrar_reporte(
    ruta_bd: str | Path,
    descripcion: str,
    fecha: date,
    operacion: str,
) -> Reporte:
    """Validar, guardar en un archivo SQLite y devolver el reporte confirmado.

    Args:
        ruta_bd: Ruta del archivo persistente; su carpeta debe existir. No admite
            el nombre vacío ni el nombre especial :memory: de SQLite.
        descripcion: Texto del error, sin quedar vacío al limpiar los extremos.
        fecha: Fecha de tipo date exacto, sin hora.
        operacion: Texto de la operación afectada, no vacío tras limpiar.

    Returns:
        Reporte con identificador REP-001 o siguiente y los datos guardados.
        La devolución ocurre después de confirmar la escritura y cerrar la
        conexión. Cada llamada válida agrega un registro.

    Raises:
        TypeError: Si la descripción, operación o fecha tienen tipos inválidos,
            o si SQLite no admite el tipo de ruta recibido.
        ValueError: Si falta descripción u operación, o la ruta indica una base
            temporal. SQLite también rechaza una ruta con caracteres nulos.
        sqlite3.Error: Si falla la apertura, el esquema o la escritura. No se
            devuelve éxito y la conexión abierta se cierra incluso ante un error.
    """
    descripcion, operacion = _validar_y_limpiar_datos(descripcion, fecha, operacion)
    if str(ruta_bd) in ("", ":memory:"):
        raise ValueError("La base debe ser un archivo persistente")

    numero = _guardar_en_sqlite(ruta_bd, descripcion, fecha, operacion)
    return Reporte(f"REP-{numero:03d}", descripcion, fecha, operacion)
