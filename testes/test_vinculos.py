"""Força e fatores do vínculo (docs/atlas/vinculos.js). Roda o módulo no Node; sem Node, os testes são pulados."""
import json
import os
import shutil
import subprocess
import unittest
from _base import RAIZ

NODE = shutil.which("node")
JS = os.path.join(RAIZ, "docs", "atlas", "vinculos.js")

SCRIPT = r"""
const V = require(process.argv[1]);
const mk = (id, o) => Object.assign({id, nome: id, aliases: [], mitre: null, ferramentas: [], relatorios: [], setores: [], motivos: [], pais: "??"}, o || {});
const raro = mk("a", {mitre: {tecnicas: ["T1", "T9"]}}), raro2 = mk("b", {mitre: {tecnicas: ["T1", "T8"]}});
const comum = Array.from({length: 20}, (_, i) => mk("c" + i, {mitre: {tecnicas: ["T7", "T" + (100 + i)]}}));
const todos = [raro, raro2, ...comum];
const ctx = V.contexto(todos);
const out = {};
out.pesos = V.FATORES.reduce((s, f) => s + f.peso, 0);
out.simetrico = V.vinculo(raro, raro2, ctx).score === V.vinculo(raro2, raro, ctx).score;
out.rara = V.vinculo(raro, raro2, ctx).score;            // compartilham T1, que só eles têm
out.comum = V.vinculo(comum[0], comum[1], ctx).score;    // compartilham T7, que todo mundo tem
const so_pais = [mk("p", {pais: "CN", motivos: ["espionagem"], setores: ["gov"]}), mk("q", {pais: "CN", motivos: ["espionagem"], setores: ["gov"]})];
out.so_contexto = V.vinculo(so_pais[0], so_pais[1], V.contexto(so_pais)).nivel;   // país, motivo e setor sozinhos não são vínculo
const nomes = [mk("x", {nome: "X", aliases: ["Grizzly"]}), mk("y", {nome: "Y", aliases: ["grizzly"]})];
out.alias = V.vinculo(nomes[0], nomes[1], V.contexto(nomes)).fatores.find(f => f.id === "nomes").evidencia;
out.nivel_ordem = V.LIMIAR.fraco < V.LIMIAR.medio && V.LIMIAR.medio < V.LIMIAR.forte;
const rel = V.relacionados(raro, todos, ctx, 3);
out.rel_ordenado = rel.every((v, i) => i === 0 || rel[i - 1].score >= v.score);
console.log(JSON.stringify(out));
"""


@unittest.skipUnless(NODE, "Node não instalado")
class TestVinculos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r = subprocess.run([NODE, "-e", SCRIPT, JS], capture_output=True, text=True, timeout=60)
        if r.returncode:
            raise AssertionError(r.stderr)
        cls.o = json.loads(r.stdout)

    def test_pesos_somam_100(self):
        self.assertEqual(self.o["pesos"], 100)

    def test_simetria(self):
        self.assertTrue(self.o["simetrico"])

    def test_tecnica_rara_pesa_mais_que_a_comum(self):
        self.assertGreater(self.o["rara"], self.o["comum"])

    def test_pais_motivo_setor_sozinhos_nao_ligam(self):
        self.assertEqual(self.o["so_contexto"], "nenhum")

    def test_alias_em_comum_aparece_como_evidencia(self):
        self.assertEqual(self.o["alias"], ["grizzly"])

    def test_limiares_e_ordem(self):
        self.assertTrue(self.o["nivel_ordem"])
        self.assertTrue(self.o["rel_ordenado"])


if __name__ == "__main__":
    unittest.main()
