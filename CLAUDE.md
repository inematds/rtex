# rtex

Reel 9:16 de "N peças" do INEMA (padrão rtex) com o avatar real do Nei. Processo e decisões em `README.md`.

- Autor dos commits: `inematds <inematds@gmail.com>` (config local). Repo público `inematds/rtex`, branch main. Versão em `VERSAO` (rtex.py) e `package.json`.
- **Nunca citar a origem do formato**: chame de "padrão rtex". Antes de cada commit, o grep de fonte do QA (`rtex/qa.py`, `PADRAO_FONTE`) tem de dar 0 em todo o diretório.
- **Independente**: base copiada do r7ex v1.1.0 (ritmo, retempo, whisper, pecas, heygen, render). Não importar nada do r7ex; não editar o r7ex. Única ligação: `rtex.py fila` usa a fila com timer do r7ex (`~/projetos/r7ex/fila/fila.py`, sobrescreve com `RTEX_FILA`).
- Avatar só pelo estúdio do HeyGen (assinatura) com `avatar/APROVADO_HEYGEN` daquela produção (um avatar por reel); status/download pela leitura da API (exceção do Nei). Navegador sempre em `DISPLAY=:99`; só o login vai para a tela do Nei. Nunca aceitar troca de plano no HeyGen.
- Depois do envio ao estúdio a fala está congelada: erro de texto se corrige na legenda (`trocas`) e nos objetos, não num 2º avatar.
- Amarelo `#FACC15` sólido só na pílula das opções da isca (um elemento; o QA conta). Número só com fonte em `fontes[]`, conferida há ≤ 7 dias.
- **Isca de opinião (v1.1.0, 28/10/2026):** o CTA é uma pergunta forte, emocional e com lado (`isca.tipo "opiniao"`, `pergunta`, `opcoes`, `lado`, `tensao`). Nunca prometer entrega ("te mando", "link na bio", "comenta X que…", "está no fixado"): o Nei não responde comentário. `isca.palavra`/`entregavel` acabaram.
- **Gancho e um tema (v1.1.0):** `gancho.tipo` contrario | perda | estatistica_medo | historia_terceiro; manchete do quadro 0 ≤ 6 palavras, caixa alta, 1 palavra amarela, mais agressiva que a fala; objeto-metáfora com dano; prova ≤ 20 s; problema com absolvição logo depois; um tema por vídeo (as N peças são passos). Nada de gancho de lista.
- Zonas seguras: nada útil em y > 1536 nem em x > 950 (ícones).
- Antes de enviar: LER `build/folha.jpg` e `build/qa.json`; revisor independente (nunca quem escreveu). Publicar só pela fila, nunca upload direto.
- `/rtex` no inemaccbot ainda é o `/r7ex` — não mexer sem o Nei.
- Falhou? Linha em `FALHAS.md` (data | o que quebrou | menor correção | prompt/infra).
