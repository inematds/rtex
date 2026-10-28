# rtex — o reel de "N peças" do INEMA

[![rtex](capa/capa.png)](https://inematds.github.io/rtex/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O rtex é o motor que o Nei usa para fazer reels (vídeos curtos verticais) do INEMA com o próprio rosto: o avatar dele no HeyGen fala o roteiro, e o motor desenha por cima as telas, a legenda palavra por palavra e o cartão final. Cada vídeo segue um formato fixo de "N peças", do quadro de abertura com a tese até o pedido "comenta PALAVRA". Um validador, um crítico automático e um QA conferem o formato antes de publicar. O código é aberto para estudar e adaptar; para gerar o seu vídeo, você precisa do seu próprio avatar no HeyGen, além de Python, Node, ffmpeg e Whisper.

## 📖 Guia de uso

Guia completo (landing + passo a passo + o que muda em relação ao r7ex): **https://inematds.github.io/rtex/guia/** · vídeo exemplo: https://www.youtube.com/watch?v=vLOgLCVs7gg

**rtex = o que o INEMA já tem (motor r7ex v1.1.0) + o padrão rtex de roteiro e tela.**
Um reel vertical (9:16, 60–90 s) com o avatar real do Nei falando em 1ª pessoa: a tese escrita no quadro 0, uma prova social
com número e fonte, "N peças" anunciadas com índice, o método numerado, uma prova com fonte, a ressalva honesta, a máxima em
antítese depois de um silêncio e o fecho "comenta PALAVRA" com o cartão segurado. Objetivo: levar gente ao inema.club.

Versão **1.0.0** (28/10/2026). Repo: `inematds/rtex`.

---

## O processo, do início ao fim

🧠 = sessão com o Nei (gasta tokens) · ⚙️ = script (zero token) · 🤖 = `claude -p` curto pela assinatura (nunca API)

| # | Passo | Comando / o que acontece | Quem |
|---|---|---|---|
| 1 | Pedido | o Nei diz o tema (ou as pautas), a página do inema.club e o canal | Nei |
| 2 | Pesquisa e fontes | conferir cada número na fonte (estrelas do GitHub no dia, matéria com data) e anotar em `fontes[]` com `valor` e `verificado_em` | 🧠 |
| 3 | Roteiro | `python3 rtex.py novo <slug>` e escrever `roteiro.json`: os blocos do padrão (abaixo), a fala por extenso, o objeto de cada bloco, a isca | 🧠 |
| 4 | Validador | `python3 rtex.py checar <pasta>`: ordem dos blocos, índice = método, fala sem algarismo nem "!", ≥ 8 palavras por bloco, gatilhos na fala, fonte em todo número, isca = tese plantada no quadro 0, duração estimada 60–90 s | ⚙️ |
| 5 | Crítico | `python3 rtex.py critico <pasta>` (`prompts/critico.md`): nota por bloco + bloqueios; passa sem bloqueio, tese ≥ 8, média ≥ 7,5, nenhum < 6 | 🤖 |
| 6 | OK do avatar | `avatar/APROVADO_HEYGEN` com a frase do Nei para ESTA produção (um avatar por reel) | 🧠 |
| 7 | Estúdio | `python3 rtex.py avatar-enviar <pasta>`: a fala vai ao estúdio do HeyGen (assinatura, tela `:99`), grava `avatar/video_id.txt` | ⚙️ |
| 8 | Prints | `python3 rtex.py prints <pasta>`: prints reais das páginas do GitHub (`ferramentas/print.mjs`) e logos; LER os prints | ⚙️ |
| 9 | Prévia sem avatar (opcional) | numa cópia da pasta: `python3 ferramentas/tempos_sinteticos.py <cópia>` + `rtex.py cena` + `node motor/render.mjs <cópia> --quadros 1,10,20` — acha bug de layout antes do HeyGen | ⚙️ |
| 10 | Avatar e ritmo | `python3 rtex.py avatar-conferir <pasta>` (leitura) até `pronto`; `python3 rtex.py avatar <pasta>`: tempo de cada palavra (Whisper), fala esticada até ~182 palavras/min (máx. 12%), silêncio antes da máxima, 9 s de cartão. **Minutos a horas** — espera longa vai para o vigia `continua` | ⚙️ |
| 11 | Cena e render | `python3 rtex.py cena <pasta>` + `python3 rtex.py render <pasta>`: palco (`motor/palco.html`) a 30 fps + avatar no terço de baixo + trilha, −14 LUFS em 2 passadas | ⚙️ |
| 12 | QA | `python3 rtex.py qa <pasta>` → `build/qa.json` + `build/folha.jpg` (16 quadros); LER a folha | ⚙️ |
| 13 | Revisor independente | `Agent` general-purpose novo (nunca fork) ou `claude -p` com `~/.claude/runbooks/revisor-independente.md`: lê só a folha + `qa.json` + este README; nota em `~/projetos/wifi/scripts/revisor-nota.py` | 🤖 |
| 14 | Entregar | `python3 rtex.py enviar <pasta>` (bot v3) e `python3 rtex.py fila <pasta>` (fila com timer do r7ex, canal em `publicar.fila`) | ⚙️ |
| 15 | A isca | o Nei responde quem comentou a palavra com o entregável (ou o comentário fixado de `publicar.comentario_fixado`); sem automação de DM (seria API: precisa de autorização) | Nei |

Atalho: `python3 rtex.py fazer <pasta>` = passos 4, 8, 10, 11 e 12 em sequência.

---

## Decisões (28/10/2026)

- **Paleta INEMA:** fundo `#0c0c10`, cartão `#16161e` com borda `#272730`, texto `#e9e9ee`/`#9a9aa6`. Títulos **Sora**, corpo **Inter**,
  rótulos/fonte/índice **JetBrains Mono**, legenda Montserrat Black com contorno preto. **Amarelo `#FACC15` racionado:** como letra
  (palavra-chave, item ativo, destaque do título) e **uma única superfície amarela sólida no vídeo inteiro: a pílula da palavra-isca**.
  O QA conta (`background:` amarelo no palco = 1). Verde `#2bff88` só para ✓, vermelho `#ff2a1f` só para ✗/erro, `#F2B45C` na ressalva,
  azul `#38bdf8` só na pílula inema.club.
- **Apresentador:** o avatar real do Nei no HeyGen, pelo estúdio (assinatura), como no r7ex — não ilustração. Fica no **terço de baixo**
  (1080×640 em y 1280) o reel inteiro; os 2/3 de cima são do conteúdo (como a D17 do kit para reels 9:16).
- **Estrutura (o padrão rtex), no lugar das 7 etapas do r7ex:**
  1. `tese` — escrita no quadro 0 (≤ 9 palavras, a palavra-isca em destaque), algo se mexe no 1º segundo;
  2. `autoridade` — prova social com número e fonte na tela (contador que **pousa** no valor da fonte);
  3. `problema` — a dor com um objeto (ex.: chat sendo riscado);
  4. `virada` — "N peças" anunciadas; o índice 01–N aparece antes do 1º item e vira pílulas no topo até a máxima;
  5. `metodo` — os itens numerados (30–60% do tempo), um objeto por item, rótulo "0N / NOME";
  6. `prova` — um fato com fonte que confirma;
  7. `ressalva` — limitações honestas faladas, legíveis (≥ 40 px), convertidas em instrução;
  8. `maxima` — antítese curta, com ~0,6–0,75 s de silêncio antes (voz e trilha somem);
  9. `cta` — "comenta PALAVRA": a palavra é a tese, plantada no quadro 0; o cartão fica 9 s depois da última palavra com o gesto de
     comentar encenado; **o entregável fica atrás da palavra** (não é ditado no vídeo) e tem de existir no dia — nunca prometer o que não existe.
- **Mantido do r7ex:** avatar pelo estúdio, legenda karaokê, painéis no tempo da fala, ritmo (`rtex/ritmo.py`), Whisper/retempo,
  crítico 🤖 + revisor independente, fila com timer e envio ao v3.
- **Ritmo e som:** fala 160–190 palavras/min, −14 LUFS (TP ≤ −1,5), troca visual ≥ 17/min (medida pelos eventos da cena; a régua de
  luminância a 1 fps vai no QA como informação, porque dissolve subconta).
- **Ética:** número só com fonte lida no dia; a voz não infla a tela; "grátis" só se a página diz; a ressalva vem antes da máxima.

## O que tem aqui

| Arquivo | O que faz |
|---|---|
| `rtex.py` | a linha de comando (validador, crítico, estúdio, prints, cena, render, QA, envio, fila) |
| `modelo/roteiro.json` | roteiro de exemplo (a 1ª edição) — o formato do `roteiro.json` |
| `rtex/cena.py` | roteiro + tempos das palavras → `cena.js` (cada gatilho de palavra vira um instante; lista de eventos para o QA) |
| `motor/palco.html` | a composição: componentes `tese`, `contador`, `chat_riscado`, `indice` (+ pílulas de progresso), `pasta`, `repo` (print real + estrelas), `manchete`, `selo_prova`, `ressalva`, `maxima` (flash tipográfico), `isca` (pílula amarela) e a caixa de comentário |
| `motor/render.mjs` | filma o palco a 30 fps (Playwright, tela `:99`) |
| `motor/mix.sh` | avatar no terço de baixo + trilha com ducking + loudness em 2 passadas |
| `rtex/qa.py` | medições e folha de revisão |
| `rtex/ritmo.py`, `retempo.py`, `whisper.py`, `pecas.py`, `heygen/` | cópias do r7ex v1.1.0 (ritmo da fala, tempos, transcrição, prints/logos, estúdio do HeyGen) |
| `ferramentas/print.mjs` | print de página pelo Playwright |
| `ferramentas/tempos_sinteticos.py` | prévia do palco sem avatar |
| `prompts/critico.md` | pedido do crítico de viralidade |

## Pendências

- **Comando `/rtex` do inemaccbot:** hoje é apelido do `/r7ex` e já vale como OK do avatar. **Não foi mexido.** Repontar para este motor
  (ou criar outro comando) só com o Nei sabendo.
- Registrar as decisões do rtex no kit `inema-design` (`DECISOES.md`/`HISTORICO.md`) — o orquestrador decide o número (o D18 já está duplicado lá).
- Produção sem sessão (timer como o `producao/` do r7ex) e skill `/rtex`.
- Modo longo (110–135 s), skin claro (`papel`) e composição em HyperFrames ficam para a v2.
- Entrega automática da isca (DM por palavra) só com autorização de API.

## Licença
MIT.
