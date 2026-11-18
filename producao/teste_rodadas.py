"""Portão do crítico com rodadas (D29), sem chamar modelo. Rode em producao/: python3 -m unittest teste_rodadas"""
import json
import tempfile
import unittest
from pathlib import Path

import rodadas_critico as RC


def aprovado(c):
    n = c["notas"]
    return not c.get("bloqueios") and n[0] >= 8 and sum(n) / len(n) >= 7.5 and min(n) >= 6


def serve(c):
    n = c["notas"]
    return not c.get("bloqueios") and n[0] >= 7 and sum(n) / len(n) >= 7.5 and min(n) >= 6


BOM, QUASE, FRACO = [8] * 7, [7, 8, 8, 8, 8, 8, 7], [6] * 7
FALAS = ["o seu assistente mente para você todo dia", "ele diz pronto sem ter feito nada", "veja como cobrar prova"]


class Base(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory(); self.addCleanup(t.cleanup)
        self.d = Path(t.name); self.fonte = self.d / "ficha.yaml"; self.chamadas = 0; self.fila = []

    def criticar(self):
        self.chamadas += 1
        return {"notas": self.fila.pop(0), "resumo": "r"}

    def rodar(self, texto, falas=FALAS, manchete="SUA IA MENTE", extra=False):
        self.fonte.write_text(texto)
        return RC.portao(self.fonte, self.d / "c.json", self.d / "h.jsonl", self.d / "copias", RC.nucleo(falas, manchete),
                         aprovado, serve, self.criticar, extra=extra)


class Mudanca(unittest.TestCase):
    base = RC.nucleo(FALAS, "SUA IA MENTE")

    def test_troca_minima_mantem(self):
        ok, _ = RC.mudanca(self.base, RC.nucleo(["seu assistente mente para você todo dia"] + FALAS[1:], "Sua IA mente"))
        self.assertTrue(ok)

    def test_manchete_abertura_tamanho_e_numero_voltam(self):
        casos = [RC.nucleo(FALAS, "OUTRA MANCHETE"),
                 RC.nucleo(["agora tudo mudou de vez para você hoje"] + FALAS[1:], "SUA IA MENTE"),
                 RC.nucleo(FALAS[:2] + [FALAS[2] + " com um plano novo que muda toda a sua rotina de hoje"], "SUA IA MENTE"),
                 RC.nucleo(FALAS[:2] + ["veja como cobrar sete provas"], "SUA IA MENTE"),
                 RC.nucleo(FALAS, "SUA IA MENTE", ["painel 42%"])]
        for atual in casos:
            self.assertFalse(RC.mudanca(self.base, atual)[0], atual)


class Portao(Base):
    def test_aprovado_fica_aprovado_com_ajuste_pequeno(self):
        self.fila = [BOM]
        self.rodar("v1")
        c, notas = self.rodar("v2 só muda a cor")
        self.assertEqual(self.chamadas, 1)
        self.assertTrue(aprovado(c)); self.assertEqual(len(c["ajustes"]), 1); self.assertIn("mantida", notas[0])

    def test_mudanca_grande_depois_de_aprovado_volta_ao_critico(self):
        self.fila = [BOM, BOM]
        self.rodar("v1")
        self.rodar("v2", manchete="OUTRA COISA")
        self.assertEqual(self.chamadas, 2)

    def test_terceira_rodada_segue_marcada_se_cumpre_regua_minima(self):
        self.fila = [FRACO, FRACO, QUASE]
        self.rodar("v1"); self.rodar("v2")
        c, _ = self.rodar("v3")
        self.assertEqual(c["saida"], "sugestao")
        self.assertEqual(self.rodar("v3")[0]["saida"], "sugestao"); self.assertEqual(self.chamadas, 3)

    def test_teto_para_sem_chamar_critico(self):
        self.fila = [FRACO, FRACO, FRACO]
        for v in ("v1", "v2", "v3"):
            c, _ = self.rodar(v)
        self.assertNotIn("saida", c)
        with self.assertRaises(RC.Parado):
            self.rodar("v4")
        self.assertEqual(self.chamadas, 3)

    def test_versao_anterior_que_serve_pode_voltar_sem_critica(self):
        self.fila = [QUASE, FRACO, FRACO]
        for v in ("v1", "v2", "v3"):
            self.rodar(v)
        with self.assertRaises(RC.Parado) as e:
            self.rodar("v4")
        self.assertIn("rodada 1", str(e.exception))
        c, _ = self.rodar((self.d / "copias/ficha-1.yaml").read_text())
        self.assertEqual(c["saida"], "sugestao"); self.assertEqual(self.chamadas, 3)

    def test_rodada_extra_so_com_ordem(self):
        self.fila = [FRACO, FRACO, FRACO, BOM]
        for v in ("v1", "v2", "v3"):
            self.rodar(v)
        self.assertTrue(aprovado(self.rodar("v4", extra=True)[0]))

    def test_critica_antiga_vira_rodada_um_e_historico_guarda_tudo(self):
        (self.d / "c.json").write_text(json.dumps({"notas": FRACO, "hash": "velho"}))
        self.fila = [FRACO]
        c, _ = self.rodar("v1")
        self.assertEqual(c["rodada"], 2)
        h = RC.carregar(self.d / "h.jsonl")
        self.assertEqual([e["rodada"] for e in h], [1, 2]); self.assertTrue((self.d / "copias/ficha-2.yaml").exists())


if __name__ == "__main__":
    unittest.main()
