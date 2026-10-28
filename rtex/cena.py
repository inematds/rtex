"""roteiro.json + avatar/tempos.json → cena.js do palco (motor/palco.html).
Os helpers de alinhamento (n, _roteiro, acha) são cópia do r7ex v1.1.0; o resto é do rtex: cada bloco vira um objeto no
tempo da fala, cada gatilho de palavra vira um instante (`t`) e a lista `eventos` conta as trocas visuais (QA)."""
import difflib, json, re, unicodedata
from pathlib import Path

NUM = re.compile(r"\d")
MAX_LEG = 21
EXTENSO = {"um": "1", "dois": "2", "tres": "3", "quatro": "4", "cinco": "5", "seis": "6"}                          # letras por bloco de legenda (r7ex: 23 já encosta na borda)


def n(s):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", str(s).lower()).encode("ascii", "ignore").decode())


def _roteiro(t, texto):
    """troca as palavras ouvidas pelas da legenda, mantendo os tempos (r7ex)"""
    tok, W = texto.split(), t["palavras"]
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, [n(x) for x in tok], [n(p["w"]) for p in W], autojunk=False).get_opcodes():
        if op == "equal":
            out += [{"w": tok[i1 + k], "t": W[j1 + k]["t"], "f": W[j1 + k]["f"]} for k in range(i2 - i1)]
        elif i2 > i1:
            a = W[j1]["t"] if j2 > j1 else (W[j1 - 1]["f"] if j1 else t["ini"])
            b = W[j2 - 1]["f"] if j2 > j1 else (W[j1]["t"] if j1 < len(W) else a + .3)
            d = (b - a) / (i2 - i1)
            out += [{"w": tok[i1 + k], "t": round(a + k * d, 3), "f": round(a + (k + 1) * d, 3)} for k in range(i2 - i1)]
    return out


def acha(palavras, palavra, k=1):
    achou = 0
    for p in palavras:
        if n(palavra) == n(p["w"]) or (len(n(palavra)) > 3 and n(palavra) in n(p["w"])):
            achou += 1
            if achou == k:
                return p["t"]
    return None


def _fonte_linha(r, b):
    fo = {x["id"]: x for x in r.get("fontes") or []}.get(b.get("fonte") or "")
    if not fo:
        return None
    d = fo["verificado_em"].split("-")
    data = f"{d[2]}/{d[1]}/{d[0]}"
    txt = {"soma": f"GITHUB · {fo.get('conta', '')} MIL · {data}",
           "roadster": "ELECTREK · 15/10/2026 · E MOTOR1",
           "hackathon": f"README DO ECC · GITHUB · {data}",
           "skills": "DOCUMENTAÇÃO DA ANTHROPIC · AGENT SKILLS"}.get(fo["id"])
    if not txt:
        u = fo["url"].replace("https://", "")
        txt = f"{u} · {fo['valor']} ⭐ · {data}"
    return txt


def montar(pasta, r, falas):
    pasta = Path(pasta)
    T = json.loads((pasta / "avatar/tempos.json").read_text())
    leg = {f["id"]: f["legenda"] for f in falas}
    for t in T:
        t["brutas"] = t["palavras"]
        t["palavras"] = _roteiro(t, leg[t["id"]])
    F = {t["id"]: t for t in T}
    ritmo = json.loads((pasta / "avatar/ritmo.json").read_text()) if (pasta / "avatar/ritmo.json").exists() else None
    ult = T[-1]
    fala_fim = ult["palavras"][-1]["f"]
    DUR = round(ritmo["duracao"] if ritmo else fala_fim + 9.0, 2)

    def em(fid, palavra, k=1):
        v = acha(F[fid]["palavras"], palavra, k)
        if v is None:   # a legenda trocou a palavra ("cinco" → "5"): procura o algarismo, depois o que o Whisper ouviu
            v = acha(F[fid]["palavras"], EXTENSO.get(n(palavra), palavra), k)
        if v is None:
            v = acha(F[fid]["brutas"], palavra, k)
        if v is None:
            raise SystemExit(f"{fid}: '{palavra}' não está na fala: " + " ".join(p["w"] for p in F[fid]["palavras"]))
        return round(v, 3)

    blocos, eventos = [], []
    tipos = [b["tipo"] for b in r["blocos"]]
    for i, b in enumerate(r["blocos"]):
        fid = f"f{i + 1}"
        ini = 0.0 if i == 0 else round(F[fid]["ini"] - .1, 3)
        fim = round(F[f"f{i + 2}"]["ini"] - .1, 3) if i + 1 < len(r["blocos"]) else DUR
        o = b["objeto"]; pr = dict(o.get("params") or {})
        # gatilhos de palavra → instantes
        for k in list(pr):
            if (k == "em" or k.endswith("_em")) and isinstance(pr[k], str):
                pr[k] = em(fid, pr[k])
        for k in ("msgs", "itens", "linhas", "papeis"):
            if pr.get(k) and isinstance(pr[k][0], list) and not (o["comp"] == "indice"):
                pr[k] = [{"t": em(fid, x[0]), "txt": x[1]} for x in pr[k]]
        if isinstance(pr.get("dica"), list):
            pr["dica"] = {"t": em(fid, pr["dica"][0]), "txt": pr["dica"][1]}
        if o["comp"] == "repo":
            pr["img"] = f"prints/b{i + 1}.png"
            pr["dominio"] = f"github.com/{pr['repo']}"
        if o["comp"] == "pasta" and pr.get("logo"):
            pr["logo"] = f"prints/logo-{pr['logo']}.png"
        d = {"tipo": b["tipo"], "comp": o["comp"], "ini": ini, "fim": fim, "p": pr, "fonte": _fonte_linha(r, b)}
        if b["tipo"] == "tese":
            d["tela"] = b["tela"]
        if b["tipo"] == "metodo":
            d["rotulo"] = f"{b['n']:02d} / {b['nome']}"; d["n"] = b["n"]
        blocos.append(d)
        eventos.append(ini)
        if o["comp"] == "repo":            # estrelas contando (ini+0,5) e a frase entrando (ini+1,6), além da palavra marcada
            eventos += [ini + .5, min(pr.get("marca_em", ini + 1.9) - .3, ini + 1.6)]
        if o["comp"] == "contador":        # o número começa a correr 0,9 s antes da palavra e pousa nela
            eventos.append(pr["em"] - .9)
        for v in pr.values():
            if isinstance(v, (int, float)) and not isinstance(v, bool) and ini < v < fim and v != pr.get("ate") and v != pr.get("de"):
                eventos.append(v)
            if isinstance(v, list):
                eventos += [x["t"] for x in v if isinstance(x, dict) and "t" in x]
            if isinstance(v, dict) and "t" in v:
                eventos.append(v["t"])

    # índice persistente no topo: da virada até a máxima; peça ativa = bloco de método da vez
    vi = tipos.index("virada")
    nomes = r["blocos"][vi]["objeto"]["params"]["itens"]
    met = [(b["n"], blocos[i]["ini"]) for i, b in enumerate(r["blocos"]) if b["tipo"] == "metodo"]
    pilulas = {"ini": blocos[vi + 1]["ini"], "fim": blocos[tipos.index("maxima")]["ini"], "nomes": nomes, "ativa": met}

    # cartão segurado: comentário digitado depois da última palavra
    isca = r["isca"]["palavra"]
    comenta = {"fala_fim": round(fala_fim, 3), "texto": isca} if DUR - fala_fim >= 4 else None
    eventos += [fala_fim + .3, fala_fim + 1.0 + len(isca) / 8 + 1.0, fala_fim + 1.0 + len(isca) / 8 + 1.5] if comenta else []

    cores = {n(k): v for k, v in (r.get("cores") or {}).items()}
    legenda = []
    for t in T:
        bloco = []; ant = None
        for i, p in enumerate(t["palavras"]):
            w = p["w"]; k = n(w)
            if bloco and len(" ".join(x["w"] for x in bloco) + " " + w) > MAX_LEG:
                legenda.append({"ini": bloco[0]["t"] - .05, "fim": ant["f"] + .12, "palavras": bloco}); bloco = []
            ant = p
            cor = cores.get(k) or ("#FACC15" if NUM.search(k) else None)
            bloco.append({"w": w, "t": p["t"], **({"cor": cor} if cor else {})})
            if len(bloco) == 3 or w[-1:] in ".?!,:" or i == len(t["palavras"]) - 1:
                legenda.append({"ini": bloco[0]["t"] - .05, "fim": p["f"] + .12, "palavras": bloco}); bloco = []
    for a, b in zip(legenda, legenda[1:]):
        a["fim"] = min(max(a["fim"], b["ini"]), b["ini"])
    if legenda:
        legenda[-1]["fim"] = min(legenda[-1]["fim"], fala_fim + .2)   # último quadro sem legenda

    eventos = sorted({round(x, 2) for x in eventos if 0 <= x <= DUR})
    C = {"duracao": DUR, "marca": r["marca"], "isca": isca, "blocos": blocos, "pilulas": pilulas, "comenta": comenta,
         "legenda": legenda, "eventos": eventos, "pausa": (ritmo or {}).get("pausa")}
    (pasta / "cena.js").write_text("window.CENA=" + json.dumps(C, ensure_ascii=False) + ";")
    return DUR, len(eventos) + len(legenda) * 0
