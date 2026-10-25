import datetime as dt
import importlib.util
import json
import pathlib
import tempfile
import unittest

_p = pathlib.Path(__file__).resolve().parent.parent / "ferramentas/feed/ingerir_kev.py"
_s = importlib.util.spec_from_file_location("ingerir_kev", _p)
kev = importlib.util.module_from_spec(_s)
_s.loader.exec_module(kev)

CAT = {"catalogVersion": "t", "count": 3, "vulnerabilities": [
    {"cveID": "CVE-1", "vendorProject": "A", "product": "p", "vulnerabilityName": "n1", "dateAdded": "2026-10-20",
     "shortDescription": "d", "knownRansomwareCampaignUse": "Known", "notes": "https://x.test/a ; https://x.test/b"},
    {"cveID": "CVE-2", "vendorProject": "B", "product": "q", "vulnerabilityName": "n2", "dateAdded": "2026-01-01",
     "shortDescription": "d", "notes": ""},
    {"cveID": "CVE-3", "vendorProject": "C", "product": "r", "vulnerabilityName": "n3", "dateAdded": "2026-10-23",
     "shortDescription": "d", "notes": ""}]}
ATR = {"cve": "CVE-2", "atores": ["Qilin"], "tipo": "ransomware", "uso": "u", "atribuido_por": "x",
       "confianca": "alta", "fontes": ["https://x.test/f"]}


class TestFeed(unittest.TestCase):
    def test_janela_corta_e_mantem_curados(self):
        hoje = dt.date(2026, 10, 23)
        ids = [v["cveID"] for v in kev.janela(CAT, 30, hoje)]
        self.assertEqual(ids, ["CVE-3", "CVE-1"])
        ids = [v["cveID"] for v in kev.janela(CAT, 30, hoje, {"CVE-2"})]
        self.assertIn("CVE-2", ids)

    def test_compacta_notas(self):
        self.assertEqual(kev.compacta(CAT["vulnerabilities"][0])["notes"], ["https://x.test/a", "https://x.test/b"])

    def test_valida_atribuicao(self):
        self.assertEqual(kev.valida_atribuicoes([ATR]), [])
        self.assertTrue(kev.valida_atribuicoes([{**ATR, "fontes": ["http://x"]}]))
        self.assertTrue(kev.valida_atribuicoes([{**ATR, "confianca": "certeza"}]))
        self.assertTrue(kev.valida_atribuicoes([{k: v for k, v in ATR.items() if k != "fontes"}]))

    def test_junta_resolve_ator_por_alias(self):
        idx = kev.indice_atores([{"id": "qilin", "nome": "Qilin", "aliases": ["Agenda"]}])
        itens = kev.junta([kev.compacta(CAT["vulnerabilities"][1])], [ATR], idx)
        self.assertEqual(itens[0]["atribuicao"]["atores"], [{"nome": "Qilin", "id": "qilin"}])

    def test_ator_desconhecido_fica_sem_id(self):
        itens = kev.junta([kev.compacta(CAT["vulnerabilities"][1])], [{**ATR, "atores": ["Settra"]}], {})
        self.assertIsNone(itens[0]["atribuicao"]["atores"][0]["id"])

    def test_ponta_a_ponta_e_novos(self):
        with tempfile.TemporaryDirectory() as d:
            raiz = pathlib.Path(d)
            (raiz / "dados/feed").mkdir(parents=True)
            (raiz / "docs/atlas").mkdir(parents=True)
            json.dump({"atribuicoes": [ATR]}, open(raiz / "dados/feed/atribuicoes.json", "w"))
            json.dump({"atores": [{"id": "qilin", "nome": "Qilin", "aliases": []}]}, open(raiz / "docs/atlas/atores.json", "w"))
            arq = raiz / "kev.json"
            json.dump(CAT, open(arq, "w"))
            self.assertEqual(kev.main(["--arquivo", str(arq), "--raiz", d, "--dias", "30"]), 0)
            self.assertEqual((raiz / "dados/feed/novidades.md").read_text().count("CVE-"), 0)
            CAT2 = json.loads(json.dumps(CAT))
            CAT2["vulnerabilities"].append({"cveID": "CVE-9", "vendorProject": "Z", "product": "z", "vulnerabilityName": "n9",
                                            "dateAdded": "2026-10-24", "shortDescription": "d", "notes": ""})
            json.dump(CAT2, open(arq, "w"))
            kev.main(["--arquivo", str(arq), "--raiz", d, "--dias", "30"])
            self.assertIn("CVE-9", (raiz / "dados/feed/novidades.md").read_text())
            feed = json.load(open(raiz / "docs/feed/feed.json"))
            self.assertEqual(feed["meta"]["n_atribuidos"], 1)
            self.assertIn("<entry>", (raiz / "docs/feed/atom.xml").read_text())

    def test_catalogo_vazio_aborta(self):
        with tempfile.TemporaryDirectory() as d:
            arq = pathlib.Path(d) / "k.json"
            json.dump({"vulnerabilities": []}, open(arq, "w"))
            self.assertEqual(kev.main(["--arquivo", str(arq), "--raiz", d]), 1)


if __name__ == "__main__":
    unittest.main()
