# Validierungsbericht – Python 3.14

**Stand:** 23.10.2026  
**Implementierung:** IFC Quantity Agent MVP-1 UI v0.3.1  
**Zielumgebung:** Python 3.14.8  
**IFC-Bibliothek:** IfcOpenShell 0.8.4.post1

## Ziel

Nachweis, dass API, UI-Adapter, Collector und Regelengine auf der vorhandenen Python-3.14-Umgebung des Windows-Zielrechners betrieben werden können.

## Prüfumfang

- Installation aller versionierten Abhängigkeiten unter Python 3.14
- Import und Nutzung von IfcOpenShell 0.8.4.post1
- API-Vertrag und UI-Auslieferung
- Upload und Analyse des Referenzmodells `Z445_799_ECA_BM_801_3D.ifc`
- Projektübersicht, Regelresultate, Findings, Objektliste und Objekt-Drilldown
- Vergleich gegen die versionierte JSON-Baseline

## Ergebnis

- Abhängigkeiten vollständig installiert
- 15/15 automatisierte Tests bestanden
- 32/32 Regelresultate bestanden
- Z445-End-to-End-Lauf ohne Abweichung zur freigegebenen Baseline

## Bewertung

Python 3.14 ist für den gegenwärtigen read-only MVP-1-Analyseumfang freigegeben. Das Projekt verwendet dafür `ifcopenshell==0.8.4.post1`, da diese Distribution ein offizielles Python-3.14-Wheel bereitstellt.

Die Freigabe umfasst das Lesen und Analysieren vorhandener IFC-Dateien. Spätere Funktionen, die IFC-Dateien verändern oder neu schreiben, benötigen eigene Regressionstests, bevor sie in diese Freigabe einbezogen werden.
