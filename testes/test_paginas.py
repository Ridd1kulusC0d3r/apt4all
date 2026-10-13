"""Páginas estáticas: arquivos referenciados existem e os dicionários PT/EN têm as mesmas chaves."""
import os, re, unittest
from _base import RAIZ

DOCS = os.path.join(RAIZ, "docs")


def ler(*p):
    with open(os.path.join(DOCS, *p), encoding="utf-8") as f:
        return f.read()


def chaves(bloco):
    return set(re.findall(r'(?:^|[,{]\s*)"?([A-Za-zÀ-ú_][\wÀ-ú]*)"?\s*:', bloco))


class TestPaginas(unittest.TestCase):
    def test_existem(self):
        for p in ("index.html", "atlas/index.html", "recursos/index.html", "manual/index.html"):
            self.assertTrue(os.path.exists(os.path.join(DOCS, p)), p)

    def test_atlas_busca_arquivos(self):
        s = ler("atlas", "index.html")
        for f in ("atores.json", "paises.json", "mapa.json"):
            self.assertIn(f, s)
            self.assertTrue(os.path.exists(os.path.join(DOCS, "atlas", f)))

    def test_atlas_bilingue(self):
        s = ler("atlas", "index.html")
        pt = s[s.index(" pt:{"):s.index(" en:{")]
        en = s[s.index(" en:{"):s.index("};", s.index(" en:{"))]
        self.assertEqual(chaves(pt) - chaves(en), set())
        self.assertEqual(chaves(en) - chaves(pt), set())

    def test_data_t_tem_traducao(self):
        s = ler("atlas", "index.html")
        en = s[s.index(" en:{"):s.index("};", s.index(" en:{"))]
        for k in set(re.findall(r'data-t="([^"]+)"', s)):
            self.assertIn(k, chaves(en), k)

    def test_sem_localstorage_sem_try(self):
        for p in ("index.html", "atlas/index.html", "recursos/index.html"):
            s = ler(*p.split("/"))
            for m in re.finditer(r"localStorage\.\w+", s):
                trecho = s[max(0, m.start() - 120):m.start()]
                self.assertIn("try", trecho, p)


if __name__ == "__main__":
    unittest.main()


class TestLinksInternos(unittest.TestCase):
    """Todo link relativo entre as páginas de docs/ aponta para um arquivo (e uma âncora) que existe."""

    def test_links_relativos(self):
        import glob
        from urllib.parse import unquote
        quebrados = []
        for fn in glob.glob(os.path.join(DOCS, "**", "*.html"), recursive=True):
            with open(fn, encoding="utf-8") as f:
                s = f.read()
            for ref in re.findall(r'(?:href|src)="([^"]+)"', s):
                if re.match(r"^(https?:|mailto:|data:|javascript:|\$\{)", ref) or "${" in ref:
                    continue
                alvo, _, anc = ref.partition("#")
                destino = os.path.normpath(os.path.join(os.path.dirname(fn), unquote(alvo))) if alvo else fn
                if os.path.isdir(destino):
                    if not os.path.exists(os.path.join(destino, "index.html")):
                        continue  # prefixo de caminho montado em JavaScript (ex.: "img/" + nome)
                    destino = os.path.join(destino, "index.html")
                if not os.path.exists(destino):
                    quebrados.append((os.path.relpath(fn, DOCS), ref))
                    continue
                if anc and destino.endswith(".html") and not destino.endswith(os.path.join("atlas", "index.html")):  # o Atlas usa #rota em JS
                    with open(destino, encoding="utf-8") as f:
                        if f'id="{unquote(anc)}"' not in f.read():
                            quebrados.append((os.path.relpath(fn, DOCS), ref))
        self.assertEqual(quebrados, [])
