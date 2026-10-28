# FALHAS — rtex

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 28/10/2026 | 1º render: rosto cortado na testa no terço de baixo (recorte 1350x800) e etiqueta "NEI MALDANER · INEM" (drawtext comeu a última letra do arquivo sem quebra de linha) | recorte 1620x960 do 1920x1080; `tag-nei.txt` com espaço + quebra de linha no fim | infra |
| 28/10/2026 | QA: maior trecho parado 4,7 s (bloco do ponytail) e contador parado em "0,0" por 2 s | frase do repo entra em ini+1,6 s; contador corre desde o início do bloco e pousa na palavra; animações internas contadas como eventos | prompt |
| 28/10/2026 | QA de legibilidade lia `left:60px` como tamanho de letra | regex procura o px dentro de `font:` | prompt |
| 28/10/2026 | `pecas.screenshot` (chrome headless `--screenshot` + `virtual-time-budget`) travou 180 s na página do GitHub do Understand-Anything | print pelo Playwright com `domcontentloaded` + 3,5 s (`ferramentas/print.mjs`) | infra |
| 28/10/2026 | gatilho "cinco" não achado: a legenda troca "cinco peças" → "5 peças" e a busca é na legenda | `em()` tenta o algarismo (EXTENSO) e depois as palavras ouvidas pelo Whisper | prompt |
| 28/10/2026 | prévia: o flash da máxima (camada escura) cobria o texto da máxima; objeto esmaecia no fim de cada bloco | `#flash` antes de `#obj` no DOM; opacidade do objeto fixa em 1 (cada componente faz a própria entrada) | prompt |
| 28/10/2026 | crítico 🤖 não convergiu (média 7,1–7,3 em 3 rodadas, mesma queixa: o Roadster "fora do tema") | bloqueios zerados na 2ª rodada; o Roadster é pauta do Nei (5 pautas = 5 peças), assumido na fala ("a quarta nem é de IA"); decisão registrada em `critico_decisao` do roteiro | prompt |
