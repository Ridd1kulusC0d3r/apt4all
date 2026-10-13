# Sources and licenses

Português: [FONTES.md](FONTES.md)

Everything the Atlas shows comes from open sources. This page states where each piece of data came from, under which license, and how APT4ALL uses it.

## Atlas data

| Source | What we use | License | How we fetch it |
|---|---|---|---|
| [APT Groups and Operations](https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU) (Florian Roth and contributors) | Vendor names, operations, tools, targets, country from the tabs | CC BY 4.0 | CSV per tab; copy in `dados/brutos/planilha-apt/` |
| [MISP Galaxy: threat-actor](https://github.com/MISP/misp-galaxy/blob/main/clusters/threat-actor.json) | Aliases, attributed country, victims, sectors, motivation, references | CC0 1.0 or BSD-2-Clause (your choice) | `raw.githubusercontent.com` |
| [MITRE ATT&CK Enterprise (STIX)](https://github.com/mitre-attack/attack-stix-data) | Groups, techniques and software linked by relationships | [ATT&CK Terms of Use](https://attack.mitre.org/resources/terms-of-use/) (free use with attribution) | `raw.githubusercontent.com` (52 MB, not versioned) |
| [EternalLiberty](https://github.com/StrangerealIntel/EternalLiberty) | Name equivalence table | No declared license; we use only names and relations, with credit | `raw.githubusercontent.com` |
| [APTnotes](https://github.com/aptnotes/data) | Title, date and link of public reports linked to each actor | No declared license; we use only metadata and links | `raw.githubusercontent.com` |
| [Natural Earth 1:110m](https://www.naturalearthdata.com/) | Country centroids and names for the hex map | Public domain | versioned copy in `dados/brutos/` (from `nvkelso/natural-earth-vector`) |

"® MITRE ATT&CK and ATT&CK are registered trademarks of The MITRE Corporation." APT4ALL is not affiliated with MITRE.

## How APT4ALL merges the sources

1. Each record from each source becomes a list of normalized names (primary name + aliases).
2. Anchors first: ATT&CK groups, then the sheet, MISP and EternalLiberty, in that order.
3. A new record joins an existing actor only if it shares a name with it. A name used by two different actors becomes **ambiguous** and merges nothing. This prevents the snowball where Lazarus, Andariel and BlueNoroff collapse into one actor.
4. Country: ATT&CK and the sheet outrank MISP. With no clear country, the actor goes to **??**.

Each run's result is in [`dados/gerados/resumo.md`](dados/gerados/resumo.md).

## Curated resources

The 169 links in [RESOURCES.md](RESOURCES.md) point to third-party sites. The descriptions are ours (CC BY 4.0); each site keeps its own license. Items tagged **original list** came from the maintainer's initial curation.

## A note on attribution

Attack attribution is a claim made by vendors and governments, with varying confidence, and it changes over time. APT4ALL **collects** what the sources say; it neither confirms nor disputes it. Before citing "actor X is from country Y", go to the original source linked in the actor's card.
