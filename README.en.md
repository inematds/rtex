# rtex — INEMA’s “N pieces” reel

[![rtex](capa/capa.png)](https://inematds.github.io/rtex/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

rtex is the engine Nei uses to make reels (short vertical videos) for INEMA featuring his own face: his HeyGen avatar speaks the script, while the engine overlays the screens, word-by-word captions, and final card. Each video covers just one topic in a fixed format: a strong hook in the opening frame, the method’s steps in “N pieces,” and, at the end, an opinion question for the audience to answer in the comments. A validator, an automatic critic, and QA check the format before publication. The code is open to study and adapt; to generate your own video, you need your own HeyGen avatar, as well as Python, Node, ffmpeg, and Whisper.

## 📖 User guide

Complete guide (landing page + walkthrough + what changes compared with r7ex): **https://inematds.github.io/rtex/guia/en/** · sample video (format v1.0.0, before the opinion hook): https://www.youtube.com/watch?v=vLOgLCVs7gg

**rtex = what INEMA already has (r7ex v1.1.0 engine) + the rtex script and screen standard.**
One vertical reel (9:16, 60–90 s), one topic per video, with Nei’s real avatar speaking in the first person: the hook in frame 0
(short, aggressive headline + an object that breaks), proof with a source or authority within 20 s, the viewer’s problem
(with “não é culpa sua” (“it’s not your fault”)), “N pieces” (the method’s steps) with an index, proof with a source, an honest caveat, the maxim in
antithesis after a silence, and a close with an **opinion question** and the card held on screen. Goal: bring people to inema.club.

Version **1.1.0** (28/10/2026). Repo: `inematds/rtex`.

---

## The process, from beginning to end

🧠 = session with Nei (uses tokens) · ⚙️ = script (zero tokens) · 🤖 = short `claude -p` using the subscription (never API)

| # | Step | Command / what happens | Who |
|---|---|---|---|
| 1 | Request | Nei gives the topic (or topics), the inema.club page, and the channel | Nei |
| 2 | Research and sources | verify each number against the source (GitHub stars on the day, dated article) and record it in `fontes[]` with `valor` and `verificado_em` | 🧠 |
| 3 | Script | `python3 rtex.py novo <slug>` and write `roteiro.json`: one topic, the `gancho`, the standard blocks (below), the full spoken text, the object for each block, the opinion `isca` | 🧠 |
| 4 | Validator | `python3 rtex.py checar <pasta>`: hook (type, headline ≤ 6 words in uppercase with 1 yellow word, no list/“did you know”/“I did,” metaphor object), proof ≤ 20 s, problem followed immediately by absolution, one topic (method without 3+ different sources), block order, index = method, speech without numerals or “!”, ≥ 8 words per block, spoken triggers, source for every number, opinion hook (below), estimated duration 60–90 s | ⚙️ |
| 5 | Critic | `python3 rtex.py critico <pasta>` (`prompts/critico.md`): score per block + blockers; passes with no blockers, thesis ≥ 8, average ≥ 7.5, none < 6 | 🤖 |
| 6 | Avatar OK | `avatar/APROVADO_HEYGEN` with Nei’s phrase for THIS production (one avatar per reel) | 🧠 |
| 7 | Studio | `python3 rtex.py avatar-enviar <pasta>`: speech goes to the HeyGen studio (subscription, screen `:99`), records `avatar/video_id.txt` | ⚙️ |
| 8 | Screenshots | `python3 rtex.py prints <pasta>`: real screenshots of GitHub pages (`ferramentas/print.mjs`) and logos; READ the screenshots | ⚙️ |
| 9 | Preview without avatar (optional) | in a copy of the folder: `python3 ferramentas/tempos_sinteticos.py <cópia>` + `rtex.py cena` + `node motor/render.mjs <cópia> --quadros 1,10,20` — catches layout bugs before HeyGen | ⚙️ |
| 10 | Avatar and pacing | `python3 rtex.py avatar-conferir <pasta>` (read-only) until `pronto`; `python3 rtex.py avatar <pasta>`: timing for each word (Whisper), stretches speech to ~182 words/min (max 12%), silence before the maxim, 9 s card. **Minutes to hours** — long waits go to the `continua` watchdog | ⚙️ |
| 11 | Scene and render | `python3 rtex.py cena <pasta>` + `python3 rtex.py render <pasta>`: stage (`motor/palco.html`) at 30 fps + avatar in the lower third + soundtrack, −14 LUFS in 2 passes | ⚙️ |
| 12 | QA | `python3 rtex.py qa <pasta>` → `build/qa.json` + `build/folha.jpg` (16 frames); READ the sheet | ⚙️ |
| 13 | Independent reviewer | new general-purpose `Agent` (never a fork) or `claude -p` with `~/.claude/runbooks/revisor-independente.md`: reads only the sheet + `qa.json` + this README; score in `~/projetos/wifi/scripts/revisor-nota.py` | 🤖 |
| 14 | Deliver | `python3 rtex.py enviar <pasta>` (bot v3) and `python3 rtex.py fila <pasta>` (queue with r7ex timer, channel in `publicar.fila`) | ⚙️ |
| 15 | Comments | nothing to do: the hook asks for an opinion and no one expects a reply. Reading comments is optional (useful for the next topic). Links/sources, if desired, go static in `publicar.comentario_fixado` | Nei (optional) |

Shortcut: `python3 rtex.py fazer <pasta>` = steps 4, 8, 10, 11, and 12 in sequence.

---

## Decisions (28/10/2026; opinion hook, opening hook, and one topic per video in v1.1.0)

- **INEMA palette:** background `#0c0c10`, card `#16161e` with `#272730` border, text `#e9e9ee`/`#9a9aa6`. Titles **Sora**, body **Inter**,
  labels/source/index **JetBrains Mono**, Montserrat Black captions with black outline. **Yellow `#FACC15` is rationed:** used as lettering
  (keyword, active item, title highlight) and for **one solid yellow surface in the entire video: the options pill for the
  hook** (one element, with options separated by dark dividers). QA counts it (`background:` yellow on the stage = 1). Green `#2bff88` only for ✓, red `#ff2a1f` only for ✗/errors, `#F2B45C` for the caveat,
  blue `#38bdf8` only on the inema.club pill.
- **Presenter:** Nei’s real HeyGen avatar, through the studio (subscription), as in r7ex — not an illustration. It stays in the **lower third**
  (1080×640 at y 1280) throughout the reel; the top 2/3 are for the content (as in D17 of the kit for 9:16 reels).
- **One topic per video (v1.1.0):** the list format with 5 different topics in the same video was removed from the model; “N pieces” are the
  method’s steps for that topic. `checar` rejects a method with 3 or more different sources.
- **Structure (the rtex standard), replacing r7ex’s 7 steps:**
  1. `tese` — the **hook** (frame 0 + first 3 seconds), with `gancho.tipo` = `contrario` (tells people to stop doing something everyone
     does), `perda` (what if X disappeared?), `estatistica_medo` (with source on screen), or `historia_terceiro` (with a number). Forbidden: lists
     (“5 pieces of the month,” “N things…”), “did you know…,” “I did…”. The headline (`tela.linhas`) has up to 6 words, uppercase,
     **one** yellow word (`tela.destaque`), and is more aggressive than the spoken line (the text grabs people scrolling without sound, the voice softens it); it is
     already ready in frame 0, which serves as the cover. A metaphor object with damage (`objeto.params.metafora`, today `"fio"`: agents connected
     by a thread that stretches, snaps, and falls) changes every ~1 s during the first 3 seconds;
  2. `autoridade` — proof (a number with a source or an authority) on screen **within 20 s** (a counter that **lands** on the source’s value, or a seal);
  3. `problema` — the viewer’s pain, **immediately after** the proof, with absolution in the spoken line (“não é culpa sua” (“it’s not your fault”)), with an object (e.g., crossed-out chat);
  4. `virada` — announces “N pieces”; the 01–N index appears before the first item and becomes pills at the top through the maxim;
  5. `metodo` — numbered steps (30–60% of the runtime), one object per step, label “0N / NAME”;
  6. `prova` — a fact with a source that confirms it;
  7. `ressalva` — honest, legible limitations (≥ 40 px), converted into an instruction;
  8. `maxima` — short antithesis, with ~0.6–0.75 s of silence beforehand (voice and soundtrack disappear);
  9. `cta` — **opinion hook** (v1.1.0, requested by Nei on 28/10/2026: the hook must not require Nei to reply to every comment):
     a strong, emotional question with a clear stance, tied to the thesis, which people answer with their own opinion. Nei states his own side
     before asking to provoke discussion. The card stays for 9 s after the last word, showing the question, options, and staged
     comment gesture (a hand types an option and taps Publish). **Nothing is delivered to people who comment.**
- **The hook in `roteiro.json`:**
  ```json
  "isca": {"tipo": "opiniao", "pergunta": "Um agente só ou um para cada tarefa?", "opcoes": ["UM", "VÁRIOS"],
           "lado": "um agente só (o Nei diz antes de perguntar)", "tensao": "agente"}
  ```
  `pergunta` ends in “?” (≤ 70 characters) and is spoken in the CTA; `opcoes` = 2 or 3 words in UPPERCASE, spoken in the CTA (without
  `opcoes`, the question is open-ended and `exemplo` is the short answer the hand types); `lado` = Nei’s position; `tensao` = one word
  from the question that appears in frame 0 (headline or thesis line) and returns in the maxim or CTA. `publicar.descricao` ends with the question.
  `checar` rejects promises of delivery in any spoken line, the hook, the CTA parameters, the title, the description, and the context
  (“te mando” (“I’ll send it to you”), “eu mando” (“I’ll send it”), “eu envio” (“I’ll send it”), “manda o link” (“send the link”), “link na bio” (“link in bio”), “comenta X que…” (“comment X and…”), “para receber” (“to receive”), “no privado” (“in a private message”)) and, in the spoken lines, any mention of the pinned comment. `isca.palavra` and `isca.entregavel` return errors: they’re gone. `publicar.comentario_fixado` can include links and sources (it stays static; no one needs to interact).
- **Retained from r7ex:** avatar through the studio, karaoke captions, panels timed to speech, pacing (`rtex/ritmo.py`), Whisper/retiming,
  critic 🤖 + independent reviewer, queue with timer, and delivery to v3.
- **Pacing and sound:** speech at 160–190 words/min, −14 LUFS (TP ≤ −1.5), visual change ≥ 17/min (measured by scene events; the luminance meter at 1 fps goes into QA as information because dissolves are undercounted).
- **Safe zones for the reel:** nothing useful below 80% of the height (y > 1536) or in the network icons’ right column (x > 950).
  Content stays in the top 2/3; the comment card ends at x 940.
- **Ethics:** numbers only with a source read that day; the voice doesn’t inflate what’s on screen; “grátis” (“free”) only if the page says so; the caveat comes before the maxim; the hook promises nothing.

## What’s here

| File | What it does |
|---|---|
| `rtex.py` | the command line (validator, critic, studio, screenshots, scene, render, QA, delivery, queue) |
| `modelo/roteiro.json` | v1.1.0 sample script (one topic: “one agent and one folder per task,” contrary hook, opinion hook) — the `roteiro.json` format |
| `rtex/cena.py` | script + word timings → `cena.js` (each word trigger becomes a moment; event list for QA) |
| `motor/palco.html` | the composition: `tese` components (with the `fio` metaphor in frame 0), `contador`, `chat_riscado`, `indice` (+ progress pills), `pasta`, `repo` (real screenshot + stars), `manchete`, `selo_prova`, `ressalva`, `maxima` (typographic flash), `isca` (question + yellow options pill), and the comment box |
| `motor/render.mjs` | records the stage at 30 fps (Playwright, screen `:99`) |
| `motor/mix.sh` | avatar in the lower third + soundtrack with ducking + loudness in 2 passes |
| `rtex/qa.py` | measurements and review sheet |
| `rtex/ritmo.py`, `retempo.py`, `whisper.py`, `pecas.py`, `heygen/` | copies from r7ex v1.1.0 (speech pacing, timings, transcription, screenshots/logos, HeyGen studio) |
| `ferramentas/print.mjs` | page screenshot using Playwright |
| `ferramentas/tempos_sinteticos.py` | stage preview without an avatar (synthetic timings and pacing; with a gray placeholder video in place of the avatar, you can also run `render` and `qa`) |
| `prompts/critico.md` | prompt for the virality critic |

## Pending items

- **`/rtex` command in inemaccbot:** currently an alias for `/r7ex` and already counts as avatar OK. **It was not changed.** Point it to this engine
  (or create another command) only with Nei’s knowledge.
- Record the rtex decisions in the `inema-design` kit (`DECISOES.md`/`HISTORICO.md`) — the orchestrator decides the number (D18 is already duplicated there).
- Production without a session (timer like r7ex’s `producao/`) and `/rtex` skill.
- Long mode (110–135 s), light skin (`papel`), and HyperFrames composition are deferred to v2.
- The published edition `2026-10-28-cinco-pecas-ia` uses the old format (PASTA hook + deliverable, list of 5 topics); question and headline proposals for the next one are in `edicoes/2026-10-28-cinco-pecas-ia/PROPOSTA-ISCA.md` (do not re-render without Nei’s OK).

## License
MIT.