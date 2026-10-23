#!/usr/bin/env python3
"""Portão de qualidade da atualização automática.

Compara os números da base reconstruída (árvore de trabalho) com os do commit
atual (HEAD). Se algum número essencial cair demais, uma fonte sumir ou o
arquivo ficar ilegível, a atualização NÃO é mesclada sozinha: o PR fica aberto
com o rótulo `revisar` e o relatório abaixo.

Uso:  python3 ferramentas/atualizacao/portao.py [--saida relatorio.md]
Saída: código 0 = pode mesclar; 1 = precisa de revisão humana.
Só biblioteca padrão.
"""
import argparse
import json
import subprocess
import sys

QUEDA_MAX = 0.10      # queda tolerada por indicador (10%)
ALTA_MAX = 0.50       # alta acima disso vira aviso (fonte mudou de formato?)

# arquivo -> indicadores numéricos do bloco "meta"
INDICADORES = {
    "docs/atlas/atores.json": ["n_atores", "n_registros", "n_relatorios"],
    "docs/atlas/ransomware.json": ["n_grupos", "n_ferramentas", "n_usos"],
}


def meta_antiga(caminho):
    """meta do arquivo no HEAD; None se o arquivo ainda não existe lá."""
    r = subprocess.run(["git", "show", f"HEAD:{caminho}"], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout).get("meta", {})


def meta_nova(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f).get("meta", {})


def comparar(antiga, nova, indicadores, fontes_antigas=None, fontes_novas=None):
    """Devolve (erros, avisos, linhas) para um arquivo."""
    erros, avisos, linhas = [], [], []
    for k in indicadores:
        a, n = antiga.get(k), nova.get(k)
        if n is None:
            erros.append(f"`{k}` sumiu do arquivo novo")
            continue
        if not a:
            linhas.append((k, a, n, "novo"))
            continue
        var = (n - a) / a
        sinal = f"{var:+.1%}"
        if var < -QUEDA_MAX:
            erros.append(f"`{k}` caiu {sinal} ({a} → {n})")
        elif var > ALTA_MAX:
            avisos.append(f"`{k}` subiu {sinal} ({a} → {n}); confira se a fonte mudou de formato")
        linhas.append((k, a, n, sinal))
    for fonte, qtd in (fontes_antigas or {}).items():
        if qtd and not (fontes_novas or {}).get(fonte):
            erros.append(f"fonte `{fonte}` zerou (antes {qtd})")
    return erros, avisos, linhas


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--saida", help="grava o relatório em Markdown neste arquivo")
    a = ap.parse_args()

    erros, avisos, corpo = [], [], []
    for caminho, indicadores in INDICADORES.items():
        try:
            nova = meta_nova(caminho)
        except (OSError, ValueError) as e:
            erros.append(f"`{caminho}` ilegível: {e}")
            continue
        antiga = meta_antiga(caminho)
        if antiga is None:
            corpo.append(f"### {caminho}\nSem versão anterior para comparar.\n")
            continue
        e, w, linhas = comparar(antiga, nova, indicadores, antiga.get("fontes"), nova.get("fontes"))
        erros += [f"{caminho}: {x}" for x in e]
        avisos += [f"{caminho}: {x}" for x in w]
        corpo.append(f"### {caminho}\n\n| indicador | antes | depois | variação |\n|---|---|---|---|")
        corpo += [f"| {k} | {x} | {y} | {v} |" for k, x, y, v in linhas]
        corpo.append("")

    ok = not erros
    rel = ["## Portão de qualidade: " + ("✅ aprovado" if ok else "⛔ revisão necessária"), ""]
    rel += [f"- ⛔ {x}" for x in erros] + [f"- ⚠️ {x}" for x in avisos]
    rel += [""] + corpo
    texto = "\n".join(rel)
    print(texto)
    if a.saida:
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(texto)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
