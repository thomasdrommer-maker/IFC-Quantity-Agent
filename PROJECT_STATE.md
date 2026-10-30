# IFC Quantity Agent – Projektstatus

**Stand:** 23.10.2026  
**Entwicklungskonzept:** v1.11  
**Implementierungspaket:** v0.3.2  
**API-Vertrag:** v1.0.0  
**Regelpaket:** IQA-M1-Z445-ECA v0.1.0

## Fertiggestellt

- Z445-ECA-Inventur und prüfbare MVP-1-Abnahmebasis
- maschinenlesbare Referenzbaseline
- 32 stabile MVP-1-Regel-IDs
- deterministischer IFC-Collector auf Basis von IfcOpenShell
- CLI-Regressionslauf mit JSON- und JUnit-Ausgabe
- plattformneutraler Application Service
- REST-/OpenAPI-Adapter
- Projektübersicht, Regelresultate, Findings, Objektliste und Objekt-Drilldown als API
- Quellenabgrenzung für natives `NetVolume`
- 14 automatisierte Tests, davon ein vollständiger Z445-End-to-End-Test
- Ergebnis am Referenzmodell: 32/32 Regeln bestanden
- erste browserbasierte MVP-1-Oberfläche mit IFC-Upload
- Projektübersicht, filterbarer Prüfbericht, Objektliste und Objekt-Drilldown
- Mehrfachauswahl über GlobalIds mit vorbereitetem Selektionsereignis `iqa:select-objects`
- sichtbare Leerzustände für die weiteren Konzeptansichten
- Windows-Zielbetrieb mit Python 3.14 und IfcOpenShell 0.8.4.post1
- CI-Kompatibilitätsmatrix für Python 3.12 und 3.14
- vollständiger Z445-End-to-End-Lauf unter Python 3.14.8: 15/15 Tests und 32/32 Regeln bestanden
- UI v0.3.2: SHA-256-Identität und Referenzabweichungen explizit kennzeichnen; Regelquote als Referenzvergleich benennen

## Bewusste MVP-Grenzen

- Analyseergebnisse werden noch im Arbeitsspeicher gehalten.
- Analyse läuft synchron.
- noch keine Datenbank, Authentifizierung oder Rollenverwaltung
- noch keine 3D-Geometrieausgabe
- noch keine integrierte 3D-Modellansicht; Selektion ist als GlobalId-Schnittstelle vorbereitet

## Nächster Schritt

MVP-1-UI anhand des Z445-Modells fachlich und visuell prüfen. Danach Mengenübersicht und 3D-Viewer-Adapter über die vorbereitete GlobalId-Selektion ergänzen.

## Referenzmodell

`Z445_799_ECA_BM_801_3D.ifc` wird nicht im Repository gespeichert. Für den lokalen End-to-End-Test wird der Pfad über `IFC_MVP1_REFERENCE_MODEL` gesetzt.

