# Fontes e licenças

English: [SOURCES.md](SOURCES.md)

Tudo o que o Atlas mostra vem de fontes abertas. Esta página diz de onde veio cada dado, sob qual licença e como o APT4ALL usa.

## Dados do Atlas

| Fonte | O que usamos | Licença | Como baixamos |
|---|---|---|---|
| [APT Groups and Operations](https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU) (Florian Roth e colaboradores) | Nomes por fornecedor, operações, ferramentas, alvos, país das abas | CC BY 4.0 | CSV por aba; cópia em `dados/brutos/planilha-apt/` |
| [MISP Galaxy: threat-actor](https://github.com/MISP/misp-galaxy/blob/main/clusters/threat-actor.json) | Aliases, país atribuído, vítimas, setores, motivação, referências | CC0 1.0 ou BSD-2-Clause (à escolha) | `raw.githubusercontent.com` |
| [MITRE ATT&CK Enterprise (STIX)](https://github.com/mitre-attack/attack-stix-data) | Grupos, técnicas e softwares ligados por relação | [Termos de Uso do ATT&CK](https://attack.mitre.org/resources/terms-of-use/) (uso livre com atribuição) | `raw.githubusercontent.com` (52 MB, não versionado) |
| [EternalLiberty](https://github.com/StrangerealIntel/EternalLiberty) | Tabela de equivalência de nomes | Sem licença declarada; usamos só nomes e relações, com crédito | `raw.githubusercontent.com` |
| [APTnotes](https://github.com/aptnotes/data) | Título, data e link de relatórios públicos ligados a cada ator | Sem licença declarada; usamos só metadados e links | `raw.githubusercontent.com` |
| [Natural Earth 1:110m](https://www.naturalearthdata.com/) | Centroides e nomes de países para o mapa hexagonal | Domínio público | cópia versionada em `dados/brutos/` (origem: `nvkelso/natural-earth-vector`) |

"® MITRE ATT&CK e ATT&CK são marcas registradas da The MITRE Corporation." O APT4ALL não tem relação com a MITRE.

## Como o APT4ALL junta as fontes

1. Cada registro de cada fonte vira uma lista de nomes (nome principal + aliases), normalizados.
2. Âncoras primeiro: grupos do ATT&CK, depois planilha, MISP e EternalLiberty, nessa ordem.
3. Um registro novo só entra num ator existente se compartilhar um nome com ele. Nome usado por dois atores diferentes vira **ambíguo** e não une nada. Isso evita a "bola de neve" em que Lazarus, Andariel e BlueNoroff viram um ator só.
4. País: ATT&CK e planilha valem mais que o MISP. Sem país claro, o ator fica em **??**.

O resultado de cada rodada fica em [`dados/gerados/resumo.md`](dados/gerados/resumo.md).

## Recursos curados

Os 169 links de [RECURSOS.md](RECURSOS.md) apontam para sites de terceiros. As descrições são nossas (CC BY 4.0); cada site mantém sua própria licença. Os itens marcados como **lista original** vieram da curadoria inicial do mantenedor.

## Aviso sobre atribuição

Atribuição de ataques é uma afirmação de fornecedores e governos, com graus de confiança diferentes, e muda com o tempo. O APT4ALL **reúne** o que as fontes dizem; não confirma nem contesta. Antes de citar "o ator X é do país Y", vá à fonte original indicada na ficha.
