#!/usr/bin/env python3
"""rtex — reel 9:16 do INEMA no padrão rtex: tese escrita no quadro 0 → prova social com número e fonte → "N peças" com
índice → método numerado → prova com fonte → ressalva honesta → máxima em antítese (silêncio antes) → CTA "comenta PALAVRA"
com o cartão segurado. Avatar real do Nei (estúdio HeyGen) no terço de baixo, legenda karaokê, painéis no tempo da fala.
Base copiada do r7ex v1.1.0 (ritmo, retempo, estúdio, render); composição própria (motor/palco.html). Ver README.md.

  python3 rtex.py novo <slug>             cria edicoes/<data>-<slug>/roteiro.json a partir de modelo/roteiro.json
  python3 rtex.py checar <pasta>          validador do roteiro (estrutura, fala, isca, fontes, palavras-gatilho)
  python3 rtex.py critico <pasta>         crítico de viralidade (claude -p, assinatura): gancho ≥ 8, média ≥ 7,5, nenhuma < 6
  python3 rtex.py avatar-enviar <pasta>   manda a fala ao estúdio do HeyGen (precisa de avatar/APROVADO_HEYGEN)
  python3 rtex.py avatar-conferir <pasta> uma conferência no HeyGen (leitura): pronto | processando
  python3 rtex.py avatar <pasta> [--de <mp4>]   espera/baixa o avatar (ou reaproveita um mp4) + tempos + ritmo
  python3 rtex.py prints <pasta>          prints reais das páginas citadas (GitHub) + logos
  python3 rtex.py cena <pasta>            roteiro + tempos → cena.js (motor/palco.html)
  python3 rtex.py render <pasta>          palco (tela :99) + avatar no terço de baixo + trilha → <pasta>/video.mp4
  python3 rtex.py qa <pasta>              medições (duração, wpm, LUFS, silêncio, trocas/min, cartão, fonte) → build/qa.json + folha
  python3 rtex.py enviar <pasta>          manda ao bot v3
  python3 rtex.py fila <pasta>            fim da fila do canal (a fila com timer do r7ex, canal de publicar.fila)
  python3 rtex.py fazer <pasta>           checar → prints + avatar → cena → render → qa
"""
import json, os, re, subprocess, sys
import datetime as dt
from pathlib import Path

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
from rtex import cena as CENA, pecas, retempo as RT, ritmo as RITMO  # noqa: E402

VERSAO = "1.0.0"
PERFIL = Path(os.environ.get("RTEX_HEYGEN_PERFIL", Path.home() / ".cache/inemaccbot/perfil-heygen"))   # perfil compartilhado (tem trava própria)
TEMPLATE_HEYGEN = os.environ.get("RTEX_HEYGEN_TEMPLATE", "TEMPLATE-AVATAR16")
HEYGEN_DIR = R / "heygen"
TELA = ":99"                                    # nunca a tela do Nei
ORDEM = ["tese", "autoridade", "problema", "virada", "metodo", "prova", "ressalva", "maxima", "cta"]
OBRIGATORIOS = {"tese", "virada", "metodo", "prova", "ressalva", "maxima", "cta"}
COMPS = {"tese", "contador", "chat_riscado", "indice", "pasta", "repo", "manchete", "selo_prova", "ressalva", "maxima", "isca"}
PROVA = {"contador", "repo", "selo_prova"}       # objeto que carrega número/print com fonte na tela
DUR_MIN, DUR_MAX = 60, 90                        # alvo do rtex curto (s), cartão incluído
WPM_MIN, WPM_MAX = 160, 190


def log(*a):
    print("[rtex]", *a, flush=True)


def falha(msg):
    sys.exit(f"[rtex] REPROVOU: {msg}")


def roteiro(pasta):
    p = Path(pasta).resolve()
    return p, json.loads((p / "roteiro.json").read_text())


def legenda_de(r, fala):
    for a, b in (r.get("trocas") or {}).items():
        fala = fala.replace(a, b)
    return fala


def falas(p, r):
    out = [{"id": f"f{i + 1}", "fala": b["fala"].strip(), "legenda": legenda_de(r, b["fala"].strip())} for i, b in enumerate(r["blocos"])]
    (p / "falas.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return out


def gatilhos(b):
    """todas as palavras-gatilho do bloco (uma palavra da fala cada): params com sufixo _em/em + 1º elemento das listas de pares"""
    pr = (b.get("objeto") or {}).get("params") or {}
    ws = [v for k, v in pr.items() if (k == "em" or k.endswith("_em")) and isinstance(v, str)]
    for k in ("msgs", "itens", "linhas", "papeis", "parcelas"):
        for x in pr.get(k) or []:
            if isinstance(x, list) and k != "parcelas" and not (k == "itens" and b["objeto"]["comp"] == "indice"):
                ws.append(x[0])
    if isinstance(pr.get("dica"), list):
        ws.append(pr["dica"][0])
    return ws


# ------------------------------------------------------------------ comandos
def cmd_novo(slug):
    p = R / "edicoes" / f"{dt.date.today().isoformat()}-{slug}"
    if (p / "roteiro.json").exists():
        sys.exit(f"já existe: {p / 'roteiro.json'}")
    (p / "avatar").mkdir(parents=True, exist_ok=True)
    m = json.loads((R / "modelo/roteiro.json").read_text()); m["id"] = p.name
    (p / "roteiro.json").write_text(json.dumps(m, ensure_ascii=False, indent=1))
    log("criado", p / "roteiro.json", "— reescreva tema, isca, fontes e os blocos")


def cmd_checar(pasta):
    p, r = roteiro(pasta)
    erros, avisos = [], []
    bl = r.get("blocos") or []
    tipos = [b.get("tipo") for b in bl]
    if r.get("versao") != "rtex/1":
        erros.append("versao deve ser 'rtex/1'")
    for t in tipos:
        if t not in ORDEM:
            erros.append(f"tipo de bloco desconhecido: {t}")
    if [ORDEM.index(t) for t in tipos if t in ORDEM] != sorted(ORDEM.index(t) for t in tipos if t in ORDEM):
        erros.append("blocos fora da ordem: " + " → ".join(ORDEM))
    for t in OBRIGATORIOS - set(tipos):
        erros.append(f"falta o bloco '{t}'")
    for t in ("autoridade", "problema"):
        if t not in tipos:
            avisos.append(f"sem bloco '{t}' (o padrão tem)")
    if tipos and tipos[0] != "tese":
        erros.append("o 1º bloco é a tese (escrita no quadro 0)")
    if tipos and tipos[-1] != "cta":
        erros.append("o último bloco é o CTA (nada de despedida depois)")
    met = [b for b in bl if b.get("tipo") == "metodo"]
    vir = next((b for b in bl if b.get("tipo") == "virada"), None)
    if vir:
        nomes = vir["objeto"]["params"].get("itens") or []
        if len(nomes) != len(met):
            erros.append(f"o índice anuncia {len(nomes)} peças e o método tem {len(met)} itens (fala ↔ tela)")
        if [b.get("nome") for b in met] != nomes:
            erros.append("os nomes do índice não batem com os 'nome' dos itens do método, na mesma ordem")
        if [b.get("n") for b in met] != list(range(1, len(met) + 1)):
            erros.append("itens do método numerados 1..N em ordem")
    if not 2 <= len(met) <= 6:
        erros.append(f"método com {len(met)} itens (2 a 6)")
    # fala
    palavras = 0
    for i, b in enumerate(bl, 1):
        f = b.get("fala") or ""
        nw = len(f.split()); palavras += nw
        if re.search(r"\d", f):
            erros.append(f"bloco {i}: algarismo na fala (o avatar lê errado) — por extenso + 'trocas'")
        if "!" in f:
            erros.append(f"bloco {i}: sem '!' na fala")
        if nw < 8:
            erros.append(f"bloco {i}: fala com {nw} palavras (mínimo 8: bloco curto some no alinhamento — FALHAS r7ex 21/10)")
        if max((len(s.split()) for s in re.split(r"[.?:]", f)), default=0) > 22:
            avisos.append(f"bloco {i}: frase longa (> 22 palavras)")
        c = (b.get("objeto") or {}).get("comp")
        if c not in COMPS:
            erros.append(f"bloco {i}: objeto.comp '{c}' não existe ({', '.join(sorted(COMPS))})")
        leg = CENA.n(legenda_de(r, f)); falan = CENA.n(f)
        for w in gatilhos(b):
            if " " in str(w).strip():
                erros.append(f"bloco {i}: gatilho '{w}' tem mais de uma palavra")
            elif CENA.n(w) not in falan and CENA.n(w) not in leg:
                erros.append(f"bloco {i}: gatilho '{w}' não está na fala")
        if c in PROVA and not b.get("fonte"):
            erros.append(f"bloco {i}: {c} mostra número/print — precisa de 'fonte'")
    ids = {x["id"]: x for x in r.get("fontes") or []}
    for i, b in enumerate(bl, 1):
        if b.get("fonte"):
            fo = ids.get(b["fonte"])
            if not fo:
                erros.append(f"bloco {i}: fonte '{b['fonte']}' não existe em fontes[]")
            elif not fo.get("verificado_em") or not fo.get("valor"):
                erros.append(f"fonte '{fo['id']}' sem valor/verificado_em")
            else:
                idade = (dt.date.today() - dt.date.fromisoformat(fo["verificado_em"])).days
                if idade > 7:
                    erros.append(f"fonte '{fo['id']}' conferida há {idade} dias (máx. 7): confira de novo")
        pr = (b.get("objeto") or {}).get("params") or {}
        if b.get("tipo") == "autoridade" and b["objeto"]["comp"] == "contador":
            fo = ids.get(b.get("fonte") or "", {})
            alvo = str(pr.get("ate")).replace(".", ",")
            if fo and alvo not in str(fo.get("valor")):
                erros.append(f"contador termina em {alvo} e a fonte diz {fo.get('valor')} (o contador pousa no valor da fonte)")
    seg = palavras / ((WPM_MIN + WPM_MAX) / 2) * 60
    estim = seg + 0.75 + RITMO.CAUDA
    if not DUR_MIN <= estim <= DUR_MAX:
        erros.append(f"{palavras} palavras ≈ {estim:.0f} s com o cartão (alvo {DUR_MIN}–{DUR_MAX} s a ~175 palavras/min)")
    if not 150 <= palavras <= 215:
        avisos.append(f"{palavras} palavras (curto: 160–210)")
    # isca = tese, plantada antes, dita no CTA, sozinha no amarelo sólido
    isca = (r.get("isca") or {}).get("palavra", "")
    if not isca or not re.fullmatch(r"[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9]{2,14}", isca):
        erros.append("isca.palavra: UMA palavra em CAIXA ALTA, fácil de digitar")
    else:
        if CENA.n(isca) not in CENA.n(bl[-1]["fala"]):
            erros.append(f"a isca '{isca}' tem de ser dita no CTA")
        if not any(CENA.n(isca) in CENA.n(b["fala"]) for b in bl if b["tipo"] in ("tese", "virada", "maxima")):
            erros.append(f"a isca '{isca}' é a tese: precisa estar na fala da tese, da virada ou da máxima")
        tese = bl[0].get("tela") or {}
        if CENA.n(isca) not in CENA.n(" ".join(tese.get("linhas") or [])):
            erros.append(f"a isca '{isca}' tem de estar escrita no quadro 0 (plantada ≥ 10 s antes do CTA)")
        if not (r.get("isca") or {}).get("entregavel"):
            erros.append("isca.entregavel: o que chega para quem comenta (e existe hoje)")
        if CENA.n(isca) not in CENA.n((r.get("publicar") or {}).get("descricao", "")):
            erros.append("a isca tem de estar na descrição do post")
    tese = bl[0].get("tela") or {} if bl else {}
    if bl and len(" ".join(tese.get("linhas") or []).split()) > 9:
        erros.append("tese do quadro 0 com mais de 9 palavras")
    mx = next((b for b in bl if b.get("tipo") == "maxima"), None)
    if mx:
        pr = mx["objeto"]["params"]
        if not (pr.get("linha1") and pr.get("linha2")) or max(len(pr["linha1"].split()), len(pr["linha2"].split())) > 7:
            erros.append("máxima: linha1 e linha2 curtas (≤ 7 palavras), em antítese")
        pa = (r.get("ritmo") or {}).get("pausa_antes") or {}
        k = tipos.index("maxima") + 1
        if not isinstance(pa, dict) or pa.get("parte") != k:
            erros.append(f"ritmo.pausa_antes.parte tem de ser {k} (o bloco da máxima) — o padrão do ritmo.py cairia no lugar errado")
        elif CENA.n(pa.get("de", "")) not in CENA.n(mx["fala"].split()[0]):
            avisos.append("ritmo.pausa_antes.de não é a 1ª palavra da máxima")
    if sum((b.get("objeto") or {}).get("comp") in PROVA for b in bl) * 3 < len(bl):
        erros.append("menos de 1 em 3 objetos é prova com fonte (contador/repo/selo_prova)")
    if not (r.get("publicar") or {}).get("fila"):
        erros.append("publicar.fila (canal) faltando")
    for a in avisos:
        log("aviso:", a)
    if erros:
        falha("\n  - " + "\n  - ".join(erros))
    log(f"roteiro OK: {len(bl)} blocos, {len(met)} peças, {palavras} palavras (≈ {estim:.0f} s com o cartão), isca {isca}")
    return r


def cmd_critico(pasta):
    """crítico de viralidade (claude -p pela assinatura): nota por bloco + bloqueios; grava critica.json"""
    import hashlib
    p, r = roteiro(pasta)
    h = hashlib.sha1((p / "roteiro.json").read_bytes()).hexdigest()
    arq = p / "critica.json"
    c = json.loads(arq.read_text()) if arq.exists() else {}
    if c.get("hash") != h:
        pedido = (R / "prompts/critico.md").read_text()
        res = subprocess.run(["claude", "-p", "--output-format", "json", "--allowedTools", "Read", "--", pedido],
                             cwd=p, capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
        try:
            txt = json.loads(res.stdout)["result"].strip()
            c = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
            c["notas"] = [int(x["nota"]) for x in sorted(c["blocos"], key=lambda x: x["n"])]
        except Exception as e:
            falha(f"crítico não respondeu direito: {str(e)[:200]} {res.stderr[-200:]}")
        c["hash"] = h
        arq.write_text(json.dumps(c, ensure_ascii=False, indent=1))
    n = c["notas"]
    log("crítico: " + " · ".join(f"{i + 1}:{x}" for i, x in enumerate(n)) + f" (média {sum(n) / len(n):.1f}) — {c.get('resumo', '')}")
    if c.get("bloqueios") or n[0] < 8 or sum(n) / len(n) < 7.5 or min(n) < 6:
        falha("crítico reprovou:\n  - " + "\n  - ".join([f"BLOQUEIO: {b}" for b in c.get("bloqueios") or []] +
              [f"bloco {x['n']} ({x['nota']}): {x.get('melhorar')}" for x in c["blocos"] if x.get("melhorar")]))
    log("crítico aprovou")


def avatar_enviar(pasta):
    p, r = roteiro(pasta); av = p / "avatar"; av.mkdir(exist_ok=True)
    if (av / "avatar.mp4").exists() or (av / "video_id.txt").exists():
        log("avatar já enviado"); return
    if not (av / "APROVADO_HEYGEN").exists():
        falha("falta avatar/APROVADO_HEYGEN (o HeyGen só roda com o OK do Nei para esta produção)")
    cmd_checar(pasta)
    falas(p, r)
    (av / "fala.txt").write_text(" ".join(b["fala"].strip() for b in r["blocos"]) + "\n")
    with open(av / "studio.log", "w") as lg:
        subprocess.run(["node", "heygen-studio.mjs", "--titulo", f"RTEX-{p.name}", "--fala-arquivo", av / "fala.txt",
                        "--perfil", PERFIL, "--template", TEMPLATE_HEYGEN], cwd=HEYGEN_DIR, env=dict(os.environ, DISPLAY=TELA),
                       stdout=lg, stderr=subprocess.STDOUT, timeout=12000)
    s = (av / "studio.log").read_text()
    if "ERRO:" in s:
        falha("estúdio: " + s[s.index("ERRO:"):][:200] + "  (sessão caiu? abra o login na tela do Nei)")
    m = re.search(r"create-v4/([0-9a-f]{32})", s)
    if not m:
        falha("estúdio não devolveu o id (avatar/studio.log)")
    (av / "video_id.txt").write_text(m.group(1))
    log("avatar enviado ao estúdio:", m.group(1))


def avatar_conferir(pasta, minutos=0.02):
    av = Path(pasta).resolve() / "avatar"
    if (av / "avatar.mp4").exists():
        return "pronto"
    res = subprocess.run(["node", "heygen-estudio-baixar.mjs", "--id", (av / "video_id.txt").read_text().strip(),
                          "--saida", av / "avatar.mp4", "--minutos", str(minutos), "--intervalo", "1" if minutos < 1 else "60"],
                         cwd=HEYGEN_DIR, capture_output=True, text=True, timeout=int(minutos * 60) + 1200)
    if res.returncode == 0:
        return "pronto"
    if res.returncode == 4:
        return "processando"
    falha("avatar no HeyGen: " + (res.stdout + res.stderr)[-300:])


def cmd_avatar(pasta, de=None):
    import shutil
    p, r = roteiro(pasta); av = p / "avatar"; av.mkdir(exist_ok=True)
    falas(p, r)
    if de:
        shutil.copy(de, av / "avatar.mp4")
    elif not (av / "avatar.mp4").exists():
        avatar_enviar(pasta)
        if avatar_conferir(pasta, minutos=290) != "pronto":
            falha("tempo esgotado esperando o HeyGen")
    t = av / "tempos.json"
    if not t.exists() or not (av / "ritmo.json").exists():
        d, sem = RT.retempo(p)
        log(f"avatar {d:.1f} s · fala × roteiro {sem:.0%}")
        if sem < 0.85:
            falha(f"o avatar não fala o roteiro ({sem:.0%} < 85%)")
    rt = RITMO.aplicar(p, r)
    if rt:
        log(f"ritmo: {rt['wpm_heygen']:.0f} → {rt['wpm']:.0f} palavras/min (×{rt['k']}) · pausa {rt['pausa']['inserida']:.2f} s "
            f"antes da máxima · cartão {rt['cauda']:.1f} s · {rt['duracao']:.1f} s")


def cmd_prints(pasta):
    """prints reais das páginas do GitHub (cartão com o domínio) e logos dos produtos citados"""
    p, r = roteiro(pasta); pr_dir = p / "prints"; pr_dir.mkdir(exist_ok=True)
    for i, b in enumerate(r["blocos"], 1):
        o = b.get("objeto") or {}
        if o.get("comp") == "repo":
            raw = pr_dir / f"raw-b{i}.png"
            if not raw.exists():
                pecas.screenshot(f"https://github.com/{o['params']['repo']}", raw)
            from PIL import Image, ImageStat
            if ImageStat.Stat(Image.open(raw).convert("L")).stddev[0] < 8:
                falha(f"print do bloco {i} saiu vazio: {o['params']['repo']}")
            pecas.recorte_print(raw, pr_dir / f"b{i}.png")
        if o.get("comp") == "pasta" and o["params"].get("logo"):
            pecas.logo_solto(o["params"]["logo"], pr_dir / f"logo-{o['params']['logo']}.png", lado=160)
    log("prints OK — LEIA prints/b*.png (banner de login/cookie pode cobrir o número)")


def cmd_cena(pasta):
    p, r = roteiro(pasta)
    fl = falas(p, r)
    dur, nev = CENA.montar(p, r, fl)
    log(f"cena.js ok: {dur} s · {nev} eventos visuais ({nev / dur * 60:.0f}/min)")


def cmd_render(pasta):
    p, r = roteiro(pasta)
    env = dict(os.environ, DISPLAY=TELA, MUSICA=str(R / "assets/trilha.mp3"))
    with open(p / "build-render.log", "w") as lg:
        res = subprocess.run(["bash", R / "motor/mix.sh", p, p / "video.mp4"], cwd=R, env=env, stdout=lg, stderr=subprocess.STDOUT,
                             timeout=3600)
    if res.returncode:
        txt = (p / "build-render.log").read_text()
        falha("render: " + txt[-600:])
    log("vídeo", p / "video.mp4")


def cmd_qa(pasta):
    from rtex import qa
    p, r = roteiro(pasta)
    res = qa.medir(p, r)
    for k, v in res["itens"].items():
        log(f"{'✅' if v['ok'] else '❌'} {k}: {v['valor']} (alvo {v['alvo']})")
    if not res["ok"]:
        falha("QA: " + ", ".join(k for k, v in res["itens"].items() if not v["ok"]))
    log("QA OK — LEIA build/folha.jpg antes de enviar")


def cmd_enviar(pasta):
    p, r = roteiro(pasta)
    subprocess.run(["node", R / "bin/enviar_bot_v3.mjs", p / "video.mp4", f"rtex · {r['tema']}"], check=True, timeout=600)


def cmd_fila(pasta):
    p, r = roteiro(pasta); pub = r["publicar"]
    # a fila com timer é a do r7ex (fila-lives7.timer lê ~/projetos/r7ex/fila/fila.json, 1 a cada 2 h, por canal): o rtex entra nela
    subprocess.run(["python3", Path(os.environ.get("RTEX_FILA", Path.home() / "projetos/r7ex/fila/fila.py")), "--add", p / "video.mp4", "--nome", r["tema"], "--titulo", pub["titulo"],
                    "--contexto", pub["contexto"], "--canal", pub.get("fila", "lives11")], check=True)


def cmd_fazer(pasta, de=None):
    cmd_checar(pasta); cmd_prints(pasta); cmd_avatar(pasta, de); cmd_cena(pasta); cmd_render(pasta); cmd_qa(pasta)
    log("Terminei: reel pronto — leia build/folha.jpg; depois `enviar` e `fila`")


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    de = a[a.index("--de") + 1] if "--de" in a else None
    c = {"novo": cmd_novo, "checar": cmd_checar, "critico": cmd_critico, "prints": cmd_prints, "cena": cmd_cena,
         "render": cmd_render, "qa": cmd_qa, "enviar": cmd_enviar, "fila": cmd_fila, "avatar-enviar": avatar_enviar}
    if a[0] == "avatar":
        cmd_avatar(a[1], de)
    elif a[0] == "fazer":
        cmd_fazer(a[1], de)
    elif a[0] == "avatar-conferir":
        print(avatar_conferir(a[1]))
    elif a[0] in c:
        c[a[0]](a[1])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
