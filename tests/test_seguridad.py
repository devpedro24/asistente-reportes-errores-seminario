"""Regresiones y casos de abuso agregados en la revisión de Semana 6."""

from contextlib import closing
from datetime import date
from pathlib import Path
import sqlite3

import pytest

from reportes import registrar_reporte


@pytest.mark.parametrize("ruta", ["", ":memory:", Path(":memory:")])
def test_rechaza_almacenamiento_temporal_antes_de_abrir_sqlite(
    ruta: str | Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """El contrato exige archivo persistente; no debe abrir una base temporal."""
    conexiones = []
    conectar_original = sqlite3.connect

    def registrar_conexion(*argumentos, **opciones):
        conexiones.append(argumentos[0])
        return conectar_original(*argumentos, **opciones)

    monkeypatch.setattr(sqlite3, "connect", registrar_conexion)
    with pytest.raises(ValueError, match="^La base debe ser un archivo persistente$"):
        registrar_reporte(ruta, "Error", date(2026, 11, 14), "consulta")
    assert conexiones == []


def test_texto_sql_en_operacion_no_borra_ni_altera_otros_reportes(
    tmp_path: Path,
) -> None:
    """Un texto hostil en el segundo campo también debe tratarse como dato."""
    ruta = tmp_path / "reportes.sqlite3"
    operacion = "consulta'); DROP TABLE reportes; --"
    registrar_reporte(ruta, "Primero", date(2026, 11, 14), operacion)
    registrar_reporte(ruta, "Segundo", date(2026, 11, 14), "confirmación")
    with closing(sqlite3.connect(ruta)) as conexion:
        filas = conexion.execute(
            "SELECT descripcion, operacion FROM reportes ORDER BY id"
        ).fetchall()
    assert filas == [("Primero", operacion), ("Segundo", "confirmación")]


def test_fallo_de_escritura_no_devuelve_exito_ni_pierde_datos(tmp_path: Path) -> None:
    """Una restricción de la base se propaga y conserva el reporte anterior."""
    ruta = tmp_path / "reportes.sqlite3"
    registrar_reporte(ruta, "Anterior", date(2026, 11, 14), "consulta")
    with closing(sqlite3.connect(ruta)) as conexion:
        conexion.execute(
            """
            CREATE TRIGGER bloquear_rechazo BEFORE INSERT ON reportes
            WHEN NEW.descripcion = 'rechazar'
            BEGIN SELECT RAISE(ABORT, 'escritura bloqueada'); END;
            """
        )
        conexion.commit()
    with pytest.raises(sqlite3.IntegrityError, match="escritura bloqueada"):
        registrar_reporte(ruta, "rechazar", date(2026, 11, 14), "consulta")
    with closing(sqlite3.connect(ruta)) as conexion:
        filas = conexion.execute("SELECT descripcion FROM reportes").fetchall()
    assert filas == [("Anterior",)]
