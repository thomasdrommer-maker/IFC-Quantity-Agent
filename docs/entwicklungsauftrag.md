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

Die [Z445-ECA-Abnahmebasis](acceptance/IFC_Quantity_Agent_MVP1_Abnahmebasis_Z445_ECA_v0.1.md) und die [JSON-Sollwerte](../baseline/IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json) sind versioniert. Die Original-IFC liegt in der freigegebenen Projektumgebung. Dort den Referenzlauf mit dem unveränderten Dateinamen ausführen.

```bash
export IFC_MVP1_REFERENCE_MODEL="/freigegebener/pfad/Z445_799_ECA_BM_801_3D.ifc"
python -m unittest discover -s tests -v
python run_regression.py --ifc "$IFC_MVP1_REFERENCE_MODEL" --output-dir reports
```

Für die MVP-1-Abnahme müssen die 32 Regeln gegen die vorgesehene Referenzrevision bestehen und die praktischen Prüfungen im Testplan bestätigt sein. Im Cloud-Lauf ohne Originalmodell übersprungene Referenzprüfungen im PR ausdrücklich ausweisen.

## GitHub Copilot einsetzen

Nach Aufnahme dieses Standes in den Default Branch und Freigabe des Repos in den GitHub-Richtlinien kann der Cloud Agent einen klar abgegrenzten Auftrag aus einem Issue übernehmen. Bei Ausführung auf GitHub Actions bereitet der [Setup-Workflow](../.github/workflows/copilot-setup-steps.yml) Python 3.14, die fixierten Python-Abhängigkeiten und Node.js 22 vor. Die vollständigen PR-Prüfungen laufen über den CI-Workflow.

Ein PR ist fachlich prüfbar, wenn er die Soll-Ergebnisse des Issues, die Regel- und Quellenbezüge und den Teststatus enthält. Mengen- oder Baseline-Änderungen und der Merge werden fachlich freigegeben.
