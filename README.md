# IFC Quantity Agent – MVP-1-Regressionspaket

Dieses Paket prüft das Referenzmodell `Z445_799_ECA_BM_801_3D.ifc` deterministisch gegen die freigegebene JSON-Baseline. Es setzt die Anforderungen aus dem Entwicklungskonzept v1.11 und der MVP-1-Abnahmebasis in stabile Regel-IDs und automatisierte Regressionstests um.

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

- Python 3.11 oder neuer
- IfcOpenShell 0.8.4

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

```bash
python run_api.py
```

Danach stehen lokal bereit:

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


