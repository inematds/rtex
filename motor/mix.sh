#!/usr/bin/env bash
# rtex: palco (render.mjs) + avatar do HeyGen no TERÇO DE BAIXO (1080x640 em y 1280, o reel inteiro) + trilha baixa com ducking.
# A trilha some junto com a voz no silêncio antes da máxima (avatar/ritmo.json) e continua no cartão segurado.
# Loudness em DUAS passadas no mix final (−14 LUFS, TP ≤ −1,5): a cadeia de uma passada do r7ex não garante −14 na saída.
# uso: motor/mix.sh <pasta-da-edicao> [saida.mp4]
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
E="$(cd "$1" && pwd)"; SAIDA="${2:-$E/video.mp4}"
MUSICA="${MUSICA:-$AQUI/../assets/trilha.mp3}"
A="$E/avatar/avatar.mp4"
TAG="$AQUI/tag-nei.txt"
FONTE=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
mkdir -p "$E/build"
[ "${PULA_RENDER:-}" = 1 ] && [ -s "$E/build/palco.mp4" ] || timeout "${RTEX_RENDER_TIMEOUT:-1800}" node "$AQUI/render.mjs" "$E" "$E/build/palco.mp4"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$E/build/palco.mp4")
FADE=$(python3 -c "print(max(0, $D - 1.6))")
VOLM=$(python3 - "$E/avatar/ritmo.json" <<'PY'
import json, sys, os
z = (json.load(open(sys.argv[1])).get("pausa") or {}) if os.path.exists(sys.argv[1]) else {}
a, b = z.get("ini"), z.get("fim")
print("0.2" if a is None else f"'0.2*clip(max(({a:.3f}-t)/0.08,(t-{b:.3f})/0.08),0,1)':eval=frame")
PY
)
# rosto: recorte 1350x800 do 1920x1080 (cabeça e ombros), escala 1080x640
ffmpeg -v error -y -i "$E/build/palco.mp4" -i "$A" -stream_loop -1 -i "$MUSICA" -filter_complex \
  "[1:v]crop=1350:800:285:30,scale=1080:640,setsar=1,fps=30[av];[0:v][av]overlay=0:1280:shortest=1,
   drawbox=x=40:y=1846:w=420:h=46:color=0x0c0c10@0.85:t=fill,drawtext=fontfile=$FONTE:textfile=$TAG:x=58:y=1858:fontsize=22:fontcolor=0xe9e9ee[v];
   [1:a]aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,asplit=2[voz][sc];[2:a]volume=$VOLM,aresample=48000[m];
   [m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300,afade=t=out:st=$FADE:d=1.6[md];
   [voz][md]amix=inputs=2:duration=first:normalize=0[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 21 -preset slow -maxrate 5M -bufsize 10M -pix_fmt yuv420p -c:a pcm_s16le -t "$D" "$E/build/mix1.mkv"
J=$(ffmpeg -nostats -i "$E/build/mix1.mkv" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
LN=$(python3 -c "import json,sys;j=json.loads(sys.argv[1]);print(f\"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true\")" "$J")
ffmpeg -v error -y -i "$E/build/mix1.mkv" -c:v copy -af "$LN,aresample=48000" -c:a aac -b:a 192k -movflags +faststart "$SAIDA"
echo "ok $SAIDA ($(du -h "$SAIDA" | cut -f1))"
