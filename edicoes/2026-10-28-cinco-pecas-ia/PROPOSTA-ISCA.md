# Proposta de isca de opinião (e manchete nova) para esta edição

28/10/2026 · rtex v1.1.0. **Esta edição já foi publicada e o avatar falado foi gerado no HeyGen: nada aqui é para re-renderizar.**
Fica registrado para a próxima (ou para uma nova versão, só com o OK do Nei para um avatar novo). O `roteiro.json` desta pasta
não foi mudado: ele é do formato antigo (isca PASTA + entregável) e o `checar` da v1.1.0 o reprova de propósito.

Regra nova (README, "Decisões"): a isca é uma pergunta forte, emocional e com lado, respondida com a opinião de quem comenta.
Ninguém recebe nada por comentar e o Nei não precisa responder ninguém. A manchete do quadro 0 tem até 6 palavras, caixa alta,
uma palavra amarela, e é mais agressiva que a fala.

## 1. Recomendada — "de quem é a culpa"

- **Pergunta:** "Quando a IA erra, a culpa é dela ou sua?" · opções **DELA** / **MINHA** · tensão: `culpa`
- **Lado do Nei (dito antes):** "Pra mim, a culpa é minha: não é a IA que é burra, é a pasta que está vazia." (amarra direto na máxima que o vídeo já tem)
- **Fala do CTA:** "Eu já sei o meu lado: a culpa é minha. E você? Quando a IA erra, a culpa é dela ou sua? Comenta dela ou minha."
- **Manchete nova do quadro 0 (gancho contrário):** `PARA DE CORRIGIR NO CHAT.` — amarelo em **CHAT**
- Por que primeiro: todo mundo já viveu isso, divide o público em dois lados de uma palavra, e a resposta "MINHA" é uma confissão (gera discussão nos comentários sem o Nei entrar).

## 2. "E se sumisse"

- **Pergunta:** "Se o Claude sumisse amanhã, você saberia mexer no seu sistema?" · opções **SIM** / **NÃO** · tensão: `sumisse`
- **Lado do Nei:** "Eu confesso: sem o mapa, eu não saberia."
- **Manchete nova do quadro 0 (perda hipotética):** `E SE O CLAUDE SUMISSE?` — amarelo em **SUMISSE**
- Ressalva: puxa para a peça 3 (o mapa); no formato de um tema por vídeo, vira um vídeo próprio sobre o Understand Anything.

## 3. "Pronto ou meu"

- **Pergunta:** "Setup pronto de outra pessoa ou montado por você?" · opções **PRONTO** / **MEU** · tensão: `setup`
- **Lado do Nei:** "Eu começo pelo pronto e vou trocando as peças."
- **Manchete nova do quadro 0 (história de terceiro, com fonte na tela):** `VENCEU O HACKATHON SÓ COM PASTAS.` — amarelo em **PASTAS** (fonte: `hackathon`, README do ECC)
- Ressalva: divide bem, mas é menos emocional que a 1; serve para um vídeo só do ECC.

## O que muda no roteiro quando for usar

`isca` passa a ser `{"tipo": "opiniao", "pergunta": …, "opcoes": […], "lado": …, "tensao": …}` (sem `palavra` nem `entregavel`),
`publicar.descricao` termina com a pergunta, o `comentario_fixado` pode guardar os links (sem ser recompensa por comentar) e o
quadro 0 ganha `gancho.tipo`, a manchete nova e `objeto.params.metafora`. O formato de lista com 5 temas também saiu do modelo:
uma versão nova desta pauta tem de escolher um tema só. Modelo completo em `modelo/roteiro.json`.
