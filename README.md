# rtex — o reel de "N peças" do INEMA

[![rtex](capa/capa.png)](https://inematds.github.io/rtex/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O rtex é o motor que o Nei usa para fazer reels (vídeos curtos verticais) do INEMA com o próprio rosto: o avatar dele no HeyGen fala o roteiro, e o motor desenha por cima as telas, a legenda palavra por palavra e o cartão final. Cada vídeo trata de um tema só, num formato fixo: um gancho forte no quadro de abertura, os passos do método em "N peças" e, no fim, uma pergunta de opinião para o público responder nos comentários. Um validador, um crítico automático e um QA conferem o formato antes de publicar. O código é aberto para estudar e adaptar; para gerar o seu vídeo, você precisa do seu próprio avatar no HeyGen, além de Python, Node, ffmpeg e Whisper.

## 📖 Guia de uso

Guia completo (landing + passo a passo + o que muda em relação ao r7ex): **https://inematds.github.io/rtex/guia/** · vídeo exemplo (formato v1.0.0, antes da isca de opinião): https://www.youtube.com/watch?v=vLOgLCVs7gg

**rtex = o que o INEMA já tem (motor r7ex v1.1.0) + o padrão rtex de roteiro e tela.**
Um reel vertical (9:16, 60–90 s), um tema por vídeo, com o avatar real do Nei falando em 1ª pessoa: o gancho no quadro 0
(manchete curta e agressiva + um objeto que se quebra), uma prova com fonte ou autoridade até 20 s, o problema de quem assiste
(com "não é culpa sua"), "N peças" (os passos do método) com índice, uma prova com fonte, a ressalva honesta, a máxima em
antítese depois de um silêncio e o fecho com uma **pergunta de opinião** com o cartão segurado. Objetivo: levar gente ao inema.club.

Versão **1.1.0** (28/10/2026). Repo: `inematds/rtex`.

---

## O processo, do início ao fim

🧠 = sessão com o Nei (gasta tokens) · ⚙️ = script (zero token) · 🤖 = `claude -p` curto pela assinatura (nunca API)

| # | Passo | Comando / o que acontece | Quem |
|---|---|---|---|
| 1 | Pedido | o Nei diz o tema (ou as pautas), a página do inema.club e o canal | Nei |
| 2 | Pesquisa e fontes | conferir cada número na fonte (estrelas do GitHub no dia, matéria com data) e anotar em `fontes[]` com `valor` e `verificado_em` | 🧠 |
| 3 | Roteiro | `python3 rtex.py novo <slug>` e escrever `roteiro.json`: um tema, o `gancho`, os blocos do padrão (abaixo), a fala por extenso, o objeto de cada bloco, a `isca` de opinião | 🧠 |
| 4 | Validador | `python3 rtex.py checar <pasta>`: gancho (tipo, manchete ≤ 6 palavras em caixa alta com 1 palavra amarela, sem lista/"você sabia"/"eu fiz", objeto-metáfora), prova ≤ 20 s, problema com absolvição logo depois, um tema (método sem 3+ fontes diferentes), ordem dos blocos, índice = método, fala sem algarismo nem "!", ≥ 8 palavras por bloco, gatilhos na fala, fonte em todo número, isca de opinião (abaixo), duração estimada 60–90 s | ⚙️ |
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
| 15 | Comentários | nada a fazer: a isca é de opinião e ninguém espera resposta. Ler os comentários é opcional (bom para a próxima pauta). Links/fontes, se quiser, vão parados no `publicar.comentario_fixado` | Nei (opcional) |

Atalho: `python3 rtex.py fazer <pasta>` = passos 4, 8, 10, 11 e 12 em sequência.

---

## Decisões (28/10/2026; isca de opinião, gancho e um tema por vídeo na v1.1.0)

- **Paleta INEMA:** fundo `#0c0c10`, cartão `#16161e` com borda `#272730`, texto `#e9e9ee`/`#9a9aa6`. Títulos **Sora**, corpo **Inter**,
  rótulos/fonte/índice **JetBrains Mono**, legenda Montserrat Black com contorno preto. **Amarelo `#FACC15` racionado:** como letra
  (palavra-chave, item ativo, destaque do título) e **uma única superfície amarela sólida no vídeo inteiro: a pílula das opções da
  isca** (um elemento só, com as opções separadas por divisórias escuras). O QA conta (`background:` amarelo no palco = 1). Verde `#2bff88` só para ✓, vermelho `#ff2a1f` só para ✗/erro, `#F2B45C` na ressalva,
  azul `#38bdf8` só na pílula inema.club.
- **Apresentador:** o avatar real do Nei no HeyGen, pelo estúdio (assinatura), como no r7ex — não ilustração. Fica no **terço de baixo**
  (1080×640 em y 1280) o reel inteiro; os 2/3 de cima são do conteúdo (como a D17 do kit para reels 9:16).
- **Um tema por vídeo (v1.1.0):** o formato de lista com 5 temas diferentes no mesmo vídeo saiu do modelo; as "N peças" são os
  passos do método desse tema. O `checar` reprova método com 3 ou mais fontes diferentes.
- **Estrutura (o padrão rtex), no lugar das 7 etapas do r7ex:**
  1. `tese` — o **gancho** (quadro 0 + 3 primeiros segundos), com `gancho.tipo` = `contrario` (manda parar algo que todo mundo
     faz), `perda` (e se X sumisse?), `estatistica_medo` (com fonte na tela) ou `historia_terceiro` (com número). Proibido: lista
     ("5 peças do mês", "N coisas…"), "você sabia que…", "eu fiz…". A manchete (`tela.linhas`) tem até 6 palavras, caixa alta,
     **uma** palavra amarela (`tela.destaque`) e é mais agressiva que a fala (o texto puxa quem rola sem som, a voz suaviza); já
     está pronta no quadro 0, que serve de capa. Um objeto-metáfora com dano (`objeto.params.metafora`, hoje `"fio"`: agentes ligados
     por um fio que estica, arrebenta e cai) muda a cada ~1 s nos 3 primeiros segundos;
  2. `autoridade` — prova (número com fonte ou autoridade) na tela **até 20 s** (contador que **pousa** no valor da fonte, ou selo);
  3. `problema` — a dor de quem assiste, **logo depois** da prova, com absolvição na fala ("não é culpa sua"), com um objeto (ex.: chat sendo riscado);
  4. `virada` — "N peças" anunciadas; o índice 01–N aparece antes do 1º item e vira pílulas no topo até a máxima;
  5. `metodo` — os passos numerados (30–60% do tempo), um objeto por passo, rótulo "0N / NOME";
  6. `prova` — um fato com fonte que confirma;
  7. `ressalva` — limitações honestas faladas, legíveis (≥ 40 px), convertidas em instrução;
  8. `maxima` — antítese curta, com ~0,6–0,75 s de silêncio antes (voz e trilha somem);
  9. `cta` — **isca de opinião** (v1.1.0, pedido do Nei em 28/10/2026: a isca não pode obrigar o Nei a responder cada comentário):
     uma pergunta forte, emocional e com lado, ligada à tese, que a pessoa responde com a própria opinião. O Nei diz o lado dele
     antes, para provocar. O cartão fica 9 s depois da última palavra com a pergunta, as opções e o gesto de comentar encenado
     (a mão digita uma opção e aperta Publicar). **Nada é entregue a quem comenta.**
- **A isca no `roteiro.json`:**
  ```json
  "isca": {"tipo": "opiniao", "pergunta": "Um agente só ou um para cada tarefa?", "opcoes": ["UM", "VÁRIOS"],
           "lado": "um agente só (o Nei diz antes de perguntar)", "tensao": "agente"}
  ```
  `pergunta` termina em "?" (≤ 70 caracteres) e é dita no CTA; `opcoes` = 2 ou 3 palavras em CAIXA ALTA, ditas no CTA (sem
  `opcoes`, a pergunta é aberta e `exemplo` é a resposta curta que a mão digita); `lado` = a posição do Nei; `tensao` = uma palavra
  da pergunta que está no quadro 0 (manchete ou fala da tese) e volta na máxima ou no CTA. `publicar.descricao` termina com a pergunta.
  O `checar` reprova promessa de entrega em qualquer fala, na isca, nos parâmetros do CTA, no título, na descrição e no contexto
  ("te mando", "eu mando", "eu envio", "manda o link", "link na bio", "comenta X que…", "para receber", "no privado") e, na fala,
  qualquer menção ao comentário fixado. `isca.palavra` e `isca.entregavel` dão erro: acabaram. `publicar.comentario_fixado` pode
  trazer links e fontes (fica parado, ninguém precisa interagir).
- **Mantido do r7ex:** avatar pelo estúdio, legenda karaokê, painéis no tempo da fala, ritmo (`rtex/ritmo.py`), Whisper/retempo,
  crítico 🤖 + revisor independente, fila com timer e envio ao v3.
- **Ritmo e som:** fala 160–190 palavras/min, −14 LUFS (TP ≤ −1,5), troca visual ≥ 17/min (medida pelos eventos da cena; a régua de
  luminância a 1 fps vai no QA como informação, porque dissolve subconta).
- **Zonas seguras do reel:** nada útil abaixo de 80% da altura (y > 1536) nem na coluna direita dos ícones da rede (x > 950).
  O conteúdo fica nos 2/3 de cima; o cartão de comentário termina em x 940.
- **Ética:** número só com fonte lida no dia; a voz não infla a tela; "grátis" só se a página diz; a ressalva vem antes da máxima;
  a isca não promete nada.

## O que tem aqui

| Arquivo | O que faz |
|---|---|
| `rtex.py` | a linha de comando (validador, crítico, estúdio, prints, cena, render, QA, envio, fila) |
| `modelo/roteiro.json` | roteiro modelo da v1.1.0 (um tema: "um agente só e uma pasta por tarefa", gancho contrário, isca de opinião) — o formato do `roteiro.json` |
| `rtex/cena.py` | roteiro + tempos das palavras → `cena.js` (cada gatilho de palavra vira um instante; lista de eventos para o QA) |
| `motor/palco.html` | a composição: componentes `tese` (com a metáfora `fio` no quadro 0), `contador`, `chat_riscado`, `indice` (+ pílulas de progresso), `pasta`, `repo` (print real + estrelas), `manchete`, `selo_prova`, `ressalva`, `maxima` (flash tipográfico), `isca` (pergunta + pílula amarela das opções) e a caixa de comentário |
| `motor/render.mjs` | filma o palco a 30 fps (Playwright, tela `:99`) |
| `motor/mix.sh` | avatar no terço de baixo + trilha com ducking + loudness em 2 passadas |
| `rtex/qa.py` | medições e folha de revisão |
| `rtex/ritmo.py`, `retempo.py`, `whisper.py`, `pecas.py`, `heygen/` | cópias do r7ex v1.1.0 (ritmo da fala, tempos, transcrição, prints/logos, estúdio do HeyGen) |
| `ferramentas/print.mjs` | print de página pelo Playwright |
| `ferramentas/tempos_sinteticos.py` | prévia do palco sem avatar (tempos e ritmo sintéticos; com um vídeo cinza de marcação no lugar do avatar dá até para rodar `render` e `qa`) |
| `prompts/critico.md` | pedido do crítico de viralidade |

## Pendências

- **Comando `/rtex` do inemaccbot:** hoje é apelido do `/r7ex` e já vale como OK do avatar. **Não foi mexido.** Repontar para este motor
  (ou criar outro comando) só com o Nei sabendo.
- Registrar as decisões do rtex no kit `inema-design` (`DECISOES.md`/`HISTORICO.md`) — o orquestrador decide o número (o D18 já está duplicado lá).
- Produção sem sessão (timer como o `producao/` do r7ex) e skill `/rtex`.
- Modo longo (110–135 s), skin claro (`papel`) e composição em HyperFrames ficam para a v2.
- A edição publicada `2026-10-28-cinco-pecas-ia` é do formato antigo (isca PASTA + entregável, lista de 5 temas); propostas de
  pergunta e manchete para a próxima em `edicoes/2026-10-28-cinco-pecas-ia/PROPOSTA-ISCA.md` (não re-renderizar sem o OK do Nei).

## Licença
MIT.
