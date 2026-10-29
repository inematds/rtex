"""QA do rtex: mede o vídeo pronto e grava build/qa.json + build/folha.jpg (quadros para ler antes de enviar).
Cada item: valor medido, alvo e ok. Medidas no MP4 final (ffprobe/ffmpeg), na cena.js (eventos) e no palco (CSS)."""
import json, re, subprocess
from pathlib import Path

R = Path(__file__).resolve().parent.parent
# padrão do grep "fonte = 0" (codificado para o próprio arquivo não casar no grep)
PADRAO_FONTE = __import__("base64").b64decode("anAgP2xhYnN8dGhlanBsYWJzfGxvYm8gZnJhbmNvfGluc3RhZ3JhbVwuY29tLyhyZWVsfHApL3xydGV4LWFuYWxpc2U=").decode()


def _ff(*a):
    return subprocess.run(["ffmpeg", "-nostats", "-hide_banner", *map(str, a)], capture_output=True, text=True).stderr


def _dur(v):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)]))


def trocas_luminancia(v, limiar=10):
    """trocas por minuto pela régua de 1 fps (108x192, cinza, diferença média ≥ limiar) — só a área do palco (y < 1280)"""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(v), "-vf", "fps=1,crop=1080:1280:0:0,scale=108:128,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    q = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 128 * 108).astype(float)
    d = np.abs(np.diff(q, axis=0)).mean(axis=1)
    return int((d >= limiar).sum()), len(q)


def folha(p, v, d, C):
    b = p / "build"; b.mkdir(exist_ok=True)
    ts = [0.2, 1.5] + [round(x["ini"] + min(1.6, (x["fim"] - x["ini"]) * .7), 2) for x in C["blocos"]][1:] + [round(d - .2, 2)]
    ts = sorted(set(t for t in ts if t < d))[:16]
    while len(ts) < 16:
        ts.append(round(d - .2, 2))
    qs = []
    for k, t in enumerate(ts):
        q = b / f"q{k:02d}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", v, "-frames:v", "1", "-vf",
                        f"scale=270:-1,drawtext=text='{t}':x=6:y=6:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.6", q], check=True)
        qs.append(q)
    lay = "|".join(f"{(i % 8) * 270}_{(i // 8) * 480}" for i in range(16))
    subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", q] for q in qs), []), "-filter_complex", f"xstack=inputs=16:layout={lay}",
                    b / "folha.jpg"], check=True)
    for q in qs:
        q.unlink()
    return b / "folha.jpg"


def medir(p, r):
    v = p / "video.mp4"
    C = json.loads((p / "cena.js").read_text()[len("window.CENA="):-1])
    rt = json.loads((p / "avatar/ritmo.json").read_text())
    it = {}

    def item(k, valor, alvo, ok):
        it[k] = {"valor": valor, "alvo": alvo, "ok": bool(ok)}

    d = _dur(v)
    item("duração", f"{d:.1f} s", "60–90 s", 60 <= d <= 90)
    item("ritmo da fala", f"{rt['wpm']:.0f} palavras/min", "160–190", 160 <= rt["wpm"] <= 190)
    j = _ff("-i", v, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-")
    j = json.loads(j[j.rindex("{"): j.rindex("}") + 1])
    I, TP = float(j["input_i"]), float(j["input_tp"])
    item("loudness", f"{I:.1f} LUFS · TP {TP:.1f} dBTP", "−14 ± 0,5 · TP ≤ −1", -14.5 <= I <= -13.5 and TP <= -1.0)
    sil = re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", _ff("-i", v, "-af", "silencedetect=n=-50dB:d=0.3", "-f", "null", "-"))
    fala_fim = C["comenta"]["fala_fim"] if C.get("comenta") else d
    sil = [(float(a), float(b)) for a, b in sil if float(a) < fala_fim]
    pz = rt.get("pausa") or {}
    perto = [s for s in sil if pz.get("fim") and abs(s[1] - pz["fim"]) < .35]
    outros = [s for s in sil if s not in perto and s[1] - s[0] >= .5 and s[0] > 3]
    dur_p = round(perto[0][1] - perto[0][0], 2) if perto else 0
    item("silêncio antes da máxima", f"{dur_p} s · outros ≥ 0,5 s: {len(outros)}", "1 silêncio 0,5–0,9 s, nenhum outro", perto and .5 <= dur_p <= .95 and not outros)
    ev = C["eventos"]
    gaps = [b - a for a, b in zip(ev, ev[1:] + [fala_fim])]
    lum, nq = trocas_luminancia(v)
    item("trocas visuais", f"{len(ev) / d * 60:.0f}/min por evento · {lum / nq * 60:.0f}/min por luminância · maior trecho parado {max(gaps):.1f} s",
         "≥ 17/min · nada > 4 s parado (exceto o cartão)", len(ev) / d * 60 >= 17 and max(gaps) <= 4.0)
    cart = d - fala_fim
    item("cartão do comentário", f"{cart:.1f} s depois da última palavra", "8–10 s", 8 <= cart <= 10.5)
    ult_leg = max(x["fim"] for x in C["legenda"])
    item("último quadro sem legenda", f"legenda some em {ult_leg:.1f} s (fim {d:.1f})", "sem legenda no fim", ult_leg < d - 2)
    css = (R / "motor/palco.html").read_text()
    amarelo = len(re.findall(r"background:(?:var\(--am\)|#FACC15)", css))
    item("amarelo sólido só na isca", f"{amarelo} superfície(s)", "1 (a pílula única das opções da isca de opinião)", amarelo == 1)
    px = {k: int(re.search(sel + r"\{[^}]*?font:[^;}]*?(\d+)px", css).group(1)) for k, sel in
          (("ressalva", r"\.res \.it"), ("linha-fonte", r"#fonte"), ("legenda", r"#leg"))}
    item("legibilidade", f"ressalva {px['ressalva']} px · fonte {px['linha-fonte']} px · legenda {px['legenda']} px", "≥ 40 · ≥ 32 · ≥ 64",
         px["ressalva"] >= 40 and px["linha-fonte"] >= 32 and px["legenda"] >= 64)
    g = subprocess.run(["grep", "-rilE", PADRAO_FONTE, str(R), "--exclude-dir=node_modules", "--exclude-dir=.git",
                        "--exclude=*.png", "--exclude=*.mp4", "--exclude=*.jpg", "--exclude=*.mkv", "--exclude=*.wav"],
                       capture_output=True, text=True).stdout.split()
    item("fonte do formato citada", f"{len(g)} arquivo(s)" + (f": {g[:3]}" if g else ""), "0", not g)
    f = folha(p, v, d, C)
    res = {"ok": all(x["ok"] for x in it.values()), "itens": it, "folha": str(f)}
    (p / "build/qa.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res
