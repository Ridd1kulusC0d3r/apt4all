# ◆ Trilha APT4ALL: do nome do grupo ao dossiê

English: [README.en.md](README.en.md)

Nove módulos para quem quer fazer CTI de verdade sobre APT e malware, no lado da defesa. Cada módulo tem **uma** ação "faça agora" com o Atlas, um entregável e uma checagem. Faça um por sessão; não precisa ler tudo antes de começar.

| # | Módulo | Tempo | Entregável |
|---|---|---|---|
| 1 | [Um grupo, dez nomes](#módulo-1--um-grupo-dez-nomes) | 45 min | Tabela de nomes de 3 atores |
| 2 | [Ler um relatório sem se perder](#módulo-2--ler-um-relatório-sem-se-perder) | 1 h | Ficha de relatório preenchida |
| 3 | [Pirâmide da Dor e Modelo Diamante](#módulo-3--pirâmide-da-dor-e-modelo-diamante) | 1 h | Diamante de um ator |
| 4 | [Mapear para o ATT&CK](#módulo-4--mapear-para-o-attck) | 1 h 30 | Camada do Navigator com 8 técnicas justificadas |
| 5 | [Atribuição com método](#módulo-5--atribuição-com-método) | 1 h | Matriz ACH com 3 hipóteses |
| 6 | [Perfil de ameaça da sua organização](#módulo-6--perfil-de-ameaça-da-sua-organização) | 1 h | Perfil país + setor com top 10 técnicas |
| 7 | [Do perfil à defesa](#módulo-7--do-perfil-à-defesa) | 2 h | Tabela de cobertura de 5 técnicas |
| 8 | [Triagem segura de malware de APT](#módulo-8--triagem-segura-de-malware-de-apt) | 1 h | Registro de triagem de um hash público |
| 9 | [Projeto final: dossiê de ator](#módulo-9--projeto-final-dossiê-de-ator) | 3 h | Dossiê no modelo, pronto para publicar |

Modelos para copiar: [`modelos/`](modelos/).

---

## Módulo 1 · Um grupo, dez nomes

**Por que importa.** Cada fornecedor batiza o mesmo grupo do seu jeito: a Microsoft usa clima (Forest Blizzard), a CrowdStrike usa animais por país (Fancy Bear), a Mandiant usa números (APT28) e prefixos para grupos ainda sem atribuição (UNC, FIN), e o ATT&CK usa IDs (G0007). Quem não domina isso lê dois relatórios sobre o mesmo grupo achando que são dois grupos.

**Leia (escolha um):**
- [MITRE ATT&CK Groups](https://attack.mitre.org/groups/)
- [CrowdStrike e Microsoft: mapa de nomes](https://www.crowdstrike.com/en-us/blog/crowdstrike-and-microsoft-unite-to-deconflict-cyber-threat-attribution/)
- [apt.threattracking.com](https://apt.threattracking.com/)

**Faça agora.** No Atlas, abra a ficha de `APT28`, `Lazarus Group` e `OilRig`. Para cada um, use a seção **Nomes por fornecedor** e anote o nome da Microsoft, da CrowdStrike, da Mandiant e o ID do ATT&CK. Faltou algum? Procure em **Nomes conhecidos** ou no apt.threattracking.com.

**Entregável.** Tabela com 3 linhas e 5 colunas (nome comum, Microsoft, CrowdStrike, Mandiant, ATT&CK).

**Checagem.** Você sabe explicar por que "Lazarus" às vezes inclui Andariel e BlueNoroff e às vezes não? (Pista: é um guarda-chuva, e cada fornecedor corta diferente.)

## Módulo 2 · Ler um relatório sem se perder

**Por que importa.** Relatório de ameaça mistura fato observado, inferência e marketing. O analista separa os três e registra a confiança de cada afirmação.

**Leia:**
- [ICD 203: padrões analíticos](https://www.dni.gov/files/documents/ICD/ICD-203.pdf) (linguagem de probabilidade e confiança)
- [mthcht/ThreatIntel-Reports](https://github.com/mthcht/ThreatIntel-Reports) (acervo para praticar)

**Faça agora.** Na ficha do `APT29` no Atlas, desça até **Relatórios (APTnotes)** e abra um. Preencha a [ficha de relatório](modelos/ficha-relatorio.md).

**Entregável.** Ficha com: quem publicou, data, vitimologia, comportamentos descritos, indicadores citados, nível de confiança declarado e o que é inferência.

**Checagem.** Você marcou pelo menos uma frase como "inferência do fornecedor" e não como fato?

## Módulo 3 · Pirâmide da Dor e Modelo Diamante

**Por que importa.** A Pirâmide da Dor mostra que bloquear hash é fácil para você e trivial para o adversário contornar; atacar comportamento (TTP) custa caro para ele. O Modelo Diamante organiza qualquer evento em adversário, capacidade, infraestrutura e vítima.

**Leia:**
- [The Pyramid of Pain (David Bianco)](https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html)
- [The Diamond Model of Intrusion Analysis](https://www.activeresponse.org/wp-content/uploads/2013/07/diamond.pdf)

**Faça agora.** Com a ficha do relatório do módulo 2, desenhe o diamante: um vértice por quadrante, com o que o relatório diz.

**Entregável.** Diamante preenchido (pode ser à mão, foto vale).

**Checagem.** Algum vértice ficou vazio? Isso é uma lacuna de inteligência: anote como pergunta para o próximo relatório.

## Módulo 4 · Mapear para o ATT&CK

**Por que importa.** O ATT&CK é a língua comum entre CTI, detecção e red team. Mapear bem é descrever o **comportamento** observado com a técnica certa, sem inventar o que o relatório não diz.

**Leia:**
- [Top ATT&CK Techniques (CTID)](https://top-attack-techniques.mitre-engenuity.org/)
- [CISA Decider](https://github.com/cisagov/Decider) (ajuda a escolher a técnica por perguntas)
- [TRAM (CTID)](https://github.com/center-for-threat-informed-defense/tram) (mapeamento assistido de texto)

**Faça agora.** Pegue 8 frases de comportamento da sua ficha e mapeie cada uma para uma técnica no [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/). Compare com as técnicas da ficha do ator no Atlas.

**Entregável.** Camada do Navigator exportada, com um comentário em cada técnica citando a frase do relatório.

**Checagem.** Alguma técnica sua não aparece na ficha do Atlas? Ou o relatório é novo, ou o mapeamento forçou a barra. Decida qual.

## Módulo 5 · Atribuição com método

**Por que importa.** Atribuição errada derruba a credibilidade do time inteiro. A Análise de Hipóteses Concorrentes (ACH), de Richards Heuer, obriga a procurar evidência que **derruba** hipóteses, não só a que confirma a favorita. Falsa bandeira existe e já foi documentada publicamente.

**Leia:**
- [Psychology of Intelligence Analysis (Heuer), cap. 8](https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/)
- O aviso de atribuição no [FONTES.md](../FONTES.md)

**Faça agora.** Monte a [matriz ACH](modelos/matriz-ach.md) com três hipóteses para o relatório do módulo 2: o ator citado, outro ator do mesmo país, e "outro ator imitando".

**Entregável.** Matriz com pelo menos 6 evidências marcadas como consistente, inconsistente ou neutra.

**Checagem.** A hipótese vencedora é a que tem **menos inconsistências**, não a que tem mais pontos a favor. Confere?

## Módulo 6 · Perfil de ameaça da sua organização

**Por que importa.** Ninguém defende contra 1.355 atores. O perfil de ameaça recorta quem já atacou organizações parecidas com a sua e quais técnicas eles usam. É o primeiro filtro de prioridade.

**Leia:**
- [Tidal: Ultimate Guide to Cyber Threat Profiling](https://www.tidalcyber.com/ultimate-guide-to-cyber-threat-profiling)
- [CTID: Threat Modeling with ATT&CK](https://center-for-threat-informed-defense.github.io/threat-modeling-with-attack/)

**Faça agora.** No Atlas, aba **Perfil de ameaça**, escolha o país e o setor da sua organização (ou de uma organização fictícia). Baixe a camada do Navigator.

**Entregável.** Lista dos 10 atores mais relevantes e das 10 técnicas a cobrir primeiro, com uma frase sobre o limite do perfil (ex.: "pouca vitimologia pública para o Brasil").

**Checagem.** Você consegue explicar a um gestor, em duas frases, por que essas 10 técnicas e não outras?

## Módulo 7 · Do perfil à defesa

**Por que importa.** Perfil sem cobertura é só relatório. Aqui você cruza as técnicas prioritárias com o que o ambiente consegue **ver** (telemetria), **barrar** (controles) e **validar** (testes). Sem biblioteca de regras pronta: o objetivo é saber onde está o buraco.

**Leia:**
- [Mappings Explorer (CTID)](https://center-for-threat-informed-defense.github.io/mappings-explorer/) e [ControlCompass](https://controlcompass.github.io/) (controle ↔ técnica)
- [MITRE D3FEND](https://d3fend.mitre.org/) (contramedidas por técnica)
- [Sigma](https://github.com/SigmaHQ/sigma) (formato aberto de detecção, para ler como as regras são estruturadas)
- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) (testes de validação; só em ambiente autorizado)

**Faça agora.** Copie a [tabela de cobertura](modelos/cobertura.md) e preencha para as 5 primeiras técnicas do seu perfil: tenho a telemetria? tenho controle mapeado? já validei?

**Entregável.** Tabela de cobertura com 5 linhas e uma decisão por linha (manter, investigar, comprar, configurar).

**Checagem.** A técnica com mais "não" virou a primeira ação da lista? Se quiser ir além, leve o perfil para o [TCE](../tce/README.md), que faz esse cruzamento para o ambiente inteiro.

## Módulo 8 · Triagem segura de malware de APT

**Por que importa.** CTI de APT encosta em malware real. A triagem segura é nível de processo: consultar, registrar e decidir, sem abrir arquivo fora de laboratório isolado.

**Leia:**
- A seção **Amostras** dos [Recursos](https://ridd1kulusc0d3r.github.io/apt4all/recursos/) (com aviso)
- [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/actors) (famílias por ator)
- [FIRST TLP 2.0](https://www.first.org/tlp/) (como compartilhar)

**Faça agora.** Escolha um hash SHA-256 citado num relatório público do seu ator. Consulte só o hash (sem baixar o arquivo) no VirusTotal ou no MalwareBazaar e preencha o [registro de triagem](modelos/registro-triagem.md).

**Entregável.** Registro com: hash, fonte do hash, família indicada, primeira vez visto, consistência com o relatório, TLP aplicado e decisão (arquivar, escalar para laboratório, descartar).

**Checagem.** Em algum momento o arquivo saiu do serviço para a sua máquina? Se sim, volte e refaça: o exercício é só consulta.

## Módulo 9 · Projeto final: dossiê de ator

**Por que importa.** O dossiê junta tudo: nomes, atribuição com confiança, vitimologia, comportamentos, impacto para a sua organização e recomendações. É o que um analista entrega a quem decide.

**Faça agora.** Copie o [modelo de dossiê](modelos/dossie-ator.md) e escolha **um** ator do seu perfil (módulo 6). Preencha uma seção por sessão, se preferir.

**Entregável.** Dossiê com BLUF de 3 linhas, tabela de nomes, avaliação de atribuição com nível de confiança, top técnicas com cobertura (módulo 7), recomendações e fontes.

**Checagem.** Um gestor lê só o BLUF e sabe o que fazer? Um analista lê as fontes e consegue refazer suas conclusões?

Quer publicar? Abra um PR adicionando o dossiê em `trilha/dossies/` (veja o [CONTRIBUTING.md](../CONTRIBUTING.md)).
