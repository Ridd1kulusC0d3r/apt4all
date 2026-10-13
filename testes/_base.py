"""Utilidades comuns dos testes (só biblioteca padrão)."""
import importlib.util, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def modulo(rel, nome):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(RAIZ, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def json_de(*partes):
    with open(os.path.join(RAIZ, *partes), encoding="utf-8") as f:
        return json.load(f)
