# Análise do TCE e ponte com o APT4ALL

English: [TCE-ANALYSIS.md](TCE-ANALYSIS.md)

Análise do repositório [Cyber-Threat-Context-Modeling](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling) (Threat Context Engineering, v0.5 "Horizon"), feita em 13/10/2026 sobre o código público. Pergunta de partida: **o que falta para o TCE mapear os cenários de ataque possíveis de toda a empresa e priorizar a proteção de forma preditiva e preemptiva, com base em inteligência de ameaças?**

## 1. O que o TCE já resolve

A resposta curta: a arquitetura para isso já existe. O TCE não é modelagem de aplicação; ele parte da missão e das joias da coroa e chega a telemetria, detecção e validação.

| Capacidade | Onde está | Estado |
|---|---|---|
| Pipeline de 13 etapas, da missão à decisão rastreável | `docs/methodology.md`, `src/tce/` | Maduro |
| Ambiente da empresa inteira (ativos, identidades, SaaS, nuvem, OT, agentes de IA) | `environment-state.schema.json`, `horizon.py` | Maduro |
| Caminhos candidatos até as joias da coroa, com pontuação de "pressão de previsão" | `horizon.py` | Maduro |
| Pontos de estrangulamento ponderados por risco | `weighted_choke_points` | Maduro |
| Detecção pela ausência: o que precisa ser observável e não é | `detection_by_absence`, `docs/detection-by-absence.md` | Maduro |
| Ações preemptivas propostas, sempre com revisão humana | `propose_preemptive_actions` | Maduro |
| KEV e EPSS como pressão de vulnerabilidade | `_vulnerability_pressure` | Maduro |
| Sinais de inteligência com meia-vida, confiabilidade e credibilidade | `_intelligence_pressure` | Maduro, mas com pouca fonte |
| STIX 2.1, Attack Flow, Navigator, OpenCTI, TAXII, D3FEND | `src/tce/standards/` | Maduro |
| IA com pacote de evidência imutável e fila de candidatos | `src/tce/ai/` | Maduro |
| Seis casos de referência executáveis | `examples/reference-cases/` | Maduro |

O ponto forte que diferencia o TCE da maioria das ferramentas: **nada gerado vira fato sozinho**. Sinais, caminhos e ações saem como candidatos e só pesam no cálculo depois de aceitos por um analista. A ponte com o APT4ALL respeita essa regra.

## 2. Onde está a lacuna

A pressão de previsão do Horizon tem sete dimensões. Seis delas são alimentadas por dados do próprio ambiente. A sétima, **pressão de inteligência (15%)**, depende de sinais que hoje chegam de três jeitos: à mão, por CSV, ou pelos pacotes do RedFrameworks. Falta uma camada sistemática que responda **"quem costuma atacar organizações como a minha, e com quais técnicas?"**. Sem ela, a parte "baseada em inteligência" da previsão fica fraca.

| Lacuna | Efeito hoje | O que preenche |
|---|---|---|
| Perfil de adversário por país e setor | Pressão de inteligência baixa ou manual | **Ponte APT4ALL** (pronta, abaixo) |
| Cobertura de controles por técnica | "Fraqueza de controle residual" informada à mão | ControlCompass e CTID Mappings Explorer |
| Calibração dos pesos | Pesos definidos por especialista, sem validação empírica | Protocolo de backtesting (seção 5) |
| Validação contra emulação | Objetos de validação manuais | Atomic Red Team, Adversary Emulation Library, dataset de simulações do skrghosh |
| Recência da atividade do ator | Um ator de 2012 pesa igual a um ativo em 2026 | Datas de relatórios do APT4ALL (APTnotes, ATT&CK) |
| Priorização em tempo de execução | O TCE decide o que detectar, mas não ordena alertas | Ideia do Anvilogic: exportar o perfil como peso de triagem |
| Problemas que não são CVE (configuração, processo) | Ficam fora da pressão de vulnerabilidade | Abordagem do ThreatCompass: mapear problema de segurança para TTP |

## 3. A ponte APT4ALL → Horizon (pronta e testada)

`ferramentas/tce/perfil_ameaca.py` monta um perfil de ameaça por vitimologia histórica e exporta:

- `navigator.json`: camada do ATT&CK Navigator com as técnicas ponderadas;
- `tce-sinais.json`: candidatos a `intelligence_signals` no formato do TCE (`status: candidate`, `review_required: true`);
- `tce-intelligence.csv`: o mesmo sinal no formato do `tce environment-import-csv`;
- `perfil.md`: relatório legível com os atores e o motivo de cada um.

O Atlas faz o mesmo no navegador, na aba **Perfil de ameaça**, com botões para baixar a camada e os sinais.

```bash
python3 ferramentas/tce/perfil_ameaca.py --pais "United States" --setor government --saida saida/us-gov
# no TCE: revisar o sinal, mudar status para accepted e incluir em environment_state.intelligence_signals
tce horizon-assess examples/cases/enterprise-identity --offline
```

**Resultado do teste com o caso de referência `enterprise-identity`:**

| Situação | Pontuação do 1º caminho | Pressão de inteligência | Faixa |
|---|---|---|---|
| Sem sinal do APT4ALL | 64,7 | 0,2455 | H2 |
| Sinal como `candidate` | 64,7 | 0,2455 | H2 (ignorado, como deve ser) |
| Sinal `accepted` (EUA, governo, 153 atores, 60 técnicas) | 65,4 | 0,2874 | **H1** |

O sinal candidato não mudou nada: a trava de revisão funcionou. Depois de aceito, a pressão de inteligência subiu 17% e o caminho passou de H2 para H1. É o comportamento esperado: a inteligência ajusta a prioridade, mas não domina as outras seis dimensões.

**Limites da ponte.** A vitimologia vem de MISP Galaxy e da planilha, que cobrem bem Estados Unidos, Europa e Ásia e mal o Brasil (só 7 atores com vítimas brasileiras registradas). Para o Brasil, o perfil precisa ser complementado com fontes locais (CERT.br, relatórios de bancos e fornecedores com operação no país). Por isso o sinal sai com `confidence: low` e `source_reliability: C`.

## 4. Materiais com valor acadêmico

Separei o que serve para pesquisa (com dado, método ou código reprodutível) do que é só referência operacional.

| Material | Valor acadêmico | Uso no TCE |
|---|---|---|
| [Gulbay (2024), Zenodo 12741055](https://zenodo.org/records/12741055) | **Alto.** Relatórios de APT deduplicados, IOCs extraídos e grafo Neo4j, com código, sob CC BY 4.0 | Prioris de prevalência ator→técnica; base para o backtesting |
| [skrghosh/apt-dataset](https://github.com/skrghosh/apt-dataset) | **Alto.** Logs rotulados de simulações no Caldera (APT29, FIN6, menuPass, OilRig, Wizard Spider) | Verdade de campo para testar a detecção pela ausência |
| [ThreatCompass (Univ. Twente)](https://research.utwente.nl/en/publications/threatcompass-a-tool-for-identifying-and-mapping-security-issues/) | **Alto** como trabalho relacionado: mapeia problemas de segurança para TTPs | Estender a pressão de vulnerabilidade para além de CVE |
| [ThreatForest (AWS)](https://aws-samples.github.io/samples-agentic-attack-tree-generator/) | Médio: linha de base de geração de árvores de ataque por agentes | Comparar com os caminhos do Horizon; entra só como candidato |
| MITRE: *Cyber Threat Modeling: Survey, Assessment, and Representative Framework* e *Enterprise Threat Model Technical Report* (no guia da Tidal) | Alto como fundamentação | Citação de base para o capítulo de método |
| [Tidal: guia de threat profiling](https://www.tidalcyber.com/ultimate-guide-to-cyber-threat-profiling) e TARA da Intel | Médio: método de perfilamento organizacional | Justifica o perfil por país e setor |
| [CFR Cyber Operations Tracker](https://www.cfr.org/cyber-operations/) e EuRepoC | Alto como verdade de campo de incidentes estatais com data, vítima e setor | Backtesting temporal |
| [ControlCompass](https://controlcompass.github.io/) e CTID Mappings Explorer | Médio: mapeamento controle↔técnica reprodutível | Calcular a fraqueza de controle automaticamente |
| [APTmap](https://github.com/andreacristaldi/APTmap) (CC BY 4.0) e Categorized-Adversary-TTPs | Médio: atributos de grupos e setores, este último desatualizado | Enriquecimento e comparação |
| APTnotes e CyberMonitor | Médio: corpus bruto, precisa de deduplicação (o Gulbay já fez) | Recência de atividade |
| SOCRadar, Anvilogic, listas awesome | Baixo para pesquisa (comercial ou secundário) | Inspiração de produto |

## 5. Proposta de pesquisa: o Horizon prevê?

Hoje o Horizon diz, com razão, que mede "atenção defensiva", não probabilidade. Dá para testar quanto essa atenção acerta, e isso é publicável:

1. **Congelar o tempo.** Para cada ano *t*, montar o perfil de ameaça (APT4ALL) usando só relatórios e atribuições publicados até *t*.
2. **Prever.** Ranquear as técnicas ATT&CK por setor com o perfil de *t*.
3. **Comparar.** Medir quantas das técnicas observadas em incidentes do setor no ano *t+1* (CFR, EuRepoC, relatórios datados) estavam no topo do ranking: precisão@k e recall@k.
4. **Calibrar.** Ajustar o peso da pressão de inteligência (hoje 15%) e a meia-vida dos sinais (hoje 30 a 90 dias) para maximizar o acerto, e reportar o ganho sobre uma linha de base ingênua (as técnicas mais comuns do ATT&CK, sem perfil).
5. **Validar a ausência.** Usar os logs rotulados do skrghosh para medir quantas técnicas marcadas como "sem telemetria" pela detecção pela ausência de fato passariam despercebidas.

O item 5 conversa diretamente com o tema de "Detecção pela Ausência": é um experimento com verdade de campo rotulada, reprodutível e com dados abertos.

## 6. Roteiro sugerido (TCE v0.6 "Horizon Intel")

| Ordem | Entrega | Esforço |
|---|---|---|
| 1 | Aceitar o formato `apt4all-threat-profile` no `horizon-intel-candidates` (já compatível; falta documentar) | Baixo |
| 2 | Importador de ControlCompass e Mappings Explorer para o catálogo de controles do Horizon | Médio |
| 3 | Peso de recência por ator (última atividade conhecida) no sinal do APT4ALL | Baixo |
| 4 | Harness de backtesting com APT4ALL + CFR/EuRepoC, gerando relatório de precisão@k | Médio |
| 5 | Fixtures de validação a partir do dataset do skrghosh | Médio |
| 6 | Exportar o perfil como peso de triagem de alertas (SIEM/SOAR) | Médio |

## Fontes

Repositório TCE (README, `docs/horizon.md`, `docs/detection-by-absence.md`, `src/tce/horizon.py`, `src/tce/horizon_intelligence.py`, `src/tce/environment_import.py`) e os materiais listados na seção 4.
