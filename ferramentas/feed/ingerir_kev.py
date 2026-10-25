#!/usr/bin/env python3
"""Feed vivo de vulnerabilidades exploradas (CISA KEV) ligado aos atores do Atlas.

Fluxo semanal: baixa o catálogo KEV, mantém uma janela de dias, cruza com a
curadoria humana de atribuições (dados/feed/atribuicoes.json) e publica:

  dados/feed/kev.json        janela do catálogo (dados persistidos, versionados)
  docs/feed/feed.json        o que o site lê (itens + atribuições + resumo)
  docs/feed/atom.xml         assinatura por leitor de feeds
  dados/feed/novidades.md    o que entrou desde a última rodada (corpo do PR)

Atribuição NUNCA é inferida aqui: só entra o que está em atribuicoes.json, com
fonte pública. Só biblioteca padrão.

Uso:
  python3 ferramentas/feed/ingerir_kev.py --baixar [--dias 120]
  python3 ferramentas/feed/ingerir_kev.py --arquivo kev.json     # offline / testes
"""
import argparse
import datetime as dt
import json
import pathlib
import sys
import urllib.request
from xml.sax.saxutils import escape

RAIZ = pathlib.Path(__file__).resolve().parents[2]
URL_KEV = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
SITE = "https://ridd1kulusc0d3r.github.io/apt4all/"
CAMPOS = ("cveID", "vendorProject", "product", "vulnerabilityName", "dateAdded",
          "shortDescription", "dueDate", "knownRansomwareCampaignUse", "cwes")


def baixar(url=URL_KEV):
    req = urllib.request.Request(url, headers={"User-Agent": "apt4all-feed/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def compacta(v):
    """Só os campos usados; descartar o resto mantém o arquivo pequeno e estável."""
    o = {k: v.get(k) for k in CAMPOS if v.get(k) not in (None, "", [])}
    o["notes"] = [u.strip() for u in (v.get("notes") or "").split(";") if u.strip().startswith("http")][:3]
    return o


def janela(catalogo, dias, hoje, curados=()):
    """Itens adicionados nos últimos `dias` dias, mais os que têm atribuição curada."""
    corte = (hoje - dt.timedelta(days=dias)).isoformat()
    itens = [compacta(v) for v in catalogo["vulnerabilities"]
             if v["dateAdded"] >= corte or v["cveID"] in curados]
    itens.sort(key=lambda v: (v["dateAdded"], v["cveID"]), reverse=True)
    return itens


def indice_atores(atores):
    """nome/alias em minúsculas -> id do Atlas."""
    idx = {}
    for a in atores:
        for n in [a["nome"], *a.get("aliases", [])]:
            idx.setdefault(n.strip().lower(), a["id"])
    return idx


def valida_atribuicoes(lista):
    erros = []
    for i, x in enumerate(lista):
        rot = x.get("cve", f"#{i}")
        for k in ("cve", "atores", "tipo", "uso", "atribuido_por", "confianca", "fontes"):
            if not x.get(k):
                erros.append(f"{rot}: falta `{k}`")
        if x.get("confianca") not in ("alta", "media", "baixa"):
            erros.append(f"{rot}: confianca deve ser alta, media ou baixa")
        if not all(str(u).startswith("https://") for u in x.get("fontes", [])):
            erros.append(f"{rot}: fontes devem ser URLs https")
    return erros


def junta(itens, atribuicoes, idx_atores):
    por_cve = {x["cve"]: x for x in atribuicoes}
    saida = []
    for v in itens:
        x = por_cve.get(v["cveID"])
        v = dict(v)
        if x:
            v["atribuicao"] = {
                **{k: x[k] for k in ("tipo", "uso", "atribuido_por", "confianca", "fontes", "rotulos", "nota_atlas") if k in x},
                "atores": [{"nome": n, "id": idx_atores.get(n.strip().lower())} for n in x["atores"]],
            }
        saida.append(v)
    return saida


def atom(itens, gerado_em):
    ent = []
    for v in itens[:50]:
        link = (v.get("notes") or [SITE + "feed/"])[0]
        atr = v.get("atribuicao")
        resumo = v.get("shortDescription", "")
        if atr:
            resumo += " Atribuição: " + ", ".join(a["nome"] for a in atr["atores"]) + f" ({atr['atribuido_por']})."
        ent.append(
            f"<entry><id>urn:apt4all:{v['cveID']}</id><title>{escape(v['cveID'] + ' · ' + v['vulnerabilityName'])}</title>"
            f"<updated>{v['dateAdded']}T00:00:00Z</updated><link href=\"{escape(link)}\"/>"
            f"<summary>{escape(resumo)}</summary></entry>")
    return ('<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">'
            f'<title>APT4ALL · vulnerabilidades exploradas</title><id>urn:apt4all:feed</id>'
            f'<updated>{gerado_em}T00:00:00Z</updated><link href="{SITE}feed/"/>' + "".join(ent) + "</feed>\n")


def novidades_md(novos, atribuidos_novos, gerado_em):
    L = [f"# Feed de vulnerabilidades ({gerado_em})", "", f"- Novos itens no CISA KEV: **{len(novos)}**"]
    if atribuidos_novos:
        L.append(f"- Com atribuição curada: **{len(atribuidos_novos)}**")
    L.append("")
    for v in novos[:40]:
        r = " · ransomware" if v.get("knownRansomwareCampaignUse") == "Known" else ""
        L.append(f"- `{v['cveID']}` {v['vendorProject']} {v['product']}: {v['vulnerabilityName']} ({v['dateAdded']}){r}")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--baixar", action="store_true")
    g.add_argument("--arquivo")
    ap.add_argument("--dias", type=int, default=120)
    ap.add_argument("--raiz", default=str(RAIZ))
    a = ap.parse_args(argv)
    raiz = pathlib.Path(a.raiz)

    cat = baixar() if a.baixar else json.load(open(a.arquivo, encoding="utf-8"))
    if not cat.get("vulnerabilities"):
        print("catálogo vazio; abortando sem alterar nada", file=sys.stderr)
        return 1
    hoje = dt.date.fromisoformat(max(v["dateAdded"] for v in cat["vulnerabilities"]))
    atr = json.load(open(raiz / "dados/feed/atribuicoes.json", encoding="utf-8"))["atribuicoes"]
    erros = valida_atribuicoes(atr)
    if erros:
        print("atribuicoes.json inválido:\n- " + "\n- ".join(erros), file=sys.stderr)
        return 1

    itens = janela(cat, a.dias, hoje, {x["cve"] for x in atr})
    ant = raiz / "dados/feed/kev.json"
    vistos = {v["cveID"] for v in json.load(open(ant, encoding="utf-8"))["itens"]} if ant.exists() else set()
    novos = [v for v in itens if v["cveID"] not in vistos] if vistos else []

    atores = json.load(open(raiz / "docs/atlas/atores.json", encoding="utf-8"))["atores"]
    final = junta(itens, atr, indice_atores(atores))
    gerado = hoje.isoformat()
    meta = {"gerado_em": gerado, "fonte": "CISA Known Exploited Vulnerabilities", "url": URL_KEV,
            "versao_catalogo": cat.get("catalogVersion"), "n_kev_total": cat.get("count", len(cat["vulnerabilities"])),
            "janela_dias": a.dias, "n_itens": len(final),
            "n_atribuidos": sum(1 for v in final if "atribuicao" in v),
            "n_ransomware": sum(1 for v in final if v.get("knownRansomwareCampaignUse") == "Known")}

    (raiz / "dados/feed").mkdir(parents=True, exist_ok=True)
    (raiz / "docs/feed").mkdir(parents=True, exist_ok=True)
    json.dump({"meta": meta, "itens": itens}, open(ant, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"meta": meta, "itens": final}, open(raiz / "docs/feed/feed.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    (raiz / "docs/feed/atom.xml").write_text(atom(final, gerado), encoding="utf-8")
    (raiz / "dados/feed/novidades.md").write_text(
        novidades_md(novos, [v for v in novos if v["cveID"] in {x["cve"] for x in atr}], gerado), encoding="utf-8")
    print(f"feed: {meta['n_itens']} itens ({meta['n_atribuidos']} atribuídos, {meta['n_ransomware']} com ransomware), {len(novos)} novos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
