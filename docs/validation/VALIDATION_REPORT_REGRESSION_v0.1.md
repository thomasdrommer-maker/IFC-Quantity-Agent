# Validierungsbericht – IFC Quantity Agent MVP-1 Regression v0.1

**Datum:** 21.10.2026  
**Referenzmodell:** `Z445_799_ECA_BM_801_3D.ifc`  
**Baseline:** `IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json`  
**Regelpaket:** `IQA-M1-Z445-ECA` Version 0.1.0  
**IfcOpenShell:** 0.8.4

## Ergebnis

| Prüfung | Ergebnis |
| --- | ---: |
| freigegebene Regeln | 32 |
| bestanden | 32 |
| fehlgeschlagen | 0 |
| Auswertungsfehler | 0 |
| Unit-/Strukturtests | 5 bestanden |
| End-to-End-Modelltest | 1 bestanden |

**Gesamtstatus: BESTANDEN**

## Abgedeckte Bereiche

- Dateiidentität, Dateigröße, Schema, ViewDefinition und Exportzeitstempel
- ECA-Modelltypableitung mit transparenter Herkunft
- Projekt-Einheiten und räumliche Struktur
- Product-, Element-, STEP- und Repräsentationszählungen
- native IFC-Klassenverteilung
- GlobalId-Abdeckung und Dubletten
- räumliche Zuordnung einschließlich unzugeordneter Objekte
- PSet-/QTO-Abdeckung
- LV-Ident-Verteilung einschließlich leerer Werte
- Schlüsselfelder und getrennte Erfassung von `BIM_Core.IfcClass`
- Materialien, Assemblies, Öffnungen und Voids-Beziehungen
- Brutto-/Netto-Volumen, LV-Gruppensummen und QTO-Abgleich
- erwartete Reviewbefunde einschließlich GlobalId-basierter Evidenz

## Nachgewiesene Schutzwirkung

Der End-to-End-Test hat eine semantisch wichtige Quellenabgrenzung bestätigt: Ein allgemeines Suchen nach `NetVolume` würde auch gleichnamige Werte aus benutzerdefinierten PropertySets erfassen. Dadurch würden 70 statt 66 Vergleichsobjekte und abweichende Summen entstehen. Die freigegebene Implementierung liest `NetVolume` deshalb ausschließlich aus nativen Sets nach dem Muster `Qto_*BaseQuantities`.

Diese Festlegung verhindert eine stille Vermischung von IFC-Basisquantities und projektspezifischen Properties und entspricht dem Rückverfolgbarkeitsprinzip aus Entwicklungskonzept v1.11.

## Automatisierte Ausgaben

- JSON-Prüfbericht mit Soll, Ist, Status und Objekt-Evidenz
- JUnit-XML für CI/CD
- Exitcode 0 bei vollständigem Bestehen
- Exitcode 1 bei Regelabweichung oder Regelfehler
- Exitcode 2 bei Lade- oder Aufruffehler

## Freigabestatus

Das Paket ist als technische MVP-1-Regressionsbasis für das Referenzmodell Z445 ECA geeignet. Es ersetzt noch keine UI-Abnahme; die gleichen Regelresultate sollen im nächsten Schritt über API und UI unverändert dargestellt werden.

