#!/usr/bin/env python3
"""Refaz as telas do manual (docs/manual/img) e os marcadores numerados.
Opcional: precisa do Playwright (pip install playwright; playwright install chromium).

Uso: python3 ferramentas/manual/capturar_telas.py
"""
import functools, http.server, json, os, re, socketserver, sys, threading
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(RAIZ, "docs")
OUT = os.path.join(DOCS, "manual", "img") + os.sep
class Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


h = functools.partial(Quieto, directory=DOCS)
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), h)
threading.Thread(target=srv.serve_forever, daemon=True).start()
B = f"http://127.0.0.1:{srv.server_address[1]}/"
marks={}
def caixa(pg, sel, nth=0):
    loc=pg.locator(sel).nth(nth)
    b=loc.bounding_box()
    return b
def shot(pg, nome, alvos, lang="pt", full=False):
    vw=pg.viewport_size
    res=[]
    for i,(sel,nth,ancora) in enumerate(alvos,1):
        b=caixa(pg,sel,nth)
        if not b: print("SEM", nome, sel); continue
        x = b["x"]+(b["width"] if ancora=="d" else 0 if ancora=="e" else b["width"]/2)
        y = b["y"]+b["height"]/2 if b["height"] < 0.3*vw["height"] else b["y"]+28
        res.append({"n":i,"x":round(100*x/vw["width"],1),"y":round(100*y/vw["height"],1),
                    "box":[round(100*b["x"]/vw["width"],1),round(100*b["y"]/vw["height"],1),round(100*b["width"]/vw["width"],1),round(100*b["height"]/vw["height"],1)]})
    pg.screenshot(path=OUT+nome+".jpg", type="jpeg", quality=80)
    marks[nome]=res
with sync_playwright() as p:
    b=p.chromium.launch()
    for lang in ("pt","en"):
        ctx=b.new_context(viewport={"width":1280,"height":800}, locale="pt-BR" if lang=="pt" else "en-US", device_scale_factor=1)
        ctx.add_init_script(f"try{{localStorage.setItem('apt4all-lang','{lang}')}}catch(e){{}}")
        pg=ctx.new_page(); pg.emulate_media(reduced_motion="reduce")
        pg.goto(B); pg.wait_for_timeout(900)
        shot(pg,f"inicio-{lang}",[("a.btn",0,"c"),(".idioma",0,"c"),("#nums",0,"c")])
        pg.goto(B+"atlas/#BR"); pg.wait_for_timeout(1500)
        # garante o idioma
        pg.locator(f'.idioma button[data-l="{lang}"]').click(); pg.wait_for_timeout(300)
        pg.evaluate("escolhe('BR')"); pg.wait_for_timeout(400)
        shot(pg,f"mapa-{lang}",[("#busca",0,"c"),("nav.modos",0,"c"),("#fmot",0,"c"),('#mapa',0,"c"),("#dossie",0,"c"),(".idioma",0,"c")])
        pg.evaluate("abreAtor('apt28')"); pg.wait_for_timeout(400)
        shot(pg,f"ator-{lang}",[(".gaveta h2",0,"c"),(".gaveta .sec.aviso",0,"c"),(".gaveta table.forn",0,"c"),(".gaveta .nuvem",1,"c"),(".gaveta .fecha",0,"c")])
        pg.evaluate("fechaAtor()")
        pg.evaluate("vai('perfil');window.scrollTo(0,0)"); pg.wait_for_timeout(300)
        pg.locator('#pSetor .chip[data-v="finance"]').click(); pg.wait_for_timeout(400)
        pg.evaluate("window.scrollTo(0, document.querySelector('#perfilForm').getBoundingClientRect().top + scrollY - 110)"); pg.wait_for_timeout(200)
        shot(pg,f"perfil-{lang}",[("#pPais .chip[aria-pressed=true]",0,"c"),("#pBusca",0,"c"),("#pSetor .chip[aria-pressed=true]",0,"c"),("#pOrigem",0,"c"),("#perfilRes .resumo",0,"e"),("#perfilRes .barras",0,"c")])
        pg.evaluate("vai('fluxos');window.scrollTo(0,0)"); pg.wait_for_timeout(700)
        pg.evaluate("window.scrollTo(0, document.querySelector('#fluxoFiltros').getBoundingClientRect().top + scrollY - 110)"); pg.wait_for_timeout(200)
        shot(pg,f"fluxos-{lang}",[("#fluxoFiltros .grupo .rot",0,"d"),("#fluxoFiltros .grupo .rot",1,"d"),("#fluxoFiltros .grupo .rot",2,"d"),("#sankey .coltit",0,"e"),("#sankey .coltit",2,"e"),("#sankey .coltit",3,"e")])
        pg.evaluate("vai('rede');window.scrollTo(0,0)"); pg.wait_for_timeout(900)
        pg.evaluate("window.scrollTo(0, document.querySelector('#grafo').getBoundingClientRect().top + scrollY - 150)"); pg.wait_for_timeout(200)
        pg.locator("#grafo .nd.ator").nth(1).hover(); pg.wait_for_timeout(300)
        shot(pg,f"rede-{lang}",[("#grafo .nd.ator",1,"c"),("#grafo .nd.on.tec",0,"c"),("#redeTam",0,"c")])
        pg.mouse.move(5,5)
        pg.evaluate("vai('ranking');window.scrollTo(0,0)"); pg.wait_for_timeout(200)
        shot(pg,f"ranking-{lang}",[("#rankTab th",0,"c"),("#rankTab tbody tr",0,"c")])
        pg.goto(B+"recursos/"); pg.wait_for_timeout(900)
        shot(pg,f"recursos-{lang}",[("#q",0,"c"),("#cats",0,"c"),("#extra",0,"c"),(".card",0,"c")])
        ctx.close()
    m=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True)
    m.add_init_script("try{localStorage.setItem('apt4all-lang','pt')}catch(e){}")
    pg=m.new_page(); pg.goto(B+"atlas/#BR"); pg.wait_for_timeout(1500)
    pg.screenshot(path=OUT+"celular.jpg",type="jpeg",quality=78)
    print("scroll", pg.evaluate("document.documentElement.scrollWidth"))
    b.close()
srv.shutdown()
manual = os.path.join(DOCS, "manual", "index.html")
html = open(manual, encoding="utf-8").read()
html = re.sub(r"const MARCAS=/\*MARCAS\*/.*?;\n", lambda m: "const MARCAS=/*MARCAS*/" + json.dumps(marks, separators=(",", ":")) + ";\n", html, count=1)
open(manual, "w", encoding="utf-8").write(html)
print("telas:", len(marks), "· marcadores:", sum(len(v) for v in marks.values()))
