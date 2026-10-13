#!/usr/bin/env python3
"""verificar_links.py — confere se os links de recursos/recursos.json respondem (só biblioteca padrão).

Uso: python3 ferramentas/recursos/verificar_links.py [--saida dados/gerados/links.json]
Saída: um JSON {url: {"codigo": 200, "ok": true, "quando": "..."}} usado pelo gerador de listas.
Código 0 = não foi possível conectar (rede bloqueada, DNS ou tempo esgotado): o link não é dado como morto.
"""
import argparse, json, os, sys, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = {"User-Agent": "Mozilla/5.0 (apt4all link checker; +https://github.com/Ridd1kulusC0d3r/apt4all)"}


def testa(url):
    for metodo in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=metodo, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                return url, r.status
        except urllib.error.HTTPError as e:
            if metodo == "HEAD" and e.code in (403, 405, 400, 429, 501):
                continue
            return url, e.code
        except Exception:
            if metodo == "HEAD":
                continue
            return url, 0
    return url, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", default=os.path.join(RAIZ, "dados", "gerados", "links.json"))
    a = ap.parse_args()
    dados = json.load(open(os.path.join(RAIZ, "recursos", "recursos.json"), encoding="utf-8"))
    urls = sorted({r["url"] for r in dados["recursos"]})
    quando = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with ThreadPoolExecutor(12) as ex:
        res = dict(ex.map(testa, urls))
    out = {u: {"codigo": c, "ok": 200 <= c < 400 or c in (401, 403, 429), "quando": quando} for u, c in res.items()}
    os.makedirs(os.path.dirname(a.saida), exist_ok=True)
    json.dump(out, open(a.saida, "w"), indent=1)
    mortos = [u for u, v in out.items() if v["codigo"] in (404, 410)]
    sem = [u for u, v in out.items() if v["codigo"] == 0]
    print(f"{len(urls)} links · {sum(v['ok'] for v in out.values())} ok · {len(mortos)} mortos (404/410) · {len(sem)} sem conexão")
    for u in mortos:
        print("  MORTO", u)
    return 1 if mortos else 0


if __name__ == "__main__":
    sys.exit(main())
