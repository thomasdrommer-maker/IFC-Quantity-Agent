# AGENTS.md

## Verbindliche Grundlagen

- Fachliche Grundlage ist `docs/concept/IFC_Quantity_Agent_Entwicklungskonzept_v1.12.md`.
- MVP-1-Sollwerte liegen ausschließlich in `baseline/IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json`.
- Stabile Regeln liegen in `rules/mvp1_rules_v0.1.json`.
- API, CLI und spätere UI müssen dieselbe Core- und Regelengine verwenden.

- Ergänzende Fachvorgaben: `docs/handover/README.md` und beide Fachkonzepte v0.2 einschließlich PR01–PR20. Kategoriegrenzen extern pflegen; Entwurfsprofile nicht automatisch aktivieren. Die Pakete sind noch nicht als Laufzeitregeln integriert.

## Unverhandelbare Fachprinzipien

- Keine fehlenden IFC-Werte erfinden oder still ergänzen.
- Native IFC-Klasse nicht mit `BIM_Core.IfcClass` überschreiben.
- Brutto-, Netto- und projektspezifische Mengenquellen getrennt halten.
- `NetVolume` nur aus nativen `Qto_*BaseQuantities` lesen.
- Reviewfälle niemals automatisch umklassifizieren.
- Jeder Befund bleibt über GlobalId, Regel-ID und Quelldaten nachvollziehbar.
- IFC-Dateien und sensible Projektdaten nicht committen.

## Entwicklungsregeln

- Python 3.14 mit IfcOpenShell 0.8.4.post1 ist die Windows-Zielumgebung. Python 3.12 bleibt als zweite CI-Referenz erhalten.
- Änderungen an Collector, Regeln oder Baseline benötigen Regressionstests.
- Vor Übergabe ausführen:
  `python -m unittest discover -s tests -v`
- API-Vertrag nach API-Änderungen neu erzeugen:
  `python export_openapi.py`
- Regel-IDs werden nicht wiederverwendet. Fachliche Änderungen erhöhen die Regelversion.
- Generierte Laufberichte gehören nicht ins Repository.


