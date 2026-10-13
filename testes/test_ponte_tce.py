"""Ponte APT4ALL -> TCE Horizon (perfil_ameaca.py)."""
import csv, json, os, shutil, tempfile, unittest


def carrega(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def linhas_csv(caminho):
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f))
from _base import json_de, modulo

pa = modulo("ferramentas/tce/perfil_ameaca.py", "perfil_ameaca")

SINT = [
    {"id": "a", "nome": "Alfa", "pais": "XX", "vitimas": ["Brazil"], "setores": ["finance"], "alvos": "",
     "mitre": {"id": "G9001", "tecnicas": ["T1566", "T1078"]}},
    {"id": "b", "nome": "Bravo", "pais": None, "vitimas": [], "setores": ["finance"], "alvos": "",
     "mitre": None},
    {"id": "c", "nome": "Charlie", "pais": "YY", "vitimas": ["Chile"], "setores": ["energy"], "alvos": "",
     "mitre": {"id": "G9002", "tecnicas": ["T1566"]}},
]


class TestCalcula(unittest.TestCase):
    def test_pontuacao(self):
        res, tec = pa.calcula(SINT, "Brazil", "finance")
        self.assertEqual([x["ator"]["nome"] for x in res], ["Alfa", "Bravo"])
        self.assertEqual(res[0]["score"], 5)   # país 2 + setor 2 + ATT&CK 1
        self.assertEqual(res[1]["score"], 2)
        self.assertEqual(dict(tec), {"T1566": 5, "T1078": 5})

    def test_origem_estado(self):
        res, _ = pa.calcula(SINT, "", "finance", "estado")
        self.assertEqual([x["ator"]["nome"] for x in res], ["Alfa"])

    def test_sem_filtro_inclui_todos(self):
        res, _ = pa.calcula(SINT)
        self.assertEqual(len(res), 3)


class TestExporta(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_arquivos_e_trava_de_revisao(self):
        res, tec = pa.calcula(SINT, "Brazil", "finance")
        sid = pa.exporta(res, tec, {"gerado_em": "2026-10-13", "attack_versao": "19.2"}, "Brazil", "finance", self.d)
        self.assertEqual(sid, "SIG-APT4ALL-BRAZIL-FINANCE")
        for f in ("navigator.json", "tce-sinais.json", "tce-intelligence.csv", "perfil.md"):
            self.assertTrue(os.path.exists(os.path.join(self.d, f)), f)
        s = carrega(os.path.join(self.d, "tce-sinais.json"))
        self.assertFalse(s["auto_accept"])
        c = s["intelligence_signal_candidates"][0]
        self.assertEqual(c["status"], "candidate")
        self.assertTrue(c["review_required"])
        self.assertEqual(c["confidence"], "low")
        self.assertEqual(c["technique_ids"], ["T1566", "T1078"])
        linhas = linhas_csv(os.path.join(self.d, "tce-intelligence.csv"))
        self.assertEqual(linhas[0]["status"], "candidate")
        self.assertEqual(linhas[0]["technique_ids"], "T1566;T1078")
        nav = carrega(os.path.join(self.d, "navigator.json"))
        self.assertEqual(nav["domain"], "enterprise-attack")
        self.assertEqual(nav["versions"]["attack"], "19")

    def test_base_real(self):
        d = json_de("docs", "atlas", "atores.json")
        res, tec = pa.calcula(d["atores"], "United States", "government")
        self.assertGreater(len(res), 50)
        self.assertGreater(len(tec), 50)


class TestIntegracaoTCE(unittest.TestCase):
    """Roda só se o pacote tce estiver instalado (pip install -e Cyber-Threat-Context-Modeling)."""

    def test_trava_de_revisao_no_horizon(self):
        try:
            from datetime import datetime, timezone
            from tce import horizon
        except Exception:
            self.skipTest("tce não instalado")
        if not hasattr(horizon, "_intelligence_pressure"):
            self.skipTest("versão do tce sem _intelligence_pressure")
        res, tec = pa.calcula(SINT, "Brazil", "finance")
        d = tempfile.mkdtemp()
        try:
            pa.exporta(res, tec, {"gerado_em": "2026-10-13", "attack_versao": "19.2"}, "Brazil", "finance", d)
            sinal = carrega(os.path.join(d, "tce-sinais.json"))["intelligence_signal_candidates"][0]
        finally:
            shutil.rmtree(d)
        agora = datetime(2026, 10, 13, tzinfo=timezone.utc)
        cand, _ = horizon._intelligence_pressure({"intelligence_signals": [sinal]}, ["n1"], {"T1566"}, agora)
        self.assertEqual(cand, 0.0)          # candidato não pesa
        aceito = dict(sinal, status="accepted")
        valor, contrib = horizon._intelligence_pressure({"intelligence_signals": [aceito]}, ["n1"], {"T1566"}, agora)
        self.assertGreater(valor, 0.0)       # aceito pesa
        self.assertEqual(contrib[0]["id"], "SIG-APT4ALL-BRAZIL-FINANCE")


if __name__ == "__main__":
    unittest.main()
