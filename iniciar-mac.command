#!/usr/bin/env sh
# APT4ALL: dois cliques para abrir / double-click to open
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then PY=python3; elif command -v python >/dev/null 2>&1; then PY=python; else
  echo "Instale o Python 3.9+ (sudo apt install python3). / Install Python 3.9+."; read -r _; exit 1; fi
exec "$PY" iniciar.py
