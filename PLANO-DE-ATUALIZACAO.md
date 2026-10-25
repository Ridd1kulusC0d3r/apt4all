# Plano de atualização automática

Tudo roda no GitHub Actions, só com biblioteca padrão do Python. Humano entra em **um** ponto: mesclar o PR semanal.

## Calendário

| Quando | O quê | Workflow | Resultado |
|---|---|---|---|
| Toda segunda, 06:00 UTC | Baixa MISP Galaxy, MITRE ATT&CK, planilha APT Groups and Operations, EternalLiberty, APTnotes e Ransomware Tool Matrix; reconstrói Atlas, mapa, matriz de ransomware, listas e páginas | `atualizar-dados` | PR `dados/atualizacao-semanal` |
| Toda segunda, 06:00 UTC (mesmo PR) | **Feed vivo**: baixa o CISA KEV, mantém janela de 120 dias, cruza com `dados/feed/atribuicoes.json` e publica `docs/feed/feed.json` e `atom.xml`; o corpo do PR lista os itens novos em `dados/feed/novidades.md` | `atualizar-dados` | Itens novos no feed e nos dossiês dos atores |
| Em todo PR semanal | **Portão de qualidade** compara os números com a base atual | `atualizar-dados` | Rótulo `dados` (aprovado) ou `dados, revisar` + issue (reprovado) |
| Ao mesclar na `main` | Republica o site | `pages` | Site atualizado |
| Todo dia 1º, 07:00 UTC | Verifica os links de `recursos/recursos.json` | `verificar-links` | Issue `links` se algum morreu |
| A cada push/PR | Testes em Python 3.9 e 3.12 e integração com o TCE | `testes` | Check verde/vermelho |
| Todo mês | Atualiza versões das Actions usadas | Dependabot | PR `dependencias` |

## Portão de qualidade (`ferramentas/atualizacao/portao.py`)

Reprova (exige revisão) se, em relação ao commit atual:
- `n_atores`, `n_registros`, `n_relatorios`, `n_grupos`, `n_ferramentas` ou `n_usos` caírem mais de **10%**;
- uma fonte (`misp`, `planilha`, `mitre`, `eternalliberty`) zerar;
- um indicador sumir ou o arquivo ficar ilegível.

Avisa (não reprova) se algum número subir mais de 50%: costuma ser fonte que mudou de formato.
Os limites ficam no topo do script e têm testes em `testes/test_portao.py`.

## Feed vivo: como a atribuição entra

O CISA KEV diz **o que** está sendo explorado; quem explora vem só da curadoria humana em `dados/feed/atribuicoes.json`. Cada linha exige ator(es), tipo, quem atribuiu, confiança (`alta`, `media`, `baixa`) e fontes `https://`. O script reprova o arquivo se faltar algo. Nada é inferido automaticamente.

Para incluir uma atribuição nova: edite o arquivo (ou abra uma issue com a fonte), rode `python3 ferramentas/feed/ingerir_kev.py --baixar` e confira em `docs/feed/`.

## O que você faz

1. Segunda ou terça: abra o PR "Dados: atualização semanal das fontes".
2. Sem rótulo `revisar`: confira o resumo e **mescle**. O site republica sozinho.
3. Com `revisar`: leia o relatório do portão no resumo da execução; se a queda for legítima (fonte limpou duplicados), mescle; se for quebra, abra issue na fonte ou ajuste `construir_dados.py`.

## Por que o merge não é automático

Dado de ameaça entra no Atlas como fato citável. Mesclar sem olhar esconde erros de atribuição e quebra de fonte. Se um dia quiser automatizar, o caminho é: ativar *Allow auto-merge* e proteção de branch exigindo o check `testes`, e então habilitar `gh pr merge --auto` no workflow. É uma decisão sua, não vem ligada.

## Ajustes únicos no GitHub

- **Settings → Actions → General → Workflow permissions**: marcar *Read and write permissions* e *Allow GitHub Actions to create and approve pull requests* (necessário para o PR semanal).
- **Settings → Pages → Source: GitHub Actions**.
- **Settings → Code security → Private vulnerability reporting: Enable**.
- Criar os rótulos `dados`, `revisar`, `links` e `dependencias` (o workflow tenta criar `dados`).

## Próximas evoluções sugeridas

1. Selo "dados atualizados em AAAA-MM-DD" no README, lido de `docs/atlas/atores.json`.
2. Feed de novidades: diff semanal (atores novos, aliases novos) no corpo do PR.
3. Nova fonte por vez, cada uma com portão próprio.
