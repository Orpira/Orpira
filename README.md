<a href="https://www.orpira.es">
  <img src="assets/banner.svg" width="100%" alt="OrπRa (OrPiRa), Orlando Pineda Raad · Tecnología con visión de negocio · Full Stack, Coordinación IT y Producto Digital">
</a>

<p align="center">
  <a href="https://www.orpira.es"><strong>Portfolio · orpira.es</strong></a>
  &nbsp;·&nbsp;
  <a href="#proyectos">Proyectos</a>
  &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/in/orlando-pineda-raad-273402257">LinkedIn</a>
</p>

Soy **Orlando Pineda Raad**. En [orpira.es](https://www.orpira.es) cuento qué construyo y para quién; aquí está el código que lo demuestra. Este perfil es una guía para leerlo: qué decisiones tomo, en qué archivo se ven y por dónde conviene empezar en cada repositorio.

Vengo de coordinar el área de TI de una operación logística, así que programo pensando en quien va a usar la herramienta a diario y en quien tendrá que mantenerla después.

## 3 · Decisiones que se pueden comprobar

Cinco criterios que repito de un proyecto a otro, cada uno con el archivo donde se ve.

- **Las reglas de negocio no dependen de nada.** En Inout, el cálculo de horas extra, festivos y parámetros legales es un paquete TypeScript sin dependencias que comparten el servidor y el cliente: [`packages/core`](https://github.com/Orpira/Inout/tree/main/packages/core/src).
- **Lo que depende de la fecha se prueba en varias zonas horarias.** Inout se desarrolla en España y se usa en Colombia, así que la integración continua ejecuta las pruebas en UTC, Madrid y Bogotá contra un PostgreSQL real: [`ci.yml`](https://github.com/Orpira/Inout/blob/main/.github/workflows/ci.yml).
- **Los datos viven donde menos riesgo corren.** Private Balance guarda todo en el dispositivo, y su esquema local ya va por la versión 37, cada una con su migración: [`db.ts`](https://github.com/Orpira/finance-app/blob/main/src/database/db.ts).
- **El tiempo real sale de la base de datos, no de un servicio aparte.** En Las Delicias, PostgreSQL avisa de cada pedido y un único bus lo reparte al panel del local, al cliente y a las automatizaciones, con cada aviso firmado: [`eventos.js`](https://github.com/Orpira/lasdelicias/blob/main/server/src/eventos.js) y [`firma.js`](https://github.com/Orpira/lasdelicias/blob/main/server/src/firma.js).
- **La IA entra con límites.** En WebWiz, la clave de Claude solo existe en el servidor y las correcciones tienen un tope diario: [`explain-review`](https://github.com/Orpira/test_interactivo-supabase/tree/main/supabase/functions/explain-review).

<a name="proyectos"></a>

## 3.1 · Proyectos, y por qué archivo empezar

### Inout · `En línea`

Control horario y liquidación de horas extra para una operación logística con turnos rotativos. El kiosko de fichaje sigue funcionando sin conexión.

- **Empieza por:** [`liquidacion.ts`](https://github.com/Orpira/Inout/blob/main/packages/core/src/liquidacion.ts), el motor que liquida minuto a minuto, y [`reglas-liquidacion.md`](https://github.com/Orpira/Inout/blob/main/docs/reglas-liquidacion.md), que explica las reglas en lenguaje de negocio.
- **Stack:** React · Fastify · Drizzle ORM · PostgreSQL · PWA · Docker · Vitest
- [Abrir la app](https://inout.orpira.es/) · [Repositorio](https://github.com/Orpira/Inout)

### Private Balance · `Beta`

Gestión financiera personal y profesional que mantiene los datos en el dispositivo. Una sola base de código para web, PWA y Android.

- **Empieza por:** [`docs/`](https://github.com/Orpira/finance-app/tree/main/docs), la arquitectura documentada decisión a decisión, y [`test/`](https://github.com/Orpira/finance-app/tree/main/test), con más de 200 archivos de pruebas.
- **Stack:** React · TypeScript · Vite · Tailwind CSS · Dexie (IndexedDB) · Capacitor · Vitest
- [Abrir la app](https://private-balance.orpira.es/) · [Repositorio](https://github.com/Orpira/finance-app) · [Caso de estudio](https://www.orpira.es/casos/private-balance)

### Las Delicias · `Piloto`

Pedidos desde la mesa con QR, encargos para recoger y pantallas en directo para la barra y la cocina de una cafetería panadería.

- **Empieza por:** [`server/migrations/`](https://github.com/Orpira/lasdelicias/tree/main/server/migrations), trece migraciones SQL que cuentan cómo creció el producto: del esquema inicial a las cuentas, los cierres diarios y la idempotencia.
- **Stack:** React · TypeScript · Tailwind CSS · Fastify · PostgreSQL · Zod · Docker · n8n
- [Abrir la app](https://lasdelicias.orpira.es/) · [Repositorio](https://github.com/Orpira/lasdelicias) · [Caso de estudio](https://www.orpira.es/casos/las-delicias)

### WebWiz Quiz · `En producción`

Práctica de desarrollo web con retos de código, incidencias reales para depurar y laboratorios de SQL y Git.

- **Empieza por:** [`sql/engine.ts`](https://github.com/Orpira/test_interactivo-supabase/blob/main/src/features/sql/engine.ts), un PostgreSQL que se ejecuta dentro del navegador para los ejercicios de SQL, y [`learning/fsrs.ts`](https://github.com/Orpira/test_interactivo-supabase/blob/main/src/features/learning/fsrs.ts), el repaso espaciado.
- **Stack:** React · TypeScript · Supabase · Claude API · Capacitor · Playwright
- [Abrir la app](https://webwiz.orpira.es/) · [Repositorio](https://github.com/Orpira/test_interactivo-supabase) · [Caso de estudio](https://www.orpira.es/casos/webwiz)

### Dominó 3D y suite de juegos · `En producción`

Cinco juegos multijugador para el navegador, con salas con código, turnos y ranking. El Dominó 3D, a cuatro jugadores contra bots o en línea, es el más ambicioso.

- **Empieza por:** [`lib/core`](https://github.com/Orpira/Cleta-s-stop/tree/main/lib/core), las salas y la puntuación que comparten los juegos, y [`lib/games`](https://github.com/Orpira/Cleta-s-stop/tree/main/lib/games), con un módulo por juego. El código del Dominó 3D no es público.
- **Stack:** Next.js · TypeScript · Supabase · Three.js
- [Jugar al Dominó 3D](https://domino-3d.orpira.es/) · [Suite de juegos](https://suite-juegos.orpira.es/juegos) · [Repositorio de la suite](https://github.com/Orpira/Cleta-s-stop) · [Caso de estudio](https://www.orpira.es/casos/juegos)

### Seguimiento de empleabilidad · `MVP`

Sustituye los Excel con los que una entidad de empleo sigue las candidaturas de sus aspirantes, e importa los antiguos.

- **Stack:** Next.js · Supabase · ExcelJS
- [Demo con acceso por invitación](https://laboratorio.orpira.es/) · código privado

**También:** [PRL Master](https://www.orpira.es/casos/prl-master) ([repositorio](https://github.com/Orpira/test_interactivo-prl)) y el [portfolio](https://github.com/Orpira/orpira-portfolio), hecho con Astro y Tailwind CSS.

## 3.14 · Stack en uso

Solo lo que está en el código de los repositorios anteriores.

| Categoría | Tecnologías |
| --- | --- |
| **Frontend** | React · TypeScript · Vite · Tailwind CSS · Next.js · Astro |
| **Backend** | Node.js · Fastify · Zod |
| **Bases de datos** | PostgreSQL · Supabase · Drizzle ORM · IndexedDB (Dexie) |
| **Aplicaciones móviles** | PWA sin conexión · Capacitor (Android) |
| **Infraestructura y DevOps** | Docker · Vercel · GitHub Actions · n8n |
| **Testing y herramientas** | Vitest · Playwright · Testing Library · ESLint · Lefthook |
| **IA aplicada** | Claude API · OpenAI API |

## 3.141 · Qué rastro deja cada fase

**Análisis → Arquitectura → Desarrollo → Validación → Entrega**

Cada fase deja algo en el repositorio que se puede abrir.

| Fase | Qué queda en el repositorio |
| --- | --- |
| **Análisis** | Las reglas escritas en lenguaje de negocio antes que en código, como [las de liquidación de Inout](https://github.com/Orpira/Inout/blob/main/docs/reglas-liquidacion.md). |
| **Arquitectura** | Documentos de decisión numerados, como los de [Private Balance](https://github.com/Orpira/finance-app/tree/main/docs). |
| **Desarrollo** | Migraciones versionadas que permiten reconstruir el producto paso a paso, como las de [Las Delicias](https://github.com/Orpira/lasdelicias/tree/main/server/migrations). |
| **Validación** | Comprobación de tipos y pruebas antes de cada subida y en cada cambio, con [Lefthook](https://github.com/Orpira/finance-app/blob/main/lefthook.yml) y GitHub Actions. |
| **Entrega** | Cada proyecto tiene una dirección pública donde probarlo. |

## 3.1415 · Contacto

- **Portfolio:** [www.orpira.es](https://www.orpira.es)
- **LinkedIn:** [orlando-pineda-raad](https://www.linkedin.com/in/orlando-pineda-raad-273402257)
- **GitHub:** [github.com/Orpira](https://github.com/Orpira)

<p align="center">
  <br>
  <img src="assets/cubo-orpira.webp" width="56" alt="Cubo OrPiRa"><br>
  <sub>OrPiRa · Tecnología con visión de negocio · Bilbao<br>Las secciones se numeran con los decimales de π.</sub>
</p>
