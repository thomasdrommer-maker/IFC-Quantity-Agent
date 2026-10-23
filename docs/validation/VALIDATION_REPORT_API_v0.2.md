# Validierungsbericht – IFC Quantity Agent MVP-1 API v0.2

**Datum:** 23.10.2026  
**API-Vertrag:** 1.0.0  
**Paketversion:** 0.2.0  
**Referenzmodell:** `Z445_799_ECA_BM_801_3D.ifc`  
**Regelpaket:** `IQA-M1-Z445-ECA` Version 0.1.0

## Ergebnis

| Prüfung | Ergebnis |
| --- | ---: |
| freigegebene Regel-IDs | 32 |
| Regelresultate am Referenzmodell | 32 bestanden, 0 fehlgeschlagen, 0 Fehler |
| automatisierte Tests | 14 bestanden |
| OpenAPI-Vertrag | gültig und exportiert |
| Projektübersicht | bestanden |
| Regelresultat-Filter | bestanden |
| Finding-Filter und GlobalId-Evidenz | bestanden |
| Objektliste und Objekt-Drilldown | bestanden |
| Fehlerbehandlung für Dateityp und unbekannte Analyse | bestanden |

**Gesamtstatus: BESTANDEN**

## Bereitgestellte API

| Methode und Pfad | UI-/Systemzweck |
| --- | --- |
| `GET /api/v1/health` | Betriebsstatus und aktives Regelpaket |
| `GET /api/v1/rule-packages/current` | versionierter Regelkatalog |
| `POST /api/v1/analyses` | IFC-Upload und synchroner MVP-1-Prüflauf |
| `GET /api/v1/analyses/{id}/overview` | Datenbasis der Projektübersicht |
| `GET /api/v1/analyses/{id}/rule-results` | reproduzierbarer Prüfbericht mit Soll/Ist |
| `GET /api/v1/analyses/{id}/findings` | objektbezogene Prüfhinweise mit GlobalId |
| `GET /api/v1/analyses/{id}/objects` | filter- und paginierbare Objektliste |
| `GET /api/v1/analyses/{id}/objects/{globalId}` | Objekt-Drilldown mit PSets, QTOs, Mengenquellen und Findings |

## Nachgewiesener End-to-End-Ablauf

1. Das Referenzmodell wird als IFC-Datei hochgeladen.
2. Die Datei wird mit derselben Core- und Regelengine wie der Kommandozeilenlauf ausgewertet.
3. Alle 32 Regelresultate stimmen mit der JSON-Baseline überein.
4. Die Projektübersicht liefert unter anderem 202 `IfcElement`, ECA als Modelltyp und 121 leere bzw. fehlende LV-Ident-Werte.
5. Der Finding-Endpunkt liefert die drei Einzelfundamente ohne Bruttovolumen mit GlobalId und der Ursprungsregel `IQA-M1-QTY-006`.
6. Die Objektliste liefert für `missing_lv_ident=true` exakt 121 Objekte.
7. Der Objekt-Drilldown liefert native IFC-Daten, räumliche Zuordnung, Assembly-Beziehungen, Materialien, PropertySets, getrennte Mengenquellen, Reviewflags und objektbezogene Findings.

## Architekturentscheidungen

- Die REST-API ist nur ein Adapter; sie enthält keine zweite Fach- oder Mengenlogik.
- Regelresultate, CLI und API verwenden dieselbe Baseline und dieselbe Rule Engine.
- Die native IFC-Klasse und `BIM_Core.IfcClass` bleiben getrennt.
- `NetVolume` wird ausschließlich aus nativen `Qto_*BaseQuantities` gelesen.
- Serverseitige Dateipfade werden nicht über die API ausgegeben.
- Die temporäre IFC-Uploadkopie wird unmittelbar nach der Analyse entfernt.
- Der OpenAPI-Vertrag besitzt feste Antwortmodelle für Projektübersicht, Regelpaket, Sammlungen und Objekt-Drilldown.

## Bewusste MVP-Grenzen

- Analyseergebnisse liegen in dieser ersten Fassung im Arbeitsspeicher und sind nach Neustart nicht mehr verfügbar.
- Der Prüflauf erfolgt synchron; eine Job Queue ist noch nicht enthalten.
- Authentifizierung, Rollen, Projektpersistenz und Datenbank folgen als getrennte Bausteine.
- Die API liefert noch keine 3D-Geometrie. Der spätere Viewer kann Objekte über `GlobalId` koppeln.
- UI-Aktionen verändern weder IFC-Daten noch Regelresultate.

## Freigabe für den nächsten Schritt

Die API v0.2 ist als stabile Datenbasis für das MVP-1-UI-Grundgerüst geeignet. Als nächster Schritt können Projektübersicht, Prüfbericht und Objekt-Drilldown ausschließlich gegen den versionierten OpenAPI-Vertrag aufgebaut werden.

