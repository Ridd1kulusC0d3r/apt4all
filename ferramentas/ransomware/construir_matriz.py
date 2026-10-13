#!/usr/bin/env python3
"""construir_matriz.py: Ransomware Tool Matrix (BushidoUK, CC BY 4.0) -> docs/atlas/ransomware.json.

Lê as tabelas "Tool Name | Threat Group Usage" de cada categoria, normaliza os grupos e
liga cada grupo a um ator do Atlas quando o nome bate com um nome ou apelido conhecido.
Só biblioteca padrão.

Uso:
  python3 ferramentas/ransomware/construir_matriz.py            # usa a cópia em dados/brutos
  python3 ferramentas/ransomware/construir_matriz.py --baixar   # baixa a versão atual do GitHub
"""
import argparse, json, os, re, sys, urllib.request
from collections import Counter
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRUTOS = os.path.join(RAIZ, "dados", "brutos", "ransomware-tool-matrix")
BASE = "https://raw.githubusercontent.com/BushidoUK/Ransomware-Tool-Matrix/main/Tools/"
CATEGORIAS = [  # arquivo, chave, pt, en
    ("RMM-Tools", "rmm", "Acesso remoto (RMM)", "Remote access (RMM)"),
    ("CredentialTheft", "credenciais", "Roubo de credenciais", "Credential theft"),
    ("DefenseEvasion", "evasao", "Evasão de defesa", "Defense evasion"),
    ("DiscoveryEnum", "descoberta", "Descoberta", "Discovery"),
    ("Networking", "rede", "Túneis e rede", "Tunnels and networking"),
    ("Offsec", "offsec", "Ferramentas ofensivas", "Offensive tools"),
    ("LOLBAS", "lolbas", "Binários do próprio sistema", "Living-off-the-land"),
    ("Exfiltration", "exfiltracao", "Exfiltração", "Exfiltration"),
]


def norm(a):
    return re.sub(r"[^a-z0-9]", "", (a or "").lower())


def baixar():
    os.makedirs(BRUTOS, exist_ok=True)
    for arq, *_ in CATEGORIAS:
        with urllib.request.urlopen(BASE + arq + ".md", timeout=60) as r:
            open(os.path.join(BRUTOS, arq + ".md"), "wb").write(r.read())


def tipo_grupo(bruto):
    """Convenção do repositório: '*Nome' = broker de acesso, 'Nome*' = afiliado, 'Nome+' = ligado a Estado."""
    if bruto.startswith("*"):
        return "iab"
    if bruto.endswith("*"):
        return "afiliado"
    if bruto.endswith("+"):
        return "estado"
    return "gangue"


def ler_tabelas():
    usos = []   # (categoria, ferramenta, grupo_bruto)
    for arq, chave, *_ in CATEGORIAS:
        fn = os.path.join(BRUTOS, arq + ".md")
        if not os.path.exists(fn):
            print("[aviso] faltando", fn)
            continue
        for linha in open(fn, encoding="utf-8", errors="replace"):
            if not linha.startswith("|") or "---" in linha or "Tool Name" in linha:
                continue
            cel = [c.strip() for c in linha.strip().strip("|").split("|")]
            if len(cel) < 2 or not cel[0]:
                continue
            ferramenta = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cel[0]).strip()
            for g in cel[1].split(","):
                g = g.strip()
                if g:
                    usos.append((chave, ferramenta, g))
    return usos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baixar", action="store_true")
    a = ap.parse_args()
    if a.baixar:
        baixar()
    usos = ler_tabelas()
    atores = json.load(open(os.path.join(RAIZ, "docs", "atlas", "atores.json"), encoding="utf-8"))["atores"]
    # Ligação com o Atlas: primeiro pelo nome principal; por apelido só quando o ator não traz
    # vários nomes de outras gangues entre os apelidos (sinal de lista de famílias misturada na fonte).
    nomes_rw = {norm(g.strip("*+ ")) for _, _, g in usos}
    principal, indice = {}, {}
    for x in atores:
        principal.setdefault(norm(x["nome"]), set()).add(x["id"])
        contaminado = sum(1 for n in x["aliases"] if norm(n) in nomes_rw) >= 3
        if not contaminado:
            for n in x["aliases"]:
                indice.setdefault(norm(n), set()).add(x["id"])
    grupos, ferramentas = {}, {}
    for cat, ferr, bruto in usos:
        nome = bruto.strip("*+ ").strip()
        k = norm(nome)
        if not k:
            continue
        g = grupos.setdefault(k, {"nome": nome, "tipo": tipo_grupo(bruto), "ferramentas": set(), "categorias": Counter()})
        g["ferramentas"].add(ferr)
        g["categorias"][cat] += 1
        f = ferramentas.setdefault(norm(ferr), {"nome": ferr, "cat": cat, "grupos": set()})
        f["grupos"].add(g["nome"])
    for k, g in grupos.items():
        ids = principal.get(k) or indice.get(k, set())
        g["ator"] = next(iter(ids)) if len(ids) == 1 else None
    saida = {
        "meta": {"gerado_em": date.today().isoformat(), "fonte": "BushidoUK/Ransomware-Tool-Matrix",
                 "licenca": "CC BY 4.0", "url": "https://github.com/BushidoUK/Ransomware-Tool-Matrix",
                 "n_grupos": len(grupos), "n_ferramentas": len(ferramentas), "n_usos": len(usos),
                 "ligados_ao_atlas": sum(1 for g in grupos.values() if g["ator"])},
        "categorias": [{"id": c, "pt": pt, "en": en} for _, c, pt, en in CATEGORIAS],
        "grupos": sorted(({"nome": g["nome"], "tipo": g["tipo"], "ator": g["ator"], "ferramentas": sorted(g["ferramentas"]),
                           "categorias": dict(g["categorias"])} for g in grupos.values()), key=lambda g: (-len(g["ferramentas"]), g["nome"])),
        "ferramentas": sorted(({"nome": f["nome"], "cat": f["cat"], "grupos": sorted(f["grupos"])} for f in ferramentas.values()),
                              key=lambda f: (-len(f["grupos"]), f["nome"])),
    }
    with open(os.path.join(RAIZ, "docs", "atlas", "ransomware.json"), "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, separators=(",", ":"))
    m = saida["meta"]
    print(f"{m['n_grupos']} grupos · {m['n_ferramentas']} ferramentas · {m['n_usos']} usos · {m['ligados_ao_atlas']} ligados ao Atlas")
    print("mais versáteis:", [(g["nome"], len(g["ferramentas"])) for g in saida["grupos"][:6]])
    print("mais usadas:", [(f["nome"], len(f["grupos"])) for f in saida["ferramentas"][:6]])
    return 0


if __name__ == "__main__":
    sys.exit(main())
