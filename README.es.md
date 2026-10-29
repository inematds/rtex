# rtex — el reel de «N piezas» de INEMA

[![rtex](capa/capa.png)](https://inematds.github.io/rtex/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

rtex es el motor que Nei usa para hacer reels (videos cortos verticales) de INEMA con su propio rostro: su avatar de HeyGen dice el guion, y el motor dibuja encima las pantallas, los subtítulos palabra por palabra y la tarjeta final. Cada video trata un solo tema, con un formato fijo: un gancho fuerte en el cuadro de apertura, los pasos del método en «N piezas» y, al final, una pregunta de opinión para que el público responda en los comentarios. Un validador, un crítico automático y un QA comprueban el formato antes de publicar. El código es abierto para estudiar y adaptar; para generar tu video, necesitas tu propio avatar en HeyGen, además de Python, Node, ffmpeg y Whisper.

## 📖 Guía de uso

Guía completa (landing + paso a paso + qué cambia con respecto a r7ex): **https://inematds.github.io/rtex/guia/es/** · video de ejemplo (formato v1.0.0, antes del anzuelo de opinión): https://www.youtube.com/watch?v=vLOgLCVs7gg

**rtex = lo que INEMA ya tiene (motor r7ex v1.1.0) + el estándar rtex de guion y pantalla.**
Un reel vertical (9:16, 60–90 s), un tema por video, con el avatar real de Nei hablando en primera persona: el gancho en el cuadro 0
(titular corto y agresivo + un objeto que se rompe), una prueba con fuente o autoridad antes de los 20 s, el problema de quien mira
(con «não é culpa sua» («no es culpa tuya»)), «N piezas» (los pasos del método) con índice, una prueba con fuente, la salvedad honesta, la máxima en
antítesis después de un silencio y el cierre con una **pregunta de opinión** y la tarjeta sostenida. Objetivo: llevar gente a inema.club.

Versión **1.1.0** (28/10/2026). Repo: `inematds/rtex`.

---

## El proceso, de principio a fin

🧠 = sesión con Nei (consume tokens) · ⚙️ = script (cero tokens) · 🤖 = `claude -p` corto con la suscripción (nunca API)

| # | Paso | Comando / qué sucede | Quién |
|---|---|---|---|
| 1 | Pedido | Nei dice el tema (o los temas), la página de inema.club y el canal | Nei |
| 2 | Investigación y fuentes | comprobar cada número en la fuente (estrellas de GitHub ese día, artículo con fecha) y anotarlo en `fontes[]` con `valor` y `verificado_em` | 🧠 |
| 3 | Guion | `python3 rtex.py novo <slug>` y escribir `roteiro.json`: un tema, el `gancho`, los bloques del estándar (abajo), el texto completo, el objeto de cada bloque, el `isca` de opinión | 🧠 |
| 4 | Validador | `python3 rtex.py checar <pasta>`: gancho (tipo, titular ≤ 6 palabras en mayúsculas con 1 palabra amarilla, sin lista/«¿sabías que?»/«yo hice», objeto-metáfora), prueba ≤ 20 s, problema con absolución justo después, un tema (método sin 3+ fuentes diferentes), orden de los bloques, índice = método, texto sin cifras ni «!», ≥ 8 palabras por bloque, desencadenantes en el texto, fuente para cada número, anzuelo de opinión (abajo), duración estimada de 60–90 s | ⚙️ |
| 5 | Crítico | `python3 rtex.py critico <pasta>` (`prompts/critico.md`): nota por bloque + bloqueos; pasa sin bloqueos, tesis ≥ 8, promedio ≥ 7,5, ninguno < 6 | 🤖 |
| 6 | OK del avatar | `avatar/APROVADO_HEYGEN` con la frase de Nei para ESTA producción (un avatar por reel) | 🧠 |
| 7 | Estudio | `python3 rtex.py avatar-enviar <pasta>`: el texto va al estudio de HeyGen (suscripción, pantalla `:99`), graba `avatar/video_id.txt` | ⚙️ |
| 8 | Capturas | `python3 rtex.py prints <pasta>`: capturas reales de las páginas de GitHub (`ferramentas/print.mjs`) y logos; LEER las capturas | ⚙️ |
| 9 | Vista previa sin avatar (opcional) | en una copia de la carpeta: `python3 ferramentas/tempos_sinteticos.py <cópia>` + `rtex.py cena` + `node motor/render.mjs <cópia> --quadros 1,10,20` — detecta errores de diseño antes de HeyGen | ⚙️ |
| 10 | Avatar y ritmo | `python3 rtex.py avatar-conferir <pasta>` (lectura) hasta que esté `pronto`; `python3 rtex.py avatar <pasta>`: tiempo de cada palabra (Whisper), habla estirada hasta ~182 palabras/min (máx. 12%), silencio antes de la máxima, 9 s de tarjeta. **De minutos a horas** — la espera larga va al vigilante `continua` | ⚙️ |
| 11 | Escena y render | `python3 rtex.py cena <pasta>` + `python3 rtex.py render <pasta>`: escenario (`motor/palco.html`) a 30 fps + avatar en el tercio inferior + pista, −14 LUFS en 2 pasadas | ⚙️ |
| 12 | QA | `python3 rtex.py qa <pasta>` → `build/qa.json` + `build/folha.jpg` (16 cuadros); LEER la hoja | ⚙️ |
| 13 | Revisor independiente | `Agent` general-purpose nuevo (nunca fork) o `claude -p` con `~/.claude/runbooks/revisor-independente.md`: lee solo la hoja + `qa.json` + este README; nota en `~/projetos/wifi/scripts/revisor-nota.py` | 🤖 |
| 14 | Entregar | `python3 rtex.py enviar <pasta>` (bot v3) y `python3 rtex.py fila <pasta>` (cola con temporizador de r7ex, canal en `publicar.fila`) | ⚙️ |
| 15 | Comentarios | nada que hacer: el anzuelo es de opinión y nadie espera respuesta. Leer los comentarios es opcional (bueno para el próximo tema). Los enlaces/fuentes, si se quiere, quedan fijos en `publicar.comentario_fixado` | Nei (opcional) |

Atajo: `python3 rtex.py fazer <pasta>` = pasos 4, 8, 10, 11 y 12 en secuencia.

---

## Decisiones (28/10/2026; anzuelo de opinión, gancho y un tema por video en la v1.1.0)

- **Paleta INEMA:** fondo `#0c0c10`, tarjeta `#16161e` con borde `#272730`, texto `#e9e9ee`/`#9a9aa6`. Títulos **Sora**, cuerpo **Inter**,
  etiquetas/fuente/índice **JetBrains Mono**, subtítulos Montserrat Black con contorno negro. **Amarillo `#FACC15` racionado:** como letra
  (palabra clave, elemento activo, destaque del título) y **una única superficie amarilla sólida en todo el video: la píldora de opciones del
  anzuelo** (un solo elemento, con las opciones separadas por divisores oscuros). El QA lo cuenta (`background:` amarillo en el escenario = 1). Verde `#2bff88` solo para ✓, rojo `#ff2a1f` solo para ✗/error, `#F2B45C` en la salvedad,
  azul `#38bdf8` solo en la píldora inema.club.
- **Presentador:** el avatar real de Nei en HeyGen, desde el estudio (suscripción), como en r7ex — no una ilustración. Queda en el **tercio inferior**
  (1080×640 en y 1280) durante todo el reel; los 2/3 superiores son para el contenido (como la D17 del kit para reels 9:16).
- **Un tema por video (v1.1.0):** el formato de lista con 5 temas diferentes en el mismo video salió del modelo; las «N piezas» son los
  pasos del método de ese tema. `checar` rechaza un método con 3 o más fuentes diferentes.
- **Estructura (el estándar rtex), en lugar de las 7 etapas de r7ex:**
  1. `tese` — el **gancho** (cuadro 0 + 3 primeros segundos), con `gancho.tipo` = `contrario` (ordena dejar de hacer algo que todo el mundo
     hace), `perda` (¿y si desapareciera X?), `estatistica_medo` (con fuente en pantalla) o `historia_terceiro` (con un número). Prohibido: lista
     («5 piezas del mes», «N cosas…»), «¿sabías que…?», «yo hice…». El titular (`tela.linhas`) tiene hasta 6 palabras, va en mayúsculas,
     **una** palabra amarilla (`tela.destaque`) y es más agresivo que el texto hablado (el texto atrae a quien desliza sin sonido, la voz suaviza); ya
     está listo en el cuadro 0, que sirve de portada. Un objeto-metáfora con daño (`objeto.params.metafora`, hoy `"fio"`: agentes conectados
     por un hilo que se estira, se rompe y cae) cambia cada ~1 s en los 3 primeros segundos;
  2. `autoridade` — prueba (número con fuente o autoridad) en pantalla **antes de los 20 s** (contador que **se detiene** en el valor de la fuente o sello);
  3. `problema` — el dolor de quien mira, **justo después** de la prueba, con absolución en el texto («não é culpa sua» («no es culpa tuya»)), con un objeto (ej.: chat tachado);
  4. `virada` — se anuncian «N piezas»; el índice 01–N aparece antes del primer elemento y se convierte en píldoras en la parte superior hasta la máxima;
  5. `metodo` — los pasos numerados (30–60% del tiempo), un objeto por paso, etiqueta «0N / NOMBRE»;
  6. `prova` — un hecho con fuente que confirma;
  7. `ressalva` — limitaciones honestas habladas, legibles (≥ 40 px), convertidas en instrucción;
  8. `maxima` — antítesis breve, con ~0,6–0,75 s de silencio antes (desaparecen la voz y la pista);
  9. `cta` — **anzuelo de opinión** (v1.1.0, pedido de Nei el 28/10/2026: el anzuelo no puede obligar a Nei a responder cada comentario):
     una pregunta fuerte, emotiva y con postura, vinculada a la tesis, que la persona responde con su propia opinión. Nei dice su postura
     antes de preguntar, para provocar. La tarjeta queda 9 s después de la última palabra con la pregunta, las opciones y el gesto de comentar representado
     (la mano escribe una opción y pulsa Publicar). **No se entrega nada a quien comenta.**
- **El anzuelo en `roteiro.json`:**
  ```json
  "isca": {"tipo": "opiniao", "pergunta": "Um agente só ou um para cada tarefa?", "opcoes": ["UM", "VÁRIOS"],
           "lado": "um agente só (o Nei diz antes de perguntar)", "tensao": "agente"}
  ```
  `pergunta` termina en "?" (≤ 70 caracteres) y se dice en el CTA; `opcoes` = 2 o 3 palabras en MAYÚSCULAS, dichas en el CTA (sin
  `opcoes`, la pregunta es abierta y `exemplo` es la respuesta corta que la mano escribe); `lado` = la postura de Nei; `tensao` = una palabra
  de la pregunta que está en el cuadro 0 (titular o texto de la tesis) y vuelve en la máxima o en el CTA. `publicar.descricao` termina con la pregunta.
  `checar` rechaza promesas de entrega en cualquier intervención, en el anzuelo, en los parámetros del CTA, en el título, en la descripción y en el contexto
  («te mando» («te lo envío»), «eu mando» («yo lo envío»), «eu envio» («yo lo envío»), «manda o link» («pide el enlace»), «link na bio» («enlace en la bio»), «comenta X que…» («comenta X y…»), «para receber» («para recibir»), «no privado» («por privado»)) y, en el texto hablado, cualquier mención al comentario fijado. `isca.palavra` e `isca.entregavel` dan error: se acabaron. `publicar.comentario_fixado` puede incluir enlaces y fuentes (se queda fijo, nadie necesita interactuar).
- **Se mantiene de r7ex:** avatar desde el estudio, subtítulos karaoke, paneles al ritmo del texto hablado, ritmo (`rtex/ritmo.py`), Whisper/ajuste de tiempos,
  crítico 🤖 + revisor independiente, cola con temporizador y envío al v3.
- **Ritmo y sonido:** texto hablado a 160–190 palabras/min, −14 LUFS (TP ≤ −1,5), cambio visual ≥ 17/min (medido por los eventos de la escena; la medición de
  luminancia a 1 fps va en el QA como información, porque los fundidos cuentan de menos).
- **Zonas seguras del reel:** nada útil por debajo del 80% de la altura (y > 1536) ni en la columna derecha de los iconos de la red (x > 950).
  El contenido queda en los 2/3 superiores; la tarjeta de comentario termina en x 940.
- **Ética:** números solo con fuente consultada ese día; la voz no exagera lo que muestra la pantalla; «gratis» solo si la página lo dice; la salvedad va antes de la máxima;
  el anzuelo no promete nada.

## Qué hay aquí

| Archivo | Qué hace |
|---|---|
| `rtex.py` | la línea de comandos (validador, crítico, estudio, capturas, escena, render, QA, envío, cola) |
| `modelo/roteiro.json` | guion modelo de la v1.1.0 (un tema: «un agente solo y una carpeta por tarea», gancho contrario, anzuelo de opinión) — el formato de `roteiro.json` |
| `rtex/cena.py` | guion + tiempos de las palabras → `cena.js` (cada desencadenante de palabra se convierte en un instante; lista de eventos para el QA) |
| `motor/palco.html` | la composición: componentes `tese` (con la metáfora `fio` en el cuadro 0), `contador`, `chat_riscado`, `indice` (+ píldoras de progreso), `pasta`, `repo` (captura real + estrellas), `manchete`, `selo_prova`, `ressalva`, `maxima` (destello tipográfico), `isca` (pregunta + píldora amarilla de opciones) y el cuadro de comentario |
| `motor/render.mjs` | graba el escenario a 30 fps (Playwright, pantalla `:99`) |
| `motor/mix.sh` | avatar en el tercio inferior + pista con ducking + nivel de sonoridad en 2 pasadas |
| `rtex/qa.py` | mediciones y hoja de revisión |
| `rtex/ritmo.py`, `retempo.py`, `whisper.py`, `pecas.py`, `heygen/` | copias de r7ex v1.1.0 (ritmo del texto hablado, tiempos, transcripción, capturas/logos, estudio de HeyGen) |
| `ferramentas/print.mjs` | captura de página con Playwright |
| `ferramentas/tempos_sinteticos.py` | vista previa del escenario sin avatar (tiempos y ritmo sintéticos; con un video gris de referencia en lugar del avatar también se puede ejecutar `render` y `qa`) |
| `prompts/critico.md` | instrucción para el crítico de viralidad |

## Pendientes

- **Comando `/rtex` de inemaccbot:** hoy es un alias de `/r7ex` y ya cuenta como OK del avatar. **No se modificó.** Redirigirlo a este motor
  (o crear otro comando) solo cuando Nei lo sepa.
- Registrar las decisiones de rtex en el kit `inema-design` (`DECISOES.md`/`HISTORICO.md`) — el orquestador decide el número (D18 ya está duplicado allí).
- Producción sin sesión (temporizador como el `producao/` de r7ex) y skill `/rtex`.
- El modo largo (110–135 s), la apariencia clara (`papel`) y la composición en HyperFrames quedan para la v2.
- La edición publicada `2026-10-28-cinco-pecas-ia` es del formato antiguo (anzuelo PASTA + entregable, lista de 5 temas); las propuestas de
  pregunta y titular para la próxima están en `edicoes/2026-10-28-cinco-pecas-ia/PROPOSTA-ISCA.md` (no volver a renderizar sin el OK de Nei).

## Licencia
MIT.