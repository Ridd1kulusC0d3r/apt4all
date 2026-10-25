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
    nav = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
    for vw, vh in [(1280, 800), (390, 844)]:
        for pagina in ["", "atlas/", "atlas/#fluxos", "atlas/#rede", "feed/", "recursos/", "manual/", "ler/index.html", "ler/trilha.html"]:
            ctx = nav.new_context(viewport={"width": vw, "height": vh})
            pg = ctx.new_page()
            erros = []
            pg.on("pageerror", lambda e: erros.append(str(e)))
            pg.goto(B + pagina)
            pg.wait_for_timeout(1200)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            caso(f"{pagina or 'inicio'} {vw}x{vh}", not erros and sw <= vw, f"erros={len(erros)} scrollWidth={sw}")
            ctx.close()
    # feed: lista renderiza, filtro por atribuição e busca funcionam, o ator liga ao Atlas
    ctxf = nav.new_context(viewport={"width": 1280, "height": 800})
    pf = ctxf.new_page()
    pf.goto(B + "feed/")
    pf.wait_for_selector(".feed-item")
    total = pf.locator(".feed-item").count()
    caso("feed lista itens", total > 0, f"itens={total}")
    pf.locator('#chips .chip[data-k="atrib"]').click()
    n_atr = pf.locator(".feed-item").count()
    caso("feed: filtro de atribuição mostra só atribuídos", 0 < n_atr == pf.locator(".feed-item .attr").count(), f"atribuídos={n_atr}")
    pf.fill("#q", "BeyondTrust")
    caso("feed: busca por produto", pf.locator(".feed-item").count() >= 1)
    href = pf.locator(".feed-item .attr a[href*='atlas']").first.get_attribute("href")
    caso("feed: ator atribuído liga ao Atlas", href is not None and "#" in href, str(href))
    ctxf.close()
    # vínculos entre atores: vista na Rede, painel de fatores e seção no dossiê
    ctxv = nav.new_context(viewport={"width": 1280, "height": 800})
    pv = ctxv.new_page()
    erros_v = []
    pv.on("pageerror", lambda e: erros_v.append(str(e)))
    pv.goto(B + "atlas/#rede")
    pv.wait_for_timeout(1500)
    pv.locator("#redeVista .chip").nth(1).click()
    pv.wait_for_timeout(600)
    n_vl = pv.locator(".vl").count()
    caso("rede: vista de vínculos desenha fios", n_vl > 0, f"fios={n_vl}")
    pv.locator(".vl").last.evaluate("e => e.dispatchEvent(new MouseEvent('click', {bubbles: true}))")
    pv.wait_for_timeout(300)
    caso("rede: clicar num fio mostra os fatores", pv.locator("#vincPainel .fator").count() == 7 and pv.locator("#vincPainel").is_visible())
    pv.goto(B + "atlas/#apt28")
    pv.reload()
    pv.wait_for_timeout(1500)
    caso("dossiê: seção de vínculos com fatores", pv.locator(".gaveta details.vinc").count() > 0)
    caso("vínculos sem erro de página", not erros_v, str(erros_v[:1]))
    ctxv.close()
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
    caso("perfil começa com Brasil marcado como filtro", pg.locator('#pPais .chip[data-v="BR"]').get_attribute("aria-pressed") == "true")
    pg.locator('#pSetor .chip[data-v="finance"]').click()
    pg.wait_for_timeout(300)
    resumo = pg.locator("#perfilRes .resumo").inner_text()
    chip_br = pg.locator('#pPais .chip[data-v="BR"] b').inner_text().strip()
    caso("resumo do perfil explica os números", resumo.startswith("55") and f"{chip_br} with victims" in resumo, resumo.splitlines()[0])
    with pg.expect_download() as d:
        pg.locator("#perfilRes .btn").first.click()
    caso("perfil baixa a camada do Navigator", d.value.suggested_filename.startswith("apt4all-navigator-BR-finance"), d.value.suggested_filename)
    pg.locator('#pSetor .chip[data-v="finance"]').click()
    pg.wait_for_timeout(200)
    caso("clicar de novo no filtro desmarca", pg.locator('#pSetor .chip[data-v=""]').get_attribute("aria-pressed") == "true")
    pg.evaluate("vai('ranking')")
    linha = pg.locator("#rankTab tbody tr").nth(1)
    nome = linha.locator("td").first.inner_text().split(" (")[0]
    linha.click()
    pg.wait_for_timeout(300)
    caso("linha do ranking abre o país no mapa", pg.locator("#v-mapa").is_visible() and pg.locator("#dossie h2").inner_text().upper() == nome.upper(), nome)
    pg.evaluate("escolhe('??')")
    pg.wait_for_timeout(300)
    sobrepostos = pg.evaluate("""() => { const r=[...document.querySelectorAll('#mapa .rotulo')].map(e=>e.getBoundingClientRect());
      let n=0; for(let i=0;i<r.length;i++)for(let j=i+1;j<r.length;j++){const a=r[i],b=r[j];if(a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom)n++} return [r.length,n] }""")
    caso("rótulos do mapa legíveis e sem sobreposição", sobrepostos[0] >= 10 and sobrepostos[1] == 0, f"rótulos={sobrepostos[0]} sobreposições={sobrepostos[1]}")
    nums = pg.evaluate("""() => { const b=[...document.querySelectorAll('#dossie .nums b')].map(x=>+x.textContent.replace(/\D/g,'')); return [b[0], document.querySelectorAll('#listaAt .ator').length] }""")
    caso("números do dossiê batem com a lista", nums[0] == nums[1], f"{nums}")
    pg.locator('#fmot .chip').nth(1).click()
    pg.wait_for_timeout(200)
    nums2 = pg.evaluate("""() => { const b=[...document.querySelectorAll('#dossie .nums b')].map(x=>+x.textContent.replace(/\D/g,'')); return [b[0], document.querySelectorAll('#listaAt .ator').length] }""")
    caso("com filtro de motivação, os números continuam batendo", nums2[0] == nums2[1] and nums2[0] < nums[0], f"{nums2}")
    pg.evaluate("vai('fluxos')")
    pg.wait_for_timeout(600)
    n = pg.locator("#sankey .lk").count()
    caso("fluxos APT desenham o Sankey", n > 30, f"fitas={n}")
    pg.locator("#fluxoFiltros .chip", has_text="Ransomware").first.click()
    pg.wait_for_timeout(500)
    n = pg.locator("#sankey .lk").count()
    caso("fluxos de ransomware desenham o Sankey", n > 20, f"fitas={n}")
    pg.evaluate("vai('rede')")
    pg.wait_for_timeout(900)
    nos = pg.locator("#grafo .nd").count()
    caso("rede de ransomware desenha nós e ligações", nos > 15 and pg.locator("#grafo .ar").count() > nos, f"nós={nos}")
    pg.locator("#redeFiltros .chip", has_text="APT").first.click()
    pg.wait_for_timeout(900)
    pg.locator("#grafo .nd.ator").first.hover()
    caso("passar o mouse na rede destaca vizinhos", pg.locator("#grafo svg.foco").count() == 1 and pg.locator("#grafo .nd.on").count() > 3)
    pg.goto(B + "atlas/#akira")
    pg.reload()
    pg.wait_for_timeout(1500)
    caso("ficha liga ao Ransomware Tool Matrix", "RANSOMWARE" in pg.locator(".gaveta").inner_text().upper())
    nav.close()
srv.shutdown()
falhas = [r for r in resultados if not r[1]]
print(f"\n{len(resultados)} casos · {len(resultados) - len(falhas)} ok · {len(falhas)} falhas")
sys.exit(1 if falhas else 0)
