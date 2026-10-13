# TCE analysis and the APT4ALL bridge

Português: [ANALISE-TCE.md](ANALISE-TCE.md)

Analysis of [Cyber-Threat-Context-Modeling](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling) (Threat Context Engineering, v0.5 "Horizon"), done on 2026-10-13 against the public code. Starting question: **what does TCE still need to map the possible attack scenarios across the whole enterprise and prioritize protection predictively and preemptively, based on threat intelligence?**

## 1. What TCE already solves

Short answer: the architecture for this already exists. TCE is not application threat modeling; it starts from mission and crown jewels and ends at telemetry, detection and validation.

| Capability | Where | State |
|---|---|---|
| 13-stage pipeline from mission to traceable decision | `docs/methodology.md`, `src/tce/` | Mature |
| Whole-enterprise environment (assets, identities, SaaS, cloud, OT, AI agents) | `environment-state.schema.json`, `horizon.py` | Mature |
| Candidate paths to crown jewels, scored as "forecast pressure" | `horizon.py` | Mature |
| Risk-weighted choke points | `weighted_choke_points` | Mature |
| Detection by absence: what must be observable and is not | `detection_by_absence`, `docs/detection-by-absence.md` | Mature |
| Proposed preemptive actions, always human-reviewed | `propose_preemptive_actions` | Mature |
| KEV and EPSS as vulnerability pressure | `_vulnerability_pressure` | Mature |
| Intelligence signals with half-life, reliability and credibility | `_intelligence_pressure` | Mature, but few sources |
| STIX 2.1, Attack Flow, Navigator, OpenCTI, TAXII, D3FEND | `src/tce/standards/` | Mature |
| AI with immutable evidence packets and a candidate queue | `src/tce/ai/` | Mature |
| Six executable reference cases | `examples/reference-cases/` | Mature |

What sets TCE apart: **nothing generated becomes fact on its own**. Signals, paths and actions are candidates and only count after an analyst accepts them. The APT4ALL bridge follows that rule.

## 2. Where the gap is

Horizon's forecast pressure has seven dimensions. Six are fed by the environment's own data. The seventh, **intelligence pressure (15%)**, depends on signals that today arrive by hand, by CSV, or from RedFrameworks packs. There is no systematic layer answering **"who usually attacks organizations like mine, and with which techniques?"**. Without it, the "intelligence-based" part of the forecast is weak.

| Gap | Effect today | What fills it |
|---|---|---|
| Adversary profile by country and sector | Low or manual intelligence pressure | **APT4ALL bridge** (ready, below) |
| Control coverage per technique | Residual control weakness entered by hand | ControlCompass and CTID Mappings Explorer |
| Weight calibration | Expert-set weights, no empirical validation | Back-testing protocol (section 5) |
| Validation against emulation | Manual validation objects | Atomic Red Team, Adversary Emulation Library, skrghosh simulation dataset |
| Actor activity recency | A 2012 actor weighs the same as one active in 2026 | APT4ALL report dates (APTnotes, ATT&CK) |
| Runtime prioritization | TCE decides what to detect but does not rank alerts | Anvilogic's idea: export the profile as a triage weight |
| Non-CVE issues (configuration, process) | Left out of vulnerability pressure | ThreatCompass approach: map security issues to TTPs |

## 3. The APT4ALL → Horizon bridge (ready and tested)

`ferramentas/tce/perfil_ameaca.py` builds a threat profile from historical victimology and exports:

- `navigator.json`: an ATT&CK Navigator layer with weighted techniques;
- `tce-sinais.json`: `intelligence_signals` candidates in TCE format (`status: candidate`, `review_required: true`);
- `tce-intelligence.csv`: the same signal in `tce environment-import-csv` format;
- `perfil.md`: a readable report with the actors and why each was included.

The Atlas does the same in the browser, in the **Threat profile** tab, with download buttons.

```bash
python3 ferramentas/tce/perfil_ameaca.py --pais "United States" --setor government --saida out/us-gov
# in TCE: review the signal, set status to accepted, add it to environment_state.intelligence_signals
tce horizon-assess examples/cases/enterprise-identity --offline
```

**Test result on the `enterprise-identity` reference case:**

| Situation | Top path score | Intelligence pressure | Band |
|---|---|---|---|
| No APT4ALL signal | 64.7 | 0.2455 | H2 |
| Signal as `candidate` | 64.7 | 0.2455 | H2 (ignored, as it should be) |
| Signal `accepted` (US, government, 153 actors, 60 techniques) | 65.4 | 0.2874 | **H1** |

The candidate signal changed nothing: the review gate worked. Once accepted, intelligence pressure rose 17% and the path moved from H2 to H1. That is the expected behavior: intelligence adjusts priority without dominating the other six dimensions.

**Bridge limits.** Victimology comes from MISP Galaxy and the spreadsheet, which cover the US, Europe and Asia well and Brazil poorly (only 10 actors with recorded Brazilian victims, counting the sheet's target text). For Brazil, the profile must be complemented with local sources (CERT.br, reports from banks and vendors operating in the country). That is why the signal ships with `confidence: low` and `source_reliability: C`.

## 4. Materials with academic value

| Material | Academic value | Use in TCE |
|---|---|---|
| [Gulbay (2024), Zenodo 12741055](https://zenodo.org/records/12741055) | **High.** Deduplicated APT reports, extracted IOCs and a Neo4j graph, with code, CC BY 4.0 | Actor→technique prevalence priors; back-testing base |
| [skrghosh/apt-dataset](https://github.com/skrghosh/apt-dataset) | **High.** Labeled Caldera simulation logs (APT29, FIN6, menuPass, OilRig, Wizard Spider) | Ground truth to test detection by absence |
| [ThreatCompass (Univ. of Twente)](https://research.utwente.nl/en/publications/threatcompass-a-tool-for-identifying-and-mapping-security-issues/) | **High** as related work: maps security issues to TTPs | Extend vulnerability pressure beyond CVEs |
| [ThreatForest (AWS)](https://aws-samples.github.io/samples-agentic-attack-tree-generator/) | Medium: baseline for agent-generated attack trees | Compare with Horizon paths; candidate-only |
| MITRE: *Cyber Threat Modeling: Survey, Assessment, and Representative Framework* and *Enterprise Threat Model Technical Report* (in the Tidal guide) | High as foundation | Base citations for the method chapter |
| [Tidal threat profiling guide](https://www.tidalcyber.com/ultimate-guide-to-cyber-threat-profiling) and Intel TARA | Medium: organizational profiling method | Justifies country and sector profiling |
| [CFR Cyber Operations Tracker](https://www.cfr.org/cyber-operations/) and EuRepoC | High as ground truth for dated state incidents with victim and sector | Temporal back-testing |
| [ControlCompass](https://controlcompass.github.io/) and CTID Mappings Explorer | Medium: reproducible control↔technique mapping | Compute control weakness automatically |
| [APTmap](https://github.com/andreacristaldi/APTmap) (CC BY 4.0) and Categorized-Adversary-TTPs | Medium: group and sector attributes; the latter is dated | Enrichment and comparison |
| APTnotes and CyberMonitor | Medium: raw corpus, needs deduplication (Gulbay did it) | Activity recency |
| SOCRadar, Anvilogic, awesome lists | Low for research (commercial or secondary) | Product inspiration |

## 5. Research proposal: does Horizon predict?

Horizon rightly says it measures "defensive attention", not probability. How often that attention is right can be tested, and it is publishable:

1. **Freeze time.** For each year *t*, build the APT4ALL threat profile using only reports and attributions published up to *t*.
2. **Predict.** Rank ATT&CK techniques per sector with the year-*t* profile.
3. **Compare.** Measure how many techniques seen in that sector's incidents in year *t+1* (CFR, EuRepoC, dated reports) were at the top of the ranking: precision@k and recall@k.
4. **Calibrate.** Tune the intelligence pressure weight (15% today) and signal half-life (30 to 90 days today) to maximize hits, and report the gain over a naive baseline (most common ATT&CK techniques, no profile).
5. **Validate absence.** Use skrghosh's labeled logs to measure how many techniques flagged as "no telemetry" by detection by absence would actually go unnoticed.

Item 5 maps directly to the "Detection by Absence" theme: an experiment with labeled ground truth, reproducible, on open data.

## 6. Suggested roadmap (TCE v0.6 "Horizon Intel")

| Order | Deliverable | Effort |
|---|---|---|
| 1 | Document the `apt4all-threat-profile` signal format in `horizon-intel-candidates` (already compatible) | Low |
| 2 | ControlCompass and Mappings Explorer importer for the Horizon control catalog | Medium |
| 3 | Per-actor recency weight (last known activity) in the APT4ALL signal | Low |
| 4 | Back-testing harness with APT4ALL + CFR/EuRepoC, producing a precision@k report | Medium |
| 5 | Validation fixtures from the skrghosh dataset | Medium |
| 6 | Export the profile as an alert triage weight (SIEM/SOAR) | Medium |

## Sources

TCE repository (README, `docs/horizon.md`, `docs/detection-by-absence.md`, `src/tce/horizon.py`, `src/tce/horizon_intelligence.py`, `src/tce/environment_import.py`) and the materials in section 4.
