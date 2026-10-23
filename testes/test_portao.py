import importlib.util
import pathlib
import unittest

_p = pathlib.Path(__file__).resolve().parent.parent / "ferramentas/atualizacao/portao.py"
_s = importlib.util.spec_from_file_location("portao", _p)
portao = importlib.util.module_from_spec(_s)
_s.loader.exec_module(portao)


class TestPortao(unittest.TestCase):
    def test_estavel_passa(self):
        e, w, _ = portao.comparar({"n": 100}, {"n": 103}, ["n"])
        self.assertEqual((e, w), ([], []))

    def test_queda_grande_reprova(self):
        e, _, _ = portao.comparar({"n": 100}, {"n": 80}, ["n"])
        self.assertEqual(len(e), 1)

    def test_queda_pequena_tolerada(self):
        e, _, _ = portao.comparar({"n": 100}, {"n": 95}, ["n"])
        self.assertEqual(e, [])

    def test_alta_enorme_avisa(self):
        e, w, _ = portao.comparar({"n": 100}, {"n": 200}, ["n"])
        self.assertEqual((e, len(w)), ([], 1))

    def test_indicador_sumiu_reprova(self):
        e, _, _ = portao.comparar({"n": 100}, {}, ["n"])
        self.assertEqual(len(e), 1)

    def test_fonte_zerada_reprova(self):
        e, _, _ = portao.comparar({"n": 1}, {"n": 1}, ["n"], {"misp": 10}, {"misp": 0})
        self.assertEqual(len(e), 1)


if __name__ == "__main__":
    unittest.main()
