"""Esquema de recursos/recursos.json e gerador de listas."""
import os, re, tempfile, unittest
from _base import json_de, modulo, RAIZ

R = json_de("recursos", "recursos.json")
TIPOS = {"gratuito", "freemium", "registro", "pago"}


class TestRecursos(unittest.TestCase):
    def test_campos_e_valores(self):
        for r in R["recursos"]:
            with self.subTest(r=r["nome"]):
                self.assertIn(r["cat"], R["categorias"])
                self.assertRegex(r["url"], r"^https?://")
                self.assertTrue(r["desc_pt"].strip() and r["desc_en"].strip())
                self.assertIn(r["tipo"], TIPOS)
                self.assertIn(r["status"], {"ativo", "legado"})
                self.assertIsInstance(r["destaque"], bool)

    def test_urls_unicas(self):
        urls = [r["url"].rstrip("/").lower() for r in R["recursos"]]
        rep = {u for u in urls if urls.count(u) > 1}
        self.assertEqual(rep, set())

    def test_categorias_bilingues(self):
        for k, c in R["categorias"].items():
            self.assertTrue(c["pt"] and c["en"] and c["desc_pt"] and c["desc_en"], k)

    def test_copia_publicada_igual(self):
        self.assertEqual(json_de("docs", "recursos.json"), R)

    def test_gerador(self):
        g = modulo("ferramentas/recursos/gerar_listas.py", "gerar_listas")
        pt, en = g.gera("pt", R, {}), g.gera("en", R, {})
        for r in R["recursos"]:
            self.assertIn(r["url"], pt)
            self.assertIn(r["url"], en)
        self.assertNotEqual(pt, en)


if __name__ == "__main__":
    unittest.main()
