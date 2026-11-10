#!/usr/bin/env python3
"""Integração no navegador: filtros, idiomas, Atlas, mobile e erro de carga.

Uso: CHROMIUM_PATH=/usr/bin/chromium python testes/campanhas_navegador.py
Dependência opcional: playwright. A suíte unittest continua só biblioteca padrão.
"""
import functools
import http.server
import os
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main():
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT / 'docs')))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = 'http://127.0.0.1:' + str(server.server_port)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or None)
            try:
                for width in (1280, 390):
                    context = browser.new_context(viewport={'width': width, 'height': 900}, locale='pt-BR')
                    page = context.new_page()
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.goto(base + '/campanhas/')
                    expect(page.locator('.case')).to_have_count(6)
                    page.select_option('#scope', 'latam')
                    expect(page.locator('.case')).to_have_count(2)
                    page.select_option('#year', '2021')
                    expect(page.locator('.case')).to_have_count(1)
                    expect(page.locator('.case h2')).to_contain_text('Spalax')
                    page.click('#clear')
                    page.fill('#q', 'T1090.001')
                    expect(page.locator('.case')).to_have_count(1)
                    expect(page.locator('.case h2')).to_contain_text('Volt Typhoon')
                    page.fill('#q', 'nao-existe-neste-catalogo')
                    expect(page.locator('.case')).to_have_count(0)
                    page.click('#clear')
                    page.click('.seg [data-l="en"]')
                    expect(page.locator('h1')).to_have_text('From campaign to evidence.')
                    page.goto(base + '/campanhas/?campanha=spalax-2021')
                    expect(page.locator('.case')).to_have_count(1)
                    expect(page.locator('details')).to_have_attribute('open', '')
                    expect(page.locator('.case')).to_contain_text('No attributed actor in the Atlas')
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
                    page.click('[data-tema]')
                    page.goto(base + '/atlas/#apt41')
                    page.wait_for_selector('.gaveta')
                    campaign_link = page.locator('.gaveta a[href*="campanha=apt41-dust-2024"]')
                    expect(campaign_link).to_have_count(1)
                    campaign_link.click()
                    expect(page.locator('.case')).to_have_count(1)
                    expect(page.locator('.case')).to_contain_text('2024-07-18')
                    expect(page.locator('.case')).to_contain_text('2024-07-19')
                    page.goto(base + '/campanhas/?ator=turla')
                    expect(page.locator('.case')).to_have_count(1)
                    expect(page.locator('.case h2')).to_contain_text('Crutch')
                    page.click('#clear')
                    expect(page.locator('.case')).to_have_count(6)
                    page.click('.seg [data-l="pt"]')
                    page.locator('.case details summary').first.click()
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                    if os.environ.get('CAMPANHAS_SCREENSHOTS'):
                        dest = Path(os.environ['CAMPANHAS_SCREENSHOTS'])
                        dest.mkdir(parents=True, exist_ok=True)
                        page.screenshot(path=str(dest / ('campanhas-' + str(width) + '.png')), full_page=True)
                    assert not errors, errors
                    context.close()
                    print('OK: filtros, idiomas, links Atlas, datas, tema e layout', width)
                page = browser.new_page(locale='pt-BR')
                page.route('**/campanhas.json', lambda route: route.abort())
                page.goto(base + '/campanhas/')
                expect(page.locator('#cases')).to_contain_text('Não foi possível carregar')
                print('OK: erro de carga visível')
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    main()
