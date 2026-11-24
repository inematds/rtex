#!/usr/bin/env bash
# Roda a fase "ficha" do /rtex (prompts/bot-ficha.md) fora do bot para os 4 reels da calculadora (Nei, 24/11/2026:
# "quero 4 videos rtex no lives1,3,4,8 falando da calculadora ... manda eles para o v3"), um por vez.
# A ficha entrega à produção sem sessão (timer rtex-producao), que manda o avatar, monta, revisa, envia ao v3 e põe na fila.
set -uo pipefail
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin" DISPLAY="${DISPLAY:-:99}"
unset ANTHROPIC_API_KEY
R=$HOME/projetos/rtex; D=$R/producao/pedidos-calculadora
set -a; . "$HOME/.config/inema/modelos.env"; set +a
MODELO=${INEMA_CLAUDE_TOPO:-claude-opus-5-5}
for c in lives1 lives3 lives4 lives8; do
  S=$D/$c.recibo
  [ -s "$S" ] && { echo "$(date '+%F %T') $c: já feita"; continue; }
  REF="sessão calculadora-da-reforma 24/11/2026 (rtex calculadora $c)"
  python3 - "$R/prompts/bot-ficha.md" "$D/$c.txt" "$REF" "$S" > "$D/$c.prompt" <<'PY'
import sys
t=open(sys.argv[1]).read(); p=open(sys.argv[2]).read()
for k,v in {"{{input}}":p,"{{ref}}":sys.argv[3],"{{saida}}":sys.argv[4]}.items(): t=t.replace(k,v)
print(t)
PY
  echo "$(date '+%F %T') $c: ficha (claude -p $MODELO)"
  (cd "$R" && timeout 7200 claude -p --model "$MODELO" --effort high --max-turns 300 \
     --permission-mode bypassPermissions --output-format text -- "$(cat "$D/$c.prompt")") > "$D/$c.log" 2>&1
  if [ -s "$S" ]; then echo "$(date '+%F %T') $c: ok $(head -1 "$S")"; else echo "$(date '+%F %T') $c: ERRO $(tail -2 "$D/$c.log" | tr '\n' ' ' | cut -c1-300)"; fi
done
echo "$(date '+%F %T') fim das fichas"
