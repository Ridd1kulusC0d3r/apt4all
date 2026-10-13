# Relatório de testes · APT4ALL 1.0

Executado em 13/10/2026, num ambiente Linux na nuvem (Python 3.10, 3.11, 3.12 e 3.13; Chromium via Playwright).

## Resumo

| Bateria | Casos | Resultado |
|---|---|---|
| Testes de unidade (`python3 -m unittest discover -s testes`) | 37 | **OK** em 3.10, 3.11, 3.12 e 3.13 (1 pulado: TCE ausente) |
| Mesma bateria com o TCE instalado | 37 | **OK**, nenhum pulado |
| Integração com o Horizon do TCE (caso `enterprise-identity`) | 3 rodadas | **OK**: candidato não pesa, aceito sobe a faixa |
| Navegador (`python3 testes/navegador.py`) | 12 | **12 OK** |
| Lançador (`iniciar.py`) | 3 requisições | **OK** (200 em `/`, `/atlas/atores.json`, `/recursos/`) |
| Reprodutibilidade do pipeline | 2 execuções | **Saída idêntica** em Python 3.10 e 3.11 |
| Links dos recursos | 169 | 68 OK, **0 mortos**, 101 sem conexão a partir desta nuvem (ver limites) |

## 1. Testes de unidade

| Arquivo | O que cobre | Casos |
|---|---|---|
| `test_unir.py` | Regra de junção: alias une ao âncora, ID do ATT&CK une, alias ambíguo não une, registro que aponta para dois atores não une, sem efeito cascata; utilidades (`norm`, `divide`, `conserta`, setores, `slug`, fornecedores) | 11 |
| `test_dados.py` | Base gerada: volume, IDs únicos, campos, atribuições conhecidas (APT28/29 RU, Lazarus KP, OilRig IR, APT41 CN), nenhum grupo do ATT&CK duplicado ou fundido, nomes por fornecedor, formato das técnicas, contagem por país, rótulos de setor, mapa | 10 |
| `test_recursos.py` | Esquema do `recursos.json`, URLs únicas, categorias bilíngues, cópia publicada igual, gerador das listas PT/EN | 5 |
| `test_ponte_tce.py` | Pontuação do perfil, filtro de origem, exportação dos 4 arquivos, trava de revisão (`candidate`, `auto_accept: false`), CSV, camada do Navigator, base real; integração com o Horizon | 6 |
| `test_paginas.py` | Páginas existem, Atlas aponta para os JSON, dicionários PT/EN com as mesmas chaves, todo `data-t` traduzido, `localStorage` sempre dentro de `try` | 5 |

O teste `test_urls_unicas` pegou 3 recursos duplicados na primeira rodada (APTnotes, vx-underground, Zenodo 12741055). Foram consolidados: o total caiu de 172 para 169.

## 2. Integração com o TCE Horizon

Caso de referência `examples/cases/enterprise-identity` do TCE, com o sinal gerado por `perfil_ameaca.py --pais "United States" --setor government` (153 atores, 60 técnicas no sinal).

| Rodada | Pontuação do 1º caminho | Pressão de inteligência | Faixa |
|---|---|---|---|
| Sem sinal | 64,7 | 0,2455 | H2 |
| Sinal `candidate` | 64,7 | 0,2455 | H2 |
| Sinal `accepted` | 65,4 | 0,2874 | **H1** |

O teste automático `test_trava_de_revisao_no_horizon` repete a verificação na função `_intelligence_pressure`: candidato = 0, aceito > 0, e o ID do sinal aparece na contribuição.

## 3. Navegador

| # | Caso | Resultado |
|---|---|---|
| 1–4 | Início, Atlas, Recursos e Manual em 1280×800: sem erro de JavaScript, sem rolagem lateral | OK |
| 5–8 | As mesmas páginas em 390×844 (celular) | OK |
| 9 | Buscar `Fancy Bear` abre a ficha `#apt28` | OK |
| 10 | Endereço `#perfil` abre a aba Perfil de ameaça | OK |
| 11 | Perfil Brasil + financeiro baixa `apt4all-navigator-Brazil-finance.json` | OK |
| 12 | Clicar na 1ª linha do Ranking abre a China no mapa | OK |

## 4. Números da base (13/10/2026)

2.494 registros lidos (planilha 411, MISP 1.060, ATT&CK 176, EternalLiberty 847) → 1.355 atores; 412 relatórios ligados; ATT&CK 19.2; maiores grupos após a junção: Kimsuky e Magic Hound (12 registros cada), nenhum acima disso. Antes da regra de âncoras, o union-find criava blocos de 41 (Lazarus) e 38 (OilRig).

## 5. Limites desta rodada

- **GitHub Actions e Pages não rodaram**: a sessão não tinha acesso de escrita ao repositório. Os YAML foram validados (sintaxe) e os comandos que eles chamam rodaram localmente.
- **Download das fontes (`--baixar`)**: a planilha do Google é bloqueada nesta nuvem; os dados vieram do export enviado pelo mantenedor. O CI baixa direto e, se o formato vier diferente, mantém a cópia local.
- **Links "sem conexão"**: o proxy desta nuvem só libera alguns domínios. Nenhum link deu 404/410. A verificação mensal no GitHub dá o número real.
- **Lançadores de Windows e macOS**: testados só por inspeção; o mesmo `iniciar.py` foi executado no Linux.
- **Fontes tipográficas**: o Google Fonts foi bloqueado aqui; as telas do manual mostram a fonte alternativa do sistema.

## Como reproduzir

```bash
python3 -m unittest discover -s testes -v
python3 ferramentas/atlas/construir_dados.py          # reconstrói a base com os dados locais
pip install playwright && playwright install chromium   # só para os dois comandos abaixo
python3 testes/navegador.py
python3 ferramentas/manual/capturar_telas.py
```
