#!/usr/bin/env python3
"""Teste da produção com edições falsas: sem HeyGen, sem Telegram, sem render. `python3 producao/teste_producao.py`"""
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import producao as P  # noqa: E402

tmp = Path(tempfile.mkdtemp(prefix="producao-teste-"))
P.AQUI = tmp; P.ESTADO = tmp / "estado.json"; P.LOG = tmp / "producao.log"; P.FILA = tmp / "fila.json"
P.FILA.write_text("[]")
avisos, chamadas = [], []
P.avisa = lambda m: avisos.append(m)
veredito = {"v": "aprovado"}
P.revisar = lambda p: {"veredito": veredito["v"], "motivo": "teste", **({"sugestoes": veredito["s"]} if veredito.get("s") else {})}
conferidas = {}


def roda(args, timeout, saida=None):
    cmd, pasta = args[0], Path(args[1]); chamadas.append((cmd, pasta.name)); av = pasta / "avatar"
    if cmd == "avatar-enviar":
        (av / "video_id.txt").write_text("x" * 32); return 0, ""
    if cmd == "avatar-conferir":
        conferidas[pasta.name] = conferidas.get(pasta.name, 0) + 1
        if conferidas[pasta.name] < 2 or pasta.name == "d":   # "d" nunca fica pronto
            return 0, "processando"
        (av / "avatar.mp4").write_text("mp4"); return 0, "pronto"
    if cmd == "fazer":
        (pasta / "video.mp4").write_text("v"); return 0, "Terminei"
    if cmd == "enviar":
        return 0, "enviado"
    if cmd == "fila":
        P.FILA.write_text(P.FILA.read_text() + str(pasta / "video.mp4")); return 0, f"na fila do lives4: {pasta.name} (posição 1)"
    raise AssertionError(cmd)


P.roda = roda


def edicao(nome, aprovado=True):
    p = tmp / nome; (p / "avatar").mkdir(parents=True); (p / "roteiro.json").write_text("{\"tema\": \"x\", \"publicar\": {}}")
    if aprovado:
        (p / "avatar/APROVADO_HEYGEN").write_text("ok")
    return p


def estado(p):
    with P.Estado() as d:
        return d[str(p)]["estado"]


ok = 0
def confere(cond, msg):
    global ok
    assert cond, msg
    ok += 1; print("ok:", msg)


# sem APROVADO não entra
sem = edicao("sem-aprovado", aprovado=False)
try:
    P.add(str(sem)); confere(False, "sem APROVADO deveria recusar")
except SystemExit:
    confere(True, "sem APROVADO_HEYGEN não entra na produção")

a, b = edicao("a"), edicao("b")
P.add(str(a)); P.add(str(b))
P.rodada()
confere([c for c in chamadas if c[0] == "avatar-enviar"] == [("avatar-enviar", "a"), ("avatar-enviar", "b")],
        "todas vão ao estúdio na mesma rodada (25/10: não esperar a anterior ficar pronta)")
confere(estado(a) == "esperando_avatar" and estado(b) == "esperando_avatar", "a e b esperando o HeyGen")
P.rodada()   # a: 2ª conferência → pronto → montar → revisão → fila
confere(estado(a) == "na_fila", "a chegou à fila na 2ª rodada")
confere(sum(1 for c in chamadas if c == ("fazer", "a")) == 1, "a montou uma vez")
confere(any(m.startswith("Terminei: rtex a") for m in avisos), "aviso Terminei no v3")
confere(P.FILA.read_text().count(str(a / "video.mp4")) == 1, "a entrou uma vez na fila")

veredito["v"] = "reprovado"
P.rodada(); P.rodada()
confere(estado(b) == "parado", "b reprovado na revisão fica parado")
confere(any(m.startswith("Falhou: rtex b") for m in avisos), "aviso Falhou no v3")
n = len(chamadas); P.rodada()
confere(len(chamadas) == n, "parado não anda sozinho")

veredito["v"] = "aprovado"; veredito["s"] = ["6 s: falta o logo do Copilot", "impacto 6/10"]
P.retomar(str(b)); confere(estado(b) == "montar", "retomar com avatar pronto volta para montar")
P.rodada()
confere(estado(b) == "na_fila", "b com sugestão segue para a fila (21/10: sugestão não para)")
confere(any(m.startswith("Terminei: rtex b") and "SUGESTÃO" in m and "logo do Copilot" in m for m in avisos),
        "aviso Terminei leva a tarja vermelha SUGESTÃO com as sugestões")
veredito.pop("s")

c = edicao("c"); (c / "video.mp4").write_text("v"); P.FILA.write_text(P.FILA.read_text() + str(c / "video.mp4"))
P.add(str(c)); confere(estado(c) == "na_fila", "edição já na fila entra como na_fila (não duplica)")
try:
    P.add(str(a)); confere(False, "add repetido deveria recusar")
except SystemExit:
    confere(True, "add repetido é recusado")

d = edicao("d"); P.add(str(d)); P.rodada()          # vai ao estúdio, fica esperando
with P.Estado() as e:
    e[str(d)]["desde"] = "2000-01-01 00:00"          # esperando há muito tempo; a 1ª conferência diz "processando"
P.rodada()
confere(estado(d) == "parado" and any("não entregou" in m for m in avisos), "avatar que não chega em 6 h para com aviso")

print(f"\n{ok} conferências ok · pasta {tmp}")
