#!/usr/bin/env python3
"""Prévia do palco ANTES do avatar: escreve avatar/tempos.json + avatar/ritmo.json sintéticos (palavras a ~182/min,
0,75 s de silêncio antes da máxima, 9 s de cartão) numa CÓPIA da edição, para achar bug de layout sem esperar o HeyGen.
uso: python3 ferramentas/tempos_sinteticos.py <pasta-copia>   (depois: rtex.py cena + node motor/render.mjs <pasta> --quadros …)"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1]); r = json.loads((p / "roteiro.json").read_text())
(p / "avatar").mkdir(exist_ok=True)
dt = 60 / 182; t = .3; T = []
k_max = [b["tipo"] for b in r["blocos"]].index("maxima")
pausa = None
for i, b in enumerate(r["blocos"]):
    if i == k_max:
        pausa = {"ini": round(t, 3), "fim": round(t + .75, 3), "inserida": .75, "fala": f"f{i + 1}"}; t += .75
    pal = []
    for w in b["fala"].split():
        pal.append({"w": w, "t": round(t, 3), "f": round(t + dt * .9, 3)}); t += dt + (.12 if w[-1] in ".:?," else 0)
    T.append({"id": f"f{i + 1}", "fala": b["fala"], "palavras": pal})
for i, x in enumerate(T):
    x["ini"] = 0.0 if i == 0 else round(T[i - 1]["palavras"][-1]["f"] + .05, 3)
for i, x in enumerate(T):
    x["fim"] = T[i + 1]["ini"] if i + 1 < len(T) else round(t + 9, 3)
ult = T[-1]["palavras"][-1]["f"]
(p / "avatar/tempos.json").write_text(json.dumps(T, ensure_ascii=False, indent=1))
(p / "avatar/ritmo.json").write_text(json.dumps({"versao": 1, "sintetico": True, "pausa": pausa, "ultima_palavra": ult,
                                                  "cauda": 9.0, "duracao": round(ult + 9, 3)}))
print(f"sintético: {ult + 9:.1f} s")
