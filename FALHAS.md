# FALHAS — rtex

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 28/10/2026 | `pecas.screenshot` (chrome headless `--screenshot` + `virtual-time-budget`) travou 180 s na página do GitHub do Understand-Anything | print pelo Playwright com `domcontentloaded` + 3,5 s (`ferramentas/print.mjs`) | infra |
| 28/10/2026 | gatilho "cinco" não achado: a legenda troca "cinco peças" → "5 peças" e a busca é na legenda | `em()` tenta o algarismo (EXTENSO) e depois as palavras ouvidas pelo Whisper | prompt |
| 28/10/2026 | prévia: o flash da máxima (camada escura) cobria o texto da máxima; objeto esmaecia no fim de cada bloco | `#flash` antes de `#obj` no DOM; opacidade do objeto fixa em 1 (cada componente faz a própria entrada) | prompt |
| 28/10/2026 | crítico 🤖 não convergiu (média 7,1–7,3 em 3 rodadas, mesma queixa: o Roadster "fora do tema") | bloqueios zerados na 2ª rodada; o Roadster é pauta do Nei (5 pautas = 5 peças), assumido na fala ("a quarta nem é de IA"); decisão registrada em `critico_decisao` do roteiro | prompt |
