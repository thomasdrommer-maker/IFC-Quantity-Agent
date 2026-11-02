# IFC Quantity Agent – MVP-1-Regressionspaket

Dieses Paket prüft das Referenzmodell `Z445_799_ECA_BM_801_3D.ifc` deterministisch gegen die freigegebene JSON-Baseline. Die implementierte MVP-1-Regression beruht auf dem Entwicklungskonzept v1.11 und der MVP-1-Abnahmebasis. Der aktuelle Gesamtauftrag ist v1.12; die darin ergänzten Kategorien und benutzerdefinierten Profile sind noch nicht implementiert.

## Aktuelle Entwicklungsgrundlagen

- [Verbindlicher Entwicklungsauftrag v1.12](docs/concept/IFC_Quantity_Agent_Entwicklungskonzept_v1.12.md)
- [Stahlbau- und Betonbau-Übergabepakete v0.2](docs/handover/README.md), einschließlich Excel/JSON, Original-ZIPs und Prüfvermerken
- [Projektstatus und nächste Schritte](PROJECT_STATE.md)

Die neuen Vorgaben umfassen benutzerdefinierte Kategorieprofile, besonders für Betonstützen, Betonwände und Stahlbleche. Sie sind Entwicklungsumfang für MVP 3/4; die laufende Anwendung bleibt MVP 1.

## Inhalt

- `rules/mvp1_rules_v0.1.json`: freigegebener Regelkatalog mit stabilen IDs
- `baseline/IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json`: Sollwerte
- `src/ifc_quantity_agent_mvp1/collector.py`: IFC-Inventuradapter
- `src/ifc_quantity_agent_mvp1/regression.py`: Regel- und Vergleichsengine
- `src/ifc_quantity_agent_mvp1/cli.py`: Kommandozeilenlauf mit JSON- und JUnit-Ausgabe
- `src/ifc_quantity_agent_mvp1/service.py`: plattformneutraler Application Service
- `src/ifc_quantity_agent_mvp1/api.py`: REST-/OpenAPI-Adapter
- `openapi/ifc_quantity_agent_mvp1_openapi_v1.json`: versionierter API-Vertrag
- `tests/`: Struktur-, Engine- und End-to-End-Tests

## Voraussetzungen

- Python 3.14 für die Windows-Zielumgebung; Python 3.12 wird zusätzlich in CI geprüft
- IfcOpenShell 0.8.4.post1

Installation:

```bash
python -m pip install -r requirements.txt
```

## Regression ausführen

Vom Paketverzeichnis aus:

```bash
python run_regression.py \
  --ifc /pfad/Z445_799_ECA_BM_801_3D.ifc \
  --output-dir reports
```

Ergebnisse:

- `reports/mvp1_regression_report.json`: vollständiger Prüfnachweis
- `reports/mvp1_regression_junit.xml`: JUnit-Ergebnis für CI/CD

Exitcode `0` bedeutet: alle Regeln bestanden. Exitcode `1` bedeutet: mindestens eine Regel ist fehlgeschlagen oder konnte nicht ausgeführt werden. Exitcode `2` kennzeichnet einen Aufruf- oder Ladefehler.

## API starten

### Einfacher Start unter Windows

1. Vorhandene Python-3.14-Installation verwenden.
2. Das Projektpaket entpacken.
3. `START_IFC_QUANTITY_AGENT.cmd` doppelklicken.

Der Starter richtet beim ersten Aufruf automatisch eine lokale `.venv314` ein, installiert die Abhängigkeiten und öffnet anschließend die Oberfläche im Browser. Git, Python 3.12 und eine manuelle Aktivierung der virtuellen Umgebung sind dafür nicht erforderlich.

Die Kombination Python 3.14.8 / IfcOpenShell 0.8.4.post1 wurde mit dem Z445-Referenzmodell vollständig geprüft: 15/15 automatisierte Tests und 32/32 Regelresultate bestanden.

### Manueller Start

```bash
python run_api.py
```

Danach stehen lokal bereit:

- MVP-1-Oberfläche: `http://127.0.0.1:8000/` (bei belegtem Port automatisch nächster freier Port)
- API: `http://127.0.0.1:8000/api/v1`
- interaktive OpenAPI-Dokumentation: `http://127.0.0.1:8000/docs`
- OpenAPI-JSON: `http://127.0.0.1:8000/openapi.json`

### UI-relevante Endpunkte

| Endpunkt | Zweck |
| --- | --- |
| `POST /api/v1/analyses` | IFC hochladen und analysieren |
| `GET /api/v1/analyses/{id}/overview` | Projektübersicht |
| `GET /api/v1/analyses/{id}/rule-results` | reproduzierbare Regelresultate |
| `GET /api/v1/analyses/{id}/findings` | objektbezogene Prüfhinweise |
| `GET /api/v1/analyses/{id}/objects` | filterbare Objektliste |
| `GET /api/v1/analyses/{id}/objects/{globalId}` | Objekt-Drilldown |

Die erste API-Fassung verarbeitet den Upload synchron und hält das Analyseergebnis im Arbeitsspeicher. Die IFC-Datei wird nach der Analyse aus dem temporären Uploadspeicher entfernt. Persistenz, Benutzer-/Rechteverwaltung und asynchrone Jobverarbeitung folgen als eigene Architekturbausteine.

### MVP-1-Oberfläche

Die Oberfläche verwendet ausschließlich die versionierte API und zeigt nach dem Upload eines IFC-Modells:

- Projektkennzahlen und Datenabdeckung,
- filterbare Findings und Regelresultate,
- eine filterbare Objektliste einschließlich leerer `LV-Ident`-Felder,
- Objekt-Drilldown mit IFC-Identität, PSets, QTOs und Findings,
- Mehrfachauswahl über GlobalIds.

Bei jeder Auswahl wird im Browser das Ereignis `iqa:select-objects` ausgelöst. Ein späterer 3D-Viewer kann damit alle gewählten GlobalIds im Modell selektieren, ohne die Quantity Engine zu verändern.

## Tests ausführen

```bash
python -m unittest discover -s tests -v
```

Der End-to-End-Test wird nur ausgeführt, wenn die Umgebungsvariable `IFC_MVP1_REFERENCE_MODEL` auf das Referenzmodell zeigt:

```bash
IFC_MVP1_REFERENCE_MODEL=/pfad/Z445_799_ECA_BM_801_3D.ifc \
python -m unittest discover -s tests -v
```

## Regel-ID-Konvention

`IQA-M1-<DOMÄNE>-<NUMMER>`

- `IQA`: IFC Quantity Agent
- `M1`: MVP 1
- Domänen: `FILE`, `UNIT`, `SPAT`, `ELEM`, `GUID`, `PSET`, `FIELD`, `MAT`, `ASM`, `OPEN`, `QTY`, `REVIEW`
- Nummer: dreistellige, dauerhaft stabile laufende Nummer innerhalb der Domäne

Regel-IDs werden nicht wiederverwendet. Inhaltliche Änderungen erhöhen die Regelversion; inkompatible Sollwertänderungen erzeugen eine neue Baseline-Version.

## Abnahme- und Änderungsprinzip

Die Baseline ist die einzige Quelle der Sollwerte. Der Collector darf keine fehlenden IFC-Werte ergänzen und keine native IFC-Klasse überschreiben. Brutto- und Netto-Mengen bleiben getrennt. Reviewfälle enthalten im JSON-Bericht die betroffenen GlobalIds als Evidenz.

`NetVolume` wird ausschließlich aus nativen `Qto_*BaseQuantities` gelesen. Gleichnamige Properties aus projektspezifischen oder benutzerdefinierten PropertySets werden nicht als IFC-Basisquantity behandelt. Dadurch bleiben Mengenquelle und Semantik reproduzierbar.



### Update v0.3.4

Links oben steht `UI v0.3.4`. IFC-Schema, Exportzeitpunkt und Referenzstand stehen nach dem Upload oberhalb der Kennzahlen. Der Starter reserviert einen freien Port und öffnet genau diese Instanz. Die im Konsolenfenster angezeigte Browser-Adresse gilt für diese Sitzung.


### UI v0.3.5 – lesbarer Objekt-Drilldown

Property Sets erscheinen gruppiert und aufklappbar als Eigenschaft/Wert-Tabellen. Mengen zeigen Wert, explizite Einheit und Quelle; fehlend und Null bleiben getrennt. Zahlenanzeige mit maximal sechs Nachkommastellen, exakter Rohwert aufklappbar. Technisches JSON ist optional. Die IFC-Daten und Mengenregeln werden nicht verändert.

### UI v0.3.6 – Objektansicht scrollen

In der Objektansicht bleiben Suche, Filter und Spaltenköpfe sichtbar. Die Liste und der Detailbereich scrollen unabhängig innerhalb der Fensterhöhe. Auf kleineren Bildschirmen stehen beide Bereiche übereinander. Der Objekttitel bleibt im Detailbereich sichtbar. Regression für diese Layoutgrenzen: `node tests/test_object_scroll.cjs` (Playwright erforderlich).

Browser-Layouttests vorbereiten: `npm ci --prefix tests/browser`, dann `node tests/browser/node_modules/playwright/cli.js install chromium --only-shell`. Node/Playwright sind nur für Entwicklungstests nötig, nicht zum Windows-Start des Agenten.
