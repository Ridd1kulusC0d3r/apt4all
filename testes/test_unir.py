"""Regra de junção de aliases (unir) com dados sintéticos."""
import unittest
from _base import modulo

cd = modulo("ferramentas/atlas/construir_dados.py", "construir_dados")


def base(*regs):
    r = cd.Registros()
    for x in regs:
        r.add(**x)
    return r


class TestUnir(unittest.TestCase):
    def grupos(self, reg):
        return sorted(sorted(x["nome"] for x in c) for c in cd.unir(reg))

    def test_alias_une_registro_ao_ancora(self):
        reg = base(dict(fonte="mitre", nome="APT28", aliases=["Fancy Bear", "Sofacy"], mitre="G0007"),
                   dict(fonte="misp", nome="Sofacy", aliases=["APT28", "Fancy Bear"]))
        self.assertEqual(self.grupos(reg), [["APT28", "Sofacy"]])

    def test_id_mitre_une(self):
        reg = base(dict(fonte="mitre", nome="APT29", aliases=[], mitre="G0016"),
                   dict(fonte="planilha", nome="Nome Qualquer", aliases=[], mitre="G0016"))
        self.assertEqual(len(cd.unir(reg)), 1)

    def test_alias_ambiguo_nao_une(self):
        reg = base(dict(fonte="mitre", nome="Lazarus Group", aliases=["Hidden Cobra"], mitre="G0032"),
                   dict(fonte="mitre", nome="Andariel", aliases=["Hidden Cobra"], mitre="G0138"),
                   dict(fonte="misp", nome="Registro Solto", aliases=["Hidden Cobra"]))
        self.assertEqual(len(cd.unir(reg)), 3)

    def test_aliases_em_dois_atores_nao_une(self):
        reg = base(dict(fonte="mitre", nome="APT28", aliases=[], mitre="G0007"),
                   dict(fonte="mitre", nome="APT29", aliases=[], mitre="G0016"),
                   dict(fonte="eternalliberty", nome="Mistura", aliases=["APT28", "APT29"]))
        self.assertEqual(len(cd.unir(reg)), 3)

    def test_sem_cascata(self):
        # A~B por um alias e B~C por outro não pode puxar C para dentro de A via registro de fonte inferior
        reg = base(dict(fonte="mitre", nome="A", aliases=["x1"], mitre="G0001"),
                   dict(fonte="mitre", nome="C", aliases=["x2"], mitre="G0002"),
                   dict(fonte="misp", nome="B", aliases=["x1", "x2"]))
        self.assertEqual(len(cd.unir(reg)), 3)


class TestUtilidades(unittest.TestCase):
    def test_norm(self):
        self.assertEqual(cd.norm("Fancy Bear"), cd.norm("fancy-bear"))

    def test_divide(self):
        self.assertEqual(cd.divide("A, B; C\nD"), ["A", "B", "C", "D"])

    def test_conserta_mojibake(self):
        self.assertEqual(cd.conserta("Boyusec â€“ Guangzhou"), "Boyusec – Guangzhou")

    def test_setores_canonicos(self):
        self.assertIn("finance", cd.setores_canonicos(["Banking and financial institutions"]))
        self.assertIn("government", cd.setores_canonicos(["Government, Administration"]))

    def test_slug(self):
        self.assertEqual(cd.slug("Lazarus Group"), "lazarus-group")

    def test_fornecedor(self):
        self.assertEqual(cd.fornecedor("Crowdstrike"), "CrowdStrike")
        self.assertEqual(cd.fornecedor("Cisco (Sourcefire/VRT > Talos)"), "Cisco Talos")
        self.assertEqual(cd.fornecedor("Dell Secure Works"), "Secureworks")
        self.assertIsNone(cd.fornecedor("Comment"))


if __name__ == "__main__":
    unittest.main()
