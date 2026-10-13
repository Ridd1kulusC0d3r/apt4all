# APT4ALL → TCE Horizon bridge

Português: [README.md](README.md)

[TCE](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling) models the whole enterprise environment and forecasts where defense needs attention. APT4ALL supplies the missing piece: **who usually attacks organizations like yours, and with which techniques**.

- Full analysis (gaps, tests, academic materials, research proposal): [TCE-ANALYSIS.md](TCE-ANALYSIS.md)
- Tool: [`ferramentas/tce/perfil_ameaca.py`](../ferramentas/tce/perfil_ameaca.py) (standard library only)
- In the browser: [Atlas → Threat profile](https://ridd1kulusc0d3r.github.io/apt4all/atlas/#perfil)

## Do this now (just one thing)

```bash
python3 ferramentas/tce/perfil_ameaca.py --pais Brazil --setor finance --saida out/br-finance
```

Open `out/br-finance/perfil.md`. You now have the actor list and the techniques to cover first.

## Outputs

| File | Purpose |
|---|---|
| `perfil.md` | Readable report: actors, why each was included, techniques |
| `navigator.json` | Layer for the [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) |
| `tce-sinais.json` | `intelligence_signals` candidate (always `candidate`, `review_required: true`) |
| `tce-intelligence.csv` | Same signal in `tce environment-import-csv` format |

## Taking it into TCE

1. Read `perfil.md` and confirm the actors in the sources.
2. In `tce-sinais.json`, change `status` to `accepted` only after that review.
3. Add the signal to your case's `environment_state.intelligence_signals`.
4. Run `tce horizon-assess <case> --offline` and compare with the previous run.

A `candidate` signal changes nothing in the calculation. That gate is intentional and was tested (see section 3 of the analysis).

## Accepted values

```bash
python3 ferramentas/tce/perfil_ameaca.py --listar paises
python3 ferramentas/tce/perfil_ameaca.py --listar setores
```

Sectors: `government`, `military`, `finance`, `energy`, `health`, `education`, `telecom`, `technology`, `civil`, `private`, `manufacturing`, `transport`, `retail`, `infrastructure`.

## A limit you need to know

Public victimology covers Brazil poorly. The profile is a starting point, not a forecast: complement it with CERT.br and reports from banks and vendors operating in the country.
