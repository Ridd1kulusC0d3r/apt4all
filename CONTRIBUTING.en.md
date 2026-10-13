# How to contribute

Português: [CONTRIBUTING.md](CONTRIBUTING.md)

Thanks for helping. Pick **one** of the paths below.

## 1. Suggest a resource (5 minutes, right on GitHub)

1. Open [`recursos/recursos.json`](recursos/recursos.json) and click the pencil (edit).
2. Copy an item from the right category and change the fields:

```json
{"cat": "rastreadores", "nome": "Resource name", "url": "https://...",
 "desc_pt": "Uma frase dizendo para que serve.", "desc_en": "One sentence on what it is for.",
 "tipo": "gratuito", "status": "ativo", "destaque": false, "origem": "comunidade"}
```

3. Click **Propose changes** and open the PR. CI regenerates `RECURSOS.md`, `RESOURCES.md` and the search page.

Accepted values: `tipo` = `gratuito` (free), `freemium`, `registro` (sign-up), `pago` (paid); `status` = `ativo` (active) or `legado` (discontinued, naming the replacement in the description). Categories: see the keys under `categorias` at the top of the file. If you can't write Portuguese, leave `desc_pt` in English and a maintainer will translate it.

## 2. Fix an actor

The Atlas is generated from the sources; don't hand-edit `docs/atlas/*.json`. If an alias, country or technique is wrong:

- **Source** error: fix it upstream (MISP Galaxy, APT Groups and Operations sheet, ATT&CK). The fix arrives here with the weekly refresh.
- **Merge** error (two groups that became one, or one group split in two): open an issue naming both actors and the source that separates or joins them. The rule lives in `unir()` in [`construir_dados.py`](ferramentas/atlas/construir_dados.py).

## 3. Publish a dossier

Use the template [`trilha/modelos/dossie-ator.md`](trilha/modelos/dossie-ator.md) and save it as `trilha/dossies/<actor-id>.md`. Requirements: public sources, TLP:CLEAR, stated confidence level.

## 4. Code

```bash
python3 -m unittest discover -s testes -v      # all tests, standard library only
python3 ferramentas/atlas/construir_dados.py   # rebuilds the Atlas from local raw data
python3 ferramentas/recursos/gerar_listas.py   # regenerates RECURSOS.md and RESOURCES.md
```

House rules: Python standard library only; texts in PT and EN; no malware samples, attack procedures or credentials in the repository.

## Conduct

Be kind, cite sources and treat attribution as a hypothesis.
