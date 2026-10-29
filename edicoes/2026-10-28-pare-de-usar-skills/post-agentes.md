**Pare de usar skills?** Cada skill nova é mais peso no fio que segura o seu Claude.

[[img:/home/nmaldaner/projetos/rtex/edicoes/2026-10-28-pare-de-usar-skills/video.mp4]]
---
**O fato:** a própria equipe do Claude Code, na Anthropic, apagou **mais de 80% do prompt de sistema** quando saiu o Opus 5. O que sobrou é quase tudo segurança, permissões e interface.

E no **modo simples** (`CLAUDE_CODE_SIMPLE=1`), que tira os prompts, o modelo fica um pouco mais inteligente.
---
**O método, em 3 peças:**

**1. Apague.** A cada 6 meses, tire o `CLAUDE.md`, as skills e os hooks, e veja o que ele faz sozinho.

**2. Observe.** Use no trabalho de verdade e anote onde ele tropeça. Esqueceu de rodar o teste? Anota, mas não conserta ainda.

**3. Devolva.** Uma regra por vez, e só depois de ver o mesmo erro de novo.
---
**Atenção:** segurança e permissões nunca saem. Teste numa cópia, nunca no original. Comece por uma skill só, aquela que você nem lembra para que serve.

> Regra velha não te protege. Ela te prende.
---
**Kit aberto e gratuito** — auditoria de ablação (só leitura, não apaga nada, só propõe):
https://inematds.github.io/audit-ablacaocc/guia/

**O motor que fez este vídeo (rtex):**
https://inematds.github.io/rtex/guia/

E você: **apagar suas skills ou manter?**
