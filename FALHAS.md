# FALHAS — rtex

| 2026-11-18 | Crítico: 1 de 17 aprovou na 1ª rodada, com o corte do r7ex em roteiros de 9 a 13 blocos | média mínima 7,2, teto de 3 rodadas com saída marcada e referência como sugestão (D29) | prompt, infra |
| 2026-11-09 | Kit Design com IA parou no QA por quadros sem mudança por 7,7s | distribuir entradas de texto e ícone por gatilhos reais da fala; novo QA: maior intervalo 3,6s | prompt |

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-11-18 | Envio ao v3 parou no timeout de IPv6 do Telegram depois do revisor aprovar (astra-placar) | `NODE_OPTIONS=--dns-result-order=ipv4first` + `enviar`, `fila` e `--retomar`; proteção que falta: IPv4 primeiro no envio | infra |
| 2026-11-18 | `tese.params.linhas` desenhou o cartão por cima da capa desde o quadro 0 (o QA passou; o revisor barrou) | cartão só entra quando a capa sai | prompt |
| 2026-11-18 | QA reprovou astra-placar: capa parada 15 s na tese longa e exigência de pausa que o ritmo D26 não cria | `tese.params.linhas` e QA ciente do ritmo v2 | infra |
| 2026-11-18 | `cena` parou: gatilho do contador era `vinte`, mas a legenda virou `22%` pelas `trocas` (astra-placar) | `em: 22%`; proteção que falta: `checar` validar os gatilhos depois das `trocas` | prompt |
| 2026-11-18 | ficha era-dos-conceitos: crítico reprovou 5 rodadas (6,4→6,8; tese 7) pedindo falas mais longas, enquanto o `checar` trava em 90 s (~233 palavras); tema com 3 fatos (China, MIT, Brasil) + método não cabe | proteção que falta: o crítico receber o teto de palavras do `checar` e sugerir só reescrita dentro dele (ou tema com 3 fatos ir para o modo longo) | prompt |
| 2026-11-18 | Whisper perdeu a fala f9 do avatar (astra-placar) e a produção parou em `montar`: "fala f9 não achada" | `retempo_pedacos.py` + `producao.py --retomar`; proteção que falta: o retempo cair sozinho para pedaços (3ª vez) | infra |
| 2026-11-05 | QA jarvis-local: trecho parado 5,5 s no bloco autoridade (contador de 8,8 s só gera 3 eventos: ini, em−0,9, em) | bloco virou `manchete` com linhas por palavra; proteção que falta: `checar` recusar contador em bloco > ~8 s | prompt |
| 2026-11-04 | QA openduet: trecho parado 5,8 s na tese (fio só tinha quebra_em no fim da fala) e 4,2 s em autoridade/virada | deixas mais cedo: quebra_em "fila", contador em "tem", índice em "costas"; proteção que falta: `checar` prever os vãos > 4 s antes do render | prompt |
| 2026-11-04 | crítico oscilou ±0,5 entre rodadas quase iguais (openduet: ~16 rodadas, aprovou 1× a 7,7 e depois deu 7,3 com sugestões contraditórias) | parar no 1º aprovado e registrar `critico_decisao`; proteção que falta: crítico com 2 amostras e média, ou teto de 5 rodadas | prompt |
| 2026-11-04 | Whisper pulou 53→62 s do avatar (claude-code-2): "fala f10 não achada"; o _tapa_buracos (buraco > 8 s) retranscreveu e não achou nada | `~/projetos/wifi/longrun/2026-11-01-claude-code-2/tools/retempo_pedacos.py` (pedaços de 20 s + 2 s) e depois `rtex.py avatar`; proteção que falta: retempo cair sozinho para pedaços quando uma fala some | infra |
| 2026-11-04 | rtex: legenda de 21 letras cortou "EMPRESA MOSTRANDO QUE" na borda; linhas pendentes a 20% ilegíveis | MAX_LEG 19, dim .45; chat com hd/ia por parâmetro | infra |
| 2026-11-01 | Whisper large-v3 pulou ~20 s do avatar inteiro (comece-por-tres): "fala f7/f8 não achada" no retempo | transcrever em pedaços de 20 s (+2 s de sobra) e montar o tempos.json; retempo reaproveita | infra |
| 29/10/2026 | pílula da isca "APAGAR \| MANTER" a 100 px estourou a tela (x > 950, MANTER cortado) | fonte da pílula = min(100, 840/caracteres das opções) no palco | infra |
| 29/10/2026 | loudness −14,6 LUFS (QA −14 ± 0,5): o 2º passe linear do loudnorm parou no teto de pico | alimiter −3 dBFS antes dos 2 passes no mix.sh → −14,3 | infra |
| 29/10/2026 | `cena` parou: gatilho "oitenta"/"seis"/"três" não existe na fala depois das `trocas` (vira 80%/6/3) | gatilho `em`/linhas usa a forma da legenda (depois das trocas) | prompt |
| 28/10/2026 | `qa` na prévia sintética: KeyError `wpm` (o `ritmo.json` de `tempos_sinteticos.py` não tinha o campo) | `tempos_sinteticos.py` grava `wpm` | infra |
| 28/10/2026 | cartão de comentário com o "Publicar" em x 940–1020, na coluna dos ícones da rede (zona segura x > 950) | `#com` com `right:140px` (termina em x 940) | prompt |
| 28/10/2026 | 1º render: rosto cortado na testa no terço de baixo (recorte 1350x800) e etiqueta "NEI MALDANER · INEM" (drawtext comeu a última letra do arquivo sem quebra de linha) | recorte 1620x960 do 1920x1080; `tag-nei.txt` com espaço + quebra de linha no fim | infra |
| 28/10/2026 | QA: maior trecho parado 4,7 s (bloco do ponytail) e contador parado em "0,0" por 2 s | frase do repo entra em ini+1,6 s; contador corre desde o início do bloco e pousa na palavra; animações internas contadas como eventos | prompt |
| 28/10/2026 | QA de legibilidade lia `left:60px` como tamanho de letra | regex procura o px dentro de `font:` | prompt |
| 28/10/2026 | `pecas.screenshot` (chrome headless `--screenshot` + `virtual-time-budget`) travou 180 s na página do GitHub do Understand-Anything | print pelo Playwright com `domcontentloaded` + 3,5 s (`ferramentas/print.mjs`) | infra |
| 28/10/2026 | gatilho "cinco" não achado: a legenda troca "cinco peças" → "5 peças" e a busca é na legenda | `em()` tenta o algarismo (EXTENSO) e depois as palavras ouvidas pelo Whisper | prompt |
| 28/10/2026 | prévia: o flash da máxima (camada escura) cobria o texto da máxima; objeto esmaecia no fim de cada bloco | `#flash` antes de `#obj` no DOM; opacidade do objeto fixa em 1 (cada componente faz a própria entrada) | prompt |
| 28/10/2026 | crítico 🤖 não convergiu (média 7,1–7,3 em 3 rodadas, mesma queixa: o Roadster "fora do tema") | bloqueios zerados na 2ª rodada; o Roadster é pauta do Nei (5 pautas = 5 peças), assumido na fala ("a quarta nem é de IA"); decisão registrada em `critico_decisao` do roteiro | prompt |
