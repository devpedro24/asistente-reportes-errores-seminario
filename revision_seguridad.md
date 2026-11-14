# Informe de revisión de código y seguridad

Proyecto: Asistente para priorizar reportes de errores, HU-01.
Estudiante: Pedro José Ortiz Méndez. Fecha: 2026-11-14.
Commit revisado antes de corregir: `65f2ce4e886e98b3712516bf4f16d72bd55f61c2`.

**Estado: revisión concluida y publicación autorizada por el usuario.** Las correcciones se organizan en commits verificables, conservando el historial de Semana 5.

## 1. Herramientas y criterios

Ruff 0.17.5, reglas **E,F,B,S** en `pyproject.toml`; pytest 9.2.0; pip-audit 2.10.1. Se revisaron corrección, pruebas, legibilidad y los cinco puntos de seguridad. Codex efectuó una segunda revisión independiente. [Salidas y contraste](evidencias/semana6/revision_ia.md).

| Punto | Aplicación y resultado |
|---|---|
| Inyección | Sí: INSERT parametrizado. Texto SQL en descripción y operación permanece como dato, sin ejecutar el SQL recibido. |
| Secretos | Sí: fuente e historial revisados por lectura y patrones. Sin coincidencias; `.env` ignorado y `.env.example` versionado sin claves. |
| Contraseñas | No aplica: HU-01 no guarda ni verifica credenciales; no utiliza hashes de contraseñas. |
| Acceso | No aplica control por rol: función/CLI local sin cuentas ni operaciones restringidas. El sistema operativo controla el archivo. |
| Dependencias | 34 paquetes de desarrollo fijados; producto solo con librería estándar. Auditoría final: cero avisos conocidos; no es garantía de seguridad total. |

## 2. Tabla de hallazgos

Las líneas pertenecen al commit revisado. No se atribuyen al proyecto los defectos sembrados de `codigo_practica_s6`, leído como referencia.

| Id | Archivo y línea | Problema | Categoría | Severidad | Corrección | Commit |
|---|---|---|---|---|---|---|
| H-01 | registro.py:50 | Base vacía o :memory: pierde datos al cerrar. | Integridad/contrato | Media | Rechazo previo; tres regresiones nuevas. | 100f863 |
| H-02 | .gitignore:6 | Falta plantilla; .env.* la excluiría. | Configuración | Baja | Excepción y ejemplo sin secretos. | 7048e43 |
| H-03 | registro.py:24,47; demo.py:11 | Contratos incompletos; almacenamiento mezclado con registro. | Legibilidad | Baja | Docstrings y helper de persistencia; diff revisado. | 99bc731 |
| H-04 | README.md:71-118 | Faltan ocho secciones y autor/licencia. | Documentación | Baja | Reorganización y comandos probados en copia local limpia. | 3de559a |
| H-05 | requirements-dev.txt:1; entorno | Transitivas sin fijar; pip 25.0.1 con avisos. | Dependencias | Media, desarrollo | Fijar conjunto y pip 26.3; reauditar. | 5a192c8 |
| H-06 | demo.py:12 | Línea extensa, E501. | Estilo | Baja | Dividir ArgumentParser. | 99bc731 |

`registro.py` está en `reportes/`. Ruff pasó de 22 avisos a cero con configuración justificada. Se conservan las veinte pruebas originales y pasan los **25 casos**. La prueba de SQL y la de escritura fallida completan la revisión de abuso sin inventar roles.

### Avisos justificados

| Regla y ubicación | Razón |
|---|---|
| S101 en tests/test_registro.py:29, 32, 50, 51, 54, 74, 75, 84, 85, 86, 99, 102, 117, 132, 149, 165, 180, 193, 194, 195, 210 | Aserciones de pytest. Excepción solo en tests/**; ninguna validación del producto usa assert. |

## 3. Revisión con IA

Prompt: revisar corrección, diseño y seguridad; tabla con línea, severidad y evidencia; separar problemas confirmados de sospechas, sin modificar código. Texto y respuesta en [revisión IA](evidencias/semana6/revision_ia.md) y bitácora S6-01.

| Hallazgo de IA | Clasificación y comprobación |
|---|---|
| IA-01 / H-01 | Real: tres fallos antes del arreglo; 25 casos pasan después. |
| IA-02 / H-02 | Real: árbol Git y check-ignore; plantilla versionada y no ignorada. |
| IA-03 / H-03 | Real: comparación de docstrings con el código y pruebas antes de integrar. |
| IA-04 / H-04 | Real: ocho secciones y ejecución en copia local limpia. |
| IA-05 / H-05 | Real en fijación; la auditoría, no una suposición, determinó los avisos. |

La IA no emitió falsos positivos como hallazgos; descartó las alertas genéricas de conexión sin cierre y roles web inexistentes. **No encontró** los avisos de pip: pip-audit detectó seis IDs únicos en doce entradas del servicio, limitados al entorno de desarrollo. Tras actualizar, entorno y conjunto fijado dieron cero. También se reparó un entorno virtual ligado a un Python retirado, detectado durante la verificación independiente.

La publicación consolida el código ya revisado en `agente/semana6-codigo-revisado` (`99bc731`). Se leyó su diff y pasaron 25 pruebas y Ruff antes de integrar (`914fee7`); evidencia 20. La pausa y retirada del historial provisional se conservan como antecedente en la bitácora.

## 4. Pendientes

| Pendiente | Razón y plan |
|---|---|
| Renovar auditoría al actualizar dependencias | Los avisos cambian; repetir pip-audit antes de otra entrega. |
| Permisos multiusuario y reglas de severidad | Fuera del alcance local; definirlos antes de exponer un servicio o implementar HU-05. |

**Claves expuestas: Ninguna identificada.** La búsqueda por patrones no prueba ausencia de todo secreto posible. Referencias verificadas: [SQLite y bases temporales](https://www.sqlite.org/inmemorydb.html), [Ruff S101](https://docs.astral.sh/ruff/rules/assert/), [pip-audit](https://github.com/pypa/pip-audit).
