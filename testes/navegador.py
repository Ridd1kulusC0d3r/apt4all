#!/usr/bin/env python3
"""Teste de fumaça no navegador (opcional; precisa do Playwright).
Browser smoke test (optional; needs Playwright).

Uso: python3 testes/navegador.py
"""
import functools, http.server, os, socketserver, sys, threading
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Quieto, directory=os.path.join(RAIZ, "docs")))
threading.Thread(target=srv.serve_forever, daemon=True).start()
B = f"http://127.0.0.1:{srv.server_address[1]}/"
resultados = []


def caso(nome, ok, detalhe=""):
    resultados.append((nome, ok, detalhe))
    print(("OK   " if ok else "FALHA"), nome, detalhe)


with sync_playwright() as p:
    nav = p.chromium.launch()
    for vw, vh in [(1280, 800), (390, 844)]:
        for pagina in ["", "atlas/", "recursos/", "manual/"]:
            ctx = nav.new_context(viewport={"width": vw, "height": vh})
            pg = ctx.new_page()
            erros = []
            pg.on("pageerror", lambda e: erros.append(str(e)))
            pg.goto(B + pagina)
            pg.wait_for_timeout(1200)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            caso(f"{pagina or 'inicio'} {vw}x{vh}", not erros and sw <= vw, f"erros={len(erros)} scrollWidth={sw}")
            ctx.close()
    ctx = nav.new_context(viewport={"width": 1280, "height": 800}, accept_downloads=True)
    pg = ctx.new_page()
    pg.goto(B + "atlas/")
    pg.wait_for_timeout(1500)
    pg.fill("#busca", "Fancy Bear")
    pg.wait_for_timeout(300)
    pg.locator("#sug button, #sug [role=option], #sug a, #sug div").first.click()
    pg.wait_for_timeout(300)
    caso("busca por alias abre a ficha certa", pg.evaluate("location.hash") == "#apt28" and pg.locator(".gaveta h2").inner_text() == "APT28")
    pg.keyboard.press("Escape")
    pg.goto(B + "atlas/#perfil")
    pg.reload()
    pg.wait_for_timeout(1500)
    caso("#perfil abre a aba de perfil", pg.locator("#v-perfil").is_visible())
    pg.select_option("#pPais", "Brazil")
    pg.select_option("#pSetor", "finance")
    pg.wait_for_timeout(300)
    with pg.expect_download() as d:
        pg.locator("#perfilRes .btn").first.click()
    caso("perfil baixa a camada do Navigator", d.value.suggested_filename.startswith("apt4all-navigator-Brazil-finance"), d.value.suggested_filename)
    pg.evaluate("vai('ranking')")
    pg.locator("#rankTab tbody tr").first.click()
    pg.wait_for_timeout(300)
    caso("linha do ranking abre o país no mapa", pg.locator("#v-mapa").is_visible() and "CHINA" in pg.locator("#dossie").inner_text().upper())
    nav.close()
srv.shutdown()
falhas = [r for r in resultados if not r[1]]
print(f"\n{len(resultados)} casos · {len(resultados) - len(falhas)} ok · {len(falhas)} falhas")
sys.exit(1 if falhas else 0)
