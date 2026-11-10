#!/usr/bin/env python3
"""Publica a seleção editorial CyberMonitor; não baixa PDFs, IOCs ou amostras.

Fonte única: dados/campanhas/cybermonitor.json. Requer revisão explícita de cada
registro. Relações com atores são verificadas contra o Atlas, nunca inferidas
por título/alias. Datas de publicação, índice e revisão permanecem separadas.
"""
import csv
import json
import re
from copy import deepcopy
from datetime import date
from pathlib import Path
from urllib.parse import quote, urlsplit, unquote

RAIZ = Path(__file__).resolve().parents[2]
REPO = 'CyberMonitor/APT_CyberCriminal_Campagin_Collections'
BILINGUES = ('foco', 'observacao', 'telemetria', 'hipotese', 'lacunas', 'validar', 'nota')


def ler_json(path):
    with Path(path).open(encoding='utf-8') as f:
        return json.load(f)


def url_chave(url):
    """Normalização restrita; não remove parâmetros que podem identificar o documento."""
    p = urlsplit(url)
    return (p.hostname or '').lower().removeprefix('www.') + unquote(p.path).rstrip('/') + ('?' + p.query if p.query else '')


def url_publica(url):
    p = urlsplit(url)
    if p.scheme != 'https' or not p.hostname or p.username or p.password:
        raise ValueError('Referência deve ser uma URL HTTPS sem credenciais: ' + str(url))


def validar(dados, atores, tecnicas):
    if dados.get('schema_version') != '1.0':
        raise ValueError('Versão de esquema desconhecida')
    fonte = dados['fonte']
    if fonte['repositorio'] != REPO or not re.fullmatch(r'[0-9a-f]{40}', fonte['commit']):
        raise ValueError('Origem ou commit inválido')
    por_id = {a['id']: a for a in atores}
    ids, urls, caminhos = set(), set(), set()
    for c in dados['campanhas']:
        ident = c['id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ident) or ident in ids:
            raise ValueError('ID de campanha inválido ou duplicado: ' + ident)
        ids.add(ident)
        url_publica(c['fonte_primaria'])
        chave = url_chave(c['fonte_primaria'])
        if chave in urls:
            raise ValueError('Fonte primária duplicada: ' + ident)
        urls.add(chave)
        for campo in BILINGUES:
            if any(not isinstance(c[campo].get(l), str) or not c[campo][l].strip() for l in ('pt', 'en')):
                raise ValueError('Tradução ausente: ' + campo)
        for campo in ('publicado_em', 'data_diretorio', 'revisado_em'):
            parsed = date.fromisoformat(c[campo])
            if parsed.year < 1900:
                raise ValueError('Data sentinela não é publicação: ' + ident)
        if c['publicado_em'] > c['revisado_em']:
            raise ValueError('Revisão anterior à publicação: ' + ident)
        if c['status_fonte'] != 'fonte_primaria_consultada' or c['status_deteccao'] != 'hipotese_nao_testada':
            raise ValueError('Este catálogo publica apenas fontes revisadas e hipóteses não testadas')
        if c['mapeamento_tecnicas'] != 'curadoria_apt4all':
            raise ValueError('Autoria do mapeamento deve ser explícita')
        if not c['tecnicas'] or not set(c['tecnicas']) <= set(tecnicas):
            raise ValueError('Técnica ausente na versão local do Atlas: ' + ident)
        if c['ator_id'] is None:
            if c['mitre_id'] is not None or c['fonte_vinculo_ator'] is not None or c['tipo_vinculo_ator'] != 'nao_atribuido':
                raise ValueError('Campanha sem atribuição não pode carregar ID de ator')
        else:
            a = por_id.get(c['ator_id'])
            if not a or (a.get('mitre') or {}).get('id') != c['mitre_id']:
                raise ValueError('Vínculo com o Atlas precisa de revisão: ' + ident)
            if c['tipo_vinculo_ator'] not in ('atribuido_na_fonte', 'nome_associado_attck'):
                raise ValueError('Tipo de vínculo não reconhecido')
            if c['fonte_vinculo_ator'] != 'https://attack.mitre.org/groups/' + c['mitre_id'] + '/':
                raise ValueError('Referência do vínculo deve apontar ao grupo selecionado')
        pasta = c['caminho_cybermonitor']
        if '..' in pasta.split('/') or not re.fullmatch(r'\d{4}/[^/]+', pasta):
            raise ValueError('Diretório inválido: ' + ident)
        esperado = 'https://github.com/' + REPO + '/tree/' + fonte['commit'] + '/' + quote(pasta, safe='/')
        if c['arquivo_cybermonitor'] != esperado or pasta in caminhos:
            raise ValueError('Arquivo deve ser único e fixado no commit da fonte')
        caminhos.add(pasta)
        if not c['referencias_arquivadas']:
            raise ValueError('Falta referência ao documento arquivado')
        for r in c['referencias_arquivadas']:
            if '..' in r['caminho'].split('/') or not r['caminho'].startswith(pasta + '/') or not r['caminho'].endswith('.pdf'):
                raise ValueError('Somente referências a relatórios PDF desta campanha')
            for campo in ('sha1_declarado', 'git_blob_sha'):
                if not re.fullmatch(r'[0-9a-f]{40}', r[campo]):
                    raise ValueError('Hash de referência inválido')
            if date.fromisoformat(r['publicado_em_indice']).year < 1900:
                raise ValueError('Data desconhecida no índice exige revisão')


def gerar(dados, atores, tecnicas, aptnotes):
    validar(dados, atores, tecnicas)
    saida = deepcopy(dados)
    por_id = {a['id']: a for a in atores}
    for c in saida['campanhas']:
        a = por_id.get(c['ator_id'])
        c['ator_nome'] = a['nome'] if a else None
        hashes = {r['sha1_declarado'] for r in c['referencias_arquivadas']}
        c['aptnotes_correspondencias'] = []
        for r in aptnotes:
            por_hash = bool(r.get('SHA-1')) and r['SHA-1'].lower() in hashes
            por_url = url_chave(r.get('Link', '')) == url_chave(c['fonte_primaria'])
            if por_hash or por_url:
                c['aptnotes_correspondencias'].append({'titulo': r['Title'], 'url': r['Link'],
                    'criterio': 'sha1_declarado' if por_hash else 'url'})
    saida['meta'] = {'n_campanhas': len(saida['campanhas']),
        'n_com_ator': sum(bool(c['ator_id']) for c in saida['campanhas']),
        'n_latam': sum(c['recorte'] == 'latam' for c in saida['campanhas']),
        'revisado_em': max(c['revisado_em'] for c in saida['campanhas']),
        'n_com_correspondencia_aptnotes': sum(bool(c['aptnotes_correspondencias']) for c in saida['campanhas'])}
    return saida


def main():
    dados = ler_json(RAIZ / 'dados/campanhas/cybermonitor.json')
    atores = ler_json(RAIZ / 'docs/atlas/atores.json')['atores']
    tecnicas = ler_json(RAIZ / 'docs/atlas/paises.json')['tecnicas']
    with (RAIZ / 'dados/brutos/APTnotes.csv').open(encoding='utf-8', newline='') as f:
        aptnotes = list(csv.DictReader(f))
    saida = gerar(dados, atores, tecnicas, aptnotes)
    destino = RAIZ / 'docs/campanhas/campanhas.json'
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(saida['meta'], ensure_ascii=False))


if __name__ == '__main__':
    main()
