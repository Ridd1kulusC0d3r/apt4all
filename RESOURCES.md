# CTI, APT and malware resources

Versão em português: [RECURSOS.md](RECURSOS.md)

Curated, bilingual, automatically checked list. ★ = start here. Generated from `recursos/recursos.json`; to suggest a resource, edit the JSON and open a PR.

**169 resources** · [Start here](#start-here) · [Threat actor encyclopedias](#threat-actor-encyclopedias) · [Names, aliases and taxonomies](#names-aliases-and-taxonomies) · [Reports and archives](#reports-and-archives) · [State operations and conflict trackers](#state-operations-and-conflict-trackers) · [TTPs, ATT&CK and mapping](#ttps-attck-and-mapping) · [Threat profiling and modeling](#threat-profiling-and-modeling) · [CTI platforms](#cti-platforms) · [Feeds and IOCs](#feeds-and-iocs) · [Awesome lists](#awesome-lists) · [Malware analysis](#malware-analysis) · [Sandboxes](#sandboxes) · [Samples (caution)](#samples-caution) · [DFIR and memory](#dfir-and-memory) · [Detection and hunting](#detection-and-hunting) · [Emulation and validation](#emulation-and-validation) · [Research datasets](#research-datasets) · [Academic research](#academic-research) · [Learn: courses, books and challenges](#learn-courses-books-and-challenges) · [Channels and people](#channels-and-people)

## Start here

The few resources that answer most questions about an actor.

| Resource | What it is for | Access |
|---|---|---|
| ★ [APT Groups and Operations](https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU) | The classic alias spreadsheet by country (CC BY 4.0). Base of this repo's Atlas. | free |
| ★ [awesome-threat-actor-resources](https://github.com/rstcloud/awesome-threat-actor-resources) | Meta list comparing 30+ actor databases and their coverage. | free |
| ★ [ETDA Threat Group Cards](https://apt.etda.or.th/cgi-bin/listgroups.cgi) | ETDA/ThaiCERT encyclopedia: full cards per group with activity dates. | free |
| ★ [Malpedia (Fraunhofer FKIE)](https://malpedia.caad.fkie.fraunhofer.de/actors) | Actors and malware families with an organized bibliography. | free |
| ★ [MITRE ATT&CK Groups](https://attack.mitre.org/groups/) | Authoritative group reference with mapped techniques and software. | free |
| ★ [mthcht/ThreatIntel-Reports](https://github.com/mthcht/ThreatIntel-Reports) | Thousands of extracted CTI reports searchable by keyword, with a search site. | free |

## Threat actor encyclopedias

Group profiles: names, targets, tools and history.

| Resource | What it is for | Access |
|---|---|---|
| ★ [MISP Galaxy: threat actors](https://misp-galaxy.org/threat-actor/) | 1,000+ actors with synonyms, country and victims; MISP's base (CC0/BSD). | free |
| [APT Intelligence Dashboard](https://github.com/michaelelizarov/apt-intelligence-dashboard) | Dashboard merging MISP, ATT&CK and APTnotes: map, timeline and dossiers (MIT). | free |
| [APTmap](https://andreacristaldi.github.io/APTmap/) | Interactive group map with target, motive and sponsor filters; JSON data (CC BY 4.0). | free |
| [BSI: grupos APT ativos na Alemanha](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Cyber-Sicherheitslage/Analysen-und-Prognosen/Threat-Intelligence/Aktive_APT-Gruppen/aktive-apt-gruppen_node.html) | A government's view of groups targeting its country. | free |
| [CrowdStrike Adversary Universe](https://www.crowdstrike.com/adversaries/) | CrowdStrike's public adversary profiles (Panda, Bear, Kitten, Spider). | free |
| [Dragos threat groups](https://www.dragos.com/threat-groups/) | ICS/OT adversary profiles. | free |
| [ETDA Threat Actor Encyclopedia (PDF)](https://www.thaicert.or.th/downloads/files/A_Threat_Actor_Encyclopedia.pdf) | Book version of the Threat Group Cards. | free |
| [EUREPOC APT profiles](https://eurepoc.eu/advanced-persistent-threats-apts/) | Profiles from the European cyber incident repository. | free |
| [Google Threat Intelligence: APT groups](https://cloud.google.com/security/resources/insights/apt-groups) | Mandiant's numbered APT groups (former FireEye page). | free |
| [Kaspersky APT Logbook](https://apt.securelist.com/) | Kaspersky's targeted attack log with timeline. | free |
| [Microsoft: nomenclatura de atores](https://learn.microsoft.com/en-us/unified-secops-platform/microsoft-threat-actor-naming) | Microsoft's weather taxonomy (Typhoon, Blizzard, Sandstorm) with name mapping. | free |
| [RedDrip APT_Digital_Weapon](https://github.com/RedDrip7/APT_Digital_Weapon) | APT digital weapon profiles and hashes, Chinese CTI community view. | free |
| [Secureworks Threat Profiles](https://www.secureworks.com/research/threat-profiles) | Profiles with aliases and research notes (BRONZE, IRON, COBALT...). | free |
| [SOCRadar threat actor profiles](https://socradar.io/category/threat-actor-profiles/) | Commented profiles of actors and ransomware groups. | free |
| [Unit 42 threat actor groups](https://unit42.paloaltonetworks.com/threat-actor-groups-tracked-by-palo-alto-networks-unit-42/) | Groups tracked by Unit 42 (constellation naming). | free |
| [Wiz Cloud Threat Landscape](https://threats.wiz.io/all-actors) | Cloud-focused threat actors. | free |

## Names, aliases and taxonomies

Every vendor names the same group differently. Translate here.

| Resource | What it is for | Access |
|---|---|---|
| ★ [EternalLiberty](https://github.com/StrangerealIntel/EternalLiberty) | Table of ~850 actors with each vendor's name. | free |
| [apt.threattracking.com](https://apt.threattracking.com/) | Short address of the APT Groups and Operations sheet: answers 'what else is this group called?'. | free |
| [Microsoft x CrowdStrike: mapa de nomes](https://www.crowdstrike.com/en-us/blog/crowdstrike-and-microsoft-unite-to-deconflict-cyber-threat-attribution/) | Official mapping between both naming schemes. | free |
| [Categorized-Adversary-TTPs](https://github.com/tropChaud/Categorized-Adversary-TTPs) | ATT&CK actors joined with sector, country and motive; MISP-importable. Dated but useful. | free · legacy |

## Reports and archives

Where public campaign reports live, indexed.

| Resource | What it is for | Access |
|---|---|---|
| [APT & CyberCriminal Campaign Collections](https://github.com/CyberMonitor/APT_CyberCriminal_Campagin_Collections) | Campaign report archive organized by year. | free |
| [APTnotes](https://github.com/aptnotes/data) | Historical index of public APT reports with metadata. | free |
| [Awesome Threat Intel Blogs](https://github.com/muchdogesec/awesome_threat_intel_blogs) | CTI research blogs to monitor via RSS. | free |
| [ThreatIntel-Reports (site de busca)](https://mthcht.github.io/ThreatIntel-Reports/) | Search interface over the extracted report archive. | free |

## State operations and conflict trackers

Databases of state-attributed incidents and cyber conflict maps.

| Resource | What it is for | Access |
|---|---|---|
| ★ [CFR Cyber Operations Tracker](https://www.cfr.org/cyber-operations/) | State-sponsored incidents since 2005, with sponsor, victim and type. | free |
| [CSIS Significant Cyber Incidents](https://www.csis.org/programs/strategic-technologies-program/significant-cyber-incidents) | Chronological list of significant cyber incidents. | free |
| [CyberWar Map (National Security Archive)](https://embed.kumu.io/0b023bf1a971ba32510e86e8f1a38c38#apt-index) | Visual map of actors and events in state-on-state cyber conflict. | free |
| [EuRepoC](https://eurepoc.eu/) | European cyber incident database with attribution and impact. | free |
| [IISS Cyberspace](https://www.iiss.org/research-paper/) | IISS research on cyber power and state operations. | free |

## TTPs, ATT&CK and mapping

Common behavior vocabulary and tools to map reports.

| Resource | What it is for | Access |
|---|---|---|
| ★ [MITRE CTI (STIX)](https://github.com/mitre-attack/attack-stix-data) | ATT&CK data in STIX 2.1, base for automation. | free |
| [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) | Visualize and compare coverage and actor profiles as layers. | free |
| [CISA Decider](https://github.com/cisagov/Decider) | Question-driven guide to map behavior to ATT&CK techniques. | free |
| [Malware Behavior Catalog (MBC)](https://github.com/MBCProject/mbc-markdown) | ATT&CK-style malware behaviors, used by capa. | free |
| [Mappings Explorer (CTID)](https://center-for-threat-informed-defense.github.io/mappings-explorer/) | Links security controls (NIST, cloud, VERIS) to ATT&CK techniques. | free |
| [MITRE D3FEND](https://d3fend.mitre.org/) | Defensive countermeasure vocabulary linked to ATT&CK. | free |
| [mitreattack-python](https://github.com/mitre-attack/mitreattack-python) | Official library to query ATT&CK and generate layers. | free |
| [Top ATT&CK Techniques (CTID)](https://top-attack-techniques.mitre-engenuity.org/) | Calculator to prioritize techniques by prevalence and context. | free |
| [TRAM (CTID)](https://github.com/center-for-threat-informed-defense/tram) | Research on automatic report-to-ATT&CK mapping. | free |

## Threat profiling and modeling

From 'who might attack me' to 'where to invest first'.

| Resource | What it is for | Access |
|---|---|---|
| ★ [ControlCompass](https://controlcompass.github.io/) | Links ~600 techniques to 10k+ public controls and 2,100 offensive tests. | free |
| ★ [Cyber-Threat-Context-Modeling (TCE)](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling) | Threat Context Engineering: from business and crown jewels to paths, telemetry and detection, with a predictive layer (Horizon). | free |
| ★ [Tidal Cyber: Ultimate Guide to Cyber Threat Profiling](https://www.tidalcyber.com/ultimate-guide-to-cyber-threat-profiling) | Guide to organization-wide threat profiling. | free |
| [Anvilogic: Threat Prioritization](https://www.anvilogic.com/) | Alert scoring that combines attack surface and threat modeling. | paid |
| [CTID: Threat Modeling with ATT&CK](https://center-for-threat-informed-defense.github.io/threat-modeling-with-attack/) | CTID methodology for threat modeling with ATT&CK and evidence. | free |
| [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling) | OWASP entry point for threat modeling. | free |
| [THEORY (threatcraft-co)](https://github.com/threatcraft-co/theory) | Builds an actor dossier from 15+ sources, exporting STIX 2.1 and Navigator layers (MIT). | free |
| [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) | The values and four questions of threat modeling. | free |
| [ThreatForest (AWS samples)](https://aws-samples.github.io/samples-agentic-attack-tree-generator/) | AI agents that generate ATT&CK-mapped attack trees from a project. | free |
| [Tidal Cyber Community Edition](https://app.tidalcyber.com/) | Free platform to build threat profiles and coverage on ATT&CK. | sign-up |
| [Tidal: perfil de ameaça compartilhado](https://app.tidalcyber.com/share/8bd9e111-0a06-4609-aadb-0b337e4c7c7c) | Example threat profile built in Tidal and shared by link. | sign-up |
| [tidalcyber/cyber-threat-profiling](https://github.com/tidalcyber/cyber-threat-profiling) | Library of frameworks, sources, quantification and tools that accompanies the guide. | free |

## CTI platforms

Where to store, correlate and share intelligence.

| Resource | What it is for | Access |
|---|---|---|
| ★ [MISP](https://github.com/MISP/MISP) | Reference open platform to share and correlate intelligence. | free |
| [AlienVault OTX](https://otx.alienvault.com/) | Open indicator exchange community (pulses). | sign-up |
| [IntelOwl](https://github.com/intelowlproject/IntelOwl) | Automatic IOC enrichment with dozens of analyzers. | free |
| [OpenCTI](https://github.com/OpenCTI-Platform/opencti) | Graph-based CTI knowledge management, STIX 2.1 native. | free |
| [SOCRadar](https://socradar.io/) | Commercial intelligence platform with public conflict and actor dashboards. | freemium |
| [TheHive](https://github.com/TheHive-Project/TheHive) | Incident response case management, MISP-integrable. | free |
| [Yeti](https://github.com/yeti-platform/yeti) | Unified repository of observables, IOCs and TTPs for CTI and DFIR. | free |

## Feeds and IOCs

Indicators and exploited vulnerabilities from live sources.

| Resource | What it is for | Access |
|---|---|---|
| ★ [abuse.ch](https://abuse.ch/) | MalwareBazaar, URLhaus, ThreatFox, Feodo Tracker and SSLBL: essential free feeds. | free |
| ★ [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | Known exploited vulnerabilities: the list that defines what to patch first. | free |
| [FireHOL blocklist-ipsets](https://github.com/firehol/blocklist-ipsets) | IP blocklist collection with history. | free |
| [FIRST EPSS](https://www.first.org/epss/) | Probability that each CVE is exploited in the next 30 days. | free |
| [Public-Intelligence-Feeds](https://github.com/CriticalPathSecurity/Public-Intelligence-Feeds) | Public feeds consolidated in standard formats. | free |
| [threat-intelligence-feeds (kraloveckey)](https://github.com/kraloveckey/threat-intelligence-feeds) | 300+ feeds with automated daily validation. | free |

## Awesome lists

Community-maintained meta lists.

| Resource | What it is for | Access |
|---|---|---|
| ★ [mthcht/awesome-lists](https://github.com/mthcht/awesome-lists) | Hunting lists for SOC/CTI: keywords, pipes, TLDs, abused tools, rules. | free |
| [awesome-incident-response](https://github.com/bryanwills/awesome-incident-response) | Incident response and forensics tools. | free |
| [awesome-malware-analysis](https://github.com/rshipp/awesome-malware-analysis) | The reference list of malware analysis tools. | free |
| [awesome-threat-detection](https://github.com/0x4D31/awesome-threat-detection) | Detection and hunting: tools, data, articles. | free |
| [awesome-threat-intelligence](https://github.com/hslatman/awesome-threat-intelligence) | The best-known CTI awesome list. | free |
| [Malware, IR - Tools & Resources (planilha)](https://docs.google.com/spreadsheets/d/13wBzwmfAoEBPUgcYM4CgSoj--xLicPz777IQ6iSUlNk) | Community spreadsheet of malware, IR and hunting tools. Many old links were updated in this repo. | free |
| [Malware-IR-Tools-Resources](https://github.com/sanjaynitttr/Malware-IR-Tools-Resources) | Malware, IR, hunting and intelligence resources compiled as a spreadsheet. | free |
| [RazviOverflow/Malware_Resources](https://github.com/RazviOverflow/Malware_Resources) | Personal collection on malware analysis, exploitation and RE. | free |
| [Threat Taming Tools Collection (T3C)](https://act.globalcyberalliance.org/index.php?title=Threat_Taming_Tools_Collection_(T3C)) | ~300 Global Cyber Alliance resources: feeds, tools, frameworks. | free |

## Malware analysis

Triage, reverse engineering and deobfuscation tools.

| Resource | What it is for | Access |
|---|---|---|
| [Binary Ninja](https://binary.ninja/) | Modern RE platform with a great API; free version. | free |
| [capa](https://github.com/mandiant/capa) | Identifies binary capabilities and maps to ATT&CK and MBC. | free |
| [CyberChef](https://gchq.github.io/CyberChef/) | Swiss army knife to decode, decrypt and transform data. | free |
| [Detect It Easy](https://github.com/horsicq/Detect-It-Easy) | Identifies compilers, packers and protectors. | free |
| [dnSpyEx](https://github.com/dnSpyEx/dnSpy) | NET debugger and editor (maintained dnSpy fork). | free |
| [FLARE-VM](https://github.com/mandiant/flare-vm) | Installs a complete Windows VM for malware analysis. | free |
| [FLOSS](https://github.com/mandiant/flare-floss) | Automatically extracts obfuscated strings. | free |
| [Ghidra](https://ghidra-sre.org/) | NSA's free reverse engineering framework. | free |
| [IDA Free / IDA Pro](https://hex-rays.com/ida-free/) | The reference disassembler; limited free version. | free |
| [ILSpy](https://github.com/icsharpcode/ILSpy) | .NET decompiler. | free |
| [oletools](https://github.com/decalage2/oletools) | Office document and macro analysis. | free |
| [PDF tools (Didier Stevens)](https://blog.didierstevens.com/programs/pdf-tools/) | pdfid and pdf-parser for malicious PDFs. | free |
| [PE-bear](https://github.com/hasherezade/pe-bear) | Quick view of PE files, including malformed ones. | free |
| [pestudio](https://www.winitor.com/) | Static PE triage with indicators. | free |
| [ProcDOT](https://www.procdot.com/) | Turns Procmon and PCAP into a behavior graph. | free |
| [radare2 / Cutter](https://rada.re/n/) | Free command-line RE framework, with the Cutter GUI. | free |
| [REMnux](https://remnux.org/) | Linux distribution for malware analysis. | free |
| [Sysinternals Suite](https://learn.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite) | Process Monitor, Autoruns, Process Explorer and more. | free |
| [System Informer](https://github.com/winsiderss/systeminformer) | Process Hacker's successor. | free |
| [x64dbg](https://x64dbg.com/) | Free Windows debugger. | free |
| [XORSearch](https://blog.didierstevens.com/programs/xorsearch/) | Finds XOR-hidden data and similar. | free |
| [YARA-X](https://github.com/VirusTotal/yara-x) | Next-generation YARA in Rust; classic YARA is in maintenance. | free |
| [yarGen](https://github.com/Neo23x0/yarGen) | Generates draft YARA rules from samples. | free |
| [de4dot](https://github.com/de4dot/de4dot) | .NET deobfuscator; archived, still useful on older samples. | free · legacy |
| [OllyDbg](http://www.ollydbg.de/) | Classic 32-bit debugger; replaced by x64dbg. | free · legacy |
| [PEiD](https://www.aldeid.com/wiki/PEiD) | Historic packer identifier; use Detect It Easy. | free · legacy |

## Sandboxes

Controlled detonation, online and on-premises.

| Resource | What it is for | Access |
|---|---|---|
| [ANY.RUN](https://any.run/) | Interactive online sandbox. | freemium |
| [Assemblyline](https://github.com/CybercentreCanada/assemblyline) | Large-scale triage by the Canadian Centre for Cyber Security. | free |
| [CAPEv2](https://github.com/kevoreilly/CAPEv2) | Free sandbox with config extraction; practical Cuckoo successor. | free |
| [Hatching Triage](https://tria.ge/) | Online sandbox with family config extraction. | sign-up |
| [Hybrid Analysis](https://www.hybrid-analysis.com/) | CrowdStrike's free online sandbox. | sign-up |
| [Joe Sandbox](https://www.joesandbox.com/) | Commercial sandbox with a basic public version. | freemium |
| [urlscan.io](https://urlscan.io/) | URL and page analysis. | freemium |
| [VirusTotal](https://www.virustotal.com/) | Multi-engine scanning and intelligence pivots. | freemium |
| [Cuckoo Sandbox](https://github.com/cuckoosandbox/cuckoo) | Historic sandbox; unmaintained. Use CAPEv2. | free · legacy |

## Samples (caution)

Real malware archives. Isolated lab only.

> ⚠️ **Live malware.** Download and open only in an isolated lab (VM with no network or simulated network). Never on your work machine.

| Resource | What it is for | Access |
|---|---|---|
| [APTMalware (cyber-research)](https://github.com/cyber-research/APTMalware) | ~3.5k APT-attributed samples used in academic research. | free |
| [MalShare](https://malshare.com/) | Community sample repository. | sign-up |
| [Malware-Traffic-Analysis.net](https://www.malware-traffic-analysis.net/) | Malicious traffic PCAPs and exercises. | free |
| [MalwareBazaar](https://bazaar.abuse.ch/) | Recent samples by hash, tag and family. | free |
| [theZoo](https://github.com/ytisf/theZoo) | Historic samples for study. | free |
| [VirusShare](https://virusshare.com/) | Large research sample archive. | sign-up |
| [vx-underground samples](https://vx-underground.org/) | Massive sample archive organized by family and APT, plus the malware paper collection. | free |

## DFIR and memory

Incident response, disk and memory forensics.

| Resource | What it is for | Access |
|---|---|---|
| [Autopsy](https://www.autopsy.com/) | Disk forensics with a GUI. | free |
| [bulk_extractor](https://github.com/simsong/bulk_extractor) | Artifact extraction from disk images. | free |
| [Chainsaw](https://github.com/WithSecureLabs/chainsaw) | Fast EVTX hunting with Sigma rules. | free |
| [Eric Zimmerman's tools](https://ericzimmerman.github.io/) | Windows artifact parsers used across DFIR. | free |
| [Hayabusa](https://github.com/Yamato-Security/hayabusa) | Windows log timeline and hunting. | free |
| [KAPE](https://www.kroll.com/en/services/cyber/incident-response-recovery/kroll-artifact-parser-and-extractor-kape) | Fast artifact collection and processing. | free |
| [LiME](https://github.com/504ensicsLabs/LiME) | Linux memory acquisition. | free |
| [RegRipper](https://github.com/keydet89/RegRipper3.0) | Windows registry analysis. | free |
| [Velociraptor](https://github.com/Velocidex/velociraptor) | Endpoint collection and hunting with VQL. | free |
| [Volatility 3](https://github.com/volatilityfoundation/volatility3) | Memory forensics. | free |
| [Rekall](https://github.com/google/rekall) | Archived memory framework. | free · legacy |

## Detection and hunting

Rules, hunting lists and data to test detections.

| Resource | What it is for | Access |
|---|---|---|
| [EVTX-ATTACK-SAMPLES](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES) | Windows event logs per attack technique, to test detections. | free |
| [HEARTH](https://github.com/THORCollective/HEARTH) | Community repository of hunting hypotheses. | free |
| [osquery](https://osquery.io/) | SQL-queryable endpoint. | free |
| [Security Datasets (OTRF)](https://github.com/OTRF/Security-Datasets) | Simulation data for detection research. | free |
| [Sigma](https://github.com/SigmaHQ/sigma) | Standard detection rule format, convertible to SIEMs. | free |
| [Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) | Detailed process, network and file telemetry on Windows. | free |
| [The ThreatHunting Project](https://www.threathunting.net/) | Introduction and hunt catalog. | free |

## Emulation and validation

Test your defenses with real actor behavior.

| Resource | What it is for | Access |
|---|---|---|
| [Adversary Emulation Library (CTID)](https://github.com/center-for-threat-informed-defense/adversary_emulation_library) | Emulation plans for real actors (APT29, FIN6, menuPass and others). | free |
| [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) | Small per-technique ATT&CK tests to validate detections. | free |
| [MITRE Caldera](https://github.com/mitre/caldera) | Automated adversary emulation. | free |

## Research datasets

Structured data for studies and models.

| Resource | What it is for | Access |
|---|---|---|
| ★ [Gulbay (2024): DEVIL / APT reports graph dataset (Zenodo)](https://zenodo.org/records/12741055) | Deduplicated APT reports, extracted IOCs and a Neo4j graph for strategic CTI (Gulbay, 2024, CC BY 4.0). | free |
| [APT simulation datasets (skrghosh)](https://github.com/skrghosh/apt-dataset) | Caldera simulation logs of APT29, FIN6, menuPass, OilRig and Wizard Spider, plus families like Redline and AsyncRAT. | free |
| [APTmap JSON](https://github.com/andreacristaldi/APTmap) | Group data and 29 GB of attributed sample features (CC BY 4.0). | free |

## Academic research

Papers and research tools on CTI and modeling.

| Resource | What it is for | Access |
|---|---|---|
| [Intel TARA / Threat Agent Library](https://www.oasis-open.org/committees/download.php/66239/Intel%20Corp_Threat%20Agent%20Library_07-2202w.pdf) | Threat agent library for risk assessment. | free |
| [MITRE: Cyber Threat Modeling: Survey, Assessment, and Representative Framework](https://www.mitre.org/sites/default/files/2021-11/prs-18-1174-ngci-cyber-threat-modeling.pdf) | Review of threat modeling frameworks. | free |
| [ThreatCompass (Univ. Twente)](https://research.utwente.nl/en/publications/threatcompass-a-tool-for-identifying-and-mapping-security-issues/) | Research tool that identifies security issues and maps them to TTPs with an attack graph. | free |

## Learn: courses, books and challenges

Free and paid paths, books and reverse engineering CTFs.

| Resource | What it is for | Access |
|---|---|---|
| [begin.re](https://www.begin.re/) | RE for beginners. | free |
| [challenges.re](https://challenges.re/) | RE exercises by architecture. | free |
| [crackmes.one](https://crackmes.one/) | Community RE challenges. | free |
| [FLARE-On](https://flare-on.com/) | Annual Google/Mandiant RE challenge; solutions published. | free |
| [Livro: Evasive Malware](https://nostarch.com/evasive-malware) | Kyle Cucci (2024): evasion techniques and how to analyze them. | paid |
| [Livro: Practical Malware Analysis](https://nostarch.com/malware) | Sikorski and Honig. The classic. | paid |
| [Livro: The Art of Memory Forensics](https://www.wiley.com/en-us/The+Art+of+Memory+Forensics-p-9781118825099) | Ligh, Case, Levy and Walters. | paid |
| [Livro: Windows Internals](https://learn.microsoft.com/en-us/sysinternals/resources/windows-internals) | Foundation for understanding what malware abuses in Windows. | paid |
| [Malware Unicorn RE101](https://malwareunicorn.org/workshops/re101.html) | Introductory reverse engineering workshop. | free |
| [MalwareTech challenges](https://www.malwaretech.com/beginner-malware-reversing-challenges) | Beginner reversing challenges. | free |
| [OpenSecurityTraining2](https://ost2.fyi/) | Free x86, RE and firmware courses (OpenSecurityTraining's successor). | free |
| [Practical Malware Analysis labs](https://github.com/mikesiko/PracticalMalwareAnalysis-Labs) | Labs for the classic book. | free |
| [Reverse Engineering for Beginners (Yurichev)](https://beginners.re/) | Free reverse engineering book. | free |
| [RPISEC Malware](https://github.com/RPISEC/Malware) | Open university malware analysis course. | free |
| [SANS FOR578](https://www.sans.org/cyber-security-courses/cyber-threat-intelligence/) | Reference CTI course. | paid |
| [SANS FOR610](https://www.sans.org/cyber-security-courses/reverse-engineering-malware-malware-analysis-tools-techniques/) | Reference malware reverse engineering course. | paid |

## Channels and people

Who teaches malware analysis on video.

| Resource | What it is for | Access |
|---|---|---|
| [hasherezade](https://www.youtube.com/@hasherezade) | Video channel on malware analysis and reverse engineering. | free |
| [John Hammond](https://www.youtube.com/@_JohnHammond) | Video channel on malware analysis and reverse engineering. | free |
| [LiveOverflow](https://www.youtube.com/@LiveOverflow) | Video channel on malware analysis and reverse engineering. | free |
| [MalwareAnalysisForHedgehogs](https://www.youtube.com/@MalwareAnalysisForHedgehogs) | Video channel on malware analysis and reverse engineering. | free |
| [MalwareTech](https://www.youtube.com/@MalwareTechBlog) | Video channel on malware analysis and reverse engineering. | free |
| [OALabs](https://www.youtube.com/@OALABS) | Video channel on malware analysis and reverse engineering. | free |
