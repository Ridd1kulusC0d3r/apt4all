#!/usr/bin/env python3
"""Abre o APT4ALL no navegador, sem internet e sem instalar nada.
Opens APT4ALL in the browser, offline, with nothing to install.

Uso / usage: python3 iniciar.py [--porta 8765] [--sem-navegador]
"""
import argparse, functools, http.server, os, socket, socketserver, sys, threading, webbrowser

RAIZ = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(RAIZ, "docs")


def porta_livre(inicial):
    for p in range(inicial, inicial + 30):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                continue
    raise SystemExit("Nenhuma porta livre entre %d e %d. / No free port." % (inicial, inicial + 29))


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--porta", type=int, default=8765)
    ap.add_argument("--sem-navegador", action="store_true")
    a = ap.parse_args()
    if sys.version_info < (3, 9):
        raise SystemExit("Precisa de Python 3.9 ou mais novo. / Needs Python 3.9+.")
    if not os.path.exists(os.path.join(DOCS, "atlas", "atores.json")):
        raise SystemExit("Não achei docs/atlas/atores.json. Baixe o repositório completo. / Download the full repository.")
    porta = porta_livre(a.porta)
    url = f"http://localhost:{porta}/"
    h = functools.partial(Silencioso, directory=DOCS)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", porta), h) as srv:
        print("◆ APT4ALL")
        print(f"  Aberto em / Running at: {url}")
        print("  Atlas:    " + url + "atlas/")
        print("  Manual:   " + url + "manual/")
        print("  Para fechar: feche esta janela ou aperte Ctrl+C. / To stop: close this window or press Ctrl+C.")
        if not a.sem_navegador:
            threading.Timer(0.8, lambda: webbrowser.open(url)).start()
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\nAté a próxima. / Bye.")


if __name__ == "__main__":
    main()
