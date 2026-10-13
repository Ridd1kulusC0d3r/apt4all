#!/usr/bin/env python3
"""gerar_listas.py — gera RECURSOS.md (PT-BR) e RESOURCES.md (EN) a partir de recursos/recursos.json.

A fonte da verdade é o JSON: edite lá e rode este script. Se existir dados/gerados/links.json
(do verificar_links.py), links mortos (404/410) aparecem marcados.

Uso: python3 ferramentas/recursos/gerar_listas.py
"""
import json, os, shutil

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROT = {
    "pt": {"tipo": {"gratuito": "gratuito", "pago": "pago", "registro": "com cadastro", "freemium": "freemium"},
           "status": {"legado": "legado", "arquivado": "arquivado"}, "morto": "link fora do ar",
           "titulo": "Recursos de CTI, APT e malware", "sumario": "Sumário",
           "intro": "Lista curada, bilíngue e verificada automaticamente. ★ = comece por aqui. Gerada de `recursos/recursos.json`; para sugerir um recurso, edite o JSON e abra um PR.",
           "cols": ("Recurso", "Para que serve", "Acesso"), "outro": "English version: [RESOURCES.md](RESOURCES.md)",
           "aviso_amostras": "> ⚠️ **Malware real.** Baixe e abra só em laboratório isolado (VM sem rede ou com rede simulada). Nunca no seu computador de trabalho.",
           "total": "recursos", "legenda": "★ comece por aqui · 🔹 da lista original do mantenedor"},
    "en": {"tipo": {"gratuito": "free", "pago": "paid", "registro": "sign-up", "freemium": "freemium"},
           "status": {"legado": "legacy", "arquivado": "archived"}, "morto": "link down",
           "titulo": "CTI, APT and malware resources", "sumario": "Contents",
           "intro": "Curated, bilingual, automatically checked list. ★ = start here. Generated from `recursos/recursos.json`; to suggest a resource, edit the JSON and open a PR.",
           "cols": ("Resource", "What it is for", "Access"), "outro": "Versão em português: [RECURSOS.md](RECURSOS.md)",
           "aviso_amostras": "> ⚠️ **Live malware.** Download and open only in an isolated lab (VM with no network or simulated network). Never on your work machine.",
           "total": "resources", "legenda": "★ start here · 🔹 from the maintainer's original list"},
}


def ancora(t):
    import re
    return re.sub(r"[^a-z0-9à-ú -]", "", t.lower()).replace(" ", "-")


def gera(lang, dados, links):
    R = ROT[lang]
    cats = dados["categorias"]
    linhas = [f"# {R['titulo']}", "", R["outro"], "", R["intro"], "",
              f"**{len(dados['recursos'])} {R['total']}** · " + " · ".join(
                  f"[{cats[c][lang]}](#{ancora(cats[c][lang])})" for c in cats), "", R["legenda"], ""]
    for c, meta in cats.items():
        itens = [r for r in dados["recursos"] if r["cat"] == c]
        if not itens:
            continue
        linhas += [f"## {meta[lang]}", "", meta["desc_" + lang], ""]
        if c == "amostras":
            linhas += [R["aviso_amostras"], ""]
        linhas += [f"| {R['cols'][0]} | {R['cols'][1]} | {R['cols'][2]} |", "|---|---|---|"]
        for r in sorted(itens, key=lambda x: (not x["destaque"], x["status"] != "ativo", x["nome"].lower())):
            nome = ("★ " if r["destaque"] else "") + f"[{r['nome']}]({r['url']})"
            acesso = R["tipo"].get(r["tipo"], r["tipo"])
            if r["status"] != "ativo":
                acesso += " · " + R["status"].get(r["status"], r["status"])
            info = links.get(r["url"])
            if info and info.get("codigo") in (404, 410):
                acesso += " · ⚠️ " + R["morto"]
            if r.get("origem") == "lista do usuário":
                nome += " 🔹"
            desc = r["desc_" + lang].replace("|", "\\|")
            linhas.append(f"| {nome} | {desc} | {acesso} |")
        linhas.append("")
    return "\n".join(linhas)


def main():
    dados = json.load(open(os.path.join(RAIZ, "recursos", "recursos.json"), encoding="utf-8"))
    fl = os.path.join(RAIZ, "dados", "gerados", "links.json")
    links = json.load(open(fl)) if os.path.exists(fl) else {}
    open(os.path.join(RAIZ, "RECURSOS.md"), "w", encoding="utf-8").write(gera("pt", dados, links))
    open(os.path.join(RAIZ, "RESOURCES.md"), "w", encoding="utf-8").write(gera("en", dados, links))
    os.makedirs(os.path.join(RAIZ, "docs"), exist_ok=True)
    shutil.copy(os.path.join(RAIZ, "recursos", "recursos.json"), os.path.join(RAIZ, "docs", "recursos.json"))
    print(f"RECURSOS.md e RESOURCES.md gerados com {len(dados['recursos'])} recursos")


if __name__ == "__main__":
    main()
