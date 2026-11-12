<a href="https://www.orpira.es">
  <img src="assets/banner.svg" width="100%" alt="OrπRa (OrPiRa), Orlando Pineda Raad · Tecnología con visión de negocio · Full Stack, Coordinación IT y Producto Digital">
</a>

<p align="center">
  <a href="https://www.orpira.es"><strong>Portfolio · orpira.es</strong></a>
  &nbsp;·&nbsp;
  <a href="#proyectos">Proyectos</a>
  &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/in/orpira">LinkedIn</a>
</p>

Soy **Orlando Pineda Raad**. En [orpira.es](https://www.orpira.es) cuento qué construyo y para quién; aquí está el código que lo demuestra. Este perfil es una guía para leerlo: qué decisiones tomo y en qué archivo se ven, y los proyectos donde probarlo.

Vengo de coordinar el área de TI de una operación logística, así que programo pensando en quien va a usar la herramienta a diario y en quien tendrá que mantenerla después.

## 3 · Decisiones que se pueden comprobar

Cinco criterios que repito de un proyecto a otro, cada uno con el archivo donde se ve.

- **Las reglas de negocio no dependen de nada.** En Inout, el cálculo de horas extra, festivos y parámetros legales es un paquete TypeScript sin dependencias que comparten el servidor y el cliente: [`packages/core`](https://github.com/Orpira/Inout/tree/main/packages/core/src).
- **Lo que depende de la fecha se prueba en varias zonas horarias.** Inout se desarrolla en España y se usa en Colombia, así que la integración continua ejecuta las pruebas en UTC, Madrid y Bogotá contra un PostgreSQL real: [`ci.yml`](https://github.com/Orpira/Inout/blob/main/.github/workflows/ci.yml).
- **Los datos viven donde menos riesgo corren.** Private Balance guarda todo en el dispositivo, y su esquema local ya va por la versión 37, cada una con su migración: [`db.ts`](https://github.com/Orpira/finance-app/blob/main/src/database/db.ts).
- **El tiempo real sale de la base de datos, no de un servicio aparte.** En Las Delicias, PostgreSQL avisa de cada pedido y un único bus lo reparte al panel del local, al cliente y a las automatizaciones, con cada aviso firmado: [`eventos.js`](https://github.com/Orpira/lasdelicias/blob/main/server/src/eventos.js) y [`firma.js`](https://github.com/Orpira/lasdelicias/blob/main/server/src/firma.js).
- **La IA entra con límites.** En WebWiz, la clave de Claude solo existe en el servidor y las correcciones tienen un tope diario: [`explain-review`](https://github.com/Orpira/test_interactivo-supabase/tree/main/supabase/functions/explain-review).

<a name="proyectos"></a>

## 3.1 · Proyectos

<a href="https://inout.orpira.es/"><img src="assets/proyectos/inout.svg" width="100%" alt="01 · Inout · En línea"></a>

Control horario y liquidación de horas extra para una operación logística con turnos rotativos. El kiosko de fichaje sigue funcionando sin conexión.

`React` `Fastify` `Drizzle ORM` `PostgreSQL` `PWA` `Docker` `Vitest`

**[Abrir la app →](https://inout.orpira.es/)** &nbsp;·&nbsp; [Repositorio](https://github.com/Orpira/Inout) &nbsp;·&nbsp; [Caso de estudio](https://www.orpira.es/casos/inout)

<br>

<a href="https://private-balance.orpira.es/"><img src="assets/proyectos/private-balance.svg" width="100%" alt="02 · Private Balance · Beta"></a>

Gestión financiera personal y profesional que mantiene los datos en el dispositivo. Una sola base de código para web, PWA y Android.

`React` `TypeScript` `Vite` `Tailwind CSS` `Dexie (IndexedDB)` `Capacitor` `Vitest`

**[Abrir la app →](https://private-balance.orpira.es/)** &nbsp;·&nbsp; [Repositorio](https://github.com/Orpira/finance-app) &nbsp;·&nbsp; [Caso de estudio](https://www.orpira.es/casos/private-balance)

<br>

<a href="https://lasdelicias.orpira.es/"><img src="assets/proyectos/las-delicias.svg" width="100%" alt="03 · Las Delicias · Piloto"></a>

Pedidos desde la mesa con QR, encargos para recoger y pantallas en directo para la barra y la cocina de una cafetería panadería.

`React` `TypeScript` `Tailwind CSS` `Fastify` `PostgreSQL` `Zod` `Docker` `n8n`

**[Abrir la app →](https://lasdelicias.orpira.es/)** &nbsp;·&nbsp; [Repositorio](https://github.com/Orpira/lasdelicias) &nbsp;·&nbsp; [Caso de estudio](https://www.orpira.es/casos/las-delicias)

<br>

<a href="https://webwiz.orpira.es/"><img src="assets/proyectos/webwiz.svg" width="100%" alt="04 · WebWiz Quiz · En producción"></a>

Práctica de desarrollo web con retos de código, incidencias reales para depurar y laboratorios de SQL y Git.

`React` `TypeScript` `Supabase` `Claude API` `Capacitor` `Playwright`

**[Abrir la app →](https://webwiz.orpira.es/)** &nbsp;·&nbsp; [Repositorio](https://github.com/Orpira/test_interactivo-supabase) &nbsp;·&nbsp; [Caso de estudio](https://www.orpira.es/casos/webwiz)

<br>

<a href="https://suite-juegos.orpira.es/juegos"><img src="assets/proyectos/juegos.svg" width="100%" alt="05 · Dominó 3D y suite de juegos · En producción"></a>

Cinco juegos multijugador para el navegador, con salas con código, turnos y ranking. El Dominó 3D, a cuatro jugadores contra bots o en línea, es el más ambicioso.

`Next.js` `TypeScript` `Supabase` `Three.js`

**[Jugar al Dominó 3D →](https://domino-3d.orpira.es/)** &nbsp;·&nbsp; [Suite de juegos](https://suite-juegos.orpira.es/juegos) &nbsp;·&nbsp; [Repositorio de la suite](https://github.com/Orpira/Cleta-s-stop) &nbsp;·&nbsp; [Caso de estudio](https://www.orpira.es/casos/juegos)

<br>

<a href="https://www.orpira.es/casos/seguimiento-empleabilidad"><img src="assets/proyectos/empleabilidad.svg" width="100%" alt="06 · Seguimiento de empleabilidad · MVP"></a>

Sustituye los Excel con los que una entidad de empleo sigue las candidaturas de sus aspirantes, e importa los antiguos.

`Next.js` `TypeScript` `Supabase` `PostgreSQL` `ExcelJS`

**[Caso de estudio →](https://www.orpira.es/casos/seguimiento-empleabilidad)** &nbsp;·&nbsp; [Demo con acceso por invitación](https://laboratorio.orpira.es/) &nbsp;·&nbsp; código privado

<br>

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
- **LinkedIn:** [linkedin.com/in/orpira](https://www.linkedin.com/in/orpira)
- **GitHub:** [github.com/Orpira](https://github.com/Orpira)

<p align="center">
  <br>
  <img src="assets/cubo-orpira.webp" width="56" alt="Cubo OrPiRa"><br>
  <sub>OrPiRa · Tecnología con visión de negocio · Bilbao<br>Las secciones se numeran con los decimales de π.</sub>
</p>
