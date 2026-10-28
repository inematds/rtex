# rtex — INEMA’s “N Pieces” Reel

[![rtex](capa/capa.png)](https://inematds.github.io/rtex/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

rtex is the engine Nei uses to make INEMA reels (short vertical videos) featuring his own face: his HeyGen avatar speaks the script, and the engine overlays screens, word-by-word captions, and the end card. Each video follows a fixed “N pieces” format, from the opening frame with its thesis to the closing call to action, “comenta PALAVRA” (“comment WORD”). A validator, an automatic critic, and QA check the format before publishing. The code is open for study and adaptation; to generate your own video, you need your own HeyGen avatar, as well as Python, Node, ffmpeg, and Whisper.

## 📖 Usage guide

Complete guide (landing page + step-by-step instructions + what changes compared with r7ex): **https://inematds.github.io/rtex/guia/en/** · example video: https://www.youtube.com/watch?v=vLOgLCVs7gg

**rtex = what INEMA already has (r7ex v1.1.0 engine) + the rtex script and screen format.**
A vertical reel (9:16, 60–90 s) with Nei’s real avatar speaking in the first person: the thesis written on frame 0, social proof
with a number and source, “N pieces” announced with an index, the numbered method, proof with a source, an honest caveat, the maxim in
antithesis after a silence, and the closing “comenta PALAVRA” (“comment WORD”) with the card held on screen. Objective: bring people to inema.club.

Version **1.0.0** (28/10/2026). Repo: `inematds/rtex`.

---

## The process, from start to finish

🧠 = session with Nei (uses tokens) · ⚙️ = script (zero tokens) · 🤖 = short `claude -p` run on the subscription (never API)

| # | Step | Command / what happens | Who |
|---|---|---|---|
| 1 | Request | Nei gives the topic (or topics), the inema.club page, and the channel | Nei |
| 2 | Research and sources | verify each number against its source (GitHub stars on the day, dated article) and record it in `fontes[]` with `valor` and `verificado_em` | 🧠 |
| 3 | Script | `python3 rtex.py novo <slug>` and write `roteiro.json`: the format blocks (below), the full spoken script, each block’s object, and the hook | 🧠 |
| 4 | Validator | `python3 rtex.py checar <pasta>`: block order, index = method, spoken lines without numerals or "!", ≥ 8 words per block, spoken triggers, source for every number, hook = thesis planted in frame 0, estimated duration 60–90 s | ⚙️ |
| 5 | Critic | `python3 rtex.py critico <pasta>` (`prompts/critico.md`): score per block + blockers; passes with no blockers, thesis ≥ 8, average ≥ 7.5, none < 6 | 🤖 |
| 6 | Avatar approval | `avatar/APROVADO_HEYGEN` with Nei’s phrase for THIS production (one avatar per reel) | 🧠 |
| 7 | Studio | `python3 rtex.py avatar-enviar <pasta>`: the spoken lines go to the HeyGen studio (subscription, screen `:99`), records `avatar/video_id.txt` | ⚙️ |
| 8 | Screenshots | `python3 rtex.py prints <pasta>`: real screenshots of GitHub pages (`ferramentas/print.mjs`) and logos; REVIEW the screenshots | ⚙️ |
| 9 | Preview without avatar (optional) | in a copy of the folder: `python3 ferramentas/tempos_sinteticos.py <cópia>` + `rtex.py cena` + `node motor/render.mjs <cópia> --quadros 1,10,20` — catches layout bugs before HeyGen | ⚙️ |
| 10 | Avatar and pacing | `python3 rtex.py avatar-conferir <pasta>` (read-only) until `pronto`; `python3 rtex.py avatar <pasta>`: timing for each word (Whisper), speech stretched to ~182 words/min (max. 12%), silence before the maxim, 9 s card. **Minutes to hours** — long waits go to the `continua` watcher | ⚙️ |
| 11 | Scene and render | `python3 rtex.py cena <pasta>` + `python3 rtex.py render <pasta>`: stage (`motor/palco.html`) at 30 fps + avatar in the lower third + soundtrack, −14 LUFS in 2 passes | ⚙️ |
| 12 | QA | `python3 rtex.py qa <pasta>` → `build/qa.json` + `build/folha.jpg` (16 frames); REVIEW the sheet | ⚙️ |
| 13 | Independent reviewer | a new general-purpose `Agent` (never a fork) or `claude -p` with `~/.claude/runbooks/revisor-independente.md`: reads only the sheet + `qa.json` + this README; score in `~/projetos/wifi/scripts/revisor-nota.py` | 🤖 |
| 14 | Deliver | `python3 rtex.py enviar <pasta>` (bot v3) and `python3 rtex.py fila <pasta>` (queue with r7ex timer, channel in `publicar.fila`) | ⚙️ |
| 15 | The hook | Nei replies to anyone who commented the word with the deliverable (or the pinned comment from `publicar.comentario_fixado`); no DM automation (that would require an API: authorization needed) | Nei |

Shortcut: `python3 rtex.py fazer <pasta>` = steps 4, 8, 10, 11, and 12 in sequence.

---

## Decisions (28/10/2026)

- **INEMA palette:** background `#0c0c10`, card `#16161e` with `#272730` border, text `#e9e9ee`/`#9a9aa6`. Titles in **Sora**, body in **Inter**,
  labels/source/index in **JetBrains Mono**, captions in Montserrat Black with a black outline. **Yellow `#FACC15` used sparingly:** as lettering
  (keyword, active item, title highlight) and **a single solid yellow surface in the entire video: the hook word pill**.
  QA counts it (`background:` yellow on the stage = 1). Green `#2bff88` only for ✓, red `#ff2a1f` only for ✗/errors, `#F2B45C` for the caveat,
  blue `#38bdf8` only for the inema.club pill.
- **Presenter:** Nei’s real HeyGen avatar, through the studio (subscription), as in r7ex — not an illustration. Stays in the **lower third**
  (1080×640 at y 1280) throughout the reel; the top 2/3 are for the content (like D17 from the 9:16 reels kit).
- **Structure (the rtex format), replacing r7ex’s 7 steps:**
  1. `tese` — written on frame 0 (≤ 9 words, hook word highlighted), something moves in the first second;
  2. `autoridade` — social proof with a number and source on screen (counter that **lands** on the source value);
  3. `problema` — the pain point represented by an object (e.g., chat being crossed out);
  4. `virada` — “N pieces” announced; index 01–N appears before the first item and becomes pills at the top until the maxim;
  5. `metodo` — numbered items (30–60% of the runtime), one object per item, label “0N / NAME”;
  6. `prova` — a sourced fact that confirms the claim;
  7. `ressalva` — honest limitations spoken, legible (≥ 40 px), converted into instructions;
  8. `maxima` — short antithesis, with ~0.6–0.75 s of silence before it (voice and soundtrack fade out);
  9. `cta` — “comenta PALAVRA” (“comment WORD”): the word is the thesis, planted in frame 0; the card stays on screen for 9 s after the last word with a staged commenting gesture; **the deliverable comes after the word** (it is not spoken in the video) and must exist that day — never promise something that does not exist.
- **Kept from r7ex:** avatar through the studio, karaoke captions, panels timed to speech, pacing (`rtex/ritmo.py`), Whisper/re-timing,
  critic 🤖 + independent reviewer, timed queue, and sending to v3.
- **Pacing and sound:** speech at 160–190 words/min, −14 LUFS (TP ≤ −1.5), visual change ≥ 17/min (measured by scene events; luminance measurement at 1 fps is included in QA as information because dissolves are undercounted).
- **Ethics:** numbers only with sources read that day; the voice does not inflate what is on screen; say “free” only if the page says so; the caveat comes before the maxim.

## What’s included

| File | What it does |
|---|---|
| `rtex.py` | the command line (validator, critic, studio, screenshots, scene, render, QA, delivery, queue) |
| `modelo/roteiro.json` | sample script (the first edition) — the `roteiro.json` format |
| `rtex/cena.py` | script + word timings → `cena.js` (each word trigger becomes a moment; event list for QA) |
| `motor/palco.html` | the composition: `tese`, `contador`, `chat_riscado`, `indice` components (+ progress pills), `pasta`, `repo` (real screenshot + stars), `manchete`, `selo_prova`, `ressalva`, `maxima` (typographic flash), `isca` (yellow pill), and the comment box |
| `motor/render.mjs` | records the stage at 30 fps (Playwright, screen `:99`) |
| `motor/mix.sh` | avatar in the lower third + ducked soundtrack + loudness in 2 passes |
| `rtex/qa.py` | measurements and review sheet |
| `rtex/ritmo.py`, `retempo.py`, `whisper.py`, `pecas.py`, `heygen/` | copies from r7ex v1.1.0 (speech pacing, timings, transcription, screenshots/logos, HeyGen studio) |
| `ferramentas/print.mjs` | page screenshot using Playwright |
| `ferramentas/tempos_sinteticos.py` | stage preview without an avatar |
| `prompts/critico.md` | prompt for the virality critic |

## Pending items

- **`/rtex` command in inemaccbot:** currently an alias for `/r7ex` and already counts as avatar approval. **Untouched.** Point it to this engine
  (or create another command) only with Nei’s knowledge.
- Record rtex decisions in the `inema-design` kit (`DECISOES.md`/`HISTORICO.md`) — the orchestrator decides the number (D18 is already duplicated there).
- Production without a session (timer like r7ex’s `producao/`) and `/rtex` skill.
- Long mode (110–135 s), light skin (`papel`), and composition in HyperFrames are for v2.
- Automatic hook delivery (DM by keyword) only with API authorization.

## License
MIT.