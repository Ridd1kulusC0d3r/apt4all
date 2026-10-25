#!/usr/bin/env python3
"""mastro.py: o cabeçalho único do site (marca, idioma, tema e navegação).

As páginas estáticas de docs/ guardam o cabeçalho entre os marcadores
<!--mastro:CHAVE--> ... <!--/mastro-->. Este script reescreve esse trecho, para
que todas as páginas mostrem a mesma navegação. gerar_paginas.py usa mastro()
nas páginas geradas.

Uso: python3 ferramentas/site/mastro.py        # reaplica nas páginas estáticas
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(RAIZ, "docs")

MARCA = ('<svg width="26" height="26" viewBox="0 0 34 34" aria-hidden="true"><polygon points="17,3 29,10 29,24 17,31 5,24 5,10" '
         'fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17" cy="17" r="2.8" fill="var(--signal)"/></svg>')

# (arquivo, rótulo PT, rótulo EN, chave)
SECOES = [
    ("atlas/index.html", "Atlas", "Atlas", "atlas"),
    ("feed/index.html", "Feed", "Feed", "feed"),
    ("recursos/index.html", "Recursos", "Resources", "recursos"),
    ("ler/trilha.html", "Trilha", "Path", "trilha"),
    ("manual/index.html", "Manual", "Manual", "manual"),
    ("ler/index.html", "Textos", "Texts", "ler"),
]
# página estática -> (base relativa até docs/, chave da seção atual, legenda)
PAGINAS = {
    "index.html": ("", "", "atlas aberto de ameaças"),
    "feed/index.html": ("../", "feed", "feed de vulnerabilidades"),
    "recursos/index.html": ("../", "recursos", "recursos"),
    "manual/index.html": ("../", "manual", "manual"),
    "atlas/index.html": ("../", "atlas", "atlas"),
}


SEG = ('<div class="seg" role="group" aria-label="Idioma / Language">'
       '<button data-l="pt" aria-pressed="true">PT</button><button data-l="en" aria-pressed="false">EN</button></div>')


def mastro(base, atual, legenda, extra="", seg=True):
    atual_attr = ' aria-current="page"'
    nav = "".join(
        '<a href="%s%s" data-pt="%s" data-en="%s"%s>%s</a>' % (base, h, pt, en, atual_attr if k == atual else "", pt)
        for h, pt, en, k in SECOES)
    return (f'<header class="mast"><div class="wrap">\n'
            f'  <div class="mast-bar">\n'
            f'    <a class="brand" href="{base}index.html">{MARCA}APT4ALL <small>{legenda}</small></a>\n'
            f'    <div class="tools">{extra}{SEG if seg else ""}'
            f'<button data-tema type="button" data-pt="Tema" data-en="Theme" aria-label="Tema claro/escuro · Light/dark">Tema</button></div>\n'
            f'  </div>\n'
            f'  <nav class="nav" aria-label="Seções">{nav}</nav>\n'
            f'</div></header>')


def aplicar():
    n = 0
    for rel, (base, atual, leg) in PAGINAS.items():
        fn = os.path.join(DOCS, rel)
        if not os.path.exists(fn):
            continue
        s = open(fn, encoding="utf-8").read()
        novo = re.sub(r"<!--mastro-->.*?<!--/mastro-->", lambda m: "<!--mastro-->" + mastro(base, atual, leg) + "<!--/mastro-->", s, flags=re.S)
        if novo != s:
            open(fn, "w", encoding="utf-8").write(novo)
            n += 1
    print(f"mastro aplicado em {n} página(s)")


if __name__ == "__main__":
    sys.exit(aplicar() or 0)
