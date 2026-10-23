# IFC Quantity Agent – Projektstatus

**Stand:** 23.10.2026  
**Entwicklungskonzept:** v1.11  
**Implementierungspaket:** v0.2.0  
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

## Bewusste MVP-Grenzen

- Analyseergebnisse werden noch im Arbeitsspeicher gehalten.
- Analyse läuft synchron.
- noch keine Datenbank, Authentifizierung oder Rollenverwaltung
- noch keine 3D-Geometrieausgabe
- noch kein produktives UI

## Nächster Schritt

MVP-1-UI-Grundgerüst gegen den versionierten OpenAPI-Vertrag entwickeln:

1. Projektübersicht
2. Prüfbericht mit Filtern
3. Objektliste
4. Objekt-Drilldown
5. Kopplung einer späteren Modellselektion über GlobalId

## Referenzmodell

`Z445_799_ECA_BM_801_3D.ifc` wird nicht im Repository gespeichert. Für den lokalen End-to-End-Test wird der Pfad über `IFC_MVP1_REFERENCE_MODEL` gesetzt.

