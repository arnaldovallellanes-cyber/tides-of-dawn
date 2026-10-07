# Estado verificable de esta entrega

- Tag y commit upstream comprobados mediante la API de GitHub.
- Bootstrap y cambios de starters escritos en source local.
- Once pruebas automatizadas pasaron: importación, regresiones de warps,
  cobertura de los eventos del rival y resolución de las siete variantes de starters.
- Las funciones C reales de lookup se compilaron con GCC del host y se ejecutaron
  con comprobación de comportamiento indefinido. Incluye elecciones inválidas.
- El workflow exige source completo y ascendencia desde el commit fijado.
- El validador rechazó correctamente este bootstrap incompleto; aún no contiene
  la base del motor ni su historial upstream y no debe producir un artifact GBA.
- Workflow YAML comprobado sintácticamente.
- Repo remoto sin inicializar: GitHub devolvió 403, "Resource not accessible by integration".
- La conexión GitHub no tiene instalaciones autorizadas (lista vacía).
- Descarga git local bloqueada por conexión fallida al proxy del entorno.
- Toolchain ARM y emulador no disponibles localmente.
- No se compiló ni produjo una ROM .gba en esta entrega.
- No se ejecutó GitHub Actions ni se generó un artifact remoto.
- Boot y guardar/cargar no se probaron.
- Paquete de migración aún no recibido: mapas de Auralia y correcciones reales pendientes.

Al habilitar escritura en GitHub se puede publicar este commit inicial y ejecutar
el workflow. Su primer run importa el source fijado a la raíz y continúa la
compilación. No se reutiliza ni modifica una ROM anterior.
