#!/usr/bin/env python3
"""construir_dados.py — monta o banco de atores do apt4all (só biblioteca padrão).

Junta quatro fontes abertas, resolve aliases e gera os arquivos que o Atlas lê:

  1. Planilha "APT Groups and Operations" (Florian Roth e comunidade, CC BY 4.0) — abas por país
  2. MISP Galaxy threat-actor (CC0 1.0 / BSD-2)
  3. MITRE ATT&CK Enterprise (grupos, técnicas, softwares; termos de uso da MITRE)
  4. EternalLiberty (mapa de nomes entre fornecedores) e APTnotes (índice de relatórios) — só referência cruzada

Uso:
  python3 ferramentas/atlas/construir_dados.py                 # usa o cache em dados/brutos/
  python3 ferramentas/atlas/construir_dados.py --baixar        # baixa as fontes online antes
Saída: docs/atlas/atores.json, docs/atlas/paises.json e dados/gerados/resumo.md
"""
import argparse, csv, io, json, os, re, sys, urllib.parse, urllib.request
from collections import Counter, defaultdict
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRUTOS = os.path.join(RAIZ, "dados", "brutos")
URLS = {
    "misp-threat-actor.json": "https://raw.githubusercontent.com/MISP/misp-galaxy/main/clusters/threat-actor.json",
    "enterprise-attack.json": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json",
    "EternalLiberty.csv": "https://raw.githubusercontent.com/StrangerealIntel/EternalLiberty/main/EternalLiberty.csv",
    "APTnotes.csv": "https://raw.githubusercontent.com/aptnotes/data/master/APTnotes.csv",
}
PLANILHA_ID = "1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU"
ABAS = {"China": "CN", "Russia": "RU", "North Korea": "KP", "Iran": "IR", "Israel": "IL",
        "NATO": "NATO", "Middle East": None, "Others": None, "Unknown": None}
NAO_ALIAS = ("operation", "toolset", "targets", "modus", "comment", "link", "overlaps", "origin", "mitre")
GENERICOS = {"apt", "group", "team", "unknown", "na", "none", "hackers", "hacker", "unc", "temp", "the",
             "cyber", "army", "spider", "panda", "bear", "kitten", "chollima"}
SINONIMOS_PAIS = {
    "north korea": "KP", "dprk": "KP", "south korea": "KR", "korea": "KR", "russia": "RU", "russian federation": "RU",
    "iran": "IR", "china": "CN", "prc": "CN", "usa": "US", "us": "US", "united states": "US", "united states of america": "US",
    "uk": "GB", "united kingdom": "GB", "vietnam": "VN", "viet nam": "VN", "uae": "AE", "united arab emirates": "AE",
    "gaza": "PS", "palestine": "PS", "palestinian territories": "PS", "lebanon": "LB", "syria": "SY", "turkey": "TR",
    "türkiye": "TR", "pakistan": "PK", "india": "IN", "brazil": "BR", "brasil": "BR", "israel": "IL", "belarus": "BY",
    "ukraine": "UA", "nigeria": "NG", "kazakhstan": "KZ", "italy": "IT", "spain": "ES", "france": "FR", "germany": "DE",
    "tunisia": "TN", "morocco": "MA", "egypt": "EG", "romania": "RO", "indonesia": "ID", "taiwan": "TW", "japan": "JP",
    "colombia": "CO", "mexico": "MX", "argentina": "AR", "chile": "CL", "peru": "PE", "venezuela": "VE",
    "saudi arabia": "SA", "qatar": "QA", "kuwait": "KW", "yemen": "YE", "iraq": "IQ", "algeria": "DZ",
}


def baixar():
    os.makedirs(BRUTOS, exist_ok=True)
    for nome, url in URLS.items():
        print("baixando", nome)
        with urllib.request.urlopen(url, timeout=180) as r, open(os.path.join(BRUTOS, nome), "wb") as f:
            f.write(r.read())
    destino = os.path.join(BRUTOS, "planilha-apt")
    os.makedirs(destino, exist_ok=True)
    for aba in ABAS:
        url = f"https://docs.google.com/spreadsheets/d/{PLANILHA_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(aba)}"
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                dados = r.read().decode("utf-8", "replace")
            if "Common Name" not in "\n".join(dados.splitlines()[:6]):
                print("  [aviso] aba", aba, "veio em formato inesperado; mantida a cópia local")
                continue
            # o gviz não traz a linha de título da aba; recoloca para o formato do export
            open(os.path.join(destino, re.sub(r"[^A-Za-z0-9]+", "_", aba) + ".csv"), "w", encoding="utf-8").write(aba + "\n" + dados)
        except Exception as e:
            print("  [aviso] aba", aba, "não baixada:", e)


def conserta(s):
    """Corrige texto UTF-8 lido como cp1252 (ex.: 'â€“' -> '–')."""
    if s and ("â€" in s or "Ã" in s):
        try:
            return s.encode("cp1252").decode("utf-8")
        except Exception:
            return s
    return s


def norm(a):
    return re.sub(r"[^a-z0-9]", "", (a or "").lower())


def divide(celula):
    out = []
    for p in re.split(r"[,;\n]| / ", celula or ""):
        p = conserta(p.strip().strip('"').strip())
        if p and len(p) <= 60:
            out.append(p)
    return out


def chave_valida(n):
    return len(n) >= 3 and n not in GENERICOS and not n.isdigit()


class Registros:
    def __init__(self):
        self.itens = []          # dicts com 'fonte', 'nome', 'aliases' etc.

    def add(self, **kw):
        kw.setdefault("aliases", [])
        self.itens.append(kw)
        return len(self.itens) - 1


PT_BR = {"Irão": "Irã", "Vietname": "Vietnã", "Arménia": "Armênia", "Chéquia": "Tchéquia", "Eslovénia": "Eslovênia",
         "Estónia": "Estônia", "Letónia": "Letônia", "Macedónia do Norte": "Macedônia do Norte", "Nova Caledónia": "Nova Caledônia",
         "Polónia": "Polônia", "Quénia": "Quênia", "Roménia": "Romênia", "Iémen": "Iêmen", "Benim": "Benin",
         "Ilhas Malvinas": "Malvinas", "Gronelândia": "Groenlândia", "Moldávia": "Moldávia", "Singapura": "Singapura"}


def ler_paises():
    gj = json.load(open(os.path.join(BRUTOS, "ne_110m_admin_0_countries.geojson"), encoding="utf-8"))
    paises = {}
    for f in gj["features"]:
        p = f["properties"]
        iso = p.get("ISO_A2_EH") if p.get("ISO_A2") in ("-99", None) else p.get("ISO_A2")
        if not iso or iso == "-99":
            continue
        paises[iso] = {"iso": iso, "nome_en": p.get("NAME"), "nome_pt": PT_BR.get(p.get("NAME_PT"), p.get("NAME_PT") or p.get("NAME")),
                       "continente": p.get("CONTINENT"), "x": p.get("LABEL_X"), "y": p.get("LABEL_Y")}
    return paises


def mapa_nomes(paises):
    m = dict(SINONIMOS_PAIS)
    for iso, p in paises.items():
        for k in (p["nome_en"], p["nome_pt"]):
            if k:
                m[k.lower()] = iso
    return m


def para_iso(txt, nomes):
    if not txt:
        return None
    t = conserta(txt).strip().lower()
    if t in nomes:
        return nomes[t]
    if len(t) == 2 and t.upper() in {v for v in nomes.values()}:
        return t.upper()
    for k, v in nomes.items():
        if len(k) > 3 and re.search(r"\b" + re.escape(k) + r"\b", t):
            return v
    return None


FORNECEDORES = [("crowdstrike", "CrowdStrike"), ("kaspersky", "Kaspersky"), ("secure", "Secureworks"),
                ("mandiant", "Mandiant"), ("fireeye", "FireEye"), ("symantec", "Symantec"), ("isight", "iSight"),
                ("cisco", "Cisco Talos"), ("talos", "Cisco Talos"), ("palo alto", "Palo Alto Unit 42"),
                ("irl", "IRL"), ("fsi", "FSI (KR)"), ("nsa", "NSA")]


def fornecedor(coluna):
    c = coluna.lower().strip()
    return next((rot for chave, rot in FORNECEDORES if c.startswith(chave) or chave in c.split(" (")[0]), None)


def ler_microsoft():
    """Aba 'Microsoft 2023 renaming taxonomy': nome novo, nome antigo e outros nomes."""
    fn = os.path.join(BRUTOS, "planilha-apt", "Microsoft_2023_renaming_taxonomy.csv")
    porNome, outros = {}, {}
    if not os.path.exists(fn):
        return porNome, outros
    for l in csv.reader(open(fn, encoding="utf-8", errors="replace")):
        for i in (1, 6):  # a aba tem duas tabelas lado a lado
            if len(l) > i + 3 and l[i + 1].strip() and l[i].strip().lower() != "previous name":
                antigo, novo = conserta(l[i].strip()), conserta(l[i + 1].strip())
                par = (novo, antigo)
                for n in (antigo, novo):
                    porNome.setdefault(norm(n), par)
                for o in divide(l[i + 3]):
                    outros.setdefault(norm(o), set()).add(par)
    return porNome, outros


def ler_planilha(reg, nomes):
    pasta = os.path.join(BRUTOS, "planilha-apt")
    for aba, iso_aba in ABAS.items():
        fn = os.path.join(pasta, re.sub(r"[^A-Za-z0-9]+", "_", aba) + ".csv")
        if not os.path.exists(fn):
            continue
        linhas = list(csv.reader(io.StringIO(open(fn, encoding="utf-8", errors="replace").read())))
        # a primeira linha é o título da aba; o cabeçalho é a primeira que começa com "Common Name"
        h = next((i for i, l in enumerate(linhas) if l and l[0].strip().lower() == "common name"), None)
        if h is None:
            continue
        cab = [c.strip() for c in linhas[h]]
        for l in linhas[h + 1:]:
            if not l or not l[0].strip():
                continue
            row = {cab[i]: (l[i] if i < len(l) else "") for i in range(len(cab))}
            nome = conserta(l[0].strip())
            aliases, mitre, ops, ferr, alvos, links, origem = [nome], None, [], [], "", [], ""
            forn = {}
            for c, v in row.items():
                cl = c.lower()
                if not v.strip():
                    continue
                if cl.startswith("mitre"):
                    m = re.search(r"G\d{4}", v)
                    mitre = m.group(0) if m else mitre
                elif cl.startswith("operation"):
                    ops += divide(v)
                elif cl.startswith("toolset"):
                    ferr += divide(v)
                elif cl.startswith("targets"):
                    alvos = conserta(v.strip())
                elif cl.startswith("link"):
                    if v.strip().startswith("http"):
                        links.append(v.strip())
                elif cl.startswith("origin"):
                    origem = v.strip()
                elif not cl.startswith(NAO_ALIAS) and cl != "common name":
                    aliases += divide(v)
                    rot = None if cl.startswith("other name") else fornecedor(c)
                    if rot:
                        forn.setdefault(rot, [])
                        forn[rot] += [conserta(x) for x in divide(v) if conserta(x) not in forn[rot]]
            # aliases que são IDs da MITRE escondidos em "Other Names"
            for a in list(aliases):
                if re.fullmatch(r"G\d{4}", a):
                    mitre = mitre or a
                    aliases.remove(a)
            iso = iso_aba if iso_aba else para_iso(origem, nomes)
            reg.add(fonte="planilha", nome=nome, aliases=aliases, mitre=mitre, operacoes=ops, ferramentas=ferr,
                    alvos_txt=alvos, links=links, pais=iso, aba=aba, origem_txt=origem, fornecedores=forn)


def ler_misp(reg, nomes):
    d = json.load(open(os.path.join(BRUTOS, "misp-threat-actor.json"), encoding="utf-8"))
    for v in d["values"]:
        m = v.get("meta", {})
        mitre = None
        for na in m.get("name-attribution", []) + m.get("synonyms", []):
            mm = re.match(r"(G\d{4})", na)
            if mm:
                mitre = mm.group(1)
        als = [v["value"]] + [s for s in m.get("synonyms", []) if not re.fullmatch(r"G\d{4}", s)]
        als += [na.split(":")[0] for na in m.get("name-attribution", []) if not re.match(r"G\d{4}", na)]
        iso = m.get("country") or para_iso(m.get("cfr-suspected-state-sponsor"), nomes)
        reg.add(fonte="misp", nome=v["value"], aliases=als, mitre=mitre, pais=iso,
                descricao=(v.get("description") or "").strip(), links=m.get("refs", [])[:20],
                setores=m.get("cfr-target-category", []) + m.get("targeted-sector", []),
                vitimas=m.get("cfr-suspected-victims", []), incidente=m.get("cfr-type-of-incident"),
                confianca=m.get("attribution-confidence"), uuid=v.get("uuid"))


def ler_mitre(reg):
    fn = os.path.join(BRUTOS, "enterprise-attack.json")
    if not os.path.exists(fn):
        print("[aviso] ATT&CK ausente; rode com --baixar para técnicas e softwares")
        return
    objs = json.load(open(fn, encoding="utf-8"))["objects"]
    por_id = {o["id"]: o for o in objs}
    ext = lambda o: next((r["external_id"] for r in o.get("external_references", []) if r.get("source_name") == "mitre-attack"), None)
    grupos = {o["id"]: o for o in objs if o["type"] == "intrusion-set" and not o.get("revoked") and not o.get("x_mitre_deprecated")}
    tecnicas, softwares = defaultdict(set), defaultdict(set)
    for r in objs:
        if r["type"] != "relationship" or r.get("relationship_type") != "uses" or r.get("revoked"):
            continue
        if r["source_ref"] in grupos:
            alvo = por_id.get(r["target_ref"])
            if not alvo or alvo.get("revoked") or alvo.get("x_mitre_deprecated"):
                continue
            if alvo["type"] == "attack-pattern":
                tecnicas[r["source_ref"]].add(ext(alvo))
            elif alvo["type"] in ("malware", "tool"):
                softwares[r["source_ref"]].add(alvo["name"])
    versao = next((o.get("x_mitre_version") for o in objs if o["type"] == "x-mitre-collection"), None)
    NOMES_TECNICAS.update({ext(o): o["name"] for o in objs if o["type"] == "attack-pattern" and not o.get("revoked")})
    for gid, g in grupos.items():
        desc = re.sub(r"\(Citation:[^)]*\)", "", g.get("description", "")).strip()
        reg.add(fonte="mitre", nome=g["name"], aliases=g.get("aliases", []), mitre=ext(g),
                descricao=desc, tecnicas=sorted(t for t in tecnicas[gid] if t), softwares=sorted(softwares[gid]),
                modificado=g.get("modified", "")[:10])
    return versao


NOMES_TECNICAS = {}


def ler_eternal(reg, nomes):
    fn = os.path.join(BRUTOS, "EternalLiberty.csv")
    if not os.path.exists(fn):
        return
    for r in csv.DictReader(open(fn, encoding="utf-8", errors="replace")):
        nome = r.pop("Threat Actor Official Name", "").strip()
        if not nome:
            continue
        conf, tipo, pais = r.pop("Confidence", ""), r.pop("Type", ""), r.pop("Country", "")
        mitre = None
        als = [nome]
        for fornecedor, v in r.items():
            for a in divide(v or ""):
                if re.fullmatch(r"G\d{4}", a):
                    mitre = a
                else:
                    als.append(a)
        reg.add(fonte="eternalliberty", nome=nome, aliases=als, mitre=mitre, tipo=tipo, confianca_txt=conf,
                pais=para_iso(pais, nomes))


def unir(reg):
    """Resolução por âncoras (evita o efeito cascata do union-find).

    Ordem de confiança: MITRE ATT&CK > planilha > MISP > EternalLiberty. Cada registro novo se junta a um ator
    já existente pelo ID da MITRE, pelo nome principal ou por um alias que aponte para um único ator. Aliases
    reivindicados por dois atores viram ambíguos e deixam de ligar registros.
    """
    atores = []                 # lista de listas de registros
    idx = {}                    # alias normalizado -> índice do ator (ou -1 se ambíguo)
    por_g = {}

    def registra(n, k):
        if not chave_valida(n):
            return
        if n in idx and idx[n] != k:
            idx[n] = -1
        elif n not in idx:
            idx[n] = k

    def acha(r):
        if r.get("mitre") and r["mitre"] in por_g:
            return por_g[r["mitre"]]
        n = norm(r["nome"])
        if idx.get(n, -1) >= 0:
            return idx[n]
        cands = {idx[norm(a)] for a in r["aliases"] if idx.get(norm(a), -1) >= 0}
        return cands.pop() if len(cands) == 1 else None

    for fonte in ("mitre", "planilha", "misp", "eternalliberty"):
        for r in [x for x in reg.itens if x["fonte"] == fonte]:
            k = None if fonte == "mitre" else acha(r)
            if k is None:
                k = len(atores)
                atores.append([])
            atores[k].append(r)
            if r.get("mitre"):
                por_g.setdefault(r["mitre"], k)
            for a in [r["nome"]] + r["aliases"]:
                registra(norm(a), k)
    return atores


MOTIVOS = [("espionagem", r"espionage|espionagem|intelligence (?:collection|gathering)|state-sponsored|nation-state"),
           ("financeiro", r"financially motivated|financial gain|organi[sz]ed crime|cybercrim|ransomware|banking trojan|fraud|theft of funds"),
           ("sabotagem", r"sabotage|destructive|wiper|disrupt"),
           ("hacktivismo", r"hacktivis|activist|defacement"),
           ("influência", r"influence operation|information operation|disinformation")]


def motivo(cl):
    partes = []
    for r in cl:
        for k in ("incidente", "tipo"):
            v = r.get(k)
            partes += v if isinstance(v, list) else [v or ""]
        partes.append((r.get("descricao") or "")[:700])
    txt = " ".join(p for p in partes if isinstance(p, str))
    out = [m for m, rx in MOTIVOS if re.search(rx, txt, re.I)]
    return out or ["indefinido"]


SETORES = [  # chave canônica, rótulo PT, rótulo EN, regex sobre os valores das fontes
    ("government", "Governo", "Government", r"govern|administra|public sector|diplomat|embass|ministr|policy|politic"),
    ("military", "Defesa e militar", "Defense and military", r"militar|defen[cs]e|armed forces|aerospace"),
    ("finance", "Financeiro", "Finance", r"financ|bank|insur|crypto|payment|fintech"),
    ("energy", "Energia", "Energy", r"energy|oil|gas|utilit|electric|nuclear|power"),
    ("health", "Saúde", "Healthcare", r"health|medical|pharma|hospital"),
    ("education", "Educação e pesquisa", "Education and research", r"educat|universit|academ|research|think tank"),
    ("telecom", "Telecomunicações", "Telecommunications", r"telecom|telco|isp|satellite"),
    ("technology", "Tecnologia", "Technology", r"tech|software|it |information technology|semiconductor|cloud|msp"),
    ("civil", "Sociedade civil e mídia", "Civil society and media", r"civil|ngo|activist|journal|media|dissident|human rights|religio"),
    ("private", "Setor privado (genérico)", "Private sector (general)", r"private sector|commercial|business"),
    ("manufacturing", "Indústria", "Manufacturing", r"manufactur|industr|automotive|chemical|engineering"),
    ("transport", "Transporte e logística", "Transportation and logistics", r"transport|aviation|airline|maritime|shipping|logistic|rail"),
    ("retail", "Varejo e hotelaria", "Retail and hospitality", r"retail|hospitality|hotel|restaurant|e-commerce|gaming|casino"),
    ("infrastructure", "Infraestrutura crítica", "Critical infrastructure", r"critical infra|ics|scada|water|ot "),
]


def setores_canonicos(valores):
    out = set()
    for v in valores:
        for k, _, _, rx in SETORES:
            if re.search(rx, " " + str(v).lower() + " "):
                out.add(k)
    return sorted(out)


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-") or "ator"


def consolida(clusters, notas, microsoft=None):
    ms_nome, ms_outros = microsoft or ({}, {})
    atores, usados = [], set()
    for cl in clusters:
        prio = {"mitre": 0, "planilha": 1, "misp": 2, "eternalliberty": 3}
        cl.sort(key=lambda r: prio[r["fonte"]])
        nome = cl[0]["nome"]
        aliases = []
        vistos = {norm(nome)}
        for r in cl:
            for a in [r["nome"]] + r["aliases"]:
                n = norm(a)
                if n and n not in vistos and not re.fullmatch(r"g\d{4}", n):
                    vistos.add(n)
                    aliases.append(a)
        # país: planilha > MISP > EternalLiberty
        pais = None
        for f in ("planilha", "misp", "eternalliberty"):
            cands = [r.get("pais") for r in cl if r["fonte"] == f and r.get("pais")]
            if cands:
                pais = Counter(cands).most_common(1)[0][0]
                break
        mitre = next((r for r in cl if r["fonte"] == "mitre"), None)
        mitre_id = mitre["mitre"] if mitre else next((r["mitre"] for r in cl if r.get("mitre")), None)
        misp = next((r for r in cl if r["fonte"] == "misp"), None)
        plan = [r for r in cl if r["fonte"] == "planilha"]
        desc = (mitre or {}).get("descricao") or (misp or {}).get("descricao") or ""
        desc = re.sub(r"\[([^\]]+)\]\((?:https?://)[^)]+\)", r"\1", desc)
        desc = re.sub(r"\s+", " ", desc)
        frases = re.split(r"(?<=[.!?])\s+", desc)
        links = []
        for r in cl:
            for l in r.get("links", []):
                if l not in links:
                    links.append(l)
        forn = {}
        if mitre_id:
            forn["MITRE ATT&CK"] = [mitre_id]
        par = next((ms_nome[n] for n in [norm(nome)] + [norm(a) for a in aliases] if n in ms_nome), None)
        if not par and len(ms_outros.get(norm(nome), ())) == 1:
            par = next(iter(ms_outros[norm(nome)]))
        if par:
            forn["Microsoft"] = [par[0]] + ([f"{par[1]} (antigo · old)"] if par[1] and par[1] != par[0] else [])
        for r in plan:
            for k, v in (r.get("fornecedores") or {}).items():
                forn.setdefault(k, [])
                forn[k] += [x for x in v if x not in forn[k]]
        sid = slug(nome)
        while sid in usados:
            sid += "-x"
        usados.add(sid)
        atores.append({
            "id": sid, "nome": nome, "aliases": aliases[:40], "n_aliases": len(aliases), "pais": pais,
            "motivos": motivo(cl),
            "mitre": {"id": mitre_id, "url": f"https://attack.mitre.org/groups/{mitre_id}/",
                      "tecnicas": (mitre or {}).get("tecnicas", []), "softwares": (mitre or {}).get("softwares", []),
                      "modificado": (mitre or {}).get("modificado")} if mitre_id else None,
            "descricao": " ".join(frases[:3])[:700],
            "setores": setores_canonicos({s for r in cl for s in r.get("setores", []) if s} |
                                         {r["alvos_txt"] for r in plan if r.get("alvos_txt")}),
            "vitimas": sorted({v for r in cl for v in r.get("vitimas", []) if v})[:30],
            "alvos": " | ".join(dict.fromkeys(r["alvos_txt"] for r in plan if r.get("alvos_txt")))[:900],
            "operacoes": list(dict.fromkeys(o for r in plan for o in r.get("operacoes", [])))[:20],
            "ferramentas": list(dict.fromkeys([f for r in plan for f in r.get("ferramentas", [])] +
                                              (mitre or {}).get("softwares", [])))[:40],
            "confianca": (misp or {}).get("confianca") or next((r.get("confianca_txt") for r in cl if r.get("confianca_txt")), None),
            "fontes": sorted({r["fonte"] for r in cl}),
            "abas": sorted({r["aba"] for r in plan}),
            "links": links[:15], "relatorios": [], "fornecedores": forn,
        })
    return atores


RUINS_PARA_TITULO = {"lazarus", "turla", "sofacy"}  # nenhum é ruim; lista mantida para ajuste manual


def liga_aptnotes(atores):
    fn = os.path.join(BRUTOS, "APTnotes.csv")
    if not os.path.exists(fn):
        return 0
    notas = list(csv.DictReader(open(fn, encoding="utf-8", errors="replace")))
    total = 0
    for a in atores:
        termos = [x for x in [a["nome"]] + a["aliases"] if len(norm(x)) >= 5 and norm(x) not in GENERICOS]
        if not termos:
            continue
        rx = re.compile(r"\b(" + "|".join(re.escape(t) for t in termos[:40]) + r")\b", re.I)
        for n in notas:
            if rx.search(n.get("Title", "")):
                a["relatorios"].append({"titulo": n["Title"].strip(), "fonte": n.get("Source", "").strip(),
                                        "data": n.get("Date", "").strip(), "link": n.get("Link", "").strip()})
        a["relatorios"] = sorted(a["relatorios"], key=lambda r: r["data"], reverse=True)[:25]
        total += len(a["relatorios"])
    return total


def agrega_paises(atores, paises):
    por = defaultdict(list)
    for a in atores:
        por[a["pais"] or "??"].append(a)
    out = {}
    for iso, lista in por.items():
        p = paises.get(iso, {})
        mot = Counter(m for a in lista for m in a["motivos"])
        tec = Counter(t for a in lista if a["mitre"] for t in a["mitre"]["tecnicas"])
        set_ = Counter(s for a in lista for s in a["setores"])
        vit = Counter(v for a in lista for v in a["vitimas"])
        out[iso] = {
            "iso": iso,
            "nome_pt": {"NATO": "OTAN / Five Eyes", "??": "Sem país atribuído"}.get(iso, p.get("nome_pt", iso)),
            "nome_en": {"NATO": "NATO / Five Eyes", "??": "Unattributed"}.get(iso, p.get("nome_en", iso)),
            "atores": len(lista), "com_mitre": sum(1 for a in lista if a["mitre"]),
            "aliases": sum(a["n_aliases"] for a in lista),
            "relatorios": sum(len(a["relatorios"]) for a in lista),
            "motivos": mot.most_common(), "top_tecnicas": tec.most_common(15),
            "top_setores": set_.most_common(10), "top_vitimas": vit.most_common(12),
            "ids": [a["id"] for a in sorted(lista, key=lambda a: (-(len(a["mitre"]["tecnicas"]) if a["mitre"] else 0), a["nome"]))],
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baixar", action="store_true")
    ap.add_argument("--saida", default=os.path.join(RAIZ, "docs", "atlas"))
    a = ap.parse_args()
    if a.baixar:
        baixar()
    paises = ler_paises()
    nomes = mapa_nomes(paises)
    reg = Registros()
    ler_planilha(reg, nomes)
    ler_misp(reg, nomes)
    versao = ler_mitre(reg)
    ler_eternal(reg, nomes)
    clusters = unir(reg)
    atores = consolida(clusters, None, ler_microsoft())
    nrel = liga_aptnotes(atores)
    atores.sort(key=lambda x: x["nome"].lower())
    agg = agrega_paises(atores, paises)
    os.makedirs(a.saida, exist_ok=True)
    meta = {"gerado_em": date.today().isoformat(), "attack_versao": versao, "n_atores": len(atores),
            "n_registros": len(reg.itens), "fontes": Counter(r["fonte"] for r in reg.itens), "n_relatorios": nrel}
    json.dump({"meta": meta, "atores": atores}, open(os.path.join(a.saida, "atores.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    usadas = {t for x in atores if x["mitre"] for t in x["mitre"]["tecnicas"]}
    json.dump({"meta": meta, "setores": {k: {"pt": pt, "en": en} for k, pt, en, _ in SETORES}, "tecnicas": {t: NOMES_TECNICAS.get(t, t) for t in sorted(usadas)}, "paises": agg, "geo": {k: {"x": v["x"], "y": v["y"], "nome_pt": v["nome_pt"],
              "nome_en": v["nome_en"]} for k, v in paises.items()}},
              open(os.path.join(a.saida, "paises.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    os.makedirs(os.path.join(RAIZ, "dados", "gerados"), exist_ok=True)
    with open(os.path.join(RAIZ, "dados", "gerados", "resumo.md"), "w", encoding="utf-8") as f:
        f.write(f"# Resumo da base ({meta['gerado_em']})\n\n- Registros lidos: {meta['n_registros']} {dict(meta['fontes'])}\n"
                f"- Atores após resolução de aliases: {meta['n_atores']}\n- Versão ATT&CK: {versao}\n"
                f"- Relatórios APTnotes ligados: {nrel}\n\n| País | Atores | Com ATT&CK | Aliases |\n|---|---|---|---|\n")
        for iso, p in sorted(agg.items(), key=lambda kv: -kv[1]["atores"]):
            f.write(f"| {p['nome_pt']} ({iso}) | {p['atores']} | {p['com_mitre']} | {p['aliases']} |\n")
    print(json.dumps(meta, default=dict, ensure_ascii=False))
    top = sorted(agg.values(), key=lambda p: -p["atores"])[:12]
    print(" | ".join(f"{p['iso']}:{p['atores']}" for p in top))
    grandes = sorted(clusters, key=len, reverse=True)[:5]
    print("maiores clusters:", [(len(c), c[0]["nome"]) for c in grandes])
    return 0


if __name__ == "__main__":
    sys.exit(main())
