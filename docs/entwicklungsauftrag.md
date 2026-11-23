# IFC Quantity Agent – Entwicklungsauftrag

Fachliche Grundlage ist das [Entwicklungskonzept v1.12](concept/IFC_Quantity_Agent_Entwicklungskonzept_v1.12.md). Der [Projektstatus](../PROJECT_STATE.md) hält den Implementierungs- und Abnahmestand fest. [AGENTS.md](../AGENTS.md) definiert die verbindlichen Arbeitsregeln.

## Aktueller Meilenstein

MVP 1 mit UI v0.3.7 am freigegebenen Referenzmodell abschließen. Der [Testplan v0.3.7](acceptance/IFC_Quantity_Agent_MVP1_UI_v0.3.7_Testplan.md) führt durch Windows-Start, Modellstruktur, Objekt-Drilldown und Regression. Die Scrollkorrektur aus v0.3.6 ist bereits bestätigt. Der praktische Windows-Start, die Z445-Modellstruktur und die Gesamtfreigabe stehen laut Projektstatus aus.

Nach der Abnahme werden Folgearbeiten als einzelne Issues mit fachlichem Ziel, betroffenen Regeln und überprüfbaren Soll-Ergebnissen beauftragt. Die [Stahl- und Betonbau-Übergaben](handover/README.md) enthalten die Vorgaben für die späteren Kategorieprofile in MVP 3/4. Offene fachliche Festlegungen werden als Entscheidung dokumentiert, bevor daraus aktive Regeln entstehen.

## Reproduzierbare Prüfungen

Die Befehle laufen vom Repo-Stamm aus. Maßgeblich für die automatisierten Checks ist der [CI-Workflow](../.github/workflows/tests.yml). Windows-Zielbetrieb ist Python 3.14, die CI prüft zusätzlich Python 3.12. Die Laufzeitabhängigkeiten stehen in [requirements.txt](../requirements.txt).

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
node tests/test_object_details.cjs
node tests/test_structure_view.cjs
```

Bei Änderungen am API-Vertrag `python export_openapi.py` ausführen und den Diff des OpenAPI-Vertrags prüfen. Für UI-Änderungen die betroffenen Browserprüfungen aus dem CI-Job `object-layout` verwenden. Der Windows-Job prüft die nativen Imports und den Runtime-Startpfad.

### Fachlicher Referenzlauf

Aktuelle Referenz ist `Z445_799_ECA_BM-801-3D.ifc` (Referenz v0.2, SHA-256 `EA051785…C1BE`, fachlich freigegeben durch Tom am 23.11.2026). Grundlage sind die [Z445-ECA-Abnahmebasis v0.2](acceptance/IFC_Quantity_Agent_MVP1_Abnahmebasis_Z445_ECA_v0.2.md), die [JSON-Sollwerte v0.2](../baseline/IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.2.json) und das Regelpaket `rules/mvp1_rules_v0.2.json` (Standard in CLI, API und Service). Die Regeln `IQA-M1-ASM-001` und `IQA-M1-OPEN-001` sind an diesem Modell nicht prüfbar. Ein späterer Re-Export ist eine neue Referenz v0.3. Die Original-IFC liegt in der freigegebenen Projektumgebung und wird nie committet.

Die Dateien v0.1 (Abnahmebasis, Baseline, Regeln) bleiben für das ursprüngliche, nicht mehr auffindbare Modell erhalten und sind mit `--baseline` und `--rules` weiter nutzbar. Der Referenztest `tests/test_reference_model.py` wählt die Baseline anhand der SHA-256 des Modells.

```bash
export IFC_MVP1_REFERENCE_MODEL="/freigegebener/pfad/Z445_799_ECA_BM-801-3D.ifc"
python -m unittest discover -s tests -v
python run_regression.py --ifc "$IFC_MVP1_REFERENCE_MODEL" --output-dir reports
```

Für die MVP-1-Abnahme müssen die 32 Regeln gegen die vorgesehene Referenzrevision bestehen und die praktischen Prüfungen im Testplan bestätigt sein. Im Cloud-Lauf ohne Originalmodell übersprungene Referenzprüfungen im PR ausdrücklich ausweisen.

## GitHub Copilot einsetzen

Nach Aufnahme dieses Standes in den Default Branch und Freigabe des Repos in den GitHub-Richtlinien kann der Cloud Agent einen klar abgegrenzten Auftrag aus einem Issue übernehmen. Bei Ausführung auf GitHub Actions bereitet der [Setup-Workflow](../.github/workflows/copilot-setup-steps.yml) Python 3.14, die fixierten Python-Abhängigkeiten und Node.js 22 vor. Die vollständigen PR-Prüfungen laufen über den CI-Workflow.

Ein PR ist fachlich prüfbar, wenn er die Soll-Ergebnisse des Issues, die Regel- und Quellenbezüge und den Teststatus enthält. Mengen- oder Baseline-Änderungen und der Merge werden fachlich freigegeben.

## Laufende UI-Nachbesserung v0.3.8

Windows-Start und Modellstruktur in v0.3.7 sind vom Nutzer bestätigt. Die Auffindbarkeit wird mit v0.3.8 verbessert; siehe [Testplan v0.3.8](acceptance/IFC_Quantity_Agent_MVP1_UI_v0.3.8_Testplan.md). Baugruppen sind mit dem aktuellen Modell nicht prüfbar. Die Gesamtfreigabe bleibt offen.
