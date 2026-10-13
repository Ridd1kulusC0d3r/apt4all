@echo off
chcp 65001 >nul
title APT4ALL
cd /d "%~dp0"
where py >nul 2>nul && (py -3 iniciar.py & goto fim)
where python >nul 2>nul && (python iniciar.py & goto fim)
echo Python nao encontrado. Instale em https://www.python.org/downloads/ marcando "Add python.exe to PATH".
echo Python not found. Install it from https://www.python.org/downloads/ ticking "Add python.exe to PATH".
:fim
pause
