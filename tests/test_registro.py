"""Pruebas del contrato de HU-01, escritas antes de su implementación."""

from contextlib import closing
from datetime import date, datetime
from pathlib import Path
import sqlite3

import pytest

from reportes import Reporte, registrar_reporte


def leer_reportes(ruta_bd: Path) -> list[tuple[str, str, str]]:
    """Leer los datos conservados mediante una conexión independiente."""
    with closing(sqlite3.connect(ruta_bd)) as conexion:
        return conexion.execute(
            "SELECT descripcion, fecha, operacion FROM reportes ORDER BY rowid"
        ).fetchall()


# Normal; criterio original CA-HU01-1: conservar y mostrar datos como REP-001.
def test_registra_el_caso_original_y_devuelve_sus_datos(tmp_path: Path) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"

    reporte = registrar_reporte(
        ruta_bd, "No se confirma el pedido", date(2026, 10, 24), "confirmación"
    )

    assert reporte == Reporte(
        "REP-001", "No se confirma el pedido", date(2026, 10, 24), "confirmación"
    )
    assert leer_reportes(ruta_bd) == [
        ("No se confirma el pedido", "2026-10-24", "confirmación")
    ]


# Normal; CA-HU01-1 y contrato: agregar sin sobrescribir datos anteriores.
def test_segundo_reporte_recibe_otro_identificador_y_conserva_el_primero(
    tmp_path: Path,
) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"
    primero = registrar_reporte(
        ruta_bd, "No se confirma el pedido", date(2026, 10, 24), "confirmación"
    )

    segundo = registrar_reporte(
        str(ruta_bd), "Falla al abrir pedidos", date(2026, 11, 7), "consulta"
    )

    assert primero.identificador == "REP-001"
    assert segundo == Reporte(
        "REP-002", "Falla al abrir pedidos", date(2026, 11, 7), "consulta"
    )
    assert leer_reportes(ruta_bd) == [
        ("No se confirma el pedido", "2026-10-24", "confirmación"),
        ("Falla al abrir pedidos", "2026-11-07", "consulta"),
    ]


# Normal; CA-HU01-1: persistencia verificable al abrir otra conexión.
def test_datos_siguen_en_el_archivo_despues_de_cerrar_y_reabrir(
    tmp_path: Path,
) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"
    registrar_reporte(ruta_bd, "Error de consulta", date(2026, 11, 7), "consulta")

    with closing(sqlite3.connect(ruta_bd)) as conexion:
        primera_lectura = conexion.execute("SELECT COUNT(*) FROM reportes").fetchone()
    with closing(sqlite3.connect(ruta_bd)) as nueva_conexion:
        segunda_lectura = nueva_conexion.execute(
            "SELECT descripcion, fecha, operacion FROM reportes"
        ).fetchall()

    assert primera_lectura == (1,)
    assert segunda_lectura == [("Error de consulta", "2026-11-07", "consulta")]


# Límite; contrato: no imponer un mínimo de longitud superior a un carácter.
def test_admite_descripcion_y_operacion_de_un_caracter(tmp_path: Path) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"

    reporte = registrar_reporte(ruta_bd, "x", date(2026, 11, 7), "y")

    assert reporte.descripcion == "x"
    assert reporte.operacion == "y"
    assert leer_reportes(ruta_bd) == [("x", "2026-11-07", "y")]


# Límite; contrato: limpiar solo espacios exteriores y aceptar fecha bisiesta.
def test_limpia_espacios_exteriores_y_conserva_espacios_internos(
    tmp_path: Path,
) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"

    reporte = registrar_reporte(
        ruta_bd, " \tFalla  al confirmar\n", date(2024, 2, 29), "  confirmación  "
    )

    assert reporte == Reporte(
        "REP-001", "Falla  al confirmar", date(2024, 2, 29), "confirmación"
    )
    assert leer_reportes(ruta_bd) == [
        ("Falla  al confirmar", "2024-02-29", "confirmación")
    ]


# Error; CA-HU01-2: descripción vacía, también después de limpiar espacios.
@pytest.mark.parametrize("descripcion", ["", " \t\n "], ids=["vacia", "espacios"])
def test_descripcion_vacia_informa_el_mensaje_y_no_abre_la_base(
    tmp_path: Path, descripcion: str
) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"

    with pytest.raises(ValueError, match="^Falta la descripción$"):
        registrar_reporte(ruta_bd, descripcion, date(2026, 11, 7), "consulta")

    assert not ruta_bd.exists()


# Error; CA-HU01-2: rechazar la entrada no elimina ni agrega registros previos.
@pytest.mark.parametrize("descripcion", ["", " \t\n "], ids=["vacia", "espacios"])
def test_error_de_descripcion_conserva_los_registros_existentes(
    tmp_path: Path, descripcion: str
) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"
    registrar_reporte(ruta_bd, "Reporte anterior", date(2026, 11, 6), "consulta")
    antes = leer_reportes(ruta_bd)

    with pytest.raises(ValueError, match="^Falta la descripción$"):
        registrar_reporte(ruta_bd, descripcion, date(2026, 11, 7), "consulta")

    assert leer_reportes(ruta_bd) == antes


# Error; decisión de diseño del contrato: fecha debe ser date, no datetime/texto.
@pytest.mark.parametrize(
    "fecha_invalida",
    ["2026-11-07", datetime(2026, 11, 7, 12, 0), None],
    ids=["texto", "datetime", "nula"],
)
def test_fecha_con_tipo_incorrecto_no_crea_la_base(
    tmp_path: Path, fecha_invalida: object
) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"

    with pytest.raises(TypeError):
        registrar_reporte(ruta_bd, "Error", fecha_invalida, "consulta")  # type: ignore[arg-type]

    assert not ruta_bd.exists()


# Error; decisiones de diseño: no convertir valores no textuales silenciosamente.
@pytest.mark.parametrize("valor_invalido", [None, 23], ids=["nulo", "numero"])
@pytest.mark.parametrize("campo", ["descripcion", "operacion"])
def test_campos_no_textuales_no_crean_la_base(
    tmp_path: Path, campo: str, valor_invalido: object
) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"
    descripcion = valor_invalido if campo == "descripcion" else "Error"
    operacion = valor_invalido if campo == "operacion" else "consulta"

    with pytest.raises(TypeError):
        registrar_reporte(ruta_bd, descripcion, date(2026, 11, 7), operacion)  # type: ignore[arg-type]

    assert not ruta_bd.exists()


# Error; decisión de diseño: la operación se requiere y el fallo conserva datos.
@pytest.mark.parametrize("operacion", ["", " \t "], ids=["vacia", "espacios"])
def test_operacion_vacia_no_inserta_ni_pierde_el_reporte_anterior(
    tmp_path: Path, operacion: str
) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"
    registrar_reporte(ruta_bd, "Reporte anterior", date(2026, 11, 6), "consulta")
    antes = leer_reportes(ruta_bd)

    with pytest.raises(ValueError, match="^Falta la operación afectada$"):
        registrar_reporte(ruta_bd, "Error", date(2026, 11, 7), operacion)

    assert leer_reportes(ruta_bd) == antes


# Límite de entrada; contrato y ADR: SQL parametrizado conserva el texto como dato.
def test_apostrofos_y_texto_con_aspecto_de_sql_se_guardan_como_datos(
    tmp_path: Path,
) -> None:
    ruta_bd = tmp_path / "reportes.sqlite3"
    descripcion = "Pedido de O'Connor'); DROP TABLE reportes; --"

    reporte = registrar_reporte(ruta_bd, descripcion, date(2026, 11, 7), "consulta")
    segundo = registrar_reporte(ruta_bd, "Otro reporte", date(2026, 11, 7), "vista")

    assert reporte.descripcion == descripcion
    assert segundo.identificador == "REP-002"
    assert leer_reportes(ruta_bd) == [
        (descripcion, "2026-11-07", "consulta"),
        ("Otro reporte", "2026-11-07", "vista"),
    ]


# Error de almacenamiento; contrato: propagar fallo, no devolver éxito ficticio.
def test_carpeta_inexistente_propaga_el_error_de_almacenamiento(
    tmp_path: Path,
) -> None:
    ruta_bd = tmp_path / "carpeta_que_no_existe" / "reportes.sqlite3"

    with pytest.raises(sqlite3.OperationalError):
        registrar_reporte(ruta_bd, "Error", date(2026, 11, 7), "consulta")

    assert not ruta_bd.exists()
