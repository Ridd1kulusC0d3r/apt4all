# ◆ APT4ALL learning path: from a group's name to a dossier

Português: [README.md](README.md)

Nine modules for anyone who wants to do real CTI on APT and malware, on the defensive side. Each module has **one** "do this now" action using the Atlas, a deliverable and a check. Do one per session; you don't need to read everything before starting.

| # | Module | Time | Deliverable |
|---|---|---|---|
| 1 | [One group, ten names](#module-1--one-group-ten-names) | 45 min | Name table for 3 actors |
| 2 | [Reading a report without getting lost](#module-2--reading-a-report-without-getting-lost) | 1 h | Completed report sheet |
| 3 | [Pyramid of Pain and Diamond Model](#module-3--pyramid-of-pain-and-diamond-model) | 1 h | Diamond for one actor |
| 4 | [Mapping to ATT&CK](#module-4--mapping-to-attck) | 1 h 30 | Navigator layer with 8 justified techniques |
| 5 | [Attribution with method](#module-5--attribution-with-method) | 1 h | ACH matrix with 3 hypotheses |
| 6 | [Your organization's threat profile](#module-6--your-organizations-threat-profile) | 1 h | Country + sector profile with top 10 techniques |
| 7 | [From profile to defense](#module-7--from-profile-to-defense) | 2 h | Coverage table for 5 techniques |
| 8 | [Safe triage of APT malware](#module-8--safe-triage-of-apt-malware) | 1 h | Triage record for a public hash |
| 9 | [Final project: actor dossier](#module-9--final-project-actor-dossier) | 3 h | Dossier on the template, ready to publish |

Templates to copy: [`modelos/`](modelos/) (headings in Portuguese and English).

---

## Module 1 · One group, ten names

**Why it matters.** Each vendor names the same group its own way: Microsoft uses weather (Forest Blizzard), CrowdStrike uses animals by country (Fancy Bear), Mandiant uses numbers (APT28) plus prefixes for unattributed clusters (UNC, FIN), and ATT&CK uses IDs (G0007). If you don't master this, you'll read two reports on one group and think they're two groups.

**Read (pick one):**
- [MITRE ATT&CK Groups](https://attack.mitre.org/groups/)
- [CrowdStrike and Microsoft: name mapping](https://www.crowdstrike.com/en-us/blog/crowdstrike-and-microsoft-unite-to-deconflict-cyber-threat-attribution/)
- [apt.threattracking.com](https://apt.threattracking.com/)

**Do this now.** In the Atlas, open the cards for `APT28`, `Lazarus Group` and `OilRig`. For each one, use the **Names by vendor** section to note the Microsoft, CrowdStrike and Mandiant names and the ATT&CK ID. Missing one? Look under **Known names** or on apt.threattracking.com.

**Deliverable.** A table with 3 rows and 5 columns (common name, Microsoft, CrowdStrike, Mandiant, ATT&CK).

**Check.** Can you explain why "Lazarus" sometimes includes Andariel and BlueNoroff and sometimes doesn't? (Hint: it's an umbrella, and each vendor slices it differently.)

## Module 2 · Reading a report without getting lost

**Why it matters.** Threat reports mix observed fact, inference and marketing. The analyst separates the three and records the confidence of each claim.

**Read:**
- [ICD 203: Analytic Standards](https://www.dni.gov/files/documents/ICD/ICD-203.pdf) (probability and confidence language)
- [mthcht/ThreatIntel-Reports](https://github.com/mthcht/ThreatIntel-Reports) (archive to practice on)

**Do this now.** On the `APT29` card in the Atlas, scroll to **Reports (APTnotes)** and open one. Fill in the [report sheet](modelos/ficha-relatorio.md).

**Deliverable.** A sheet with: publisher, date, victimology, described behaviors, cited indicators, stated confidence and what is inference.

**Check.** Did you mark at least one sentence as "vendor inference" rather than fact?

## Module 3 · Pyramid of Pain and Diamond Model

**Why it matters.** The Pyramid of Pain shows that blocking a hash is easy for you and trivial for the adversary to bypass; going after behavior (TTPs) is costly for them. The Diamond Model organizes any event into adversary, capability, infrastructure and victim.

**Read:**
- [The Pyramid of Pain (David Bianco)](https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html)
- [The Diamond Model of Intrusion Analysis](https://www.activeresponse.org/wp-content/uploads/2013/07/diamond.pdf)

**Do this now.** Using the module 2 sheet, draw the diamond: one vertex per quadrant, with what the report says.

**Deliverable.** A completed diamond (hand-drawn is fine; a photo counts).

**Check.** Is any vertex empty? That's an intelligence gap: write it down as a question for the next report.

## Module 4 · Mapping to ATT&CK

**Why it matters.** ATT&CK is the common language between CTI, detection and red teams. Good mapping describes the **observed behavior** with the right technique, without inventing what the report doesn't say.

**Read:**
- [Top ATT&CK Techniques (CTID)](https://top-attack-techniques.mitre-engenuity.org/)
- [CISA Decider](https://github.com/cisagov/Decider) (helps you choose a technique by answering questions)
- [TRAM (CTID)](https://github.com/center-for-threat-informed-defense/tram) (assisted text mapping)

**Do this now.** Take 8 behavior sentences from your sheet and map each to a technique in the [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/). Compare with the techniques on the actor's Atlas card.

**Deliverable.** An exported Navigator layer, with a comment on each technique quoting the report sentence.

**Check.** Is one of your techniques missing from the Atlas card? Either the report is new or the mapping was a stretch. Decide which.

## Module 5 · Attribution with method

**Why it matters.** A wrong attribution sinks the whole team's credibility. Richards Heuer's Analysis of Competing Hypotheses (ACH) forces you to look for evidence that **disproves** hypotheses, not just evidence that confirms your favorite. False flags exist and have been publicly documented.

**Read:**
- [Psychology of Intelligence Analysis (Heuer), ch. 8](https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/)
- The attribution note in [SOURCES.md](../SOURCES.md)

**Do this now.** Build the [ACH matrix](modelos/matriz-ach.md) with three hypotheses for the module 2 report: the named actor, another actor from the same country, and "another actor imitating".

**Deliverable.** A matrix with at least 6 pieces of evidence marked consistent, inconsistent or neutral.

**Check.** The winning hypothesis is the one with the **fewest inconsistencies**, not the one with the most points in favor. Does yours hold?

## Module 6 · Your organization's threat profile

**Why it matters.** Nobody defends against 1,355 actors. A threat profile narrows it to who has attacked organizations like yours and which techniques they use. It's the first priority filter.

**Read:**
- [Tidal: Ultimate Guide to Cyber Threat Profiling](https://www.tidalcyber.com/ultimate-guide-to-cyber-threat-profiling)
- [CTID: Threat Modeling with ATT&CK](https://center-for-threat-informed-defense.github.io/threat-modeling-with-attack/)

**Do this now.** In the Atlas, **Threat profile** tab, choose your organization's country and sector (or a fictional one). Download the Navigator layer.

**Deliverable.** The 10 most relevant actors and the 10 techniques to cover first, plus one sentence on the profile's limits (e.g., "little public victimology for Brazil").

**Check.** Can you tell a manager, in two sentences, why these 10 techniques and not others?

## Module 7 · From profile to defense

**Why it matters.** A profile without coverage is just a report. Here you cross the priority techniques with what your environment can **see** (telemetry), **stop** (controls) and **validate** (tests). No ready-made rule library: the goal is to find the hole.

**Read:**
- [Mappings Explorer (CTID)](https://center-for-threat-informed-defense.github.io/mappings-explorer/) and [ControlCompass](https://controlcompass.github.io/) (control ↔ technique)
- [MITRE D3FEND](https://d3fend.mitre.org/) (countermeasures per technique)
- [Sigma](https://github.com/SigmaHQ/sigma) (open detection format, to learn how rules are structured)
- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) (validation tests; authorized environments only)

**Do this now.** Copy the [coverage table](modelos/cobertura.md) and fill it in for the top 5 techniques in your profile: do I have the telemetry? a mapped control? have I validated it?

**Deliverable.** A coverage table with 5 rows and one decision per row (keep, investigate, buy, configure).

**Check.** Did the technique with the most "no" answers become the first action on the list? To go further, take the profile into [TCE](../tce/README.en.md), which does this crossing for the whole environment.

## Module 8 · Safe triage of APT malware

**Why it matters.** APT CTI touches real malware. Safe triage is process-level: look up, record and decide, without opening any file outside an isolated lab.

**Read:**
- The **Samples** section of the [Resources](https://ridd1kulusc0d3r.github.io/apt4all/recursos/) (with warning)
- [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/actors) (families by actor)
- [FIRST TLP 2.0](https://www.first.org/tlp/) (how to share)

**Do this now.** Pick a SHA-256 hash cited in a public report about your actor. Look up only the hash (do not download the file) on VirusTotal or MalwareBazaar and fill in the [triage record](modelos/registro-triagem.md).

**Deliverable.** A record with: hash, where the hash came from, indicated family, first seen, consistency with the report, TLP applied and decision (archive, escalate to lab, discard).

**Check.** Did the file ever leave the service for your machine? If so, go back and redo it: the exercise is lookup only.

## Module 9 · Final project: actor dossier

**Why it matters.** The dossier brings everything together: names, attribution with confidence, victimology, behaviors, impact on your organization and recommendations. It's what an analyst hands to decision-makers.

**Do this now.** Copy the [dossier template](modelos/dossie-ator.md) and choose **one** actor from your profile (module 6). Fill in one section per session if you like.

**Deliverable.** A dossier with a 3-line BLUF, a name table, an attribution assessment with confidence level, top techniques with coverage (module 7), recommendations and sources.

**Check.** Can a manager read only the BLUF and know what to do? Can an analyst read the sources and reproduce your conclusions?

Want to publish it? Open a PR adding the dossier under `trilha/dossies/` (see [CONTRIBUTING.en.md](../CONTRIBUTING.en.md)).
