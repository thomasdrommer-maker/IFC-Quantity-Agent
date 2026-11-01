# IFC Quantity Agent – Stahlbaukategorien

**Version:** 0.2 · **Stand:** 01.11.2026 · **Autor:** OpenAI für Tom  
**Status:** Fachlicher Erweiterungsentwurf zur Projektabstimmung  
**Geltungsbereich:** Stahlbauauswertung aus IFC4 und IFC4.3 ADD2.  
**Änderungsübersicht:** v0.2 ergänzt benutzerdefinierte Kategorieprofile und 20 Profil-Sollfälle. Bisheriger Umfang v0.1: Erstfassung mit Profilgruppen, Gewichtsintervallen, Datenmodell, Summierungsregeln und Abnahmefällen.

## 1. Ziel und Einordnung

Der IFC Quantity Agent soll Stahlobjekte nachvollziehbar nach Funktion, Profil, Werkstoff, Objektmasse und Profilmetergewicht auswerten. Das Modul ergänzt die bestehende Mengenermittlung. Es ist ein eigenständiger Übergabebaustein; der aktuelle Gesamtauftrag des Quantity Agents und dessen Repository wurden für dieses Paket nicht abgeglichen oder geändert.

Die Profilreihen sind etablierte Produktbezeichnungen. Alle G-/M-Grenzen, internen Datenfelder, Regeln und Oberflächenanforderungen dieses Pakets sind eigene Entwicklungsvorschläge. Sie sind weder allgemeingültige DIN-Gewichtsklassen noch offizielle IFC-Properties oder eine verbindliche LV-Zuordnung. Kosten und Abrechnungsmengen werden daraus nicht automatisch festgelegt.

Arbeitsgrundlage ist der bereitgestellte buildingSMART-/IFC-Projektauftrag v1.0. Fachliche Quellen stehen in Abschnitt 12. Das Modul arbeitet lesend und verändert keine IFC-Klassen, BASF-Definitionen oder Modelldaten.

## 2. Lieferumfang und Verwendung

| Datei | Verwendung |
|---|---|
| IFC_Quantity_Agent_Stahlbau_Konzept_v0.2.md | In Projektquellen oder als Entwicklerübergabe ablegen |
| IFC_Quantity_Agent_Stahlbau_Katalog_v0.2.xlsx | Regeln und Datenanforderungen fachlich prüfen und pflegen |
| IFC_Quantity_Agent_Stahlbau_Regeln_v0.2.json | Maschinenlesbarer Erststand für einen späteren Importadapter |

Excel und JSON enthalten dieselben Regel-IDs, Grenzen und Profilregeln des Erststands. Zwischen den Dateien besteht noch keine automatische Synchronisation. Nach Excel-Änderungen muss der Agent künftig einen validierten JSON-Export erzeugen. Das Paket enthält keine fertige Agentenintegration und keinen vollständigen Profilstamm.

## 3. Kategorien und Bezugsobjekte

| Merkmal | Ausprägung / Zweck |
|---|---|
| Bauteilfunktion | Träger, Stütze, Verband, Pfette, Anschlussblech usw. |
| Querschnittsfamilie | I/H, U, L, T, Hohlprofile, Vollquerschnitte, Bleche |
| Profilreihe | IPE, HEA, HEB, HEM, UPE, UPN, CHS, SHS, RHS usw. |
| Exaktes Profil | Beispielsweise IPE 300 oder RHS 120×80×6 |
| Herstellungsart | Warmgewalzt, kaltgeformt, warmgefertigt, geschweißt |
| Querschnittsaufbau | Einteilig oder zusammengesetzt |
| Werkstoff | Vollständige Werkstoffbezeichnung, etwa S355J2 |
| Objektmasse | kg am eindeutig bezeichneten Bezugsobjekt |
| Profilmetergewicht | Nennmasse in kg/m aus bestätigtem Profilkatalog |

Weitere Felder für Länge, Blechdicke, Korrosionsschutz, Brandschutz und Fertigungsmerkmale sind für eine spätere Stufe sinnvoll. Blechdicke und weitere Maße sind in Abschnitt 13 für benutzerdefinierte Profile spezifiziert; die ursprünglichen Standardgrenzen bleiben erhalten.

**Bezugsobjekte:** `PART` = physisches Einzelteil, `ASSEMBLY` = dokumentierte Fertigungsbaugruppe, `MONTAGE_UNIT` = explizit definierte gemeinsam gehandhabte Montageeinheit. Eine IFC-Assembly darf erst nach bestätigtem Projektmapping als Fertigungs- oder Montageeinheit interpretiert werden. Geometrische Verschachtelung allein belegt diese Bedeutung nicht.

Ein Bauteil erhält mehrere unabhängige Merkmale. Kategorien erzeugen keine neuen Baugruppen oder Modellverschachtelungen. Eine Übersicht kann nach Kategorie gruppieren, ohne das IFC-Strukturmodell zu ändern.

## 4. Gewichtskatalog

### 4.1 Objektmasse

| Code | Bereich |
|---|---|
| G01 | über 0 bis 25 kg |
| G02 | über 25 bis 50 kg |
| G03 | über 50 bis 100 kg |
| G04 | über 100 bis 250 kg |
| G05 | über 250 bis 500 kg |
| G06 | über 500 bis 1000 kg |
| G07 | über 1000 bis 2000 kg |
| G08 | über 2000 bis 5000 kg |
| G09 | über 5000 kg |

### 4.2 Profilmetergewicht

| Code | Bereich |
|---|---|
| M01 | über 0 bis 10 kg/m |
| M02 | über 10 bis 25 kg/m |
| M03 | über 25 bis 50 kg/m |
| M04 | über 50 bis 100 kg/m |
| M05 | über 100 bis 200 kg/m |
| M06 | über 200 kg/m |

Für alle aktiven Intervalle gilt: Untergrenze exklusiv, Obergrenze inklusive. Die offene letzte Obergrenze ist in JSON `null`, in Excel eine leere Zelle. Das ist ein ausdrücklich definierter Sonderfall; leere Pflichtfelder bleiben Fehler. Es wird immer der ungerundete normalisierte Wert kategorisiert. Eine vorherige Anzeigerundung darf keine Grenze verschieben.

Fehlend → `unknown`; nicht anwendbar → `not_applicable`; negativ, nicht endlich oder null kg → `invalid` für diese positiven Masseintervalle. Ein tatsächlicher Nullwert bleibt als Rohwert erhalten, darf aber nicht als fehlend oder als G01 gelten. Positive sehr kleine Werte bleiben gültig. Unbekannte Gewichte werden gezählt und als Datenlücke sichtbar gehalten.

### 4.3 Massenbasis

| Basis | Bedeutung |
|---|---|
| NET | Masse unter Berücksichtigung geometrischer Bearbeitungen / Öffnungen gemäß dokumentierter Quelle |
| GROSS | Bruttomasse gemäß dokumentierter Quellenkonvention |
| PROFILE_THEORETICAL | Katalogmetergewicht × definierte Profillänge |
| CONTRACTUAL | Menge nach ausdrücklich dokumentierter vertraglicher Regel |
| UNKNOWN | Bedeutung oder Quelle noch ungeklärt |

Diese Werte dürfen nicht stillschweigend miteinander ausgetauscht werden. Ein NET-Bericht bleibt bei ausschließlich vorhandener GROSS-Masse unvollständig. NET und GROSS können in getrennten Ansichten ausgewertet werden. Die theoretische Profilrechnung ist keine pauschale Vertragsabrechnung. Geometrisch erkannte Öffnungen müssen im NET-Verfahren berücksichtigt werden; gelingt das nicht, ist der Wert nicht als verifiziertes NET zu kennzeichnen.

Bei `Qto_BeamBaseQuantities` beziehen sich GrossWeight und NetWeight auf den Träger ohne Anbauteile. Die Größen unterscheiden sich hinsichtlich Bearbeitungen und Öffnungen. Sie dürfen daher nicht als vollständiges Gewicht der zugehörigen Baugruppe interpretiert werden. [S05, S06]

## 5. Profilregeln und Datenquellen

Originalprofil und normalisierte Darstellung getrennt erhalten. Normalisierung vereinheitlicht Groß-/Kleinschreibung, überflüssige Leerzeichen und Maßtrenner; Dezimaltrennzeichen nur kontrolliert in Maßzahlen umsetzen. Zusatzkennzeichen und unterschiedliche Profilvarianten bleiben erhalten. `IPE A 300` und `IPE AA 300` dürfen nicht auf `IPE 300` reduziert werden. Doppelwinkel sind keine Einzelwinkel.

Die Regex-Regeln des Katalogs liefern nur eine Vorzuordnung von Familie und Reihe. Die exakte Profilbezeichnung, Abmessungen und Nennmasse benötigen einen eindeutigen Treffer in einem bestätigten versionierten Profilstamm. Bei keinem Treffer bleibt die exakte Zuordnung offen. Bei mehreren aktiven Regex-Treffern entsteht `conflict`; die Priorität dient der Anzeige/Reihenfolge und autorisiert keinen stillen First-Match.

Profilquellen werden projektspezifisch geordnet: bestätigtes Instanzfeld, zugewiesenes IFC-Material-/Profilmodell, bestätigte Typinformation, optional Name/Description/ObjectType als gekennzeichneter Hinweis. Instanzüberschreibungen haben Vorrang vor Typdefaults. Widersprüche müssen angezeigt werden. Die Profilreihe belegt keine Bauteilfunktion und nicht automatisch das Herstellungsverfahren aller Querschnitte.

### Projektfelder und Mapping

| Quelle | Vorgesehene Nutzung | Vor produktiver Nutzung |
|---|---|---|
| BASF_General / 540_LV_Ident | Führende Leistungszuordnung | Vorhandenen Katalog / Schreibweise prüfen |
| BASF_General / 603_Profil | Profilquelle | Aktuelle Definition und Vorrangregel bestätigen |
| BASF_General / 604_Bruttogewicht | Mögliche GROSS-Quelle | Einheit, Bezugsobjekt und Berechnung bestätigen |
| IFC-QTO | Versions- und klassenspezifische Mengen | Exakten Mengenpfad und Semantik bestätigen |
| Tekla Quantity / BaseQuantities | Exporterabhängige Alternativen | Reale Testdateien und Adapter erforderlich |
| Hierarchy | Zone / Ebene | Projektstruktur prüfen und Rohwerte erhalten |

Gleiche Feldnamen allein beweisen keine identische Mengenbedeutung. Das Paket legt keine neuen BASF-Propertynummern fest. Die 6xx-/7xx-Planungsstandregeln des BASF-Rulebooks werden nicht neu definiert; bei späterem Mapping ist der dann aktuelle Auftrag maßgeblich.

IFC4 und IFC4.3 benötigen eigene Adapterprüfungen. Ein bekannter QTO-Name von IfcBeam ist keine pauschale Quelle für IfcColumn, IfcMember, IfcPlate oder Assemblies. Die internen JSON-Schlüssel dieses Pakets werden zunächst ausschließlich in der Auswertungsdatenbank gehalten.

## 6. Einheitliche Verarbeitung

1. IFC-Modellstand anhand Inhaltshash identifizieren; Dateiname, Schema und Modellzuordnung erhalten.
2. Physische Objekte, Beziehungen, Material-, Profil- und Mengenquellen lesend erfassen.
3. Stahlzuordnung prüfen: bestätigt / ungeklärt / gemischt. Eine IFC-Klasse allein belegt keinen Stahlwerkstoff. Ungeklärte Objekte separat zeigen.
4. Bezugsobjekt, Massenbasis und Quellenkonvention bestimmen. Einheiten explizit auf kg und m normalisieren; objektspezifische Einheiten vor Projektdefaults beachten. Nicht allein über Feldnamen oder Zahlenordnung raten.
5. Bestätigte Mengen verwenden. Ableitungen nur aus passenden, dokumentierten Eingängen: beispielsweise Profilmetergewicht × Profillänge oder verlässliches Volumen × bestätigte Dichte. Keine versteckte Materialdichte als Hardcode.
6. Profilkatalog und Regelkatalog validieren. Positive Massen mit den ungerundeten Werten kategorisieren.
7. Für jede Aggregation die vollständige Einzelteilabdeckung erfassen und Doppelzählungen prüfen.
8. Ergebnis samt Quellen, Regeln, Datenlücken und Modellstand ausgeben.

## 7. Aggregation ohne Doppelzählung

**Standardansicht ist die Einzelteilebene.** Je Bericht wird genau eine Auswertungsebene und eine Massenbasis gewählt. Eine Baugruppe und ihre enthaltenen Einzelteile werden niemals gemeinsam zu einer Gesamttonnage addiert.

Bei PART werden nur eindeutig abgegrenzte physische Einzelteile gezählt. Bei ASSEMBLY werden Einzelteile zu einer bestätigten Baugruppe zusammengeführt oder eine bestätigte Baugruppenquelle verwendet; nicht beides addiert. Objekte ohne Baugruppe bleiben als unzugeordnete Teile sichtbar. Eine optionale kombinierte Gesamtübersicht darf diese nur anhand disjunkter Einzelteilabdeckung ergänzen und muss ihre gemischte Zählebene offenlegen.

Eine reine Gruppierung im Viewer oder ein Geometrieknoten zählt nicht zusätzlich als Material. Ein Objekt mit eigener Geometrie und Unterobjekten benötigt eine Klärung, welche Anteile bereits in der Geometrie/Masse enthalten sind. Zyklen, Mehrfachzuordnungen oder unbekannte Abdeckung sperren die betroffene Aggregation.

Baugruppen aus Kindmassen dürfen nur mit gleicher Massenbasis und kompatibler Berechnungskonvention als vollständig gelten. Fehlende Kindergewichte erzeugen `incomplete`: bekannte Teilmasse, Anzahl fehlender Kinder und Abdeckungsgrad nach Objektzahl anzeigen; keinen gewichteten Abdeckungsgrad erfinden. Keine scheinbar vollständige G-Kategorie vergeben.

Die interne Identität umfasst mindestens Modellstand und STEP-ID. GlobalId bleibt wichtig für Rückverfolgung und Modellvergleiche, wird aber auf Duplikate geprüft. Mehrere Instanzen eines Typs zählen jeweils. Verschiedene Modellstände werden nicht in eine aktuelle Summe addiert. Fachmodelle mit möglicherweise mehrfach enthaltenen physischen Objekten benötigen eine gesonderte Freigabe zur Deduplizierung.

Ein identischer `540_LV_Ident` an Assembly und Einzelteilen erlaubt gemeinsame Filterung. Er ersetzt keine Mengenabdeckungsprüfung.

## 8. Beispiel

Ein IPE 300 mit 6,00 m und 42,2 kg/m liefert 253,2 kg `PROFILE_THEORETICAL`, also G05 und M03. [S03]

Liegen für den bearbeiteten Träger **separat bestätigte NET-Werte** von 253,2 kg sowie NET-Massen zweier Kopfplatten von jeweils 12,0 kg vor, beträgt die vollständige NET-Baugruppenmasse 277,2 kg. PART-Summe und alternative ASSEMBLY-Summe ergeben jeweils 277,2 kg. Ihre Addition zu 554,4 kg ist falsch.

Liegen stattdessen nur die theoretische Profilrechnung und Netto-Plattengewichte vor, darf daraus ohne bestätigte Konvention kein vollständiges NET-Baugruppengewicht entstehen. Der Quellenmix wird sichtbar gemeldet.

## 9. Oberfläche und Ergebnisse

Die bestehende Projektübersicht um einen Bereich „Stahlbaukategorien“ erweitern. Oben Auswahl für Modellstand, Massenbasis und Auswertungsebene. Darunter Filter für Zone, Ebene, Bauteilfunktion, Profilfamilie, Reihe, exaktes Profil, Werkstoff, G-/M-Kategorie und Datenstatus.

Die Tabelle zeigt Anzahl, bekannte Gesamtmasse kg/t, Länge, fehlende Massenwerte und ungeklärte Stahlzuordnungen. Kategorien mit fehlenden Werten werden ausdrücklich angezeigt. Von einer Summenzeile führt ein Drilldown zu den zugehörigen Objekten mit GUID, STEP-ID, Quellenpfad und Rechenweg. Massenanteile nur auf die bekannte Masse derselben Basis beziehen und als solche beschriften.

Datenausgabe und API nutzen dieselbe Kategorisierungslogik. Ergebnisfelder sind im Excel-Blatt „Datenfelder“ und im JSON dokumentiert. Zusätzlich erhält jeder Lauf Inhalts-Fingerprint des Regelkatalogs, Zeitpunkt und Adapterversion. Quellenkonflikte bleiben bis zur Auflösung nachvollziehbar.

## 10. Umsetzungsschritte und Abnahme

**Stufe 1:** Regelimport, Datenmodell, Intervallvalidierung, explizite Quellenadapter, PART-Auswertung, Filter und Drilldown. Keine Preisberechnung und kein Modellwriteback.

**Stufe 2:** Bestätigter Profilstamm, exakte Variantenauflösung, vollständige Baugruppenabdeckung und ASSEMBLY-Auswertung. Eigene Montageeinheiten nur bei bestätigter Datenquelle.

**Stufe 3:** Modellstandsvergleich sowie Verbindung zu externen Kosten-/LV-Katalogen. Benutzerdefinierte Längen- und Blechdickenprofile nach Abschnitt 13 bereits in der Profilverwaltung vorsehen; Beispielgrenzen sind keine Projektfreigabe.

Für jede Stufe sind die relevanten Fälle aus „Abnahme“ umzusetzen. Das Paket liefert Sollfälle, keine Behauptung, dass der bestehende Agent sie bereits besteht. Besonders zu prüfen: alle G-/M-Grenzen mit Wert darunter, genau darauf und darüber; fehlend/Null/negativ; Einheiten; Profilvarianten; gemischte Massenbasis; vollständige und unvollständige Assemblies; identische LV-Id; doppelte GUIDs; geänderter Dateiinhalt bei gleichem Dateinamen.

Ein Standard-Regelimport muss eindeutig versionierte, aufsteigende und lückenlose aktive Intervalle für alle positiven Werte liefern. Benutzerprofile können nach Abschnitt 13 auch ausdrücklich partielle Abdeckung erlauben. Gleichartige Codes sind eindeutig. Der letzte Bereich ist offen; sonstige fehlende Grenzen sind ungültig. Ungültige Imports werden vollständig verworfen, die letzte gültige Version bleibt aktiv. Änderungen an Gewichtsgrenzen führen zu einer neuen Katalogversion und reproduzierbarer Neuberechnung.

## 11. Übergabetext für den Entwicklungsagenten

> Entwickle für den IFC Quantity Agent das Modul „Stahlbaukategorien“ nach diesem Konzept v0.2. Prüfe zuerst den aktuellen Repositoryauftrag und die vorhandene Datenstruktur. Nutze den Excel-/JSON-Regelkatalog als externe Konfiguration, ohne Grenzwerte im Programmcode festzuschreiben. Implementiere zunächst Stufe 1. Prüfe reale IFC4- und IFC4.3-Testdateien, Einheiten und Mengenbedeutung. Halte Netto-, Brutto-, theoretische Profil- und Vertragsmassen getrennt. Verhindere Doppelzählungen über eindeutige Mengenabdeckung. Erhalte Rohwerte und Quellen. Dokumentiere den Implementierungsstand, offene Mappings und ausgeführte Abnahmefälle. Verändere keine IFC-Dateien und keine BASF-Definition ohne gesonderten Auftrag.

## 12. Quellen und Grenzen

Quellenrecherche: 01.11.2026. Nur offizielle Release-Dokumentation von buildingSMART wird als Schemainformation verwendet; Vorschau-/DEV-Seiten sind keine Grundlage dieses Pakets.

- **[S01] Projektauftrag buildingSMART / IFC v1.0**: Projektquelle: buildingSMART_IFC_Entwicklungs-_und_Beratungsauftrag_v1.0.md — Arbeitsgrundlage vom 18.10.2026.

- **[S02] ArcelorMittal – Products & Solutions**: https://sections.arcelormittal.com/products_and_solutions/EN — Etablierte Profilreihen, keine Quelle für vorgeschlagene Gewichtsgrenzen.

- **[S03] ArcelorMittal – Profilkatalog 2024-2**: https://sections.arcelormittal.com/repository2/Sections/Sections_MB_ArcelorMittal_FR_EN_DE_V2024-2.pdf — IPE 300: 42,2 kg/m; Beispielwert, kein vollständiger Profilkatalog.

- **[S04] bauforumstahl – Baukosten / Kosten im Stahlbau 2026**: https://bauforumstahl.de/stahlbau/baukosten — Kostenfaktoren, keine Preisdaten im vorliegenden Modul.

- **[S05] buildingSMART – Qto_BeamBaseQuantities, IFC4.3.2.0**: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/Qto_BeamBaseQuantities.htm — GrossWeight / NetWeight am Träger ohne Anbauteile.

- **[S06] buildingSMART – Qto_BeamBaseQuantities, IFC4 ADD2**: https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2/HTML/schema/ifcsharedbldgelements/qset/qto_beambasequantities.htm — Versionsbezogener Einstieg für IFC4.

Das Beispielmetergewicht ist kein Ersatz für einen vollständigen Profilkatalog. Gewichtsgrenzen und interne Modellfelder sind Projektvorschläge. Ein produktives Mapping für das konkrete Quantity-Agent-Repository und dessen IFC-Exportvarianten steht noch aus.


## 13. Benutzerdefinierte Kategorieprofile – verbindliche Entwicklungsanforderung v0.2

Die folgende Ergänzung gilt gemeinsam für Stahl- und Betonbau. Sie beschreibt eine noch zu implementierende Funktion. Bestehende Standardprofile bleiben erhalten. Die gelieferten Benutzerprofile sind deaktivierte Entwurfsvorlagen, keine Normklassen oder freigegebenen Projektgrenzen.

### PR01 – Profile verwalten

Standardprofile schreibgeschützt mitliefern; als benutzerdefiniertes Profil kopieren. Anlegen, umbenennen, bearbeiten, duplizieren, auswählen und archivieren.

### PR02 – Speicherbereich

Persönlich oder projektbezogen; Freigabe für Kollegen separat mit Berechtigungen implementieren. Keine implizite Änderung fremder Profile.

### PR03 – Identität

Stabile profile_id, Version, Ursprung, Name, Änderungszeit und Inhalts-Fingerprint speichern. Fachliche Änderung erzeugt neue Version; alte Berichte bleiben reproduzierbar.

### PR04 – Anwendungsbereich

Objekttyp/Kategorien, Material, Querschnittsform, Mengenbasis und Zählebene explizit im scope_json. Keine Profilanwendung nur anhand eines frei geratenen Namens.

### PR05 – Einheiten

Anzeige in mm/cm/m, m², m³, kg oder kg/m. Grenzen kanonisch in m/m²/m³/kg/kg/m speichern. Einheiten nur innerhalb gleicher Dimension konvertieren.

### PR06 – Grenzregel

Untergrenze exklusiv, Obergrenze inklusive. Offene letzte Obergrenze = null/Excel-Leerwert. Untergrenzen numerisch und nicht negativ; keine Vor-Rundung.

### PR07 – Überlappung

Aktive Bänder innerhalb desselben Profils dürfen sich nicht überschneiden. Codes sind pro Profil eindeutig. Unterschiedliche Profile dürfen dieselbe Messgröße anders einteilen.

### PR08 – Abdeckung

coverage=complete verlangt lückenlose Abdeckung aller positiven Werte bis unendlich. coverage=partial erlaubt bewusste Lücken und einen begrenzten Bereich; außerhalb gilt out_of_range.

### PR09 – Unvollständige Daten

Fehlend=unknown; nicht anwendbar=not_applicable; Null/negativ/nicht endlich=invalid. Variable Dicke/Querschnitt=variable, bis eine bestätigte abschnittsweise Auswertung vorliegt.

### PR10 – Originalmaße

Rohwert, Einheit, Quelle und normalisierter Wert erhalten. Exakte Maßgruppen parallel zu Intervallen anbieten. Keine Modelländerung oder zusätzliche Verschachtelung.

### PR11 – Vorschau

Vor Speichern/Anwenden: Grenzen/Einheiten und Umfang prüfen, Treffer je Band sowie unknown/invalid/variable/not_applicable/out_of_range/conflict zeigen. Drilldown auf Objekte.

### PR12 – Auswertungswechsel

Profilwechsel kategorisiert neu; keine Rohmengenänderung. Kombinierte Filter sind Schnittmengen. Alternative Profile niemals zu zusätzlicher Materialmenge addieren.

### PR13 – Import/Export

Profile und Bänder über Excel/JSON austauschen. Fehlende Pflichtfelder, unbekannte Metriken, doppelte IDs/Versionen mit anderem Inhalt, ungültige Scopes oder Intervalle atomar ablehnen.

### PR14 – Aktivierung

Entwurfsprofile nicht automatisch aktivieren. Erst nach Validierung und Nutzerwahl anwenden; ungültiger Import erhält letzte gültige Konfiguration.

### PR15 – Stützen

Rechteck b/h in lokalen Querschnittsachsen und Rund-Ø trennen. A nur aus bestätigtem Querschnitt; nicht beliebig Volumen/Höhe bei veränderlichem Querschnitt. Rechteck- und Rundprofile getrennt filtern.

### PR16 – Wände

Dicke normal zur Wandfläche, vertikale Höhe und Achslänge mit bestätigter Konvention. Wandansichtsfläche, Öffnungsabzüge und Schalungskontaktfläche bleiben verschiedene Messgrößen.

### PR17 – Bleche

Nennblechdicke aus bestätigter Profil-/Materialquelle oder validierter lokaler Geometrie. Nicht kleinste globale Bounding-Box-Abmessung. Modellierte Dicke allein beweist keinen Stahlwerkstoff.

### PR18 – Blechflächen

Gross/Net und Fläche der Mittelfläche versus Oberfläche unterscheiden. Ausgeklinkte/gelochte Bleche nicht über Außenrechteck als Nettofläche rechnen. Abwicklung gekanteter Bleche nur mit bestätigter Quelle.

### PR19 – Ergebnisvertrag

Je Objekt: profile_id, profile_version, profile_fingerprint, metric, category_code, classification_status, canonical_value, quantity_basis und evaluation_level ausgeben. Bericht enthält Modellstand und Profilversionen.

### PR20 – UI-Workflow

Kategorieprofile öffnen, Messgröße und Scope wählen, Grenzen/Bezeichnungen pflegen, Vorschau, Speichern als neue Version, Anwenden. Noch nicht gespeichert/ungültig darf nicht als aktives Profil erscheinen.

### Konkrete Profilvorlagen dieses Pakets

| Profil | Messgröße | Anzeigeeinheit | Status |
|---|---|---|---|
| Standard: object_mass_kg | object_mass_kg | kg | readonly |
| Standard: profile_mass_per_m_kg_m | profile_mass_per_m_kg_m | kg/m | readonly |
| Beispiel Blechdicken | plate_thickness_m | mm | draft |
| Beispiel Blechflächen | plate_area_m2 | m² | draft |
| Beispiel Blechgewichte | object_mass_kg | kg | draft |

### Dateien und Umsetzung

Excel enthält zusätzlich Profile, Profil_Baender, Profil_Metriken, Profil_Regeln und Profil_Abnahme. In Profil_Baender sind Grenzen immer in der kanonischen Einheit gespeichert; display_unit steuert nur Anzeige und Eingabe in der künftigen Oberfläche. Die letzte offene Grenze ist leer. Bei neuen Benutzerprofilen profilbezogene Codes statt global eindeutiger Kategorien verwenden: Schlüssel = profile_id + profile_version + category_code. scope_json enthält strukturierte Filter. Leere oder unbekannte Scopes werden nicht als „alle Objekte“ interpretiert.

Neue unterstützte Metriken sind im Blatt Profil_Metriken beschrieben; vorhandene Metriken behalten ihre Definition aus v0.1. Stützenvolumen sowie Wandlänge/-fläche sind bereits vorhandene Mengen und müssen bei einer frei angelegten Profildefinition auswählbar sein. Blechlänge/-breite sind ebenso auswählbar, auch ohne vordefinierte Beispielintervalle. Eine frei benannte neue Kategorie ist erlaubt; ein unbekannter Messalgorithmus/Metric-Key ist zunächst zu registrieren und fachlich zu prüfen.

Stufe 1 und der Übergabeauftrag werden um die Profilverwaltung mit Validierung, Vorschau, exakten Maßgruppen, Excel-/JSON-Import/Export und versionierter Auswahl ergänzt. Gemeinsame Kernlogik für API und Oberfläche verwenden. Weder Schemawechsel noch Modelldatenänderungen sind erforderlich. Das Originalpaket v0.1 bleibt als vorheriger Stand erhalten. Katalogdaten sind geprüft; die Integration und die 20 neuen Sollfälle im echten Agenten stehen aus.
