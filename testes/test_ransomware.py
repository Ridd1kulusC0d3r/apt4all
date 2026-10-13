"""Ransomware Tool Matrix (docs/atlas/ransomware.json) e táticas do ATT&CK."""
import unittest
from _base import json_de, modulo

RW = json_de("docs", "atlas", "ransomware.json")
P = json_de("docs", "atlas", "paises.json")
A = {a["id"]: a for a in json_de("docs", "atlas", "atores.json")["atores"]}
rm = modulo("ferramentas/ransomware/construir_matriz.py", "construir_matriz")


class TestRansomware(unittest.TestCase):
    def test_volume_e_licenca(self):
        self.assertGreater(RW["meta"]["n_grupos"], 50)
        self.assertGreater(RW["meta"]["n_ferramentas"], 200)
        self.assertEqual(RW["meta"]["licenca"], "CC BY 4.0")

    def test_categorias_bilingues(self):
        ids = {c["id"] for c in RW["categorias"]}
        self.assertEqual(len(ids), 8)
        for f in RW["ferramentas"]:
            self.assertIn(f["cat"], ids, f["nome"])

    def test_consistencia_grupo_ferramenta(self):
        por_nome = {f["nome"]: set(f["grupos"]) for f in RW["ferramentas"]}
        for g in RW["grupos"]:
            for f in g["ferramentas"]:
                self.assertIn(g["nome"], por_nome[f], (g["nome"], f))

    def test_ligacoes_existem(self):
        for g in RW["grupos"]:
            if g["ator"]:
                self.assertIn(g["ator"], A, g["nome"])

    def test_ligacao_nao_usa_lista_contaminada(self):
        # BlackByte traz Conti/Royal/Black Basta como apelidos na fonte; não pode capturar essas gangues
        por = {g["nome"]: g["ator"] for g in RW["grupos"]}
        for gangue in ("Conti", "Royal", "Black Basta"):
            self.assertNotEqual(por.get(gangue), "blackbyte", gangue)

    def test_tipo_grupo(self):
        self.assertEqual(rm.tipo_grupo("*Prophet Spider"), "iab")
        self.assertEqual(rm.tipo_grupo("Scattered Spider*"), "afiliado")
        self.assertEqual(rm.tipo_grupo("DarkBit+"), "estado")
        self.assertEqual(rm.tipo_grupo("LockBit"), "gangue")


class TestTaticas(unittest.TestCase):
    def test_toda_tecnica_tem_tatica(self):
        ids = {t["id"] for t in P["taticas"]}
        self.assertGreaterEqual(len(ids), 14)
        for tec, tats in P["tecnica_taticas"].items():
            self.assertTrue(tats, tec)
            self.assertTrue(set(tats) <= ids, tec)

    def test_taticas_bilingues(self):
        for t in P["taticas"]:
            self.assertTrue(t["pt"] and t["en"], t["id"])

    def test_vitimas_iso(self):
        a = A["apt28"]
        self.assertTrue(a["vitimas_iso"])
        nomes = set(P["geo"]) | set(P["nomes_extra"])
        for x in A.values():
            self.assertTrue(set(x["vitimas_iso"]) <= nomes, x["nome"])


if __name__ == "__main__":
    unittest.main()
