# Campaigns: from sources to defensive hypotheses

[Open the campaign notebook](https://ridd1kulusc0d3r.github.io/apt4all/campanhas/) · [Português](README.md) · [Editorial dataset](../dados/campanhas/cybermonitor.json)

CyberMonitor was already listed in APT4ALL resources. This integration adds six reviewed reports and an analytical workflow: primary source → observation → telemetry → hunting hypothesis → gaps → validation plan. It complements Atlas profiles without changing alias resolution or threat scores.

## Initial selection

| Case | Publisher / original date | Existing profile | Learning objective |
|---|---|---|---|
| APT41 / DUST | Mandiant / 2024-07-18 | APT41 · G0096 | Correlate server, database and outbound traffic events |
| Volt Typhoon | Microsoft / 2023-05-24 | Volt Typhoon · G1017 | Distinguish authorized administration from suspicious sequences |
| FoggyWeb | Microsoft / 2021-09-27 | APT29 · G0016; source label: NOBELIUM | Assess federation server visibility |
| Turla / Crutch | ESET / 2020-12-02 | Turla · G0010 | Investigate unusual external storage use |
| Machete | ESET / 2019-08-05 | Machete · G0095 | Build a regional email-to-endpoint investigation timeline |
| Operation Spalax | ESET / 2021-01-12 | No attributed Atlas actor | Investigate a campaign without turning shared malware into actor identity |

Primary report links, source section locators and immutable archive references are available in every notebook entry. Technique IDs are APT4ALL editorial mappings, not validated detection coverage. NOBELIUM links to the existing APT29 profile using the [ATT&CK association](https://attack.mitre.org/groups/G0016/); associated names do not establish universal identity equivalence.

## Workflow

1. Select a case relevant to your environment. Filter by text, region or publication year.
2. Read the primary report. Separate its observations from your interpretation.
3. Check actual SIEM/EDR events and fields. Missing collection is a gap.
4. Define a hypothesis, time window and entities to correlate.
5. Test synthetic positive events and benign controls. Record results, false positives and backend versions.
6. Develop the appropriate Sigma, KQL, SPL or Wazuh rule only after checking telemetry. Successful syntax conversion alone does not establish detection effectiveness.

Use the [report worksheet](../trilha/modelos/ficha-relatorio.md), [coverage worksheet](../trilha/modelos/cobertura.md), [triage log](../trilha/modelos/registro-triagem.md) and [TCE bridge](../tce/README.en.md).

## Supplied HTML review

The attachment `APT_Intelligence_Hub.html` informed the telemetry, hypothesis, gaps and validation fields. Its SHA-256 is recorded in the manifest. Its embedded actor database and generic IR tool catalog were not duplicated. Its 19 rules were not imported as validated detections: reproducible tests were absent and 17 lacked a `references` field.

Two semantic examples: the supplied password-spray rule selects failed logins, while distinct-user aggregation lives in separate queries; the Outlook rule mentions WebDAV but selects only ports 445 and 139. These require behavioral review as well as syntax checks.

## Provenance and limitations

- Discovery archive: [CyberMonitor](https://github.com/CyberMonitor/APT_CyberCriminal_Campagin_Collections), commit `cbf136e24f5d2a4d89619580455aae8b9b0aeadb` dated 2024-07-25. This is historical material, not a current-activity feed.
- Original publication, archive directory, index publication and editorial review dates remain separate. APT41/DUST shows 2024-07-18 at the publisher and 2024-07-19 in the archive. Review on 2026-11-09 does not imply campaign activity that day.
- Declared SHA-1 document hashes and Git blob hashes are distinct. PDF bytes were not downloaded to verify them.
- No repository-wide license was found at the collection root. APT4ALL publishes selected metadata, references and original summaries. Third-party documents retain their rights at their sources; PDFs, malware samples, offensive code and IOC lists were not mirrored.
- APTnotes cross-references use normalized URLs or declared SHA-1. Matches are recorded without duplicating actor evidence. A missing exact match does not prove a report is new.
- Primary reports were consulted; detection hypotheses were not tested in a SIEM. Historical attribution does not attribute a present-day alert.
- Machete and Spalax are Latin American study cases, not claims of Brazilian operator origin.

## Maintenance

Edit `dados/campanhas/cybermonitor.json`, then run:

```bash
python3 ferramentas/campanhas/gerar_catalogo.py
python3 ferramentas/site/mastro.py
python3 ferramentas/site/gerar_paginas.py
python3 -m unittest discover -s testes -p 'test_campanhas.py' -v
```

The weekly workflow rebuilds the reviewed selection without automatically importing campaigns. Invalid actor links and missing technique IDs fail the build. Execution dates never refresh editorial review dates.
