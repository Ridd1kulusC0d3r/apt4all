#!/usr/bin/env python3
"""gerar_paginas.py: transforma os textos do repositório (Markdown) em páginas HTML navegáveis em docs/ler/.

Só biblioteca padrão. Cobre o Markdown que o projeto usa: títulos, parágrafos, listas (inclusive caixas
de seleção), tabelas, blocos de código, citações, links, negrito, itálico e código em linha.
Links entre arquivos .md viram links entre as páginas geradas.

Uso: python3 ferramentas/site/gerar_paginas.py
"""
import html, os, re, sys

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
    ("RELATORIO-DE-TESTES.md", "relatorio-de-testes", "Relatório de testes", "Sobre"),
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
:root{color-scheme:dark;--fundo:#0B0F10;--fundo2:#0D1213;--sup:#10181A;--sup2:#152022;--borda:#1F2B29;--texto:#DCE4E2;--claro:#F2F7F6;--apagado:#8A9693;--menta:#5EE6C4;--ambar:#F4BE3F;--coral:#FF7A63;
 --display:"Saira Condensed","Arial Narrow",system-ui,sans-serif;--corpo:"Inter",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,Consolas,monospace}
*{box-sizing:border-box}
html{scroll-padding-top:80px}
body{margin:0;background:var(--fundo);color:var(--texto);font:16px/1.65 var(--corpo)}
a{color:var(--menta)}
:focus-visible{outline:2px solid var(--menta);outline-offset:2px}
.topo{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:color-mix(in srgb,var(--fundo) 92%,transparent);backdrop-filter:blur(6px);border-bottom:1px solid var(--borda)}
.topo .in{max-width:1240px;margin:0 auto;padding:10px 16px;display:flex;gap:14px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.lg{font:700 20px var(--display);letter-spacing:.14em;color:var(--claro);text-decoration:none}
.lg span{color:var(--menta)}
.atalhos{display:flex;gap:4px;flex-wrap:wrap}
.atalhos a{font:600 13px var(--mono);color:var(--apagado);text-decoration:none;padding:5px 9px;border:1px solid transparent}
.atalhos a:hover,.atalhos a[aria-current]{color:var(--claro);border-color:var(--borda)}
.grade{max-width:1240px;margin:0 auto;padding:0 16px 70px;display:grid;grid-template-columns:250px minmax(0,1fr);gap:40px}
nav.lado{position:sticky;top:70px;align-self:start;padding-top:28px;max-height:calc(100vh - 80px);overflow:auto;font-size:14px}
nav.lado b{display:block;font:600 11px var(--mono);letter-spacing:.14em;color:var(--apagado);text-transform:uppercase;margin:16px 0 6px}
nav.lado a{display:block;padding:4px 10px;border-left:2px solid var(--borda);color:var(--texto);text-decoration:none}
nav.lado a:hover{color:var(--menta)}
nav.lado a[aria-current]{border-left-color:var(--ambar);color:var(--ambar)}
nav.lado .sum a{font-size:13px;color:var(--apagado);padding-left:18px}
main{min-width:0;padding-top:24px;max-width:860px}
h1{font:700 clamp(32px,5vw,48px)/1.05 var(--display);letter-spacing:.04em;text-transform:uppercase;color:var(--claro);margin:8px 0 18px;text-wrap:balance}
h2{font:700 28px/1.1 var(--display);letter-spacing:.05em;text-transform:uppercase;color:var(--claro);margin:42px 0 10px;padding-top:12px;border-top:1px solid var(--borda);text-wrap:balance}
h3{font:700 20px var(--display);letter-spacing:.05em;text-transform:uppercase;color:var(--claro);margin:28px 0 8px}
h4{font:600 13px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ambar);margin:22px 0 6px}
p,li{max-width:72ch}
strong{color:var(--claro)}
code{font:.88em var(--mono);background:var(--sup2);border:1px solid var(--borda);padding:1px 5px}
pre{background:var(--fundo2);border:1px solid var(--borda);padding:12px 14px;overflow-x:auto;line-height:1.5}
pre code{background:none;border:0;padding:0}
blockquote{margin:16px 0;border-left:3px solid var(--menta);background:var(--sup);padding:10px 16px}
blockquote p{margin:0}
.tabela{overflow-x:auto;margin:14px 0;border:1px solid var(--borda)}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--borda);vertical-align:top}
th{font:600 12px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--apagado);background:var(--sup)}
td{font-variant-numeric:tabular-nums}
tbody tr:hover{background:var(--sup)}
li.cx{list-style:none;margin-left:-22px}
li.cx input{accent-color:#5EE6C4;width:16px;height:16px;vertical-align:-2px;margin-right:6px}
hr{border:0;border-top:1px solid var(--borda);margin:28px 0}
.origem{font:12px var(--mono);color:var(--apagado);margin-top:40px;padding-top:14px;border-top:1px solid var(--borda)}
.selo{font:600 12px var(--mono);letter-spacing:.16em;color:var(--menta);text-transform:uppercase}
@media (max-width:900px){.grade{grid-template-columns:minmax(0,1fr);gap:0}nav.lado{position:static;max-height:none;padding-top:16px;border-bottom:1px solid var(--borda);padding-bottom:12px}nav.lado .sum{display:none}}
"""


def pagina(titulo, corpo, sumario, atual, origem, grupos):
    lado = []
    for g, itens in grupos.items():
        lado.append(f"<b>{g}</b>")
        for p, t in itens:
            cur = ' aria-current="page"' if p == atual else ""
            lado.append(f'<a href="{p}.html"{cur}>{html.escape(t)}</a>')
            if p == atual and sumario:
                lado.append('<div class="sum">' + "".join(f'<a href="#{a}">{html.escape(t2)}</a>' for a, t2 in sumario) + "</div>")
    return f"""<!doctype html>
<html lang="{'en' if atual.endswith('-en') or atual in ('start-here','tce-analysis','sources','contributing') else 'pt-BR'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>APT4ALL · {html.escape(titulo)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&family=Saira+Condensed:wght@600;700&display=swap">
<style>{ESTILO}</style>
</head>
<body>
<header class="topo"><div class="in"><a class="lg" href="../index.html">APT4ALL <span>/</span> LER</a>
<nav class="atalhos" aria-label="Atalhos"><a href="../atlas/index.html">Atlas</a><a href="../recursos/index.html">Recursos</a><a href="trilha.html"{' aria-current="page"' if atual == 'trilha' else ''}>Trilha</a><a href="../manual/index.html">Manual</a><a href="index.html"{' aria-current="page"' if atual == 'index' else ''}>Todos os textos</a></nav></div></header>
<div class="grade">
<nav class="lado" aria-label="Textos">{''.join(lado)}</nav>
<main>
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
    corpo = '<div class="selo">◆ Biblioteca do repositório</div><h1>Todos os textos</h1><p>Cada documento do repositório em página navegável, em português e inglês. Comece pelo <a href="comece-aqui.html">Comece aqui</a>.</p>' + "".join(cartoes)
    with open(os.path.join(SAIDA, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina("Todos os textos", corpo, [], "index", "", grupos))
    print(f"{feitas} páginas + índice em docs/ler/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
