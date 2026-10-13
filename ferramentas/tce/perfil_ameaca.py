#!/usr/bin/env python3
"""perfil_ameaca.py — ponte APT4ALL → TCE Horizon (só biblioteca padrão).

Monta um perfil de ameaça por vitimologia histórica (país e setor da organização) a partir de
docs/atlas/atores.json e exporta três arquivos:

  navigator.json       camada do ATT&CK Navigator com as técnicas pesadas pelo perfil
  tce-sinais.json      candidatos a intelligence_signals do TCE (status=candidate, review_required=true)
  tce-intelligence.csv mesma informação no formato de importação de ambiente do TCE
  perfil.md            relatório legível: atores, porquê, técnicas

O perfil é um ponto de partida para modelagem de ameaças. Presença histórica de um ator contra um país
ou setor não prova que ele mira a sua organização agora; por isso todo sinal sai como candidato.

Uso:
  python3 ferramentas/tce/perfil_ameaca.py --pais Brazil --setor "Financial" --saida saida/perfil-br-fin
  python3 ferramentas/tce/perfil_ameaca.py --listar paises | setores
"""
import argparse, csv, json, os, re, sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def carrega(caminho=None):
    caminho = caminho or os.path.join(RAIZ, "docs", "atlas", "atores.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def bate_pais(a, pais, nomes_pais=()):
    """pais pode ser ISO (BR) ou nome em inglês (Brazil). Texto livre de alvos só conta por nome completo."""
    if pais in a.get("vitimas_iso", []) or pais in a.get("vitimas", []):
        return True
    alvos = (a.get("alvos") or "").lower()
    return any(len(n) > 3 and n.lower() in alvos for n in (pais, *nomes_pais))


def nomes_do_iso(iso):
    if not (len(iso) == 2 or "-" in iso) or not iso.isupper():
        return ()
    try:
        with open(os.path.join(RAIZ, "docs", "atlas", "paises.json"), encoding="utf-8") as f:
            p = json.load(f)
    except OSError:
        return ()
    g = p.get("geo", {}).get(iso) or p.get("nomes_extra", {}).get(iso) or {}
    extra = {"US": ("United States",), "GB": ("United Kingdom",), "KR": ("South Korea",)}.get(iso, ())
    return tuple(x for x in (g.get("nome_en"),) + extra if x)


def calcula(atores, pais="", setor="", origem="todos"):
    """Mesma regra do Atlas (docs/atlas/index.html, função calculaPerfil)."""
    out = []
    nomes_pais = nomes_do_iso(pais) if pais else ()
    for a in atores:
        if origem == "estado" and not a.get("pais"):
            continue
        s, por = 0, []
        if pais and bate_pais(a, pais, nomes_pais):
            s += 2
            por.append("vítimas no país")
        if setor and setor in a.get("setores", []):
            s += 2
            por.append("setor-alvo")
        if (pais or setor) and not s:
            continue
        if a.get("mitre") and a["mitre"].get("tecnicas"):
            s += 1
            por.append("perfil ATT&CK")
        out.append({"ator": a, "score": s, "porque": por})
    out.sort(key=lambda x: (-x["score"], -(len(x["ator"]["mitre"]["tecnicas"]) if x["ator"].get("mitre") else 0), x["ator"]["nome"]))
    tec = Counter()
    for x in out:
        if x["ator"].get("mitre"):
            for t in x["ator"]["mitre"]["tecnicas"]:
                tec[t] += x["score"]
    return out, tec.most_common()


def slug(s):
    return re.sub(r"[^A-Z0-9]+", "", (s or "ALL").upper())[:20] or "ALL"


def exporta(res, tec, meta, pais, setor, saida, top=60):
    os.makedirs(saida, exist_ok=True)
    maximo = tec[0][1] if tec else 1
    versao = str(meta.get("attack_versao") or "19").split(".")[0]
    camada = {
        "name": f"apt4all · {pais or '*'} · {setor or '*'}",
        "versions": {"attack": versao, "navigator": "5.1.0", "layer": "4.5"},
        "domain": "enterprise-attack",
        "description": "Gerado pelo APT4ALL (perfil por vitimologia histórica). Revise antes de usar.",
        "techniques": [{"techniqueID": t, "score": v,
                        "comment": f"{sum(1 for x in res if x['ator'].get('mitre') and t in x['ator']['mitre']['tecnicas'])} atores"}
                       for t, v in tec[:150]],
        "gradient": {"colors": ["#1E2A27", "#F4BE3F"], "minValue": 0, "maxValue": maximo},
    }
    sid = f"SIG-APT4ALL-{slug(pais)}-{slug(setor)}"
    adversarios = [x["ator"]["mitre"]["id"] if x["ator"].get("mitre") else "apt4all:" + x["ator"]["id"] for x in res[:30]]
    sinal = {
        "id": sid, "kind": "apt4all-threat-profile", "status": "candidate", "scope": "sector" if setor else "global",
        "target_ids": [], "crown_jewel_ids": [], "technique_ids": [t for t, _ in tec[:top]], "adversary_ids": adversarios,
        "severity": "medium", "confidence": "low", "source_reliability": "C", "information_credibility": 0.5,
        "relevance": 0.6, "direction": "increase", "observed_at": meta.get("gerado_em"), "half_life_days": 90,
        "source_ref": "APT4ALL Atlas (MITRE ATT&CK, MISP Galaxy, APT Groups and Operations)",
        "rationale": (f"Perfil de ameaça por vitimologia histórica: país={pais or 'qualquer'}, setor={setor or 'qualquer'}. "
                      "Presença histórica não estabelece direcionamento atual contra a organização."),
        "review_required": True,
    }
    with open(os.path.join(saida, "navigator.json"), "w", encoding="utf-8") as f:
        json.dump(camada, f, ensure_ascii=False, indent=1)
    with open(os.path.join(saida, "tce-sinais.json"), "w", encoding="utf-8") as f:
        json.dump({"version": "0.5", "provider": "apt4all", "review_required": True, "auto_accept": False,
                   "intelligence_signal_candidates": [sinal]}, f, ensure_ascii=False, indent=1)
    campos = ["id", "kind", "scope", "target_ids", "technique_ids", "severity", "confidence", "source_reliability",
              "information_credibility", "relevance", "direction", "status", "observed_at", "half_life_days", "source_ref"]
    with open(os.path.join(saida, "tce-intelligence.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerow({k: (";".join(v) if isinstance(v, list) else v) for k, v in sinal.items() if k in campos})
    with open(os.path.join(saida, "perfil.md"), "w", encoding="utf-8") as f:
        f.write(f"# Perfil de ameaça: {pais or 'qualquer país'} · {setor or 'qualquer setor'}\n\n")
        f.write(f"Base APT4ALL de {meta.get('gerado_em')} · ATT&CK v{meta.get('attack_versao')} · {len(res)} atores relevantes.\n\n")
        f.write("> Ponto de partida para modelagem de ameaças, não previsão. Confirme cada ator nas fontes antes de decidir.\n\n")
        f.write("## Atores\n\n| # | Ator | País de origem | Pontos | Por quê |\n|---|---|---|---|---|\n")
        for i, x in enumerate(res[:40], 1):
            a = x["ator"]
            f.write(f"| {i} | {a['nome']}{' (' + a['mitre']['id'] + ')' if a.get('mitre') else ''} | {a.get('pais') or '—'} | {x['score']} | {', '.join(x['porque'])} |\n")
        f.write("\n## Técnicas a cobrir primeiro\n\n| Técnica | Peso |\n|---|---|\n")
        for t, v in tec[:25]:
            f.write(f"| [{t}](https://attack.mitre.org/techniques/{t.replace('.', '/')}/) | {v} |\n")
    return sid


def main():
    ap = argparse.ArgumentParser(description="Perfil de ameaça APT4ALL para o TCE")
    ap.add_argument("--pais", default="", help="país da organização: código ISO (BR) ou nome em inglês (Brazil)")
    ap.add_argument("--setor", default="", help="setor, como aparece no atlas (ex.: Financial, Government)")
    ap.add_argument("--origem", choices=["todos", "estado"], default="todos")
    ap.add_argument("--saida", default="saida/perfil")
    ap.add_argument("--dados")
    ap.add_argument("--listar", choices=["paises", "setores"])
    a = ap.parse_args()
    d = carrega(a.dados)
    if a.listar:
        c = Counter(v for x in d["atores"] for v in x.get("vitimas_iso" if a.listar == "paises" else "setores", []))
        for k, n in sorted(c.items()):
            print(f"{n:4}  {k}")
        return 0
    res, tec = calcula(d["atores"], a.pais, a.setor, a.origem)
    if not res:
        print("Nenhum ator para esse recorte. Use --listar paises ou --listar setores para ver os valores aceitos.")
        return 1
    sid = exporta(res, tec, d["meta"], a.pais, a.setor, a.saida)
    print(f"{len(res)} atores · {len(tec)} técnicas · sinal {sid} → {a.saida}/")
    for x in res[:8]:
        print(f"  {x['score']}  {x['ator']['nome']}  ({', '.join(x['porque'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
