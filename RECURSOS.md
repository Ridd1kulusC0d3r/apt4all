# Recursos de CTI, APT e malware

English version: [RESOURCES.md](RESOURCES.md)

Lista curada, bilíngue e verificada automaticamente. ★ = comece por aqui. Gerada de `recursos/recursos.json`; para sugerir um recurso, edite o JSON e abra um PR.

**186 recursos** · [Comece aqui](#comece-aqui) · [Enciclopédias de atores](#enciclopédias-de-atores) · [Nomes, aliases e taxonomias](#nomes-aliases-e-taxonomias) · [Relatórios e acervos](#relatórios-e-acervos) · [Operações estatais e conflitos](#operações-estatais-e-conflitos) · [TTPs, ATT&CK e mapeamento](#ttps-attck-e-mapeamento) · [Perfilamento e modelagem de ameaças](#perfilamento-e-modelagem-de-ameaças) · [Plataformas de CTI](#plataformas-de-cti) · [Feeds e IOCs](#feeds-e-iocs) · [Listas awesome](#listas-awesome) · [Análise de malware](#análise-de-malware) · [Ransomware](#ransomware) · [Sandboxes](#sandboxes) · [Amostras (cuidado)](#amostras-cuidado) · [DFIR e memória](#dfir-e-memória) · [Detecção e caça](#detecção-e-caça) · [Emulação e validação](#emulação-e-validação) · [Datasets para pesquisa](#datasets-para-pesquisa) · [Pesquisa acadêmica](#pesquisa-acadêmica) · [Aprender: cursos, livros e desafios](#aprender-cursos-livros-e-desafios) · [Canais e pessoas](#canais-e-pessoas)

★ comece por aqui · 🔹 da lista original do mantenedor

## Comece aqui

Os poucos recursos que respondem 80% das perguntas sobre um ator.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [APT Groups and Operations](https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU) 🔹 | A planilha clássica de aliases por país (CC BY 4.0). Base do Atlas deste repositório. | gratuito |
| ★ [awesome-threat-actor-resources](https://github.com/rstcloud/awesome-threat-actor-resources) 🔹 | Meta-lista que compara mais de 30 bases de atores e quantos grupos cada uma cobre. | gratuito |
| ★ [ETDA Threat Group Cards](https://apt.etda.or.th/cgi-bin/listgroups.cgi) 🔹 | Enciclopédia da ETDA/ThaiCERT: cartões completos por grupo, com datas de atividade. | gratuito |
| ★ [Malpedia (Fraunhofer FKIE)](https://malpedia.caad.fkie.fraunhofer.de/actors) | Atores e famílias de malware com bibliografia organizada. | gratuito |
| ★ [MITRE ATT&CK Groups](https://attack.mitre.org/groups/) | Referência autoritativa de grupos, com técnicas e softwares mapeados. | gratuito |
| ★ [mthcht/ThreatIntel-Reports](https://github.com/mthcht/ThreatIntel-Reports) 🔹 | Milhares de relatórios de CTI extraídos e pesquisáveis por palavra-chave, com site de busca. | gratuito |

## Enciclopédias de atores

Perfis de grupos: nomes, alvos, ferramentas e histórico.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [MISP Galaxy: threat actors](https://misp-galaxy.org/threat-actor/) | Mais de mil atores com sinônimos, país e vítimas; base do MISP (CC0/BSD). | gratuito |
| [APT Intelligence Dashboard](https://github.com/michaelelizarov/apt-intelligence-dashboard) 🔹 | Painel que junta MISP, ATT&CK e APTnotes: mapa, linha do tempo e dossiês (MIT). | gratuito |
| [APTmap](https://andreacristaldi.github.io/APTmap/) 🔹 | Mapa interativo de grupos com filtros por alvo, motivação e patrocinador; dados em JSON (CC BY 4.0). | gratuito |
| [BSI: grupos APT ativos na Alemanha](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Cyber-Sicherheitslage/Analysen-und-Prognosen/Threat-Intelligence/Aktive_APT-Gruppen/aktive-apt-gruppen_node.html) | Visão de um governo sobre os grupos que miram o seu país. | gratuito |
| [CrowdStrike Adversary Universe](https://www.crowdstrike.com/adversaries/) | Perfis públicos dos adversários da CrowdStrike (Panda, Bear, Kitten, Spider). | gratuito |
| [Dragos threat groups](https://www.dragos.com/threat-groups/) | Perfis de adversários de ICS/OT. | gratuito |
| [ETDA Threat Actor Encyclopedia (PDF)](https://www.thaicert.or.th/downloads/files/A_Threat_Actor_Encyclopedia.pdf) | Versão em livro dos Threat Group Cards. | gratuito |
| [EUREPOC APT profiles](https://eurepoc.eu/advanced-persistent-threats-apts/) | Perfis do repositório europeu de incidentes cibernéticos. | gratuito |
| [Google Threat Intelligence: APT groups](https://cloud.google.com/security/resources/insights/apt-groups) | Grupos APT numerados da Mandiant (antiga página da FireEye). | gratuito |
| [Kaspersky APT Logbook](https://apt.securelist.com/) | Registro de ataques direcionados da Kaspersky, com linha do tempo. | gratuito |
| [Microsoft: nomenclatura de atores](https://learn.microsoft.com/en-us/unified-secops-platform/microsoft-threat-actor-naming) | Taxonomia de clima da Microsoft (Typhoon, Blizzard, Sandstorm) com mapeamento de nomes. | gratuito |
| [RedDrip APT_Digital_Weapon](https://github.com/RedDrip7/APT_Digital_Weapon) | Perfis e hashes de armas digitais de APT, visão da comunidade chinesa de CTI. | gratuito |
| [Secureworks Threat Profiles](https://www.secureworks.com/research/threat-profiles) | Perfis com aliases e notas de pesquisa (BRONZE, IRON, COBALT...). | gratuito |
| [SOCRadar threat actor profiles](https://socradar.io/category/threat-actor-profiles/) 🔹 | Perfis comentados de atores e grupos de ransomware. | gratuito |
| [Unit 42 threat actor groups](https://unit42.paloaltonetworks.com/threat-actor-groups-tracked-by-palo-alto-networks-unit-42/) | Grupos rastreados pela Unit 42 (nomenclatura de constelações). | gratuito |
| [Wiz Cloud Threat Landscape](https://threats.wiz.io/all-actors) | Atores com foco em nuvem. | gratuito |

## Nomes, aliases e taxonomias

Cada fornecedor dá um nome diferente ao mesmo grupo. Aqui você traduz.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [EternalLiberty](https://github.com/StrangerealIntel/EternalLiberty) | Tabela de cerca de 850 atores com o nome que cada fornecedor usa. | gratuito |
| [apt.threattracking.com](https://apt.threattracking.com/) 🔹 | Endereço curto da planilha APT Groups and Operations: responde 'qual o outro nome deste grupo?'. | gratuito |
| [Microsoft x CrowdStrike: mapa de nomes](https://www.crowdstrike.com/en-us/blog/crowdstrike-and-microsoft-unite-to-deconflict-cyber-threat-attribution/) | Mapeamento oficial entre as duas nomenclaturas. | gratuito |
| [Categorized-Adversary-TTPs](https://github.com/tropChaud/Categorized-Adversary-TTPs) 🔹 | Atores do ATT&CK cruzados com setor, país e motivação; importável no MISP. Desatualizado, mas útil. | gratuito · legado |

## Relatórios e acervos

Onde estão os relatórios públicos de campanhas, indexados.

| Recurso | Para que serve | Acesso |
|---|---|---|
| [APT & CyberCriminal Campaign Collections](https://github.com/CyberMonitor/APT_CyberCriminal_Campagin_Collections) 🔹 | Acervo de relatórios de campanhas organizado por ano. | gratuito |
| [APTnotes](https://github.com/aptnotes/data) 🔹 | Índice histórico de relatórios públicos de APT com metadados. | gratuito |
| [Awesome Threat Intel Blogs](https://github.com/muchdogesec/awesome_threat_intel_blogs) | Blogs de pesquisa de CTI para monitorar via RSS. | gratuito |
| [ThreatIntel-Reports (site de busca)](https://mthcht.github.io/ThreatIntel-Reports/) 🔹 | Interface de busca sobre o acervo de relatórios extraídos. | gratuito |

## Operações estatais e conflitos

Bases de incidentes atribuídos a Estados e mapas de conflito cibernético.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [CFR Cyber Operations Tracker](https://www.cfr.org/cyber-operations/) 🔹 | Incidentes patrocinados por Estados desde 2005, com patrocinador, vítima e tipo. | gratuito |
| [CSIS Significant Cyber Incidents](https://www.csis.org/programs/strategic-technologies-program/significant-cyber-incidents) | Lista cronológica de incidentes cibernéticos significativos. | gratuito |
| [CyberWar Map (National Security Archive)](https://embed.kumu.io/0b023bf1a971ba32510e86e8f1a38c38#apt-index) 🔹 | Mapa visual de atores e eventos de conflito cibernético entre Estados. | gratuito |
| [EuRepoC](https://eurepoc.eu/) | Base europeia de incidentes cibernéticos com atribuição e impacto. | gratuito |
| [IISS Cyberspace](https://www.iiss.org/research-paper/) | Pesquisa do IISS sobre poder cibernético e operações estatais. | gratuito |

## TTPs, ATT&CK e mapeamento

Vocabulário comum de comportamento e ferramentas para mapear relatórios.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [MITRE CTI (STIX)](https://github.com/mitre-attack/attack-stix-data) | Dados do ATT&CK em STIX 2.1, base para automação. | gratuito |
| [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) | Visualize e compare coberturas e perfis de atores em camadas. | gratuito |
| [CISA Decider](https://github.com/cisagov/Decider) | Guia por perguntas para mapear comportamento a técnicas ATT&CK. | gratuito |
| [Malware Behavior Catalog (MBC)](https://github.com/MBCProject/mbc-markdown) | Comportamentos de malware no estilo ATT&CK, usado pelo capa. | gratuito |
| [Mappings Explorer (CTID)](https://center-for-threat-informed-defense.github.io/mappings-explorer/) | Liga controles de segurança (NIST, nuvem, VERIS) a técnicas ATT&CK. | gratuito |
| [MITRE ATT&CK no GitHub](https://github.com/mitre-attack) 🔹 | Organização oficial: dados STIX, Navigator, bibliotecas e o próprio site. | gratuito |
| [MITRE D3FEND](https://d3fend.mitre.org/) | Vocabulário de contramedidas defensivas ligado ao ATT&CK. | gratuito |
| [mitreattack-python](https://github.com/mitre-attack/mitreattack-python) | Biblioteca oficial para consultar ATT&CK e gerar camadas. | gratuito |
| [Top ATT&CK Techniques (CTID)](https://top-attack-techniques.mitre-engenuity.org/) | Calculadora para priorizar técnicas por prevalência e contexto. | gratuito |
| [TRAM (CTID)](https://github.com/center-for-threat-informed-defense/tram) | Pesquisa em mapeamento automático de relatórios para ATT&CK. | gratuito |

## Perfilamento e modelagem de ameaças

Do 'quem pode me atacar' ao 'onde investir primeiro'.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [ControlCompass](https://controlcompass.github.io/) 🔹 | Liga cerca de 600 técnicas a mais de 10 mil controles públicos e 2.100 testes ofensivos. | gratuito |
| ★ [Cyber-Threat-Context-Modeling (TCE)](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling) | Threat Context Engineering: do negócio e das joias da coroa até caminhos, telemetria e detecção, com camada preditiva (Horizon). | gratuito |
| ★ [Tidal Cyber: Ultimate Guide to Cyber Threat Profiling](https://www.tidalcyber.com/ultimate-guide-to-cyber-threat-profiling) 🔹 | Guia de perfilamento de ameaças em escala organizacional. | gratuito |
| [Anvilogic: Threat Prioritization](https://www.anvilogic.com/) 🔹 | Pontuação de alertas que combina superfície de ataque e modelagem de ameaças. | pago |
| [CTID: Threat Modeling with ATT&CK](https://center-for-threat-informed-defense.github.io/threat-modeling-with-attack/) | Metodologia do CTID para modelar ameaças com ATT&CK e evidências. | gratuito |
| [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling) | Ponto de entrada da OWASP para modelagem de ameaças. | gratuito |
| [THEORY (threatcraft-co)](https://github.com/threatcraft-co/theory) 🔹 | Gera dossiê de um ator a partir de mais de 15 fontes, com saída em STIX 2.1 e camada do Navigator (MIT). | gratuito |
| [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) | Os valores e as quatro perguntas da modelagem de ameaças. | gratuito |
| [ThreatForest (AWS samples)](https://aws-samples.github.io/samples-agentic-attack-tree-generator/) 🔹 | Agentes de IA que geram árvores de ataque mapeadas ao ATT&CK a partir de um projeto. | gratuito |
| [Tidal Cyber Community Edition](https://app.tidalcyber.com/) 🔹 | Plataforma gratuita para montar perfis de ameaça e cobertura sobre o ATT&CK. | com cadastro |
| [Tidal: perfil de ameaça compartilhado](https://app.tidalcyber.com/share/8bd9e111-0a06-4609-aadb-0b337e4c7c7c) 🔹 | Exemplo de perfil de ameaça montado no Tidal e compartilhado por link. | com cadastro |
| [tidalcyber/cyber-threat-profiling](https://github.com/tidalcyber/cyber-threat-profiling) 🔹 | Biblioteca de frameworks, fontes, quantificação e ferramentas que acompanha o guia. | gratuito |

## Plataformas de CTI

Onde guardar, correlacionar e compartilhar inteligência.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [MISP](https://github.com/MISP/MISP) | Plataforma aberta de referência para compartilhar e correlacionar inteligência. | gratuito |
| [AlienVault OTX](https://otx.alienvault.com/) 🔹 | Comunidade aberta de troca de indicadores (pulses). | com cadastro |
| [IntelOwl](https://github.com/intelowlproject/IntelOwl) | Enriquecimento automático de IOCs com dezenas de analisadores. | gratuito |
| [OpenCTI](https://github.com/OpenCTI-Platform/opencti) | Gestão de conhecimento de CTI em grafo, nativa em STIX 2.1. | gratuito |
| [SOCRadar](https://socradar.io/) 🔹 | Plataforma comercial de inteligência com painéis públicos de conflitos e atores. | freemium |
| [TheHive](https://github.com/TheHive-Project/TheHive) | Gestão de casos de resposta a incidentes, integrável ao MISP. | gratuito |
| [Yeti](https://github.com/yeti-platform/yeti) | Repositório unificado de observáveis, IOCs e TTPs para CTI e DFIR. | gratuito |

## Feeds e IOCs

Indicadores e vulnerabilidades exploradas, com fontes vivas.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [abuse.ch](https://abuse.ch/) 🔹 | MalwareBazaar, URLhaus, ThreatFox, Feodo Tracker e SSLBL: feeds gratuitos essenciais. | gratuito |
| ★ [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) 🔹 | Vulnerabilidades sabidamente exploradas: a lista que define o que corrigir primeiro. | gratuito |
| [FireHOL blocklist-ipsets](https://github.com/firehol/blocklist-ipsets) | Coleção de listas de bloqueio de IP, com histórico. | gratuito |
| [FIRST EPSS](https://www.first.org/epss/) | Probabilidade de exploração de cada CVE nos próximos 30 dias. | gratuito |
| [Public-Intelligence-Feeds](https://github.com/CriticalPathSecurity/Public-Intelligence-Feeds) | Feeds públicos consolidados em formatos padronizados. | gratuito |
| [threat-intelligence-feeds (kraloveckey)](https://github.com/kraloveckey/threat-intelligence-feeds) 🔹 | Mais de 300 feeds com verificação diária automatizada. | gratuito |
| [ThreatFox (abuse.ch)](https://threatfox.abuse.ch/) | IOCs de malware compartilhados pela comunidade, com API gratuita. | gratuito |

## Listas awesome

Meta-listas mantidas pela comunidade.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [mthcht/awesome-lists](https://github.com/mthcht/awesome-lists) 🔹 | Listas de caça para SOC/CTI: palavras-chave, pipes, TLDs, ferramentas abusadas, regras. | gratuito |
| [awesome-incident-response](https://github.com/bryanwills/awesome-incident-response) 🔹 | Ferramentas de resposta a incidentes e forense. | gratuito |
| [awesome-malware-analysis](https://github.com/rshipp/awesome-malware-analysis) | A referência em ferramentas de análise de malware. | gratuito |
| [awesome-threat-detection](https://github.com/0x4D31/awesome-threat-detection) 🔹 | Detecção e caça: ferramentas, dados, artigos. | gratuito |
| [awesome-threat-intelligence](https://github.com/hslatman/awesome-threat-intelligence) | A lista awesome mais conhecida de CTI. | gratuito |
| [Malware, IR - Tools & Resources (planilha)](https://docs.google.com/spreadsheets/d/13wBzwmfAoEBPUgcYM4CgSoj--xLicPz777IQ6iSUlNk) 🔹 | Planilha comunitária de ferramentas de malware, IR e caça. Muitos links antigos foram atualizados neste repositório. | gratuito |
| [Malware-IR-Tools-Resources](https://github.com/sanjaynitttr/Malware-IR-Tools-Resources) 🔹 | Recursos de malware, IR, caça e inteligência compilados por planilha. | gratuito |
| [RazviOverflow/Malware_Resources](https://github.com/RazviOverflow/Malware_Resources) 🔹 | Coleção pessoal de análise de malware, exploração e engenharia reversa. | gratuito |
| [Threat Taming Tools Collection (T3C)](https://act.globalcyberalliance.org/index.php?title=Threat_Taming_Tools_Collection_(T3C)) 🔹 | Cerca de 300 recursos da Global Cyber Alliance: feeds, ferramentas, frameworks. | gratuito |

## Análise de malware

Ferramentas de triagem, engenharia reversa e desofuscação.

| Recurso | Para que serve | Acesso |
|---|---|---|
| [Binary Ninja](https://binary.ninja/) | Plataforma moderna de RE com API excelente; versão gratuita. | gratuito |
| [capa](https://github.com/mandiant/capa) | Identifica capacidades de um binário e mapeia para ATT&CK e MBC. | gratuito |
| [CyberChef](https://gchq.github.io/CyberChef/) | Canivete suíço para decodificar, decifrar e transformar dados. | gratuito |
| [Detect It Easy](https://github.com/horsicq/Detect-It-Easy) | Identifica compiladores, empacotadores e protetores. | gratuito |
| [dnSpyEx](https://github.com/dnSpyEx/dnSpy) | Depurador e editor .NET (fork mantido do dnSpy). | gratuito |
| [FLARE-VM](https://github.com/mandiant/flare-vm) | Instala uma VM Windows completa para análise de malware. | gratuito |
| [FLOSS](https://github.com/mandiant/flare-floss) | Extrai strings ofuscadas automaticamente. | gratuito |
| [Ghidra](https://ghidra-sre.org/) | Framework de engenharia reversa da NSA, gratuito. | gratuito |
| [IDA Free / IDA Pro](https://hex-rays.com/ida-free/) | O disassembler de referência; versão gratuita limitada. | gratuito |
| [ILSpy](https://github.com/icsharpcode/ILSpy) | Descompilador .NET. | gratuito |
| [oletools](https://github.com/decalage2/oletools) | Análise de documentos Office e macros. | gratuito |
| [PDF tools (Didier Stevens)](https://blog.didierstevens.com/programs/pdf-tools/) | pdfid e pdf-parser para PDFs maliciosos. | gratuito |
| [PE-bear](https://github.com/hasherezade/pe-bear) | Visão rápida de arquivos PE, inclusive malformados. | gratuito |
| [pestudio](https://www.winitor.com/) | Triagem estática de PE com indicadores. | gratuito |
| [ProcDOT](https://www.procdot.com/) | Transforma Procmon e PCAP em gráfico de comportamento. | gratuito |
| [radare2 / Cutter](https://rada.re/n/) | Framework livre de RE em linha de comando, com interface Cutter. | gratuito |
| [REMnux](https://remnux.org/) | Distribuição Linux para análise de malware. | gratuito |
| [Sysinternals Suite](https://learn.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite) | Process Monitor, Autoruns, Process Explorer e mais. | gratuito |
| [System Informer](https://github.com/winsiderss/systeminformer) | Sucessor do Process Hacker. | gratuito |
| [x64dbg](https://x64dbg.com/) | Depurador livre para Windows. | gratuito |
| [XORSearch](https://blog.didierstevens.com/programs/xorsearch/) | Procura dados escondidos por XOR e similares. | gratuito |
| [YARA-X](https://github.com/VirusTotal/yara-x) | Nova geração do YARA em Rust; o YARA clássico está em manutenção. | gratuito |
| [yarGen](https://github.com/Neo23x0/yarGen) | Gera rascunhos de regras YARA a partir de amostras. | gratuito |
| [de4dot](https://github.com/de4dot/de4dot) | Desofuscador .NET; arquivado, ainda útil em amostras antigas. | gratuito · legado |
| [OllyDbg](http://www.ollydbg.de/) | Depurador clássico de 32 bits; substituído pelo x64dbg. | gratuito · legado |
| [PEiD](https://www.aldeid.com/wiki/PEiD) | Identificador de empacotadores histórico; use Detect It Easy. | gratuito · legado |

## Ransomware

Quem extorque quem, com quais ferramentas, e como testar a sua defesa contra isso.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [Ransomware Tool Matrix (BushidoUK)](https://github.com/BushidoUK/Ransomware-Tool-Matrix) 🔹 | Quais ferramentas cada gangue de ransomware usa (RMM, exfiltração, credenciais, evasão). Base dos fluxos e da rede de ransomware do Atlas. CC BY 4.0. | gratuito |
| [BushidoToken: atualizações do Ransomware Tool Matrix (jun/2026)](https://blog.bushidotoken.net/2026/06/ransomware-tool-matrix-project-updates.html) | O que entrou na matriz e três grupos para acompanhar, pelo autor do projeto. | gratuito |
| [CISA #StopRansomware](https://www.cisa.gov/stopransomware) | Alertas conjuntos com TTPs, indicadores e mitigação por grupo. | gratuito |
| [eCrime.ch](https://ecrime.ch/) | Monitoramento de ransomware e extorsão, com estatísticas por grupo e setor. | freemium |
| [ID Ransomware](https://id-ransomware.malwarehunterteam.com/) | Identifica a família pela nota de resgate ou por um arquivo cifrado. | gratuito |
| [No More Ransom](https://www.nomoreransom.org/) | Decifradores gratuitos de polícias e empresas. Primeira parada de quem foi atingido. | gratuito |
| [RansomLook](https://www.ransomlook.io/) | Agregador aberto de sites de vazamento de ransomware, com código no GitHub. | gratuito |
| [Ransomware Vulnerability Matrix](https://github.com/BushidoUK/Ransomware-Vulnerability-Matrix) | Vulnerabilidades exploradas por gangues de ransomware, para priorizar correção. | gratuito |
| [ransomware.live](https://www.ransomware.live/) | Acompanha em quase tempo real as vítimas publicadas nos sites de vazamento, com API e perfis de grupos. | freemium |
| [Ransomwhere](https://ransomwhe.re/) | Base aberta de pagamentos de resgate em bitcoin, para pesquisa. | gratuito |
| [Simulating the RansomHub ransomware (Sebastian Kandler)](https://medium.com/@sebastian.kandler/simulating-the-ransomhub-ransomware-a-vital-exercise-for-strengthening-detection-and-response-b8ecdee0f2bc) 🔹 | Exercício de purple team (set/2024) que reproduz comportamentos do RansomHub com Atomic Red Team para achar lacunas de detecção no SIEM e no EDR. | gratuito |
| [skandler/ransomhub-simulation](https://github.com/skandler/ransomhub-simulation) | Script do artigo acima. Rode só em laboratório autorizado e isolado. | gratuito |

## Sandboxes

Detonação controlada, online e local.

| Recurso | Para que serve | Acesso |
|---|---|---|
| [ANY.RUN](https://any.run/) | Sandbox interativa online. | freemium |
| [Assemblyline](https://github.com/CybercentreCanada/assemblyline) | Triagem em escala do Centro Canadense de Cibersegurança. | gratuito |
| [CAPEv2](https://github.com/kevoreilly/CAPEv2) | Sandbox livre com extração de configuração; sucessor prático do Cuckoo. | gratuito |
| [Hatching Triage](https://tria.ge/) | Sandbox online com extração de configuração de famílias. | com cadastro |
| [Hybrid Analysis](https://www.hybrid-analysis.com/) | Sandbox online gratuita da CrowdStrike. | com cadastro |
| [Joe Sandbox](https://www.joesandbox.com/) | Sandbox comercial com versão básica pública. | freemium |
| [urlscan.io](https://urlscan.io/) | Análise de URLs e páginas. | freemium |
| [VirusTotal](https://www.virustotal.com/) | Varredura multi-motor e pivôs de inteligência. | freemium |
| [Cuckoo Sandbox](https://github.com/cuckoosandbox/cuckoo) | Sandbox histórica; sem manutenção. Use CAPEv2. | gratuito · legado |

## Amostras (cuidado)

Acervos de malware real. Só em laboratório isolado.

> ⚠️ **Malware real.** Baixe e abra só em laboratório isolado (VM sem rede ou com rede simulada). Nunca no seu computador de trabalho.

| Recurso | Para que serve | Acesso |
|---|---|---|
| [APTMalware (cyber-research)](https://github.com/cyber-research/APTMalware) | Cerca de 3,5 mil amostras atribuídas a APTs, usadas em pesquisa acadêmica. | gratuito |
| [MalShare](https://malshare.com/) | Repositório comunitário de amostras. | com cadastro |
| [Malware-Traffic-Analysis.net](https://www.malware-traffic-analysis.net/) | PCAPs e exercícios de tráfego malicioso. | gratuito |
| [MalwareBazaar](https://bazaar.abuse.ch/) | Amostras recentes por hash, tag e família. | gratuito |
| [theZoo](https://github.com/ytisf/theZoo) | Amostras históricas para estudo. | gratuito |
| [VirusShare](https://virusshare.com/) | Acervo grande de amostras para pesquisa. | com cadastro |
| [vx-underground samples](https://vx-underground.org/) | Acervo massivo de amostras organizadas por família e APT, mais a coleção de papers sobre malware. | gratuito |

## DFIR e memória

Resposta a incidentes, forense de disco e memória.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [The DFIR Report](https://thedfirreport.com/) | Intrusões reais do acesso inicial ao ransomware, com linha do tempo e ATT&CK. | gratuito |
| [Autopsy](https://www.autopsy.com/) | Forense de disco com interface gráfica. | gratuito |
| [bulk_extractor](https://github.com/simsong/bulk_extractor) | Extração de artefatos de imagens de disco. | gratuito |
| [Chainsaw](https://github.com/WithSecureLabs/chainsaw) | Busca rápida em logs EVTX com regras Sigma. | gratuito |
| [Eric Zimmerman's tools](https://ericzimmerman.github.io/) | Parsers de artefatos Windows usados em todo DFIR. | gratuito |
| [Hayabusa](https://github.com/Yamato-Security/hayabusa) | Linha do tempo e caça em logs do Windows. | gratuito |
| [KAPE](https://www.kroll.com/en/services/cyber/incident-response-recovery/kroll-artifact-parser-and-extractor-kape) | Coleta e processamento rápidos de artefatos. | gratuito |
| [LiME](https://github.com/504ensicsLabs/LiME) | Captura de memória em Linux. | gratuito |
| [RegRipper](https://github.com/keydet89/RegRipper3.0) | Análise de registro do Windows. | gratuito |
| [Velociraptor](https://github.com/Velocidex/velociraptor) | Coleta e caça em endpoints com VQL. | gratuito |
| [Volatility 3](https://github.com/volatilityfoundation/volatility3) | Análise forense de memória. | gratuito |
| [Rekall](https://github.com/google/rekall) | Framework de memória arquivado. | gratuito · legado |

## Detecção e caça

Regras, listas de caça e dados para testar detecções.

| Recurso | Para que serve | Acesso |
|---|---|---|
| [DeTT&CT](https://github.com/rabobank-cdc/DeTTECT) | Mede visibilidade e cobertura de detecção por técnica e cruza com grupos de ameaça. | gratuito |
| [EVTX-ATTACK-SAMPLES](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES) | Logs de eventos do Windows por técnica de ataque, para testar detecções. | gratuito |
| [HEARTH](https://github.com/THORCollective/HEARTH) | Repositório comunitário de hipóteses de caça. | gratuito |
| [osquery](https://osquery.io/) | Endpoint consultável em SQL. | gratuito |
| [Security Datasets (OTRF)](https://github.com/OTRF/Security-Datasets) | Dados de simulação para pesquisa de detecção. | gratuito |
| [Sigma](https://github.com/SigmaHQ/sigma) | Formato padrão de regras de detecção, convertível para SIEMs. | gratuito |
| [Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) | Telemetria detalhada de processos, rede e arquivos no Windows. | gratuito |
| [The ThreatHunting Project](https://www.threathunting.net/) | Introdução e catálogo de caças. | gratuito |
| [YARA](https://github.com/VirusTotal/yara) 🔹 | Ferramenta clássica de padrões para classificar malware. Para regras novas, veja também o YARA-X. | gratuito |

## Emulação e validação

Teste suas defesas com o comportamento de atores reais.

| Recurso | Para que serve | Acesso |
|---|---|---|
| [Adversary Emulation Library (CTID)](https://github.com/center-for-threat-informed-defense/adversary_emulation_library) | Planos de emulação de atores reais (APT29, FIN6, menuPass e outros). | gratuito |
| [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) | Testes pequenos por técnica ATT&CK para validar detecções. | gratuito |
| [MITRE Caldera](https://github.com/mitre/caldera) | Emulação automatizada de adversários. | gratuito |

## Datasets para pesquisa

Dados estruturados para estudos e modelos.

| Recurso | Para que serve | Acesso |
|---|---|---|
| ★ [Gulbay (2024): DEVIL / APT reports graph dataset (Zenodo)](https://zenodo.org/records/12741055) 🔹 | Relatórios de APT deduplicados, IOCs extraídos e grafo Neo4j para CTI estratégica (Gulbay, 2024, CC BY 4.0). | gratuito |
| [APT simulation datasets (skrghosh)](https://github.com/skrghosh/apt-dataset) 🔹 | Logs de simulações no Caldera de APT29, FIN6, menuPass, OilRig e Wizard Spider, mais famílias como Redline e AsyncRAT. | gratuito |
| [APTmap JSON](https://github.com/andreacristaldi/APTmap) 🔹 | Dados de grupos e de 29 GB de amostras atribuídas (CC BY 4.0). | gratuito |

## Pesquisa acadêmica

Artigos e ferramentas de pesquisa sobre CTI e modelagem.

| Recurso | Para que serve | Acesso |
|---|---|---|
| [Intel TARA / Threat Agent Library](https://www.oasis-open.org/committees/download.php/66239/Intel%20Corp_Threat%20Agent%20Library_07-2202w.pdf) | Biblioteca de agentes de ameaça para avaliação de risco. | gratuito |
| [MITRE: Cyber Threat Modeling: Survey, Assessment, and Representative Framework](https://www.mitre.org/sites/default/files/2021-11/prs-18-1174-ngci-cyber-threat-modeling.pdf) | Revisão de frameworks de modelagem de ameaças. | gratuito |
| [ThreatCompass (Univ. Twente)](https://research.utwente.nl/en/publications/threatcompass-a-tool-for-identifying-and-mapping-security-issues/) 🔹 | Ferramenta de pesquisa que identifica problemas de segurança e os mapeia para TTPs, com grafo de ataque. | gratuito |

## Aprender: cursos, livros e desafios

Trilhas gratuitas e pagas, livros e CTFs de engenharia reversa.

| Recurso | Para que serve | Acesso |
|---|---|---|
| [begin.re](https://www.begin.re/) | RE para iniciantes. | gratuito |
| [challenges.re](https://challenges.re/) | Exercícios de RE por arquitetura. | gratuito |
| [crackmes.one](https://crackmes.one/) | Desafios de engenharia reversa da comunidade. | gratuito |
| [FLARE-On](https://flare-on.com/) | Desafio anual de engenharia reversa do Google/Mandiant; soluções publicadas. | gratuito |
| [Livro: Evasive Malware](https://nostarch.com/evasive-malware) | Kyle Cucci (2024): técnicas de evasão e como analisá-las. | pago |
| [Livro: Practical Malware Analysis](https://nostarch.com/malware) | Sikorski e Honig. O clássico. | pago |
| [Livro: The Art of Memory Forensics](https://www.wiley.com/en-us/The+Art+of+Memory+Forensics-p-9781118825099) | Ligh, Case, Levy e Walters. | pago |
| [Livro: Windows Internals](https://learn.microsoft.com/en-us/sysinternals/resources/windows-internals) | Base para entender o que o malware abusa no Windows. | pago |
| [Malware Unicorn RE101](https://malwareunicorn.org/workshops/re101.html) | Workshop introdutório de engenharia reversa. | gratuito |
| [MalwareTech challenges](https://www.malwaretech.com/beginner-malware-reversing-challenges) | Desafios de reversão para iniciantes. | gratuito |
| [OpenSecurityTraining2](https://ost2.fyi/) | Cursos gratuitos de x86, RE e firmware (sucessor do OpenSecurityTraining). | gratuito |
| [Practical Malware Analysis labs](https://github.com/mikesiko/PracticalMalwareAnalysis-Labs) | Laboratórios do livro clássico. | gratuito |
| [Reverse Engineering for Beginners (Yurichev)](https://beginners.re/) | Livro gratuito de engenharia reversa. | gratuito |
| [RPISEC Malware](https://github.com/RPISEC/Malware) | Curso universitário aberto de análise de malware. | gratuito |
| [SANS FOR578](https://www.sans.org/cyber-security-courses/cyber-threat-intelligence/) | Curso de referência em CTI. | pago |
| [SANS FOR610](https://www.sans.org/cyber-security-courses/reverse-engineering-malware-malware-analysis-tools-techniques/) | Curso de referência em engenharia reversa de malware. | pago |

## Canais e pessoas

Quem ensina análise de malware em vídeo.

| Recurso | Para que serve | Acesso |
|---|---|---|
| [hasherezade](https://www.youtube.com/@hasherezade) | Canal de vídeo sobre análise de malware e engenharia reversa. | gratuito |
| [John Hammond](https://www.youtube.com/@_JohnHammond) | Canal de vídeo sobre análise de malware e engenharia reversa. | gratuito |
| [LiveOverflow](https://www.youtube.com/@LiveOverflow) | Canal de vídeo sobre análise de malware e engenharia reversa. | gratuito |
| [MalwareAnalysisForHedgehogs](https://www.youtube.com/@MalwareAnalysisForHedgehogs) | Canal de vídeo sobre análise de malware e engenharia reversa. | gratuito |
| [MalwareTech](https://www.youtube.com/@MalwareTechBlog) | Canal de vídeo sobre análise de malware e engenharia reversa. | gratuito |
| [OALabs](https://www.youtube.com/@OALABS) | Canal de vídeo sobre análise de malware e engenharia reversa. | gratuito |
