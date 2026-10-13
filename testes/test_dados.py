"""Sanidade da base gerada (docs/atlas/*.json)."""
import unittest
from collections import Counter
from _base import json_de

A = json_de("docs", "atlas", "atores.json")
P = json_de("docs", "atlas", "paises.json")
M = json_de("docs", "atlas", "mapa.json")
POR_NOME = {a["nome"]: a for a in A["atores"]}


class TestAtores(unittest.TestCase):
    def test_volume(self):
        self.assertGreater(len(A["atores"]), 1000)
        self.assertEqual(A["meta"]["n_atores"], len(A["atores"]))

    def test_ids_unicos(self):
        ids = [a["id"] for a in A["atores"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_campos(self):
        obrig = {"id", "nome", "aliases", "pais", "motivos", "mitre", "setores", "vitimas", "fontes", "fornecedores"}
        for a in A["atores"][:200]:
            self.assertTrue(obrig <= set(a), a["nome"])

    def test_atribuicoes_conhecidas(self):
        for nome, pais in [("APT28", "RU"), ("APT29", "RU"), ("Lazarus Group", "KP"), ("OilRig", "IR"), ("APT41", "CN")]:
            self.assertIn(nome, POR_NOME)
            self.assertEqual(POR_NOME[nome]["pais"], pais, nome)

    def test_sem_super_juncao(self):
        # grupos distintos no ATT&CK não podem ter virado um ator só
        g = Counter(a["mitre"]["id"] for a in A["atores"] if a["mitre"])
        self.assertEqual([k for k, n in g.items() if n > 1], [])
        self.assertNotIn("Cozy Bear", POR_NOME["APT28"]["aliases"])
        self.assertNotEqual(POR_NOME["Lazarus Group"]["id"], POR_NOME.get("Kimsuky", {}).get("id"))

    def test_nomes_por_fornecedor(self):
        f = POR_NOME["APT28"]["fornecedores"]
        self.assertEqual(f["MITRE ATT&CK"], ["G0007"])
        self.assertEqual(f["Microsoft"][0], "Forest Blizzard")

    def test_tecnicas_formato(self):
        import re
        for a in A["atores"]:
            if a["mitre"]:
                for t in a["mitre"]["tecnicas"]:
                    self.assertRegex(t, r"^T\d{4}(\.\d{3})?$")


class TestPaisesMapa(unittest.TestCase):
    def test_contagem_bate(self):
        c = Counter(a["pais"] or "??" for a in A["atores"])
        for iso, p in P["paises"].items():
            self.assertEqual(p["atores"], c[iso], iso)

    def test_setores_rotulados(self):
        usados = {s for a in A["atores"] for s in a["setores"]}
        self.assertTrue(usados <= set(P["setores"]))
        for k, v in P["setores"].items():
            self.assertTrue(v["pt"] and v["en"], k)

    def test_mapa(self):
        self.assertGreater(len(M["hex"]), 3000)
        isos = {h[2] for h in M["hex"]}
        self.assertIn("BR", isos)
        self.assertTrue(isos <= set(P["geo"]))


if __name__ == "__main__":
    unittest.main()
