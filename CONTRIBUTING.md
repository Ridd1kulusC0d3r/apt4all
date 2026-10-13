# Como contribuir

English: [CONTRIBUTING.en.md](CONTRIBUTING.en.md)

Obrigado por ajudar. Escolha **um** dos caminhos abaixo.

## 1. Sugerir um recurso (5 minutos, direto no GitHub)

1. Abra [`recursos/recursos.json`](recursos/recursos.json) e clique no lápis (editar).
2. Copie um item da categoria certa e troque os campos:

```json
{"cat": "rastreadores", "nome": "Nome do recurso", "url": "https://...",
 "desc_pt": "Uma frase dizendo para que serve.", "desc_en": "One sentence on what it is for.",
 "tipo": "gratuito", "status": "ativo", "destaque": false, "origem": "comunidade"}
```

3. Clique em **Propose changes** e abra o PR. O CI gera `RECURSOS.md`, `RESOURCES.md` e a página de busca.

Valores aceitos: `tipo` = `gratuito`, `freemium`, `registro`, `pago`; `status` = `ativo` ou `legado` (descontinuado, com o substituto citado na descrição). Categorias: veja as chaves em `categorias` no topo do arquivo.

## 2. Corrigir um ator

O Atlas é gerado das fontes; não edite `docs/atlas/*.json` à mão. Se um alias, país ou técnica está errado:

- Erro de **fonte**: corrija na origem (MISP Galaxy, planilha APT Groups and Operations, ATT&CK). A correção chega aqui na atualização semanal.
- Erro de **junção** (dois grupos que viraram um, ou um grupo partido em dois): abra uma issue com o nome dos dois atores e a fonte que separa ou une. A regra está em `unir()`, em [`construir_dados.py`](ferramentas/atlas/construir_dados.py).

## 3. Publicar um dossiê

Use o modelo [`trilha/modelos/dossie-ator.md`](trilha/modelos/dossie-ator.md) e salve em `trilha/dossies/<id-do-ator>.md`. Exigências: fontes públicas, TLP:CLEAR, nível de confiança declarado.

## 4. Código

```bash
python3 -m unittest discover -s testes -v      # todos os testes, só biblioteca padrão
python3 ferramentas/atlas/construir_dados.py   # reconstrói o Atlas com os dados brutos locais
python3 ferramentas/recursos/gerar_listas.py   # regera RECURSOS.md e RESOURCES.md
```

Regras da casa: Python só com biblioteca padrão; textos em PT e EN; nada de amostra de malware, procedimento de ataque ou credencial no repositório.

## Conduta

Seja gentil, cite fontes e trate atribuição como hipótese.
