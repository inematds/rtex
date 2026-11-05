# rtex

Reel 9:16 de "N peças" do INEMA (padrão rtex) com o avatar real do Nei. Processo e decisões em `README.md`.

- Autor dos commits: `inematds <inematds@gmail.com>` (config local). Repo público `inematds/rtex`, branch main. Versão em `VERSAO` (rtex.py) e `package.json`.
- **Nunca citar a origem do formato**: chame de "padrão rtex". Antes de cada commit, o grep de fonte do QA (`rtex/qa.py`, `PADRAO_FONTE`) tem de dar 0 em todo o diretório.
- **Independente**: base copiada do r7ex v1.1.0 (ritmo, retempo, whisper, pecas, heygen, render). Não importar nada do r7ex; não editar o r7ex. Única ligação: `rtex.py fila` (e `producao/producao.py`) usa a fila com timer do r7ex (`~/projetos/r7ex/fila/fila.py`, sobrescreve com `RTEX_FILA`).
- Avatar só pelo estúdio do HeyGen (assinatura) com `avatar/APROVADO_HEYGEN` daquela produção (um avatar por reel); status/download pela leitura da API (exceção do Nei). Navegador sempre em `DISPLAY=:99`; só o login vai para a tela do Nei. Nunca aceitar troca de plano no HeyGen.
- Depois do envio ao estúdio a fala está congelada: erro de texto se corrige na legenda (`trocas`) e nos objetos, não num 2º avatar.
- Amarelo `#FACC15` sólido só na pílula das opções da isca (um elemento; o QA conta). Número só com fonte em `fontes[]`, conferida há ≤ 7 dias.
- **Isca de opinião (v1.1.0, 28/10/2026):** o CTA é uma pergunta forte, emocional e com lado (`isca.tipo "opiniao"`, `pergunta`, `opcoes`, `lado`, `tensao`). Nunca prometer entrega ("te mando", "link na bio", "comenta X que…", "está no fixado"): o Nei não responde comentário. `isca.palavra`/`entregavel` acabaram.
- **Gancho e um tema (v1.1.0):** `gancho.tipo` contrario | perda | estatistica_medo | historia_terceiro; manchete do quadro 0 ≤ 6 palavras, caixa alta, 1 palavra amarela, mais agressiva que a fala; objeto-metáfora com dano; prova ≤ 20 s; problema com absolvição logo depois; um tema por vídeo (as N peças são passos). Nada de gancho de lista.
- Zonas seguras: nada útil em y > 1536 nem em x > 950 (ícones).
- Antes de enviar: LER `build/folha.jpg` e `build/qa.json`; revisor independente (nunca quem escreveu). Publicar só pela fila, nunca upload direto. Exceção (Nei, 05/11/2026): quando a entrega precisa do link do YouTube (portal, link no tópico do Telegram), publicar direto com o yt-pubx no canal pedido (mesmo título e contexto do item) e marcar o item da fila como `feito` com `video_id` e nota `direto`, para não sair duas vezes; aviso no v3 em texto normal (faixa azul só no Metricool). Nos outros casos o portal pode entrar antes e ganhar o link do vídeo depois.
- **rtex e r7ex são duas coisas (Nei, 05/11/2026).** "rtex" no terminal = este projeto. O `/rtex` do inemaccbot roda ESTE motor desde 05/11/2026 (`flow.json`, prefixo `RT`, `prompts/bot-ficha.md`, produção sem sessão em `producao/` com o timer `rtex-producao`); o comando vale como OK do avatar daquele pedido.
- Falhou? Linha em `FALHAS.md` (data | o que quebrou | menor correção | prompt/infra).
