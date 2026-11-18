## 1.10.2 — 18/11/2026

Tese longa com capa: `objeto.params.linhas` na tese tira a capa na primeira palavra marcada e segue com linhas no tempo da fala, evitando trecho parado. O QA deixa de exigir pausa antes da máxima quando o ritmo v2 (D26) não inseriu pausa.

## 1.9.2 — 17/11/2026

Fluência (D26, Nei 17/11/2026: "parece não tem fluência, não parece natural eu falando"; "explicação tem que ser impactante. imagem também"). Caso: r7ex do enxame v2 (lives4), com avatar esticado 7%, quadro congelado e fala telegráfica. `rtex/ritmo.py` v2: k = 1 (velocidade natural do HeyGen), sem pausa inserida (`ritmo.pausa_congelada: true` religa); `motor/mix.sh`: o rosto sai 0,5 s depois da última palavra e o terço de baixo vira o fecho da marca ("inema.club · toda semana tem kit novo"), em vez de 9 s de rosto parado. Crítico: fala de gente (frase telegráfica ≤ 6) e explicação com comparação concreta + tela que a mostra. Revisor: fecho sem o rosto é o padrão. Testado: remix de `2026-11-12-nivel-escada` com o fecho novo conferido no quadro.

## 1.8.2 — 17/11/2026

Nunca calmo (D25, Nei 17/11/2026: "nenhum vídeo tem que sair calmo; r7ex ou rtex não são vídeos calmos, são provocativos, são virais e têm que ter gancho, fonte de imagem e de narração"). Caso: r7ex do enxame (lives4) abriu com "Você pensou em montar um enxame de agentes? A Anthropic mediu…" e passou com 8 no crítico. `checar_tom`: abertura morna reprova; `posicao` (opinião do Nei) exige gancho contrario/acusacao e tese afirmativa; aviso sem `posicao`; roteiro com avatar gravado só recebe aviso. Capa com teste do leigo no pedido ao Codex; crítico com nota de pressão e teste do leigo; revisor com "nunca calmo" como sugestão. Regra comum: `inema-design/regras/chamada.md` §2b.

## 1.7.2 — 17/11/2026

Capa: a cena chocante fica entre 36% e 58% da altura e os 40% de baixo vazios; a legenda do palco começa perto de 60% e cobria a parte de baixo da cena (mesmo achado do r7ex 1.8.7).

## 1.7.1 — 17/11/2026

Capa chocante no quadro 0 (D24, Nei 17/11/2026: "se não tem este padrão vamos criar este padrão para o r7ex e o rtex"). Novo `rtex.py capa`: o Codex image_gen desenha a capa 9:16 com a manchete da tese dentro e a cena de `gancho.capa` (momento da perda/quebra, nunca anúncio calmo); prova `capa/abertura.codex.json` (sha256 igual a um arquivo do `generated_images`). O palco mostra a capa no bloco da tese com cortes 1,00 → 1,03 → 1,06 a cada ~1 s e esconde a manchete em HTML; `checar` exige `gancho.capa`; `render` recusa sem a prova (edição antiga: `RTEX_CAPA_ANTIGA=1`); `fazer` roda a capa depois dos prints.

## 1.6.1 — 17/11/2026

Crítico pelo `producao/ia.yaml` (etapa `critico`, Claude opus-5-5/low com reserva Codex gpt-6.1-sol/medium), sem `claude -p` fixo. Trava de cota compartilhada no `ia_motor.py` (mesmo executor do r7ex 1.7.6): revisor sem cota espera sem contar erro; chamadas automáticas sem sessão no disco. 10 contratos de IA e 16 conferências passaram; crítico real no Claude.

## 1.5.1 — 15/11/2026

Isolar a variável de configuração por projeto e remover chaves herdadas dos CLIs; a seleção por etapa continua explícita. Versões dos manifestos alinhadas.

## 1.5.0 — 15/11/2026

Revisor visual configurável por etapa (tipo/motor/modelo/esforço), imagens anexadas, sem fallback pago. APIs desativadas. Teste real Codex aprovado; 6 contratos de IA e testes existentes da produção passaram. Nenhuma publicação pelo teste.

