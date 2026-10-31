---
name: bounded-loops
description: "Vor Arbeit mit Wiederholungen, Polling, Iteration, Unteragenten oder wiederholten externen Aufrufen, einschließlich autonomer Build-, Reparatur-, Review- und Übernahmeschleifen."
license: MIT
---

# Begrenzte Schleifen

Eine Mission hat ein gemeinsames Restkontingent. Wiederholung, Unteragent,
Modell-Fallback, Review-Runde, Kontext-Reset und verschachtelter Skill verbrauchen
es; sie füllen es niemals auf. [Build Flow](../backs-build-flow/SKILL.md) besitzt
die Aufgabenübergänge. Diese Methode besitzt Budgetführung, Wiederholungen, Abbruch und Checkpoints.

## Vertrag festlegen und weitertragen

Halte vor der ersten wiederholenden Handlung im vorhandenen Aufgabenpaket fest:

- `mission_id`, Integrationsverantwortlicher, Ziel und messbare Abnahmebedingung.
- Frist oder maximale Dauer, maximale Versuche/Runden und Ressourcen-/Aufrufgrenzen.
- Verbrauchtes und verbleibendes Kontingent, kleinere Rundengrenze der aktuellen
  Episode, Fehlersignatur und nächste Handlung. Nutze eine kleine explizite innere
  Grenze, oft drei Versuche; wähle sie passend zur Aufgabe, statt ein Beispiel zu verallgemeinern.
- Gemessene Kosten-/Token-/Aufrufdaten, soweit vorhanden. Kennzeichne fehlende
  Zähler als unbekannt; erfinde weder Null noch unbegrenzte Zuteilung oder
  Anbieterbudget. Setze durchsetzbare Zeit- und Versuchsgrenzen mit den tatsächlich verfügbaren Zählern.

Übernimm strengere Nutzer-/Projektgrenzen. Fehlen für eine gewöhnliche autorisierte
Aufgabe Vorgaben, wähle und benenne angemessene Grenzen und handle ohne neue
Freigaberunde. Frage nur, wenn der tatsächliche Ressourcenverbrauch eine
Autorisierung benötigt. Eine Budgeterweiterung erfordert die ausdrückliche
Entscheidung des Missionsverantwortlichen und nötige Operatorfreigaben;
ein Wechsel von Mitarbeitern oder Taktik ist keine Erweiterung.

## Die Iteration

1. Prüfe vor Arbeitsvergabe das Restkontingent. Teile Unteragentengrenzen daraus
   zu, auch parallel: Reserviere ihre Höchstzuteilungen zentral, damit die Summe
   den Elternrahmen nicht überschreitet. Unteragenten melden Verbrauch und Rest zurück.
2. Führe eine hypothesengeleitete Handlung aus. Bewahre bei Build/Fix echtes RED,
   setze den kleinsten vollständigen Fix um, führe begrenzte Lint-/Typ-/Verhaltensprüfungen
   aus und liefere Qualitätsbelege über [sniper-testing](../sniper-testing/SKILL.md)
   und [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) zurück.
3. Sichere Ergebnisse und Restkontingent an sicheren Grenzen. Ein Schreiber
   aktualisiert den autorisierten Aufgabenzustand atomar; andere liefern ihm Belege.
   Verwende bei strengem Nur-Lese-Review einen bereits autorisierten externen
   Aufgabeneintrag oder die Antwort. Nur-Lese-Umfang erlaubt kein Repository-Journal.
4. Ein identischer Fehler ohne neue Belege braucht eine geänderte Hypothese oder
   Taktik, keinen weiteren blinden Lauf. Schließe eine erschöpfte innere Episode.
   Eine andere Episode darf explizit verrechnetes Restkontingent der Mission nutzen.
5. Bei Missionserschöpfung, Abbruch oder blockierter Pflichtprüfung: Checkpoint
   schreiben, Blocker erklären, Wiederholungen stoppen. Setze unabhängige nützliche
   Arbeit nur fort, wenn Umfang und Restzuteilung es erlauben. Melde unfertige
   Fähigkeit als **STILL-BUILDING**; Timeout oder ausgelassene Prüfung sind nie GREEN oder PROVEN.

## Externe Aufrufe und Abbruch

Beachte veröffentlichte Anbieterlimits und Retry-After. Verwende Cache-Ergebnisse
weiter; beginne bei unbekannten Grenzen vorsichtig und miss. Nutze bei vorübergehender
Abweisung begrenzten exponentiellen Backoff mit maximaler Dauer und Versuchszahl.
Behandle dauerhafte Autorisierungs-/Eingabefehler nicht als vorübergehend. Warten,
Backoff und Fallback zählen alle gegen dieselbe Missionsfrist.

Stoppe an einer sicheren Zustandsgrenze: laufende Arbeit erfassen, Checkpoint
schreiben, abbrechen. Starte keinen zweiten Schreiber und lasse nach Abbruch keine
Hintergrundschleife laufen. Neue Anfragen steuern dort die aktuelle Mission;
verrechne geänderten Umfang ausdrücklich, statt das ursprüngliche Ziel still zu ersetzen.

## Übergabe und Ausstieg

Der Empfänger bekommt dieselbe Missionsidentität, Basis-/Kandidatenrevisionen,
Identität versiegelter Tests, Verbrauch und Restkontingent, Belege und nächste
Handlung. Er prüft den Zustand vor Fortsetzung. Neuer Kontext ist kein neues Budget.

Erfolg verlangt die ursprünglichen Abnahmeprüfungen und angeforderte Lieferung.
Erschöpfung verlangt einen ehrlichen Checkpoint, keine schwächeren Tests,
verschluckten Fehler, Datenlöschung, erfundenen Erfolg oder automatische äußere
Schleife mit aufgefülltem Zähler.

Siehe [session-handoff](../session-handoff/SKILL.md) zur Fortsetzung und
[fleet-ladder](../fleet-ladder/SKILL.md) vor tatsächlichem konfiguriertem Modell-Dispatch.
