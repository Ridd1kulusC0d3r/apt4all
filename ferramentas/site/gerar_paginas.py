#!/usr/bin/env python3
"""gerar_paginas.py: transforma os textos do repositório (Markdown) em páginas HTML navegáveis em docs/ler/.

Só biblioteca padrão. Cobre o Markdown que o projeto usa: títulos, parágrafos, listas (inclusive caixas
de seleção), tabelas, blocos de código, citações, links, negrito, itálico e código em linha.
Links entre arquivos .md viram links entre as páginas geradas.

Uso: python3 ferramentas/site/gerar_paginas.py
"""
import html, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mastro import mastro  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAIDA = os.path.join(RAIZ, "docs", "ler")
REPO = "https://github.com/Ridd1kulusC0d3r/apt4all/blob/main/"

# (arquivo de origem, página gerada, título curto, grupo)
PAGINAS = [
    ("COMECE-AQUI.md", "comece-aqui", "Comece aqui", "Começar"),
    ("START-HERE.md", "start-here", "Start here", "Começar"),
    ("trilha/README.md", "trilha", "Trilha (9 módulos)", "Estudar"),
    ("trilha/README.en.md", "trilha-en", "Learning path", "Estudar"),
    ("trilha/modelos/ficha-relatorio.md", "modelo-ficha-relatorio", "Modelo: ficha de relatório", "Modelos"),
    ("trilha/modelos/matriz-ach.md", "modelo-matriz-ach", "Modelo: matriz ACH", "Modelos"),
    ("trilha/modelos/cobertura.md", "modelo-cobertura", "Modelo: tabela de cobertura", "Modelos"),
    ("trilha/modelos/registro-triagem.md", "modelo-registro-triagem", "Modelo: registro de triagem", "Modelos"),
    ("trilha/modelos/dossie-ator.md", "modelo-dossie-ator", "Modelo: dossiê de ator", "Modelos"),
    ("tce/README.md", "tce", "Ponte com o TCE", "TCE"),
    ("tce/README.en.md", "tce-en", "TCE bridge", "TCE"),
    ("tce/ANALISE-TCE.md", "analise-tce", "Análise do TCE", "TCE"),
    ("tce/TCE-ANALYSIS.md", "tce-analysis", "TCE analysis", "TCE"),
    ("FONTES.md", "fontes", "Fontes e licenças", "Sobre"),
    ("SOURCES.md", "sources", "Sources and licenses", "Sobre"),
    ("CONTRIBUTING.md", "contribuir", "Como contribuir", "Sobre"),
    ("CONTRIBUTING.en.md", "contributing", "How to contribute", "Sobre"),
    ("dados/gerados/resumo.md", "resumo-da-base", "Resumo da base", "Sobre"),
]
MAPA = {os.path.normpath(o): p for o, p, _, _ in PAGINAS}
EXTRA = {"README.md": "../index.html", "README.en.md": "../index.html", "RECURSOS.md": "../recursos/index.html",
         "RESOURCES.md": "../recursos/index.html", "docs/manual/index.html": "../manual/index.html",
         "docs/manual": "../manual/index.html", "docs/manual/": "../manual/index.html",
         "trilha/": "trilha.html", "trilha": "trilha.html", "tce/": "tce.html", "tce": "tce.html",
         "trilha/modelos/": "index.html", "modelos/": "index.html"}


PAGES = "https://ridd1kulusc0d3r.github.io/apt4all/"


def resolve(href, origem):
    if href.startswith(PAGES):  # site publicado -> caminho relativo, para navegar também offline
        resto, _, anc = href[len(PAGES):].partition("#")
        if resto == "" or resto.endswith("/"):
            resto += "index.html"
        return "../" + resto + ("#" + anc if anc else "")
    if re.match(r"^(https?:|mailto:|#)", href):
        return href
    alvo, _, ancora = href.partition("#")
    base = os.path.dirname(origem)
    caminho = os.path.normpath(os.path.join(base, alvo)) if alvo else origem
    chave = caminho.replace("\\", "/")
    if chave in MAPA:
        return MAPA[chave] + ".html" + ("#" + ancora if ancora else "")
    for k in (chave, chave + "/", alvo):
        if k in EXTRA:
            return EXTRA[k] + ("#" + ancora if ancora else "")
    return REPO + chave + ("#" + ancora if ancora else "")


def ancora(txt):
    t = re.sub(r"<[^>]+>", "", txt).lower()
    t = re.sub(r"[^\w\- ]", "", t, flags=re.UNICODE)
    return t.strip().replace(" ", "-")


def inline(txt, origem, links=True):
    guardados = []
    if links:  # links primeiro, para aceitar `código` dentro do texto do link
        def guarda(m):
            alvo = m.group(2)
            ext = ' target="_blank" rel="noopener"' if alvo.startswith("http") and not alvo.startswith(PAGES) else ""
            guardados.append(f'<a href="{html.escape(resolve(alvo, origem))}"{ext}>{inline(m.group(1), origem, False)}</a>')
            return f"\x00{len(guardados) - 1}\x00"
        txt = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: (guardados.append(f'<img alt="{html.escape(m.group(1))}" src="{resolve(m.group(2), origem)}">') or f"\x00{len(guardados) - 1}\x00"), txt)
        txt = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", guarda, txt)
    partes = re.split(r"(`[^`]+`)", txt)
    out = []
    for p in partes:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>" + html.escape(p[1:-1]) + "</code>")
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", p)
        out.append(p)
    res = "".join(out)
    return re.sub("\x00(\\d+)\x00", lambda m: guardados[int(m.group(1))], res)


def celulas(linha):
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|") and not linha.endswith("\\|"):
        linha = linha[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", linha)]


def converte(md, origem):
    linhas = md.replace("\r\n", "\n").split("\n")
    out, i, sumario = [], 0, []
    # remove bloco <div align="center"> do README e comentários HTML simples
    while i < len(linhas):
        l = linhas[i]
        if l.startswith("```"):
            j = i + 1
            bloco = []
            while j < len(linhas) and not linhas[j].startswith("```"):
                bloco.append(linhas[j]); j += 1
            out.append("<pre><code>" + html.escape("\n".join(bloco)) + "</code></pre>")
            i = j + 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)$", l)
        if m:
            n = len(m.group(1)); txt = inline(m.group(2), origem); a = ancora(m.group(2))
            if n == 2:
                sumario.append((a, html.unescape(re.sub(r"<[^>]+>", "", txt))))
            out.append(f'<h{n} id="{a}">{txt}</h{n}>'); i += 1; continue
        if re.match(r"^\s*\|", l) and i + 1 < len(linhas) and re.match(r"^\s*\|?\s*:?-{3,}", linhas[i + 1]):
            cab = celulas(l); i += 2; corpo = []
            while i < len(linhas) and re.match(r"^\s*\|", linhas[i]):
                corpo.append(celulas(linhas[i])); i += 1
            t = ['<div class="tabela"><table><thead><tr>' + "".join(f"<th>{inline(c, origem)}</th>" for c in cab) + "</tr></thead><tbody>"]
            for r in corpo:
                t.append("<tr>" + "".join(f"<td>{inline(c, origem)}</td>" for c in r) + "</tr>")
            out.append("".join(t) + "</tbody></table></div>"); continue
        if l.startswith(">"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith(">"):
                bloco.append(re.sub(r"^>\s?", "", linhas[i])); i += 1
            texto = " ".join(b for b in bloco if not b.startswith("[!"))
            out.append("<blockquote><p>" + inline(texto, origem) + "</p></blockquote>"); continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", l):
            ordenada = bool(re.match(r"^\s*\d+\.", l))
            itens = []
            while i < len(linhas) and (re.match(r"^\s*([-*]|\d+\.)\s+", linhas[i]) or (linhas[i].startswith("  ") and linhas[i].strip() and itens)):
                if re.match(r"^\s*([-*]|\d+\.)\s+", linhas[i]):
                    itens.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", linhas[i]))
                else:
                    itens[-1] += " " + linhas[i].strip()
                i += 1
            lis = []
            for it in itens:
                cx = re.match(r"^\[( |x)\]\s+(.*)$", it)
                if cx:
                    lis.append(f'<li class="cx"><label><input type="checkbox"{" checked" if cx.group(1) == "x" else ""}> {inline(cx.group(2), origem)}</label></li>')
                else:
                    lis.append("<li>" + inline(it, origem) + "</li>")
            tag = "ol" if ordenada else "ul"
            out.append(f"<{tag}>" + "".join(lis) + f"</{tag}>"); continue
        if re.match(r"^-{3,}\s*$", l):
            out.append("<hr>"); i += 1; continue
        if not l.strip() or re.match(r"^\s*</?div|^\s*<img|^\s*<sub", l):
            i += 1; continue
        par = [l]; i += 1
        while i < len(linhas) and linhas[i].strip() and not re.match(r"^(#|```|>|\s*\||\s*[-*]\s|\s*\d+\.\s|-{3,})", linhas[i]):
            par.append(linhas[i]); i += 1
        out.append("<p>" + inline(" ".join(x.strip() for x in par), origem) + "</p>")
    return "\n".join(out), sumario


ESTILO = """
.grade{max-width:1180px;margin:0 auto;padding:0 20px 70px;display:grid;grid-template-columns:240px minmax(0,1fr);gap:48px}
nav.lado{position:sticky;top:16px;align-self:start;padding-top:36px;max-height:calc(100vh - 32px);overflow:auto;font-size:14px}
nav.lado b{display:block;font:600 11px var(--mono);letter-spacing:.14em;color:var(--ink-3);text-transform:uppercase;margin:18px 0 6px}
nav.lado a{display:block;padding:4px 10px;border-left:2px solid var(--rule);color:var(--ink-2);text-decoration:none}
nav.lado a:hover{color:var(--signal)}
nav.lado a[aria-current]{border-left-color:var(--signal);color:var(--ink);font-weight:600}
nav.lado .sum a{font-size:13px;color:var(--ink-3);padding-left:18px;font-weight:400}
main.texto{min-width:0;padding-top:36px;max-width:820px}
main.texto h1{font-size:clamp(30px,4.6vw,46px);margin:8px 0 18px}
main.texto h2{margin:44px 0 10px;padding-top:14px;border-top:1px solid var(--rule)}
main.texto h3{font:700 19px var(--serif);margin:28px 0 8px}
main.texto h4{font:600 12px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--signal);margin:22px 0 6px}
main.texto p,main.texto li{max-width:72ch}
main.texto strong{color:var(--ink)}
p.trocar{font:600 12px var(--mono);letter-spacing:.06em;margin:0 0 18px}
li.cx{list-style:none;margin-left:-22px}
li.cx input{accent-color:var(--signal);width:16px;height:16px;vertical-align:-2px;margin-right:6px}
hr{border:0;border-top:1px solid var(--rule);margin:28px 0}
.origem{font:12px var(--mono);color:var(--ink-3);margin-top:40px;padding-top:14px;border-top:1px solid var(--rule)}
.selo{font:600 11px var(--mono);letter-spacing:.14em;color:var(--signal);text-transform:uppercase}
.mast{margin-bottom:0}
@media (max-width:900px){.grade{grid-template-columns:minmax(0,1fr);gap:0}nav.lado{position:static;max-height:none;padding-top:16px;border-bottom:1px solid var(--rule);padding-bottom:12px}nav.lado .sum{display:none}}
"""


EN = ('trilha-en', 'tce-en', 'start-here', 'tce-analysis', 'sources', 'contributing')


def limpa(corpo):
    """Tira o losango decorativo do título e troca o rótulo 'README.en.md' por um link de idioma legível."""
    corpo = re.sub(r'(<h1[^>]*>)\s*◆\s*', r'\1', corpo)
    corpo = re.sub(r'<p>(English|Português): <a href="([^"]+)">[^<]+\.md</a></p>',
                   lambda m: '<p class="trocar"><a href="%s">%s</a></p>' % (m.group(2), 'English version' if m.group(1) == 'English' else 'Versão em português'), corpo)
    return corpo


def pagina(titulo, corpo, sumario, atual, origem, grupos):
    corpo = limpa(corpo)
    lado = []
    for g, itens in grupos.items():
        lado.append(f"<b>{g}</b>")
        for p, t in itens:
            cur = ' aria-current="page"' if p == atual else ""
            lado.append(f'<a href="{p}.html"{cur}>{html.escape(t)}</a>')
            if p == atual and sumario:
                lado.append('<div class="sum">' + "".join(f'<a href="#{a}">{html.escape(t2)}</a>' for a, t2 in sumario) + "</div>")
    return f"""<!doctype html>
<html lang="{'en' if atual in EN else 'pt-BR'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>APT4ALL · {html.escape(titulo)}</title>
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/tema.css">
<script src="../assets/tema.js"></script>
<style>{ESTILO}</style>
</head>
<body>
{mastro('../', 'trilha' if atual in ('trilha', 'trilha-en') else 'ler', 'textos' if atual not in EN else 'texts', seg=False)}
<script>document.addEventListener("DOMContentLoaded",function(){{TEMA_LANG("{'en' if atual in EN else 'pt'}")}})</script>
<div class="grade">
<nav class="lado" aria-label="Textos">{''.join(lado)}</nav>
<main class="texto">
{corpo}
<p class="origem">{'Gerado de ' + f'<a href="{REPO}{origem}">{origem}</a>' if origem else ''} · código MIT · texto CC BY 4.0</p>
</main>
</div>
<script>
// caixas de seleção da trilha e do Comece aqui ficam lembradas neste navegador
(function(){{var k="apt4all-cx-{atual}";var cx=[].slice.call(document.querySelectorAll("li.cx input"));var s={{}};
try{{s=JSON.parse(localStorage.getItem(k)||"{{}}")}}catch(e){{}}
cx.forEach(function(c,i){{if(s[i])c.checked=true;c.addEventListener("change",function(){{s[i]=c.checked;try{{localStorage.setItem(k,JSON.stringify(s))}}catch(e){{}}}})}})}})();
</script>
</body>
</html>
"""


def main():
    os.makedirs(SAIDA, exist_ok=True)
    grupos = {}
    for o, p, t, g in PAGINAS:
        grupos.setdefault(g, []).append((p, t))
    feitas = 0
    for o, p, t, g in PAGINAS:
        fn = os.path.join(RAIZ, o)
        if not os.path.exists(fn):
            print("[aviso] faltando", o)
            continue
        md = open(fn, encoding="utf-8").read()
        corpo, sumario = converte(md, o)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", corpo)
        titulo = re.sub(r"<[^>]+>", "", h1.group(1)) if h1 else t
        with open(os.path.join(SAIDA, p + ".html"), "w", encoding="utf-8") as f:
            f.write(pagina(titulo, corpo, sumario, p, o, grupos))
        feitas += 1
    # índice
    cartoes = []
    for g, itens in grupos.items():
        cartoes.append(f"<h2>{g}</h2><ul>" + "".join(f'<li><a href="{p}.html">{html.escape(t)}</a></li>' for p, t in itens) + "</ul>")
    corpo = '<div class="selo">Biblioteca do repositório</div><h1>Todos os textos</h1><p>Cada documento do repositório em página navegável, em português e inglês. Comece pelo <a href="comece-aqui.html">Comece aqui</a>.</p>' + "".join(cartoes)
    with open(os.path.join(SAIDA, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina("Todos os textos", corpo, [], "index", "", grupos))
    print(f"{feitas} páginas + índice em docs/ler/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
