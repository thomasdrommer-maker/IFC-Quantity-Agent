# IFC Quantity Agent – Betonbaukategorien für EFx und ECx

**Version:** 0.2 · **Stand:** 01.11.2026 · **Autor:** OpenAI für Tom  
**Status:** Übersicht und fachlicher Erweiterungsentwurf zur Projektabstimmung  
**Arbeitsgrundlage:** buildingSMART-/IFC-Projektauftrag v1.0 vom 18.10.2026.  
**Änderungsübersicht:** v0.2 ergänzt benutzerdefinierte Kategorieprofile und 20 Profil-Sollfälle. Bisheriger Umfang v0.1: Erstfassung für Flach-/Tiefgründung und Betonhochbau mit 42 Bauteilarten, 25 Größenintervallen, Material-/Ausführungsmerkmalen und 32 Abnahmefällen.

## 1. Empfehlung und Geltungsbereich

Für Betonbau sind **Bauteilfunktion, Bauweise, exakte Geometrie, Betonvolumen und Material-/Ausführungsanforderungen** die wichtigsten unabhängigen Auswertungsmerkmale. Die Gewichtsorientierung des Stahlbaukatalogs wird deshalb nicht unverändert übernommen. Betonvolumen in m³ ist die zentrale Materialmenge; Schalung in m² und Bewehrung in kg/t sind eigene Auswertungen. Eine universelle Kosten- oder Abrechnungskategorie entsteht daraus noch nicht.

Die Übersicht umfasst Beton, Stahlbeton, Spannbeton sowie bestätigten unbewehrten Ergänzungsbeton. Mauerwerk, Erdarbeiten, Dämmung, Hohlräume und reine Bewehrungsobjekte gehören nicht in die Betonvolumensumme. Verpressmörtel und Boden-Zement-Gemische sind gesondert zu behandeln. Für Fertigteile kann ergänzend eine bestätigte Einzel-/Montagemasse sinnvoll sein.

EFx und ECx bezeichnen die projektspezifischen Modellfamilien. Das x wird nicht als neuer konkreter Dateicode interpretiert. Die Tabellen schlagen eine erwartete Modellzugehörigkeit vor; die fachliche Funktion bleibt auch dann erhalten, wenn ein Bauteil in einem anders gegliederten Modell geliefert wird. Kombinierte ECA-Modelle werden über das bestätigte Projektmapping ausgewertet.

**Status der Inhalte:** Bauteilbezeichnungen sind übliche Fachbegriffe. Die internen Codes, Größenintervalle, Datenschlüssel und Ablaufregeln sind eigene Projektvorschläge. Betonfestigkeits-, Expositions- und andere Normklassen werden als vorhandene Anforderungen übernommen, nicht durch neue Klassen ersetzt. Die konkrete Regelwerksanwendung bleibt projektbezogen. Die IFC-Hinweise beziehen sich auf IFC4 und IFC4.3 ADD2; sie sind keine pauschale Freigabe für automatisches Modellwriteback.

## 2. Die vier Ebenen der Kategorisierung

1. **Primäre Bauteilart:** genau eine Kategorie pro physisch abgegrenztem Betonobjekt, beispielsweise EF11 Bohrpfahl oder EC13 Stütze.
2. **Bauweise und Material:** Ortbeton/Fertigteil/Halbfertigteil, Bewehrungsart, Betonart, Festigkeit und Exposition.
3. **Geometrie und Größen:** exakter Pfahl-Ø oder Querschnitt; bei konstanten Wänden/Platten zusätzlich Größenintervalle.
4. **Auswertungs- und Anforderungskontext:** Zone/Ebene, NET/GROSS, Schalung, WU, Oberfläche, Betonierabschnitt und Datenstatus.

Spezialisierte Bauteilarten wie Schachtwand können die allgemeine Wandkategorie ersetzen. Sie werden nicht zusätzlich gezählt. Alternativ darf die Oberfläche eine übergeordnete Wandgruppe anzeigen, ohne Mengen zu duplizieren. Nutzungskontexte wie Pumpensumpf, Aufzugsschacht, Becken oder Maschine sind ergänzende Tags; sie erzeugen keine neuen physischen Bauteile und keine zusätzliche Verschachtelung.

## 3. EFx – Gründung und ergänzende Betonbauteile

| Code | Bauteilart | Wichtige Geometrie |
|---|---|---|
| EF01 | Einzel-/Blockfundament | L × B × H; Form |
| EF02 | Streifenfundament | Breite; Höhe; Achslänge |
| EF03 | Fundament-/Gründungsplatte | Plattendicke; Grundfläche |
| EF04 | Kombiniertes Fundament | Form; L × B × H |
| EF05 | Freitragender Fundamentbalken | Breite; Höhe; Achslänge |
| EF06 | Pfahlkopfblock/-platte | Dicke/Höhe; Grundfläche |
| EF07 | Köcherfundament | Außenmaße; Köcherabmessungen |
| EF08 | Maschinen-/Anlagenfundament | Form; Grundfläche; Höhe |
| EF11 | Bohrpfahl aus Beton | Nenn-Ø exakt; Achslänge |
| EF12 | Verdrängungs-/Rammpfahl aus Beton | Nenn-Ø oder B × H exakt; Achslänge |
| EF13 | Sonstiger Betonpfahl | Querschnitt exakt; Achslänge |
| EF14 | Barrette / tragendes Schlitzwandelement | Querschnitt; Tiefe; Funktion |
| EF15 | Brunnen-/Senkkastengründung | Außen-/Innengeometrie; Tiefe |
| EF21 | Sauberkeitsschicht / Unterbeton | Dicke; Grundfläche |
| EF22 | Fundament-/Stützensockel | Höhe; Querschnitt |
| EF23 | Frostschürze | Dicke/Breite; Höhe; Länge |
| EF24 | Beton-Gründungswand / Stützwand | Wanddicke; Wandhöhe; Länge |

Die Tabellen betreffen den physischen Beton, nicht automatisch Bohrleistung, Aushub, Verrohrung, Abbruch oder Pfahlkopfbearbeitung. Für Pfähle sind Nennquerschnitt, Achslänge und tatsächlich betrachtete Kopf-/Fußpunkte zu dokumentieren. Bei realem Betoniermehrverbrauch bleibt die Liefer-/Ausführungsmenge getrennt vom geometrischen Sollvolumen.

Ein Fundamentrost wird über seine abgegrenzten Betonbalken/Fundamente erfasst. Ein Container oder eine Baugruppe erhält keine zusätzliche Materialmenge. Köcher, Aussparungen und Pfahlkopfanschlüsse werden hinsichtlich Abzügen und Überlappungen geprüft.

## 4. ECx – Betonhochbau und modellübergreifende Ergänzungen

| Code | Bauteilart | Wichtige Geometrie |
|---|---|---|
| EC01 | Bodenplatte ohne bestätigte Gründungsfunktion | Dicke; Grundfläche |
| EC02 | Geschossdecke | Dicke; System; Grundfläche |
| EC03 | Dachdecke | Dicke; Neigung; Grundfläche |
| EC04 | Balkon-/Kragplatte | Dicke; Auskragung; Grundfläche |
| EC11 | Betonwand / Wandscheibe | Dicke; Höhe; Länge; Öffnungen |
| EC12 | Wandpfeiler | Querschnitt; Höhe |
| EC13 | Betonstütze | B × H oder Ø exakt; Höhe |
| EC14 | Unterzug | Breite; Gesamthöhe; Unterstand; Länge |
| EC15 | Überzug | Breite; Gesamthöhe; Überstand; Länge |
| EC16 | Rand-/Ringbalken | Querschnitt; Achslänge |
| EC17 | Betonsturz | Querschnitt; Länge |
| EC21 | Treppenlauf | Laufbreite; Tragplattendicke; Steigung |
| EC22 | Treppenpodest | Dicke; Grundfläche |
| EC23 | Rampenlauf | Dicke normal zur Fläche; Breite; Neigung |
| EC24 | Rampenpodest | Dicke; Grundfläche |
| EC31 | Aufkantung | Breite/Dicke; Höhe; Länge |
| EC32 | Betonbrüstung | Dicke; Höhe; Länge |
| EC33 | Betonkonsole | Auskragung; Breite; Höhe |
| EC34 | Voute / lokale Verdickung | Verlauf; minimale/maximale Dicke |
| EC35 | Schacht-/Beckenwand | Dicke; Höhe; Innen-/Außenform |
| EC36 | Schacht-/Beckensohle oder Abdeckplatte | Dicke; Grundfläche; Lage |
| EC41 | Betonschale / Faltwerk / Sonderkörper | Flächennormale Dicke; Krümmung; Form |
| MX01 | Vergussbeton | Geometrie; Einbauort |
| MX02 | Füll-/Ausgleichsbeton | Dicke; Form; Einbauort |
| UN00 | Betonobjekt mit ungeklärter Bauteilfunktion | Vorhandene Originalmaße erhalten |

Bei Halbfertigteilen bleiben die Betonteile derselben Funktion zugeordnet: beispielsweise Fertigteilhaut und Ortbetonergänzung einer Decke. Das Gesamtelement und seine Betonanteile werden nicht addiert. Hohlräume, Dämmkerne und andere Materialien zählen nicht zum Betonvolumen.

## 5. Übliche sinnvolle Merkmale

| Merkmal | Empfohlene Auswertung |
|---|---|
| Bauweise | Ortbeton, Fertigteil, Halbfertigteil |
| Bewehrungsart | unbewehrt, Stahlbeton, Spannbeton, Faserbeton, kombiniert |
| Druckfestigkeit | exakte Klasse, z. B. C25/30; keine automatische Mindestanforderung |
| Exposition | alle festgelegten Klassen, ggf. je Oberfläche |
| Betonart | Normal-/Leicht-/Schwerbeton; Rohdichte bei Bedarf aus Quelle |
| Geometrie | prismatisch, abgestuft, geneigt, gevoutet, gekrümmt, variabel |
| WU-Anforderung | bestätigte Anforderung und Konzeptreferenz; unbekannt bleibt unbekannt |
| Oberfläche | vereinbarte Anforderungen, ggf. Sichtbetonklasse, je relevante Fläche |
| Schalung | tatsächliche Kontaktfläche, Orientierung, Krümmung, verbleibende Schalung |
| Lage | Zone, Ebene, Bauabschnitt, Erdberührung |
| Betonierabschnitt | bestätigte Abschnitts-ID; nicht aus Objektgröße raten |
| Qualität/Prozess | vorhandene BBQ-/Überwachungsangaben getrennt |

Druckfestigkeit, Exposition und Konsistenz beschreiben unterschiedliche Eigenschaften; keine davon ersetzt die anderen. Expositionsklassen können gleichzeitig und je Bauteilseite unterschiedlich gelten. Es gibt keine sinnvolle einzige „höchste“ Klasse über alle Expositionsarten. [S09]

Betonbauqualitätsklassen nach DIN 1045-1000:2023-08 sind separat zu führen. Vorhandene Werte BBQ-N, BBQ-E und BBQ-S werden übernommen. Sie sind nicht mit Überwachungsklassen gleichzusetzen. Das Paket nimmt keine eigene normative Einstufung vor. [S10, S11]

## 6. Größenkategorien als veränderbarer Startvorschlag

### Betonvolumen je Auswertungsobjekt

| Code | Bereich |
|---|---|
| V01 | über 0 bis 0,5 m³ |
| V02 | über 0,5 bis 1 m³ |
| V03 | über 1 bis 2,5 m³ |
| V04 | über 2,5 bis 5 m³ |
| V05 | über 5 bis 10 m³ |
| V06 | über 10 bis 25 m³ |
| V07 | über 25 bis 50 m³ |
| V08 | über 50 bis 100 m³ |
| V09 | über 100 m³ |

### Plattendicke

| Code | Bereich |
|---|---|
| PD01 | über 0 bis 0,15 m |
| PD02 | über 0,15 bis 0,25 m |
| PD03 | über 0,25 bis 0,4 m |
| PD04 | über 0,4 bis 0,6 m |
| PD05 | über 0,6 bis 1 m |
| PD06 | über 1 m |

### Wanddicke

| Code | Bereich |
|---|---|
| WD01 | über 0 bis 0,15 m |
| WD02 | über 0,15 bis 0,25 m |
| WD03 | über 0,25 bis 0,35 m |
| WD04 | über 0,35 bis 0,5 m |
| WD05 | über 0,5 m |

### Wandhöhe

| Code | Bereich |
|---|---|
| WH01 | über 0 bis 2 m |
| WH02 | über 2 bis 3 m |
| WH03 | über 3 bis 4 m |
| WH04 | über 4 bis 6 m |
| WH05 | über 6 m |

Die Grenzen sind **keine allgemeingültigen DIN-/VOB-Kategorien**. Sie dienen einem ersten Filter- und Vergleichskatalog und lassen sich später an Projektmengen oder den LV-Katalog anpassen. Für alle Intervalle gilt: Untergrenze exklusiv, Obergrenze inklusive. Die letzte offene Obergrenze ist in JSON null und in Excel leer. Ansonsten sind Pflichtgrenzen vollständig zu befüllen. Vor der Klassierung nicht runden.

Volumenkategorien gelten getrennt nach Mengenbasis und Auswertungsebene. Sie hängen von der Modellsegmentierung ab: Ein in drei Objekte geteilter Betonierkörper liefert andere Objektkategorien als ein ungeteilter Körper. Bauteil-, Modellobjekt- und Betonierlosgröße sind deshalb getrennt zu benennen.

**Exakt gruppieren statt grob klassieren:** Pfahldurchmesser sowie Standardquerschnitte der Stützen und Balken. Ø 0,60 und Ø 0,80 m bleiben zwei Gruppen. B × H bleibt ein geordnetes Maßpaar mit dokumentierten lokalen Achsen. Aus nichtkreisförmigen Querschnitten wird kein Ersatzdurchmesser gebildet. Geometrisch ermittelte Maße benötigen vor produktiver Gruppierung eine vereinbarte Toleranz; eine solche Toleranz wird in v0.1 noch nicht erfunden oder fest aktiviert.

Plattendicke wird normal zur Bezugsfläche gemessen; bei geneigten Platten ist das nicht die vertikale Ausdehnung. Variable Dicken oder Höhen erhalten min/max und den Status variabel. Ohne fachlich freigegebene Konvention gibt es dafür keine konstante Größenklasse anhand Mittelwert oder Maximalwert.

Für Fundamentbreiten, Balkenhöhen, Stützenquerschnittsflächen, Einbauhöhen und Fertigteilgewichte werden vorerst exakte Werte geführt. Weitere Intervalle sind erst nach Sichtung realer Modelle festzulegen.

## 7. Mengen, Öffnungen und Überlappungen

**Getrennte Mengenbasen:** GROSS, NET und CONTRACTUAL. NET berücksichtigt Öffnungen, Aussparungen und Bearbeitungen. Ist der übernommene NET-Wert oder die Geometrie bereits entsprechend reduziert, darf der Agent nicht noch einmal abziehen. Ein fehlender NET-Wert wird nicht still durch GROSS ersetzt. Vertragsmengen benötigen einen bestätigten Regelkatalog; IFC-QTO ist keine automatische VOB-Abrechnung. [S06]

Bei mehrschichtigen oder gemischten Objekten wird nur der eindeutig abgegrenzte Betonanteil summiert. Eine Materialzuweisung „Beton“ am Gesamtcontainer beweist nicht, dass sein komplettes Volumen Beton ist. Fehlende oder widersprüchliche Materialinformationen bleiben sichtbar.

**Keine Doppelzählung:** Ein Bericht verwendet genau eine Zählebene und Mengenbasis. Gesamttreppe gegenüber Läufen/Podesten, Gesamtdecke gegenüber Fertigteilhaut/Ortbeton, Schachtcontainer gegenüber Wänden/Sohle und Fundament gegenüber integriertem Sockel brauchen eine eindeutige Abdeckung. Teile eines Gesamtelements werden über ihre Mengenabdeckung verfolgt.

Überlappungen zwischen Decke und Unterzug oder Platte und Wand sind gesondert zu prüfen. Ein automatisch erzeugtes Vereinigungsvolumen darf nicht ungefragt alle fachlichen Bauteilmengen ersetzen. Entweder liefert das Modell disjunkte Körper oder der Projektauftrag legt eine dokumentierte Zuordnung der Überlappung fest. Andernfalls entsteht ein Konflikt mit separat ausgewiesener bekannter Menge.

Einheiten werden explizit nach m, m², m³ und kg normalisiert. Originalwert, Einheit, Quelle, IFC-Schema, Modellstand, Regelversion und Ableitungsweg bleiben erhalten. Doppelte GUIDs melden, Instanzen eines Typs jeweils zählen. Ein veränderter IFC-Inhalt erhält trotz gleichem Dateinamen einen neuen Modellstand; alte Stände werden nicht zur aktuellen Summe addiert.

## 8. Schalung und Bewehrung als eigene Auswertungen

Die gesamte geometrische Oberfläche ist keine Schalungsmenge. Freie Betonoberseiten, Kontakt zu Bestand oder Sauberkeitsschicht, Bauteilanschlüsse und Kontakt zum Erdreich müssen gesondert betrachtet werden. Kontakt zu Erdreich bedeutet nicht automatisch eine Ausführung ohne Schalung. Schalungskontaktflächen benötigen eine Ausführungsannahme oder eine bestätigte Quelle.

Wandansichtsfläche pro Bezugsseite, zweiseitige Wandflächen und tatsächliche Schalungskontaktfläche sind unterschiedliche Mengen. Orientierung, Krümmung, Sichtbeton und verbleibende Schalung werden ergänzend geführt. Laibungen und Stirnseiten sind nur dann enthalten, wenn die dokumentierte Berechnungskonvention sie berücksichtigt.

Die Bewehrungsmenge wird getrennt ermittelt. Ein unvollständiges oder fehlendes Bewehrungsmodell bedeutet unbekannte Menge und nicht 0 kg. Ein Bewehrungskennwert in kg/m³ ist eine eigene Kennzahl; er wird nicht als statischer Bewehrungsgrad bezeichnet. Modellmengen und Schätzansätze dürfen nicht unmarkiert vermischt werden. Fertigteilgewichte brauchen bestätigte Rohdichten/Materialmassen und einen definierten Umfang von Bewehrung/Einbauteilen.

## 9. IFC-Abbildung und Quellenpriorität

Die Datei enthält IFC-Zuordnungskandidaten je Kategorie. Sie sind Prüfhilfen, keine automatischen Klassifizierungsregeln. Bauteilfunktion, Material, Form und genaue Schemafassung müssen zusammenpassen. Vorhandene Klassen bleiben erhalten; Abweichungen werden als Prüfhinweis ausgegeben.

- Einzelfundament, Streifenfundament und Pfahlkopfplatte lassen sich bei passender Funktion über IfcFooting mit PAD_FOOTING, STRIP_FOOTING bzw. PILE_CAP beschreiben. [S03, S04]
- Gründungsplatten werden als IfcSlab/BASESLAB behandelt. BASESLAB allein entscheidet jedoch nicht über die projektspezifische Trennung von tragender Fundamentplatte und anderer erdberührter Bodenplatte. [S02]
- FOOTING_BEAM betrifft einen zwischen Auflagern freitragenden Gründungsbalken und ersetzt nicht pauschal STRIP_FOOTING. [S03]
- Betonpfähle verwenden IfcPile; BORED/DRIVEN nur bei passender Ausführung. Material und Tragmechanismus bleiben separate Angaben. [S05]
- Die Senkkastengründung benötigt einen Versionsvergleich: IFC4 führt den Footing-Typ CAISSON_FOUNDATION; IFC4.3 hat die eigene Klasse IfcCaissonFoundation. [S03, S04]
- Gesamttreppen können Container für Läufe und Podeste sein. Die Mengenabdeckung entscheidet, was summiert wird. [S07]

Für die primäre Kategorie bleibt 540_LV_Ident nach dem bestätigten Projektkatalog führend. Das Feld wird nicht als frei erratbarer Klartext behandelt. Ist es leer oder unbekannt, können Klasse, PredefinedType, Name, Description und ObjectType Hinweise liefern; diese erhalten einen sichtbaren Ableitungsstatus. Widersprüche werden nicht durch eine starre Priorität verdeckt.

Das aktuelle BASF-Rulebook ist vor produktivem Mapping zu prüfen. 701_Bruttovolumen kann eine Bruttoquelle sein; die genaue Definition und Einheit sind zu bestätigen. Weitere 7xx-Felder werden hier nicht erfunden oder pauschal zugeordnet. IFC-QTOs werden je Klasse und Schema geprüft. Zone/Ebene aus Hierarchy benötigen das Projektmapping. Die bestehenden BASF-Planungsstandregeln werden nicht durch diesen Katalog geändert.

## 10. Oberfläche, Datenumfang und Abnahme

Filter: Modellfamilie, Modellstand, Zone/Ebene, primäre Bauteilart, Bauweise, Bewehrungsart, Betonfestigkeit, Exposition, genaue Pfahl-/Querschnittsmaße, Größenkategorie und Datenstatus. Darstellung: Stückzahl, bekannte Brutto-/Nettovolumina getrennt, maßgebende Flächen/Längen, fehlende Mengen und ungeklärte Betonzuordnungen. Drilldown zu GUID/STEP-ID, Originalquellen und Berechnungsweg.

Ein Ergebnis braucht zusätzlich Mengenbasis, Zählebene, Materialabdeckung, verwendete Regel-/Adapterversion und Modell-Inhaltshash. Unbekannte Werte bleiben null mit Status, tatsächliche Null- oder negative Volumina bleiben Rohwerte mit Fehlerstatus. Ungültige und unvollständige Objekte werden separat angezeigt und dürfen keine scheinbar vollständige Gesamtmenge erzeugen.

Der Katalog enthält 32 konkrete Sollfälle. Sie wurden nicht im bestehenden Quantity Agent ausgeführt. Katalogdaten und Export werden beim Erstellen geprüft; eine erfolgreiche Integration setzt reale IFC4-/IFC4.3-Dateien sowie Adapterprüfungen voraus.

## 11. Nächster Entwicklungsschritt

Stufe 1: aktuelle Projekt-/Repositorygrundlage prüfen, lesender Import, Materialprüfung, bestätigte Bauteilzuordnung, getrennte GROSS-/NET-Volumina, exakte Pfahl-/Querschnittsgruppen und die vorgeschlagenen Größenintervalle.

Stufe 2: disjunkte Teilmengen für Baugruppen, Halbfertigteile und Schnittbereiche, nachvollziehbare Schalungsflächen sowie gesonderte Bewehrungsauswertung.

Stufe 3: Betonierabschnitte, Fertigteillogistik, Modellstandsvergleich und Verbindung zu externen Kosten-/LV-Regeln. Keine Kostenannahmen allein aus Volumenkategorien.

### Übergabetext

> Ergänze den IFC Quantity Agent um das Modul „Betonbaukategorien EFx/ECx“ nach diesem Konzept v0.2. Prüfe zuerst den aktuellen Gesamtauftrag und die vorhandene Datenstruktur. Nutze den externen Excel-/JSON-Katalog; keine Grenzwerte im Programmcode. Implementiere Stufe 1 lesend. Übernimm nur bestätigte Mengen und Einheiten. Halte Bauteilfunktion, Modellzugehörigkeit, Bauweise, Geometrie, Materialanforderungen und Mengenbasis getrennt. Gruppiere Pfahldurchmesser und Standardquerschnitte exakt. Berücksichtige Öffnungen im NET-Verfahren einmal und verhindere Doppelzählungen zwischen Containern, Teilen und sich überschneidenden Körpern. Melde offene Zuordnungen sichtbar. Dokumentiere reale IFC4-/IFC4.3-Tests und die Sollfälle. Ändere keine IFC-Dateien, BASF-Definitionen oder anderen Projektaufträge ohne gesonderten Auftrag.

## 12. Dateien, Quellen und Bearbeitung

Die Excel-Datei ist der editierbare Fachkatalog. Die JSON-Datei enthält denselben Erststand. Es besteht noch keine automatische Synchronisation. Nach Änderungen ist der Katalog zu validieren, zu versionieren und JSON neu zu erzeugen. Die IFC-Zuordnungen sind ausdrücklich Prüfkandidaten. Das bestehende Repository und dessen Gesamtauftrag wurden für dieses Paket nicht geändert.

Quellenprüfung: 01.11.2026. Normbezeichnungen werden nur soweit öffentlich belegt genannt; keine projektbezogene Anforderung wird aus Hersteller- oder Informationsseiten abgeleitet. Eigene Kategorien/Intervalle sind keine normativen Klassen.

- **[S01] Projektauftrag buildingSMART / IFC v1.0**: Projektquelle vom 18.10.2026 — Arbeitsgrundlage; keine Änderung am Gesamtauftrag des Quantity Agents.

- **[S02] buildingSMART – IfcFooting, IFC4.3.2.0**: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcFooting.htm — Fundamente, Gründungsplatten und Tiefgründung unterscheiden.

- **[S03] buildingSMART – IfcFootingTypeEnum, IFC4.3.2.0**: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcFootingTypeEnum.htm — PAD_FOOTING, STRIP_FOOTING, PILE_CAP, FOOTING_BEAM; Caisson-Versionshinweis.

- **[S04] buildingSMART – IfcFootingTypeEnum, IFC4**: https://standards.buildingsmart.org/IFC/RELEASE/IFC4/FINAL/HTML/schema/ifcstructuralelementsdomain/lexical/ifcfootingtypeenum.htm — Versionsvergleich Gründung.

- **[S05] buildingSMART – IfcPileTypeEnum, IFC4.3.2.0**: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcPileTypeEnum.htm — Pfahltypen; Material muss separat bestätigt werden.

- **[S06] buildingSMART – Qto_SlabBaseQuantities, IFC4.3.2.0**: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/Qto_SlabBaseQuantities.htm — Brutto-/Nettomengen; keine universelle Mengenquelle aller Klassen.

- **[S07] buildingSMART – IfcStair, IFC4.3.2.0**: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcStair.htm — Treppencontainer, Läufe und Podeste.

- **[S08] buildingSMART – IfcWallTypeEnum, IFC4.3.2.0**: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcWallTypeEnum.htm — Wandtypen versionsabhängig prüfen.

- **[S09] Beton.org – Auswahl des Betons**: https://www.beton.org/betonbau/beton-und-bautechnik/beton-bautechnik/auswahl-des-betons/ — Klassenbezeichnungen; keine projektspezifischen Grenzwerte daraus abgeleitet.

- **[S10] DIN Media – DIN 1045-1000:2023-08**: https://www.dinmedia.de/de/norm/din-1045-1000/369463519 — Titel, Ausgabe und Anwendungszweck der Betonbauqualitätsklassen.

- **[S11] Beton.org – Zement-Merkblatt B30, Februar 2026**: https://www.beton.org/fileadmin/beton-org/media/Dokumente/PDF/Service/Zementmerkbl%C3%A4tter/B30_ZM_2_2026.pdf — BBQ-N/E/S; BBQ und Überwachungsklassen sind getrennte Angaben.


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
| Standard: concrete_volume_m3 | concrete_volume_m3 | m³ | readonly |
| Standard: slab_thickness_m | slab_thickness_m | m | readonly |
| Standard: wall_thickness_m | wall_thickness_m | m | readonly |
| Standard: wall_height_m | wall_height_m | m | readonly |
| Beispiel Stützenquerschnitte | column_section_area_m2 | m² | draft |
| Beispiel Stützenhöhen | column_height_m | cm | draft |
| Beispiel Rundstützen | column_diameter_m | cm | draft |
| Beispiel Wanddicken | wall_thickness_m | cm | draft |
| Beispiel Wandhöhen | wall_height_m | m | draft |

### Dateien und Umsetzung

Excel enthält zusätzlich Profile, Profil_Baender, Profil_Metriken, Profil_Regeln und Profil_Abnahme. In Profil_Baender sind Grenzen immer in der kanonischen Einheit gespeichert; display_unit steuert nur Anzeige und Eingabe in der künftigen Oberfläche. Die letzte offene Grenze ist leer. Bei neuen Benutzerprofilen profilbezogene Codes statt global eindeutiger Kategorien verwenden: Schlüssel = profile_id + profile_version + category_code. scope_json enthält strukturierte Filter. Leere oder unbekannte Scopes werden nicht als „alle Objekte“ interpretiert.

Neue unterstützte Metriken sind im Blatt Profil_Metriken beschrieben; vorhandene Metriken behalten ihre Definition aus v0.1. Stützenvolumen sowie Wandlänge/-fläche sind bereits vorhandene Mengen und müssen bei einer frei angelegten Profildefinition auswählbar sein. Blechlänge/-breite sind ebenso auswählbar, auch ohne vordefinierte Beispielintervalle. Eine frei benannte neue Kategorie ist erlaubt; ein unbekannter Messalgorithmus/Metric-Key ist zunächst zu registrieren und fachlich zu prüfen.

Stufe 1 und der Übergabeauftrag werden um die Profilverwaltung mit Validierung, Vorschau, exakten Maßgruppen, Excel-/JSON-Import/Export und versionierter Auswahl ergänzt. Gemeinsame Kernlogik für API und Oberfläche verwenden. Weder Schemawechsel noch Modelldatenänderungen sind erforderlich. Das Originalpaket v0.1 bleibt als vorheriger Stand erhalten. Katalogdaten sind geprüft; die Integration und die 20 neuen Sollfälle im echten Agenten stehen aus.
