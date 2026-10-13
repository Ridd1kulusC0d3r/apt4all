#!/usr/bin/env python3
"""mapa_hex.py — gera o mapa-múndi em hexágonos usado pelo Atlas (só biblioteca padrão).

Lê os contornos de países do Natural Earth (domínio público, escala 1:110m), cobre o mundo com uma grade
de hexágonos e atribui cada hexágono ao país que contém o seu centro. Países pequenos demais para conter
um centro recebem um hexágono livre perto do ponto de rótulo.

Uso: python3 ferramentas/atlas/mapa_hex.py [--passo 2.0]
Saída: docs/atlas/mapa.json  ->  {"passo":2.0,"hex":[[coluna, linha, "BR"], ...]}
"""
import argparse, json, math, os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def poligonos(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon":
        return geom["coordinates"]
    return []


def dentro(x, y, anel):
    d = False
    j = len(anel) - 1
    for i in range(len(anel)):
        xi, yi = anel[i][0], anel[i][1]
        xj, yj = anel[j][0], anel[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            d = not d
        j = i
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passo", type=float, default=2.0)
    a = ap.parse_args()
    gj = json.load(open(os.path.join(RAIZ, "dados", "brutos", "ne_110m_admin_0_countries.geojson"), encoding="utf-8"))
    paises = []
    for f in gj["features"]:
        p = f["properties"]
        iso = p.get("ISO_A2_EH") if p.get("ISO_A2") in ("-99", None) else p.get("ISO_A2")
        if not iso or iso == "-99" or iso == "AQ":
            continue
        polys = poligonos(f["geometry"])
        xs = [pt[0] for pl in polys for pt in pl[0]]
        ys = [pt[1] for pl in polys for pt in pl[0]]
        paises.append((iso, polys, (min(xs), min(ys), max(xs), max(ys)), (p.get("LABEL_X"), p.get("LABEL_Y"))))
    dx = a.passo
    dy = dx * math.sqrt(3) / 2
    grade = {}
    lin = 0
    lat = 80.0
    while lat > -57:
        desloc = (dx / 2) if lin % 2 else 0
        col = 0
        lon = -180 + desloc
        while lon < 180:
            for iso, polys, bb, _ in paises:
                if not (bb[0] <= lon <= bb[2] and bb[1] <= lat <= bb[3]):
                    continue
                if any(dentro(lon, lat, pl[0]) and not any(dentro(lon, lat, buraco) for buraco in pl[1:]) for pl in polys):
                    grade[(col, lin)] = iso
                    break
            col += 1
            lon += dx
        lin += 1
        lat -= dy
    presentes = set(grade.values())
    for iso, polys, bb, (lx, ly) in paises:
        if iso in presentes or lx is None:
            continue
        lin_f = (80.0 - ly) / dy
        melhor = None
        for r in range(int(lin_f) - 3, int(lin_f) + 4):
            desloc = (dx / 2) if r % 2 else 0
            c0 = (lx + 180 - desloc) / dx
            for c in range(int(c0) - 3, int(c0) + 4):
                if (c, r) in grade:
                    continue
                cx, cy = -180 + desloc + c * dx, 80.0 - r * dy
                dist = (cx - lx) ** 2 + (cy - ly) ** 2
                if melhor is None or dist < melhor[0]:
                    melhor = (dist, c, r)
        if melhor:
            grade[(melhor[1], melhor[2])] = iso
    out = {"passo": dx, "lat0": 80.0, "hex": [[c, r, iso] for (c, r), iso in sorted(grade.items(), key=lambda kv: (kv[0][1], kv[0][0]))]}
    destino = os.path.join(RAIZ, "docs", "atlas", "mapa.json")
    json.dump(out, open(destino, "w"), separators=(",", ":"))
    print(f"{len(out['hex'])} hexágonos, {len(set(grade.values()))} países -> {destino}")


if __name__ == "__main__":
    main()
