# rtex — el reel de «N piezas» de INEMA

[![rtex](capa/capa.png)](https://inematds.github.io/rtex/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

rtex es el motor que Nei usa para hacer reels (videos cortos verticales) de INEMA con su propio rostro: su avatar de HeyGen dice el guion y el motor dibuja encima las pantallas, los subtítulos palabra por palabra y la tarjeta final. Cada video sigue un formato fijo de «N piezas», desde el cuadro de apertura con la tesis hasta el pedido «comenta PALABRA» (comenta PALABRA). Un validador, un crítico automático y un QA revisan el formato antes de publicar. El código es abierto para estudiar y adaptar; para generar tu propio video, necesitas tu propio avatar en HeyGen, además de Python, Node, ffmpeg y Whisper.

## 📖 Guía de uso

Guía completa (landing + paso a paso + qué cambia respecto a r7ex): **https://inematds.github.io/rtex/guia/es/** · video de ejemplo: https://www.youtube.com/watch?v=vLOgLCVs7gg

**rtex = lo que INEMA ya tiene (motor r7ex v1.1.0) + el estándar rtex de guion y pantalla.**
Un reel vertical (9:16, 60–90 s) con el avatar real de Nei hablando en primera persona: la tesis escrita en el cuadro 0, una prueba social
con número y fuente, «N piezas» anunciadas con índice, el método numerado, una prueba con fuente, la salvedad honesta, la máxima en
antítesis después de un silencio y el cierre «comenta PALABRA» (comenta PALABRA) con la tarjeta sostenida. Objetivo: llevar gente a inema.club.

Versión **1.0.0** (28/10/2026). Repo: `inematds/rtex`.

---

## El proceso, de principio a fin

🧠 = sesión con Nei (consume tokens) · ⚙️ = script (cero tokens) · 🤖 = `claude -p` breve con la suscripción (nunca API)

| # | Paso | Comando / qué sucede | Quién |
|---|---|---|---|
| 1 | Pedido | Nei dice el tema (o los temas), la página de inema.club y el canal | Nei |
| 2 | Investigación y fuentes | verificar cada número en la fuente (estrellas de GitHub del día, artículo con fecha) y anotarlo en `fontes[]` con `valor` y `verificado_em` | 🧠 |
| 3 | Guion | `python3 rtex.py novo <slug>` y escribir `roteiro.json`: los bloques del estándar (abajo), el texto completo de lo que se dice, el objeto de cada bloque, el gancho | 🧠 |
| 4 | Validador | `python3 rtex.py checar <pasta>`: orden de los bloques, índice = método, texto sin cifras ni "!", ≥ 8 palabras por bloque, palabras clave en el texto, fuente para cada número, gancho = tesis planteada en el cuadro 0, duración estimada de 60–90 s | ⚙️ |
| 5 | Crítico | `python3 rtex.py critico <pasta>` (`prompts/critico.md`): puntuación por bloque + bloqueos; pasa sin bloqueos, tesis ≥ 8, promedio ≥ 7,5, ninguno < 6 | 🤖 |
| 6 | OK del avatar | `avatar/APROVADO_HEYGEN` con la frase de Nei para ESTA producción (un avatar por reel) | 🧠 |
| 7 | Estudio | `python3 rtex.py avatar-enviar <pasta>`: el texto se envía al estudio de HeyGen (suscripción, pantalla `:99`), guarda `avatar/video_id.txt` | ⚙️ |
| 8 | Capturas | capturas reales de las páginas de GitHub (`ferramentas/print.mjs`) y logotipos; LEER las capturas | ⚙️ |
| 9 | Previsualización sin avatar (opcional) | en una copia de la carpeta: `python3 ferramentas/tempos_sinteticos.py <cópia>` + `rtex.py cena` + `node motor/render.mjs <cópia> --quadros 1,10,20` — encuentra errores de diseño antes de HeyGen | ⚙️ |
| 10 | Avatar y ritmo | `python3 rtex.py avatar-conferir <pasta>` (lectura) hasta `pronto`; `python3 rtex.py avatar <pasta>`: tiempo de cada palabra (Whisper), voz extendida hasta ~182 palabras/min (máx. 12%), silencio antes de la máxima, tarjeta de 9 s. **De minutos a horas** — las esperas largas van al vigilante `continua` | ⚙️ |
| 11 | Escena y render | `python3 rtex.py cena <pasta>` + `python3 rtex.py render <pasta>`: escenario (`motor/palco.html`) a 30 fps + avatar en el tercio inferior + pista, −14 LUFS en 2 pasadas | ⚙️ |
| 12 | QA | `python3 rtex.py qa <pasta>` → `build/qa.json` + `build/folha.jpg` (16 cuadros); LEER la hoja | ⚙️ |
| 13 | Revisor independiente | `Agent` general-purpose nuevo (nunca fork) o `claude -p` con `~/.claude/runbooks/revisor-independente.md`: lee solo la hoja + `qa.json` + este README; puntuación en `~/projetos/wifi/scripts/revisor-nota.py` | 🤖 |
| 14 | Entregar | `python3 rtex.py enviar <pasta>` (bot v3) y `python3 rtex.py fila <pasta>` (cola con temporizador de r7ex, canal en `publicar.fila`) | ⚙️ |
| 15 | El gancho | Nei responde a quien comentó la palabra con el entregable (o el comentario fijado de `publicar.comentario_fixado`); sin automatización de DM (sería API: necesita autorización) | Nei |

Atajo: `python3 rtex.py fazer <pasta>` = pasos 4, 8, 10, 11 y 12 en secuencia.

---

## Decisiones (28/10/2026)

- **Paleta INEMA:** fondo `#0c0c10`, tarjeta `#16161e` con borde `#272730`, texto `#e9e9ee`/`#9a9aa6`. Títulos **Sora**, cuerpo **Inter**,
  etiquetas/fuente/índice **JetBrains Mono**, subtítulos Montserrat Black con contorno negro. **Amarillo `#FACC15` racionado:** como letra
  (palabra clave, elemento activo, título destacado) y **una sola superficie amarilla sólida en todo el video: la píldora de la palabra-gancho**.
  El QA lo cuenta (`background:` amarillo en el escenario = 1). Verde `#2bff88` solo para ✓, rojo `#ff2a1f` solo para ✗/error, `#F2B45C` en la salvedad,
  azul `#38bdf8` solo en la píldora de inema.club.
- **Presentador:** el avatar real de Nei en HeyGen, desde el estudio (suscripción), como en r7ex; no es una ilustración. Se queda en el **tercio inferior**
  (1080×640 en y 1280) durante todo el reel; los 2/3 superiores son para el contenido (como la D17 del kit para reels 9:16).
- **Estructura (el estándar rtex), en lugar de las 7 etapas de r7ex:**
  1. `tese` — escrita en el cuadro 0 (≤ 9 palabras, la palabra-gancho destacada), algo se mueve en el primer segundo;
  2. `autoridade` — prueba social con número y fuente en pantalla (contador que **llega** al valor de la fuente);
  3. `problema` — el dolor con un objeto (p. ej., un chat tachado);
  4. `virada` — se anuncian «N piezas»; el índice 01–N aparece antes del primer elemento y se convierte en píldoras en la parte superior hasta la máxima;
  5. `metodo` — los elementos numerados (30–60% del tiempo), un objeto por elemento, etiqueta "0N / NOMBRE";
  6. `prova` — un dato con fuente que lo confirma;
  7. `ressalva` — limitaciones honestas dichas en voz alta, legibles (≥ 40 px), convertidas en instrucciones;
  8. `maxima` — antítesis breve, con ~0,6–0,75 s de silencio antes (desaparecen la voz y la pista);
  9. `cta` — «comenta PALABRA» (comenta PALABRA): la palabra es la tesis, planteada en el cuadro 0; la tarjeta permanece 9 s después de la última palabra con el gesto de comentar actuado; **el entregable está detrás de la palabra** (no se dicta en el video) y debe existir ese día — nunca prometer algo que no existe.
- **Se conserva de r7ex:** avatar desde el estudio, subtítulos karaoke, paneles al ritmo de la voz, ritmo (`rtex/ritmo.py`), Whisper/ajuste de tiempos,
  crítico 🤖 + revisor independiente, cola con temporizador y envío al v3.
- **Ritmo y sonido:** voz a 160–190 palabras/min, −14 LUFS (TP ≤ −1,5), cambio visual ≥ 17/min (medido por los eventos de la escena; la escala de
  luminancia a 1 fps va en el QA como información, porque el fundido subcuenta).
- **Ética:** los números solo con fuente consultada ese día; la voz no exagera lo que dice la pantalla; «gratis» solo si lo indica la página; la salvedad va antes de la máxima.

## Qué contiene

| Archivo | Qué hace |
|---|---|
| `rtex.py` | la línea de comandos (validador, crítico, estudio, capturas, escena, render, QA, envío, cola) |
| `modelo/roteiro.json` | guion de ejemplo (la primera edición): el formato de `roteiro.json` |
| `rtex/cena.py` | guion + tiempos de las palabras → `cena.js` (cada palabra clave se convierte en un instante; lista de eventos para el QA) |
| `motor/palco.html` | la composición: componentes `tese`, `contador`, `chat_riscado`, `indice` (+ píldoras de progreso), `pasta`, `repo` (captura real + estrellas), `manchete`, `selo_prova`, `ressalva`, `maxima` (flash tipográfico), `isca` (píldora amarilla) y el cuadro de comentario |
| `motor/render.mjs` | graba el escenario a 30 fps (Playwright, pantalla `:99`) |
| `motor/mix.sh` | avatar en el tercio inferior + pista con ducking + loudness en 2 pasadas |
| `rtex/qa.py` | mediciones y hoja de revisión |
| `rtex/ritmo.py`, `retempo.py`, `whisper.py`, `pecas.py`, `heygen/` | copias de r7ex v1.1.0 (ritmo de la voz, tiempos, transcripción, capturas/logotipos, estudio de HeyGen) |
| `ferramentas/print.mjs` | captura de página con Playwright |
| `ferramentas/tempos_sinteticos.py` | previsualización del escenario sin avatar |
| `prompts/critico.md` | solicitud para el crítico de viralidad |

## Pendientes

- **Comando `/rtex` de inemaccbot:** hoy es un alias de `/r7ex` y ya cuenta como OK del avatar. **No se modificó.** Redirigirlo a este motor
  (o crear otro comando) solo cuando Nei lo sepa.
- Registrar las decisiones de rtex en el kit `inema-design` (`DECISOES.md`/`HISTORICO.md`) — el orquestador decide el número (D18 ya está duplicado allí).
- Producción sin sesión (temporizador como `producao/` de r7ex) y skill `/rtex`.
- El modo largo (110–135 s), la skin clara (`papel`) y la composición en HyperFrames quedan para la v2.
- Entrega automática del gancho (DM por palabra) solo con autorización para usar la API.

## Licencia
MIT.