#!/usr/bin/env python3
"""Produção do rtex sem sessão aberta: leva cada edição do avatar no HeyGen até a fila do canal.

Cópia adaptada da produção do r7ex (o rtex não importa nada do r7ex). Nei, 05/11/2026: "no inemaccbot pode ter /rtex
/rtexjp /r7ex" — o /rtex do bot passa a rodar este motor. Quem espera é este script (timer `rtex-producao`, a cada
5 min); o agente (claude -p, assinatura) só entra para REVISAR a folha de 16 quadros.

Estados (só andam para a frente):
  enviar_avatar → esperando_avatar → montar → revisao → na_fila
  qualquer erro → parado (motivo no estado + aviso no v3); `--retomar <pasta>` tenta de novo do ponto certo.

Uso:
  producao.py --add <pasta>       entra na produção (precisa de avatar/APROVADO_HEYGEN ou avatar/AVATAR_DE.txt ou avatar.mp4)
  producao.py --status            mostra as edições e o estado
  producao.py --retomar <pasta>   tira do 'parado' e recalcula o estado
  producao.py                     uma rodada (é o que o timer chama)

Travas: só entra edição adicionada com --add (nunca varre edicoes/); o avatar só é gerado com APROVADO_HEYGEN
(conferido pelo rtex.py, este script nunca cria esse arquivo); o estúdio passa pela trava da ferramenta
(heygen-perfil.mjs); publicação só pela fila do canal (rtex.py fila), nunca upload direto.
"""
import fcntl, json, subprocess, sys, time
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
R = AQUI.parent
ESTADO = AQUI / "estado.json"
LOG = AQUI / "producao.log"
REVISOR = AQUI / "revisor.md"
FILA = Path.home() / "projetos/r7ex/fila/fila.json"          # a fila com timer é a do r7ex (rtex.py fila entra nela)
AVISA = Path.home() / "projetos/wifi/scripts/avisa-v3.sh"
RTEX = [sys.executable, str(R / "rtex.py")]
TETO_AVATAR_H = 6                                         # esperando o HeyGen mais que isso → parado + aviso
# falta de memória (GPU/RAM dividida com outros renders) e tempo esgotado passam sozinhos: 2 tentativas antes de avisar (20/10/2026)
PASSAGEIRO = ("NV_ERR_NO_MEMORY", "out of memory", "BindToCurrentSequence", "TimeoutError", "Timeout 30000ms",
              "tempo esgotado", "transcrever_v1.py", "GPU ocupada além do tempo de espera")
TENTATIVAS, ESPERA_S = 2, 600


def passageiro(out):
    return any(s.lower() in out.lower() for s in PASSAGEIRO)


def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}\n")
    print(msg, flush=True)


def tarja(sugestoes):
    """Nei, 21/10/2026: sugestão do revisor não para o vídeo; vai numa tarja vermelha 'SUGESTÃO' e ele decide se refaz"""
    if not sugestoes:
        return ""
    return ("\n\n🟥🟥🟥 SUGESTÃO 🟥🟥🟥\n" + "\n".join(f"🔴 {x}" for x in sugestoes)
            + "\n🟥🟥🟥🟥🟥🟥🟥🟥🟥\n(o vídeo seguiu para a fila; se quiser refazer, é só pedir)")


def avisa(msg):
    h = datetime.now()
    if h.hour == 23 and 20 <= h.minute <= 55:            # janela proibida do Telegram
        time.sleep((56 - h.minute) * 60)
    subprocess.run(["bash", str(AVISA), msg], capture_output=True, timeout=60)
    log(f"aviso: {msg}")


class Estado:
    """estado.json com trava curta a cada leitura/escrita (o --add pode rodar no meio de uma rodada)"""
    def __enter__(self):
        self.lk = open(AQUI / ".estado.lock", "w"); fcntl.flock(self.lk, fcntl.LOCK_EX)
        self.d = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
        return self.d

    def __exit__(self, *a):
        if a[0] is None:
            tmp = ESTADO.with_suffix(".tmp"); tmp.write_text(json.dumps(self.d, ensure_ascii=False, indent=1)); tmp.replace(ESTADO)
        fcntl.flock(self.lk, fcntl.LOCK_UN); self.lk.close()


def muda(pasta, estado, **campos):
    with Estado() as d:
        it = d[pasta]; ant = it["estado"]
        it.update(estado=estado, desde=f"{datetime.now():%Y-%m-%d %H:%M}", **campos)
    log(f"{Path(pasta).name}: {ant} → {estado}" + (f" ({campos['motivo']})" if campos.get("motivo") else ""))


def para(pasta, motivo):
    muda(pasta, "parado", motivo=motivo[-400:])
    avisa(f"Falhou: rtex {Path(pasta).name} — {motivo[-300:]}\n(depois de corrigir: producao.py --retomar {Path(pasta).name})")


def roda(args, timeout, saida=None):
    """roda o rtex.py; devolve (rc, últimas linhas)"""
    try:
        r = subprocess.run(RTEX + args, cwd=R, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, f"tempo esgotado ({timeout} s) em {args[0]}"
    out = r.stdout + r.stderr
    if saida:
        with open(saida, "a") as f:
            f.write(f"\n=== {datetime.now():%Y-%m-%d %H:%M:%S} rtex.py {' '.join(args)} (rc {r.returncode})\n{out}")
    return r.returncode, out.strip()[-600:]


def estado_inicial(p):
    av = p / "avatar"
    if (av / "avatar.mp4").exists() or (av / "AVATAR_DE.txt").exists():
        return "montar"
    if (av / "video_id.txt").exists():
        return "esperando_avatar"
    return "enviar_avatar"


def so_v3(p):
    """publicar.so_v3: true no roteiro = vídeo de teste, entregue só no v3."""
    return bool((json.loads((p / "roteiro.json").read_text()).get("publicar") or {}).get("so_v3"))


def na_fila(p):
    if not FILA.exists():
        return False
    return str(p / "video.mp4") in FILA.read_text()


def revisar(p):
    """agente (claude -p, assinatura) lê roteiro + folha + qa e devolve {veredito, motivo}"""
    try:
        r = subprocess.run(["claude", "-p", "--output-format", "json", "--allowedTools", "Read", "--", REVISOR.read_text()],
                           cwd=p, capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
        res = json.loads(r.stdout)["result"].strip()
        v = json.loads(res[res.index("{"): res.rindex("}") + 1])
        assert v.get("veredito") in ("aprovado", "reprovado")
        v["sugestoes"] = [str(x) for x in (v.get("sugestoes") or []) if str(x).strip()]
        if int(v.get("impacto", 10)) < 7 and not any("impacto" in x.lower() for x in v["sugestoes"]):
            v["sugestoes"].append(f"impacto {v['impacto']}/10")   # 21/10/2026: impacto baixo vira sugestão, não para
        return v
    except Exception as e:
        return {"veredito": "erro", "motivo": f"revisor não respondeu direito: {str(e)[:200]}"}


def nota_revisor(p, v):
    """grava o parecer no registro único (wifi/scripts/revisor-nota.py) para comparar com o do Nei; nunca para a produção"""
    if v.get("veredito") not in ("aprovado", "reprovado"):
        return
    cmd = [sys.executable, str(Path.home() / "projetos/wifi/scripts/revisor-nota.py"), "registra", "--fluxo", "rtex",
           "--item", p.name, "--quem", "revisor", "--veredito", v["veredito"], "--motivo", str(v.get("motivo", ""))]
    if str(v.get("impacto", "")).replace(".", "", 1).isdigit():
        cmd += ["--nota", str(v["impacto"])]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
    except Exception:
        pass


def passo(pasta, it, feito):
    """avança uma edição um passo; `feito` limita os passos pesados por rodada. Devolve True se andou."""
    p = Path(pasta); st = it["estado"]; logp = p / "producao.log"
    if st == "enviar_avatar":
        # Nei, 25/10/2026: "sempre tem que mandar e não esperar que ele fique pronto; já liberar para outros irem para o
        # studio". Todas as edições pendentes vão ao estúdio na MESMA rodada (uma após a outra, pela trava do estúdio);
        # nenhuma espera o render da anterior. Antes era uma por rodada (5 min cada).
        rc, out = roda(["avatar-enviar", pasta], 12600, logp)
        if rc:
            para(pasta, f"envio do avatar ao estúdio: {out}"); return False
        muda(pasta, "esperando_avatar"); return True
    if st == "esperando_avatar":
        rc, out = roda(["avatar-conferir", pasta], 1500, logp)
        if rc:
            para(pasta, f"avatar no HeyGen: {out}"); return False
        if out.splitlines()[-1:] == ["pronto"]:
            muda(pasta, "montar"); return True
        horas = (datetime.now() - datetime.strptime(it["desde"], "%Y-%m-%d %H:%M")).total_seconds() / 3600
        if horas > TETO_AVATAR_H:                         # ID errado, rascunho não enviado ou HeyGen travado
            para(pasta, f"o HeyGen não entregou o avatar em {TETO_AVATAR_H} h (conferir o título RTEX-{p.name} em Projetos no estúdio)")
        return False
    if st == "montar":
        if feito.get("montar"):
            return False
        feito["montar"] = True
        if time.time() < it.get("tentar_apos", 0):
            return False
        rc, out = roda(["fazer", pasta], 7200, logp)
        if rc and passageiro(out) and it.get("tentativas", 0) < TENTATIVAS:
            n = it.get("tentativas", 0) + 1                # GPU/RAM cheia: espera e tenta de novo antes de avisar
            with Estado() as d:
                d[pasta].update(tentativas=n, tentar_apos=time.time() + ESPERA_S * n)
            log(f"{p.name}: falha passageira na montagem (tentativa {n}/{TENTATIVAS}, de novo em {ESPERA_S * n // 60} min)")
            return False
        if rc:
            para(pasta, f"montagem: {out}"); return False
        muda(pasta, "revisao"); return True
    if st == "revisao":
        v = revisar(p)
        with open(logp, "a") as f:
            f.write(f"\n=== {datetime.now():%Y-%m-%d %H:%M:%S} revisor: {json.dumps(v, ensure_ascii=False)}\n")
        if v["veredito"] == "erro" and it.get("erros_revisor", 0) < 3:  # falha passageira do claude -p: tenta no próximo ciclo
            with Estado() as d:
                d[pasta]["erros_revisor"] = it.get("erros_revisor", 0) + 1
            return False
        nota_revisor(p, v)
        if v["veredito"] != "aprovado":
            para(pasta, f"revisão reprovou: {v['motivo']}"); return False
        muda(pasta, "publicar", revisao=v["motivo"][:300], sugestoes=(v.get("sugestoes") or [])[:5]); return True
    if st == "publicar":
        if not it.get("enviado_v3"):
            rc, out = roda(["enviar", pasta], 900, logp)
            if rc:
                para(pasta, f"envio ao v3: {out}"); return False
            with Estado() as d:
                d[pasta]["enviado_v3"] = True
        lugar = "já estava na fila"
        if so_v3(p):                                      # teste (publicar.so_v3: true): só no v3, sem fila nem YouTube
            lugar = "mandado só ao v3 (teste, sem fila)"
        elif not na_fila(p):                              # nunca entra duas vezes na fila
            rc, out = roda(["fila", pasta], 300, logp)
            if rc:
                para(pasta, f"entrada na fila: {out}"); return False
            lugar = next((l for l in out.splitlines() if "na fila" in l), "na fila")
        muda(pasta, "na_fila")
        avisa(f"Terminei: rtex {p.name} revisado e {lugar}" + tarja(it.get("sugestoes")))
        return True
    return False


def rodada():
    lk = open(AQUI / ".rodada.lock", "w")
    try:
        fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return                                            # rodada anterior ainda trabalhando
    feito = {}
    for _ in range(20):                                   # cada edição pode andar vários passos na mesma rodada
        with Estado() as d:
            itens = {k: dict(v) for k, v in d.items() if v["estado"] not in ("na_fila", "parado")}
        andou = False
        for pasta, it in sorted(itens.items(), key=lambda kv: kv[1]["entrou"]):
            try:
                andou |= passo(pasta, it, feito)
            except Exception as e:                        # erro do próprio script: para a edição, não a produção
                para(pasta, f"erro na produção: {e!r}")
        if not andou:
            break


def add(pasta):
    p = Path(pasta).resolve()
    if not (p / "roteiro.json").exists():
        sys.exit(f"sem roteiro.json em {p}")
    av = p / "avatar"
    if not any((av / n).exists() for n in ("APROVADO_HEYGEN", "AVATAR_DE.txt", "avatar.mp4")):
        sys.exit("falta avatar/APROVADO_HEYGEN (OK do Nei para gerar este avatar) ou avatar/AVATAR_DE.txt (reaproveitar)")
    st = "na_fila" if na_fila(p) else estado_inicial(p)
    with Estado() as d:
        if str(p) in d and d[str(p)]["estado"] not in ("parado",):
            sys.exit(f"já está na produção: {d[str(p)]['estado']}")
        d[str(p)] = {"estado": st, "entrou": f"{datetime.now():%Y-%m-%d %H:%M:%S}", "desde": f"{datetime.now():%Y-%m-%d %H:%M}"}
    log(f"{p.name}: entrou na produção ({st})")


def retomar(pasta):
    p = Path(pasta).resolve()
    with Estado() as d:
        if str(p) not in d:
            sys.exit("não está na produção (use --add)")
        it = d[str(p)]
        it.update(estado="na_fila" if na_fila(p) else estado_inicial(p), desde=f"{datetime.now():%Y-%m-%d %H:%M}")
        for k in ("motivo", "tentativas", "tentar_apos"):
            it.pop(k, None)
    log(f"{p.name}: retomada ({it['estado']})")


def status():
    with Estado() as d:
        itens = dict(d)
    if not itens:
        print("produção vazia"); return
    for k, v in sorted(itens.items(), key=lambda kv: kv[1]["entrou"]):
        print(f"{v['estado']:<17} {v['desde']}  {Path(k).name}" + (f"\n{'':<18}motivo: {v['motivo'][:160]}" if v.get("motivo") else ""))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        rodada()
    elif a[0] == "--add" and len(a) == 2:
        add(a[1])
    elif a[0] == "--retomar" and len(a) == 2:
        retomar(a[1])
    elif a[0] == "--status":
        status()
    else:
        sys.exit(__doc__)
