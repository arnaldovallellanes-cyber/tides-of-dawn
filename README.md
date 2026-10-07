# Pokémon: Tides of Dawn / Mareas del Alba

ROM hack de Pokémon Emerald para Game Boy Advance. Proyecto C/decomp sobre
`rh-hideout/pokeemerald-expansion`, tag `expansion/1.17.1`, commit
`bb1093a7c72d3961d9a37d8e02ad2abc2c866682`.

## Estado actual

Esta rama inicia la reconstrucción moderna desde source. La migración de Auralia
todavía no se ha recibido. El primer build mantiene el mundo y la historia de
Emerald como base de prueba; no es todavía la demo de Auralia hasta Naira.
Alpha 0.3.1 queda como referencia histórica, sin binary patching.

La selección inicial se modifica desde C para Treecko, Chimchar, Froakie, Riolu,
Zorua y Charcadet. Zorua permite Unova/Hisui. Charcadet recibe como objeto equipado
la Auspicious Armor o Malicious Armor real; se puede mover a la mochila. No se
modifica la estructura del guardado para estas elecciones. Los eventos de los
cuatro combates del rival de la base cubren las siete variantes, para evitar que
Riolu, Zorua o Charcadet dejen bloqueado el progreso provisional de Emerald.

Las dos habilidades simultáneas no están implementadas. Requieren trabajo real
en el battle engine y pruebas de interacciones.

## Compilar

GitHub Actions importa la base fijada en el primer build, conserva el historial
upstream como segundo padre y publica el source completo en `main` sin force-push.
La importación excluye los workflows upstream y conserva los archivos propios.
Después instala ARM GCC/binutils, newlib y libpng y compila Emerald.

El artifact se llama `Tides_of_Dawn_Modern_Alpha` y contiene:

- `Tides_of_Dawn_Modern_Alpha.gba`
- El ELF y el mapa del linker, para depuración.
- `build-manifest.json` y SHA-256 de la ROM.

Para preparar y compilar localmente (requiere git, red y el toolchain ARM):

```sh
python3 tools/tides/bootstrap_source.py
python3 tools/tides/validate_source.py
python3 -m unittest discover -s test/tides
python3 tools/tides/validate_warps.py
make -j2 FILE_NAME=Tides_of_Dawn_Modern_Alpha TITLE="TIDES DAWN" COMPARE=0
python3 tools/tides/validate_rom.py Tides_of_Dawn_Modern_Alpha.gba
```

Consultar `INSTALL.md` del upstream para instalar el toolchain. El primer comando
crea un commit local de importación; Actions usa `--publish` solamente en `main`.
El validador de source exige los archivos del motor y que el commit fijado sea
ancestro de la rama. Las pruebas locales incluyen compilar las funciones reales
de resolución de starters con GCC del host; eso no compila todavía la ROM GBA.

## Migración y pruebas pendientes

El plan y las reglas están en `docs/tides-of-dawn/migration.md`. El contrato de
warps está en `docs/tides-of-dawn/warp-contract.json`. CI valida destinos e índices
estáticos y exige los retornos de Auralia cuando aparezca cualquiera de sus mapas.
No sustituye las pruebas de arranque, guardado/carga y recorrido en emulador.

Este repositorio conserva la atribución y documentación del upstream. Sus
instrucciones de instalación y compilación siguen siendo aplicables.
