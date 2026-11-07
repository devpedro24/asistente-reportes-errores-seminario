# Guía para explicar el incremento

Esta guía ayuda a recorrer el código entregado. Conviene ejecutar la demostración y las pruebas antes de la exposición.

## Modelo y función principal

`Reporte` es una dataclass con cuatro campos tipados. `frozen=True` impide cambiar sus atributos por asignación después de crearla. Representa la salida confirmada, no una conexión a SQLite ni un modelo de IA.

`registrar_reporte` recibe la ruta de la base, la descripción, una fecha y la operación afectada. El orden del trabajo es validar, guardar y devolver los datos confirmados.

La validación revisa los tipos antes de aplicar `strip()`, para no convertir números o valores nulos a texto silenciosamente. La fecha usa `type(fecha) is date` porque `datetime` también hereda de `date`, pero el contrato admite solo una fecha sin hora. Se limpia únicamente el espacio exterior; los espacios interiores se conservan.

`sqlite3.connect` abre el archivo local. `CREATE TABLE IF NOT EXISTS` permite usar la misma función en una base nueva y en las siguientes llamadas. La clave `INTEGER PRIMARY KEY AUTOINCREMENT` la administra SQLite; el programa no cuenta los registros para adivinar la próxima clave.

`INSERT ... VALUES (?, ?, ?)` separa el comando SQL de sus datos. El apóstrofo de un nombre o un texto parecido a SQL se almacena como texto, sin concatenarlo al comando. `fecha.isoformat()` guarda la fecha como `AAAA-MM-DD`.

El bloque `with conexion` confirma si termina correctamente y revierte una escritura si se propaga una excepción. Por sí solo no cierra la conexión: `finally` la cierra incluso ante un error. La salida se construye después del bloque transaccional; no se devuelve un reporte antes de confirmar la escritura.

`cursor.lastrowid` obtiene la clave de esa inserción. `:03d` agrega ceros a la izquierda hasta completar tres dígitos y no trunca números mayores. La fecha devuelta conserva el tipo `date` del contrato.

## Refactor

La primera versión tenía la validación dentro de la función principal. El refactor extrae esa responsabilidad a un helper privado, con la misma secuencia de comprobaciones y mensajes. No cambia la firma ni las reglas. El archivo de pruebas tiene el mismo contenido en rojo, verde y después del refactor; las 20 pruebas pasan en las dos últimas etapas.

## Pruebas y datos

Las pruebas crean archivos bajo `tmp_path`, independientes del archivo de la demostración. Comprueban tanto el objeto devuelto como el contenido almacenado mediante una conexión nueva. Por eso pueden detectar una solución que devuelve datos correctos, pero no los conserva.

Se prueban el ejemplo original de REP-001 y el error original «Falta la descripción». Las reglas adicionales de espacios, tipos y operación requerida se identifican como decisiones técnicas del contrato, no como citas del cliente.

La alternativa de lista en memoria se evaluó deliberadamente y se rechazó al perder los reportes al comenzar otro proceso. No forma parte de la implementación entregada y su resultado rojo se conserva como evidencia de esa comparación.

## Límites de esta entrega

No se implementa todavía la clasificación de severidad. El siguiente incremento puede usar los reportes como entrada para HU-05, con las reglas de clasificación validadas. Tampoco se afirma haber realizado una nueva entrevista ni desplegado el programa en producción.
