# Reconstrucción moderna de Auralia

Base obligatoria: Expansion 1.17.1, `bb1093a7c72d3961d9a37d8e02ad2abc2c866682`.
La región se inspira en Puerto Rico y el Caribe. Dirección visual: HGSS y
Emerald Seaglass adaptados a pixel art GBA. Spanglish puertorriqueño natural.

## Integración pendiente del paquete de migración

1. Revisar qué archivos son source y sus dependencias sobre la antigua Expansion.
2. Importar mapas, layouts, tilesets, scripts y entrenadores al formato de 1.17.1.
3. Recorrido: Pueblo Almendro, Ruta del Mangle, Puerto Brisa, Faro de Sal,
   Villa Mangle y Gym de Naira. Terminar la demo después de su primera medalla.
4. Toda casa con retorno estático es exclusiva de su ciudad. Debe existir
   `PuertoBrisa -> HarborHouse -> PuertoBrisa`. Prohibido enlazar PuertoBrisa
   con AlmendroHome. Registrar otros interiores en `warp-contract.json`.
5. Variedad de sprites de NPC y diálogos individuales; evitar repetir personajes.
6. Integrar los starters de Ceiba en el evento migrado. La base provisional
   sigue usando la escena de la mochila de Birch hasta recibir esos scripts.
   Zorua Hisui se guarda como especie real; Charcadet y sus armaduras usan las
   constantes oficiales. Revisar rivales, entregas y estado persistente al migrar.

## Historia y sistemas

Siete faros históricos forman la Ruta de las Luces. Sus cámaras amplifican
señales entre Pokémon. Las anomalías y el grupo antagonista surgen de ese
conflicto. Personajes: Profesora Ceiba, Darío, Mara, Nexo y Naira.

Pendientes: DexNav por especie/ruta, descripciones de habilidades, Mission Log,
Remote PC, Nautical Chart, Emergency Kit (tres curaciones completas), Move
Relearner ($1,000), Egg Move Tutor ($3,000), level caps, repel reutilizable,
followers y día/noche. Mega Evolution se integra después.

Dos habilidades activas: diseñar su representación persistente y resolución
real en el motor moderno. Revisar entradas al campo, ataques, inmunidades,
supresión/cambio/copia de habilidades, orden de efectos, dobles y mensajes.
No marcar como implementado por mostrar dos nombres en UI.

## Aceptación en emulador (pendiente)

- Arranque hasta la pantalla de título y nueva partida.
- Probar cada uno de los seis starters; confirmar y cancelar sus menús.
- Probar Unovan/Hisuian Zorua y ambas armaduras de Charcadet.
- Guardar, cerrar el emulador, abrir la ROM y cargar. Verificar especie y objeto.
- Entrar/salir de todas las casas, incluidos pisos; repetir tras guardar/cargar.
- Confirmar PuertoBrisa -> HarborHouse -> PuertoBrisa en ambas direcciones.
- Recorrer toda la demo, vencer a Naira y recibir exactamente la primera medalla.

Una compilación y un encabezado GBA válido no certifican estas comprobaciones.
