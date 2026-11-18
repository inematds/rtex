"""Portão do crítico com memória de rodadas (Nei, 18/11/2026: "sim aprovado pode fazer").

Mesmo arquivo no r7ex e no rtex. Medido em 829 críticas do r7ex: depois da 3ª rodada a nota para de subir, e 182 críticas
vieram de ficha já aprovada. Regras:
- aprovado fica aprovado: ajuste pequeno não volta ao crítico, fica anotado em `ajustes`;
- versão já julgada não é julgada de novo (o histórico guarda o veredito por hash);
- no máximo 3 rodadas; depois delas segue, marcada `saida: sugestao`, a versão sem bloqueio que cumpre a régua mínima;
  as outras param para o Nei. CRITICO_RODADA_EXTRA=1 só com ordem dele.
"""
import difflib
import hashlib
import json
import re
import shutil
import time
import unicodedata
from pathlib import Path

TETO_RODADAS = 3
MAX_PALAVRAS, MAX_PALAVRAS_ABERTURA = 8, 3   # acima disso é mudança de roteiro, volta ao crítico
EXTENSO = set("""dois duas tres quatro cinco seis sete oito nove dez onze doze treze catorze quatorze quinze dezesseis
dezessete dezoito dezenove vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem cento duzentos duzentas
trezentos trezentas quatrocentos quatrocentas quinhentos quinhentas seiscentos seiscentas setecentos setecentas
oitocentos oitocentas novecentos novecentas mil milhao milhoes bilhao bilhoes trilhao trilhoes""".split())


class Parado(Exception):
    """Teto de rodadas: nenhuma crítica nova sem decisão do Nei."""


def _norm(s):
    s = unicodedata.normalize("NFD", str(s or "")).lower()
    return "".join(c for c in s if not unicodedata.combining(c))


def palavras(s):
    return re.findall(r"\d+(?:[.,]\d+)*|[a-z]+(?:-[a-z]+)*", _norm(s))


def numeros(textos):
    achados = set()
    for t in textos:
        for w in palavras(t):
            if w[0].isdigit():
                achados.add(re.sub(r"[.,]", "", w))
            elif w in EXTENSO:
                achados.add(w)
    return achados


def nucleo(falas, manchete, textos=()):
    """O que o crítico aprovou de fato: fala, manchete e os números que aparecem na peça."""
    falas = [str(x).strip() for x in falas]
    return {"falas": falas, "manchete": " ".join(palavras(manchete)),
            "numeros": sorted(numeros(list(falas) + [manchete] + list(textos)))}


def _trocadas(a, b):
    x, y = palavras(a), palavras(b)
    ops = difflib.SequenceMatcher(None, x, y, autojunk=False).get_opcodes()
    return sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in ops if op != "equal")


def mudanca(base, atual):
    """(True, motivo) se a mudança é pequena o bastante para manter a aprovação."""
    if len(base["falas"]) != len(atual["falas"]):
        return False, "mudou o número de partes"
    if base["manchete"] != atual["manchete"]:
        return False, "mudou a manchete"
    novos = sorted(set(atual["numeros"]) - set(base["numeros"]))
    if novos:
        return False, "número novo: " + ", ".join(novos)
    por_parte = [_trocadas(a, b) for a, b in zip(base["falas"], atual["falas"])]
    total = sum(por_parte)
    if por_parte and por_parte[0] > MAX_PALAVRAS_ABERTURA:
        return False, f"{por_parte[0]} palavras trocadas na abertura"
    if total > MAX_PALAVRAS:
        return False, f"{total} palavras trocadas na fala"
    return True, f"{total} palavra(s) trocada(s) na fala" if total else "fala igual, só tela ou metadados"


def carregar(arq):
    arq = Path(arq)
    if not arq.exists():
        return []
    return [json.loads(x) for x in arq.read_text().splitlines() if x.strip()]


def registrar(arq, item):
    with open(arq, "a") as s:
        s.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **item}, ensure_ascii=False) + "\n")


def abertas(hist):
    """Rodadas reprovadas desde a última aprovação ou saída."""
    n = 0
    for e in hist:
        if e.get("tipo") == "saida" or (e.get("tipo") == "critica" and e.get("passou")):
            n = 0
        elif e.get("tipo") == "critica":
            n += 1
    return n


def _copia(copias, fonte, rodada):
    fonte = Path(fonte)
    return Path(copias) / f"{fonte.stem}-{rodada}{fonte.suffix}"


def _reaproveitaveis(hist, copias, fonte, serve):
    return [e["rodada"] for e in hist[-TETO_RODADAS * 4:] if e.get("tipo") == "critica" and serve(e["critica"])
            and _copia(copias, fonte, e["rodada"]).exists()]


def portao(fonte, critica, historico, copias, nuc, aprovado, serve, criticar, extra=False):
    """Devolve (crítica, notas para o log). `criticar()` só é chamado quando há o que julgar; levanta Parado no teto."""
    fonte, critica, historico = Path(fonte), Path(critica), Path(historico)
    h = hashlib.sha1(fonte.read_bytes()).hexdigest()
    c = json.loads(critica.read_text()) if critica.exists() else {}
    notas = []
    if not historico.exists() and c.get("notas"):   # edição anterior a este portão: a crítica em disco é a rodada 1
        registrar(historico, {"tipo": "critica", "rodada": 1, "hash": c.get("hash"), "notas": c["notas"],
                              "passou": aprovado(c), "resumo": c.get("resumo"), "critica": c})
    hist = carregar(historico)
    if c.get("hash") != h:
        ja = next((e for e in reversed(hist) if e.get("tipo") == "critica" and e.get("hash") == h), None)
        base = c.get("nucleo_aprovado") if c.get("notas") and (aprovado(c) or c.get("saida") == "sugestao") else None
        pequena, motivo = mudanca(base, nuc) if base else (False, "")
        if ja:
            c = dict(ja["critica"], hash=h)
            notas.append(f"versão já julgada na rodada {ja['rodada']}: sem crítica nova")
        elif pequena:
            c["hash"] = h
            c.setdefault("ajustes", []).append({"ts": time.strftime("%Y-%m-%d %H:%M"), "motivo": motivo})
            registrar(historico, {"tipo": "ajuste", "hash": h, "motivo": motivo})
            notas.append(f"aprovação mantida: ajuste pequeno ({motivo})")
        else:
            n = abertas(hist)
            if n >= TETO_RODADAS and not extra:
                volta = _reaproveitaveis(hist, copias, fonte, serve)
                dica = (f" A rodada {volta[-1]} cumpre a régua mínima: cp {_copia(copias, fonte, volta[-1])} {fonte} e rode de novo."
                        if volta else " Nenhuma versão cumpriu a régua mínima.")
                raise Parado(f"teto de {TETO_RODADAS} rodadas do crítico.{dica} Troque o ângulo com o Nei; rodada extra só com "
                             "ordem dele (CRITICO_RODADA_EXTRA=1).")
            c = criticar()
            c["hash"], c["rodada"] = h, n + 1
            Path(copias).mkdir(exist_ok=True)
            shutil.copyfile(fonte, _copia(copias, fonte, n + 1))
            registrar(historico, {"tipo": "critica", "rodada": n + 1, "hash": h, "notas": c["notas"],
                                  "bloqueios": c.get("bloqueios") or [], "passou": aprovado(c),
                                  "resumo": c.get("resumo"), "critica": c})
            hist = carregar(historico)
    n = abertas(hist)
    if aprovado(c):
        c.pop("saida", None)
        c.setdefault("nucleo_aprovado", nuc)
    elif c.get("saida") != "sugestao":
        if n >= TETO_RODADAS and serve(c):
            c["saida"] = "sugestao"
            c.setdefault("nucleo_aprovado", nuc)
            registrar(historico, {"tipo": "saida", "hash": h, "notas": c["notas"]})
        elif n >= TETO_RODADAS:
            volta = _reaproveitaveis(hist, copias, fonte, serve)
            notas.append(f"teto de {TETO_RODADAS} rodadas atingido" + (
                f"; a rodada {volta[-1]} cumpre a régua mínima: cp {_copia(copias, fonte, volta[-1])} {fonte}" if volta else
                "; nenhuma versão cumpriu a régua mínima: pare e leve ao Nei"))
        else:
            notas.append(f"rodada {n} de {TETO_RODADAS}")
    critica.write_text(json.dumps(c, ensure_ascii=False, indent=1))
    return c, notas
