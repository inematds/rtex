## 1.7.1 — 17/11/2026

Capa chocante no quadro 0 (D24, Nei 17/11/2026: "se não tem este padrão vamos criar este padrão para o r7ex e o rtex"). Novo `rtex.py capa`: o Codex image_gen desenha a capa 9:16 com a manchete da tese dentro e a cena de `gancho.capa` (momento da perda/quebra, nunca anúncio calmo); prova `capa/abertura.codex.json` (sha256 igual a um arquivo do `generated_images`). O palco mostra a capa no bloco da tese com cortes 1,00 → 1,03 → 1,06 a cada ~1 s e esconde a manchete em HTML; `checar` exige `gancho.capa`; `render` recusa sem a prova (edição antiga: `RTEX_CAPA_ANTIGA=1`); `fazer` roda a capa depois dos prints.

## 1.6.1 — 17/11/2026

Crítico pelo `producao/ia.yaml` (etapa `critico`, Claude opus-5-5/low com reserva Codex gpt-6.1-sol/medium), sem `claude -p` fixo. Trava de cota compartilhada no `ia_motor.py` (mesmo executor do r7ex 1.7.6): revisor sem cota espera sem contar erro; chamadas automáticas sem sessão no disco. 10 contratos de IA e 16 conferências passaram; crítico real no Claude.

## 1.5.1 — 15/11/2026

Isolar a variável de configuração por projeto e remover chaves herdadas dos CLIs; a seleção por etapa continua explícita. Versões dos manifestos alinhadas.

## 1.5.0 — 15/11/2026

Revisor visual configurável por etapa (tipo/motor/modelo/esforço), imagens anexadas, sem fallback pago. APIs desativadas. Teste real Codex aprovado; 6 contratos de IA e testes existentes da produção passaram. Nenhuma publicação pelo teste.

