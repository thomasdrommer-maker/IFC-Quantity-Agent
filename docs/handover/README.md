# Fachliche Übergabepakete

Stand: 01.11.2026. Diese Pakete konkretisieren den [Entwicklungsauftrag v1.12](../concept/IFC_Quantity_Agent_Entwicklungskonzept_v1.12.md). Die Dateien sind Entwicklungsgrundlagen; die Kategorien und die Profilverwaltung sind noch nicht in die laufende MVP-1-Anwendung integriert.

| Paket | Fachkonzept | Excel-Pflege | JSON-Regeln | Download |
|---|---|---|---|---|
| Stahlbau v0.2 | [Konzept](stahlbau/v0.2/IFC_Quantity_Agent_Stahlbau_Konzept_v0.2.md) | [Katalog](stahlbau/v0.2/IFC_Quantity_Agent_Stahlbau_Katalog_v0.2.xlsx) | [Regeln](stahlbau/v0.2/IFC_Quantity_Agent_Stahlbau_Regeln_v0.2.json) | [ZIP](stahlbau/v0.2/IFC_Quantity_Agent_Stahlbau_Arbeitsgrundlage_v0.2.zip) |
| Betonbau EFx/ECx v0.2 | [Konzept](betonbau/v0.2/IFC_Quantity_Agent_Betonbau_Konzept_v0.2.md) | [Katalog](betonbau/v0.2/IFC_Quantity_Agent_Betonbau_Katalog_v0.2.xlsx) | [Regeln](betonbau/v0.2/IFC_Quantity_Agent_Betonbau_Regeln_v0.2.json) | [ZIP](betonbau/v0.2/IFC_Quantity_Agent_Betonbau_Arbeitsgrundlage_v0.2.zip) |

## Geltung und Pflege

- Jedes Paket enthält Fachkonzept, Excel-Katalog, JSON-Regeln und Prüfvermerk; das ZIP enthält dieselben vier Dateien bytegleich.
- Die übernommenen v0.2-Dateien bleiben als Originalübergabe erhalten. Aussagen darin über den damaligen, noch nicht erfolgten Repo-Abgleich beschreiben den Erstellungsstand. Dieser Einstieg und der Gesamtauftrag dokumentieren die jetzige Einordnung.
- Für die Entwicklung sind der Gesamtauftrag v1.12 und beide Fachkonzepte einschließlich PR01–PR20 gemeinsam zu lesen. Vorschlagsgrenzen sind keine Normklassen; Entwurfsprofile werden nicht automatisch aktiviert.
- Das vollständige Modellcode-Mapping stammt aus Abschnitt 4 des Gesamtauftrags: EFx/ECx sind Familienbezeichnungen, ECA/ESA kombinierte Projektcodes. Material und Objektfunktion müssen dennoch geprüft werden; beispielsweise ist nicht jedes Einbauteil im EFx-Modell Beton.
- Excel ist die fachliche Pflegequelle. JSON ist der dazu geprüfte maschinenlesbare Export. Es gibt derzeit keine automatische Synchronisation. Änderungen erfordern Versionsanhebung, erneuten Export und Konsistenzprüfung; keine stille Bevorzugung widersprüchlicher Dateien.
- Die JSON-Dateien liegen bewusst bei der Übergabe. `rules/mvp1_rules_v0.1.json` bleibt der aktive MVP-1-Regelkatalog. Erst die implementierte und geprüfte Import-/Validierungsschicht darf neue Regeln übernehmen.
- `manifest_v0.2.json` dokumentiert Pfad, Dateigröße und SHA-256 aller zehn übernommenen Dateien.
- Je Paket sind 32 fachliche und 20 zusätzliche Profil-Sollfälle beschrieben. Sie sind keine bereits bestandenen Integrationstests. Beide Pakete teilen sich die Profilanforderungen; gemeinsam zu implementierende Kernlogik soll nicht dupliziert werden.

## Geplanter Integrationsablauf

1. Gemeinsames Datenmodell und Validator für Metriken, Scopes, Profile, Bänder und versionierte Ergebniszuordnung entwickeln.
2. Stahlbauauswertung in MVP 3 und EFx/ECx-Betonauswertung in MVP 4 anbinden; vorhandene BASF-Prioritäten, native QTO-Herkunft und Mengenbasis beibehalten.
3. Profilverwaltung über denselben Core in API und UI bereitstellen: Kopieren/Anlegen, Bearbeiten, Vorschau, Speichern/Versionieren, Auswählen/Archivieren sowie Excel-/JSON-Austausch.
4. Sollfälle automatisieren und mit realen IFC4-/IFC4.3-Modellen prüfen; erst danach fachlich freigeben. Profilimport/-export ist Konfigurationsaustausch und unabhängig vom späteren Mengenbericht-Excel-Export in MVP 6.
