# Ponte APT4ALL → TCE Horizon

English: [README.en.md](README.en.md)

O [TCE](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling) modela o ambiente inteiro da empresa e prevê onde a defesa precisa de atenção. O APT4ALL entrega a parte que faltava: **quem costuma atacar organizações como a sua, e com quais técnicas**.

- Análise completa (lacunas, testes, materiais acadêmicos, proposta de pesquisa): [ANALISE-TCE.md](ANALISE-TCE.md)
- Ferramenta: [`ferramentas/tce/perfil_ameaca.py`](../ferramentas/tce/perfil_ameaca.py) (só biblioteca padrão)
- No navegador: [Atlas → Perfil de ameaça](https://ridd1kulusc0d3r.github.io/apt4all/atlas/#perfil)

## Faça agora (uma coisa só)

```bash
python3 ferramentas/tce/perfil_ameaca.py --pais Brazil --setor finance --saida saida/br-financas
```

Abra `saida/br-financas/perfil.md`. Pronto: você tem a lista de atores e as técnicas a cobrir primeiro.

## O que sai

| Arquivo | Para quê |
|---|---|
| `perfil.md` | Relatório legível: atores, por que entraram, técnicas |
| `navigator.json` | Camada para o [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) |
| `tce-sinais.json` | Candidato a `intelligence_signals` (sempre `candidate`, `review_required: true`) |
| `tce-intelligence.csv` | Mesmo sinal no formato do `tce environment-import-csv` |

## Levando para o TCE

1. Leia `perfil.md` e confirme os atores nas fontes.
2. Em `tce-sinais.json`, troque `status` para `accepted` só depois dessa revisão.
3. Inclua o sinal em `environment_state.intelligence_signals` do seu caso.
4. Rode `tce horizon-assess <caso> --offline` e compare com a rodada anterior.

Sinal `candidate` não muda nada no cálculo. Essa trava é proposital e foi testada (ver seção 3 da análise).

## Valores aceitos

```bash
python3 ferramentas/tce/perfil_ameaca.py --listar paises
python3 ferramentas/tce/perfil_ameaca.py --listar setores
```

Setores: `government`, `military`, `finance`, `energy`, `health`, `education`, `telecom`, `technology`, `civil`, `private`, `manufacturing`, `transport`, `retail`, `infrastructure`.

## Limite que você precisa saber

A vitimologia pública cobre mal o Brasil. O perfil é ponto de partida, não previsão: complemente com CERT.br, relatórios de bancos e fornecedores com operação no país.
