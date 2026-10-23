# AGENTS.md

## Verbindliche Grundlagen

- Fachliche Grundlage ist `docs/concept/IFC_Quantity_Agent_Entwicklungskonzept_v1.11.md`.
- MVP-1-Sollwerte liegen ausschließlich in `baseline/IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json`.
- Stabile Regeln liegen in `rules/mvp1_rules_v0.1.json`.
- API, CLI und spätere UI müssen dieselbe Core- und Regelengine verwenden.

## Unverhandelbare Fachprinzipien

- Keine fehlenden IFC-Werte erfinden oder still ergänzen.
- Native IFC-Klasse nicht mit `BIM_Core.IfcClass` überschreiben.
- Brutto-, Netto- und projektspezifische Mengenquellen getrennt halten.
- `NetVolume` nur aus nativen `Qto_*BaseQuantities` lesen.
- Reviewfälle niemals automatisch umklassifizieren.
- Jeder Befund bleibt über GlobalId, Regel-ID und Quelldaten nachvollziehbar.
- IFC-Dateien und sensible Projektdaten nicht committen.

## Entwicklungsregeln

- Python 3.12 und IfcOpenShell 0.8.4 sind die geprüfte Referenzumgebung.
- Änderungen an Collector, Regeln oder Baseline benötigen Regressionstests.
- Vor Übergabe ausführen:
  `python -m unittest discover -s tests -v`
- API-Vertrag nach API-Änderungen neu erzeugen:
  `python export_openapi.py`
- Regel-IDs werden nicht wiederverwendet. Fachliche Änderungen erhöhen die Regelversion.
- Generierte Laufberichte gehören nicht ins Repository.

