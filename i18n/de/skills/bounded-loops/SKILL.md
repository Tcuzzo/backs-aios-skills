---
name: bounded-loops
description: Nutze das vor jeder Schleife, die retrien, pollen, iterieren oder eine externe API rufen kann — Agent-Loops, Repair-Loops, Scheduler, Watcher. Deklariert Budget-Obergrenzen, checkpointet bei Erschöpfung und macht Hämmern strukturell unmöglich. Trigger words: bounded loop, budget, ceiling, retry, backoff, rate limit, throttle, kill-switch, checkpoint, runaway, infinite loop, spin, budget exhaustion, begrenzte Schleife, Obergrenze, Drosselung, Endlosschleife, Budget erschöpft.
license: MIT
---

# Bounded Loops

Eine unbegrenzte Schleife ist der teuerste Bug, den ein Agent ausliefern kann. Sie
verbrennt Budget, hämmert Provider, bis die dich sperren, und versteckt ihr eigenes
Scheitern im Kreiseln. Jede Schleife bekommt eine Obergrenze, einen Checkpoint und
einen lauten Weg zu sterben — bevor sie startet.

## Wann einsetzen

Vor dem Start jeder Schleife: ein Repair-Loop, ein Retry-Wrapper, ein Poller, ein
Scheduler, ein mehrstufiger autonomer Lauf — alles, was einen Call neu absetzen
oder einen Schritt neu versuchen kann.

## Die Schritte

1. **Deklariere zuerst das Budget.** Tokens, Kosten, Wanduhrzeit und maximale
   Versuche — aufgeschrieben vor der ersten Iteration. Eine Schleife ohne
   deklariertes Budget ist per Definition unbegrenzt und startet nicht.
2. **Deckle die inneren Runden.** Eine innere Episode (ein LLM-/Tool-Zyklus an
   einem Problem) bekommt eine kleine, feste Rundengrenze (etwa 4). Die Grenze
   begrenzt die Episode, nicht die Mission — unfertige Arbeit wandert nach oben,
   sie mahlt nicht weiter.
3. **Checkpointe jede Iteration.** Dauerhafter Zustand auf der Platte —
   Run-Manifest, Evidenz-Log, aktueller Schritt — nie Chat-Gedächtnis. Jeder (auch
   eine frische Session) kann vom letzten Checkpoint weitermachen.
4. **Bei Erschöpfung: checkpointen, dann eskalieren.** Übergib den Checkpoint an
   die äußere Schleife oder an deinen Menschen — mit dem, was getan ist, was fehlt,
   und dem Blocker. Fahre nie still über ein Budget hinaus. Stoppe auch nie still —
   Erschöpfung ist laut.
5. **Respektiere jede externe API.** Lerne vor dem ersten Call Rate-Limit und
   Quota des Providers; wenn unbekannt, behandle sie als strikt — ein Call, weiter
   Abstand — bis gemessen. Drossle jeden Call, cache und verwende Antworten
   wieder, und halte eine harte Obergrenze pro Zeitfenster.
6. **Weiche bei Gegenwind exponentiell zurück.** Ein 429 oder 503 heißt: warten,
   dann länger warten. Null Sofort-Retries auf denselben Endpoint. Ein enger Retry
   gegen einen Endpoint ist genau die Art, wie eine funktionierende Route stirbt:
   Er verbrennt Quota und kann deine ganze Egress-Adresse sperren lassen.
7. **Trage einen lauten, begrenzten Kill-Switch.** Jede Schleife, die einen Call
   neu absetzen kann, hat eine maximale Versuchszahl; ist sie erreicht, stoppt die
   Schleife LAUT mit der Evidenz — nie ein endloses oder stilles Kreiseln.
8. **Stoppen und Einreihen nur an sicheren Punkten.** Stopp heißt
   Checkpoint-dann-Abbruch. Neue Arbeit reiht sich für den nächsten sicheren Punkt
   ein (eine Zustandsgrenze zwischen Schritten) — nie mitten im Schritt injiziert.
   Eine Schleifeninstanz, ein Schreiber, atomare Zustands-Writes.

## Harte Regeln (woran dieser Skill scheitert)

- Eine Schleife, die ohne deklariertes Token-/Kosten-/Zeit-/Versuchs-Budget startet.
- Über ein erschöpftes Budget hinaus weitermachen, still oder nicht, ohne zu
  eskalieren.
- Ein Sofort-Retry auf denselben Endpoint, oder irgendein Retry-Pfad ohne Backoff.
- Eine Retry-Schleife ohne Versuchsdeckel, oder ein Deckel, der beim Erreichen
  leise versagt.
- Fortschrittszustand nur im Konversationsgedächtnis — ein Crash löscht den Lauf.
- Zwei Schleifeninstanzen, die denselben Zustand schreiben, oder nicht-atomare
  Zustands-Writes.
- Der Schleife entkommen, indem sie ihre eigenen Exit-Checks schwächt — ein Grün,
  das durch Latte-Senken, Daten-Löschen oder Fehler-Schlucken entsteht, ist ein
  Fake Green, kein Exit.

## Passt gut zu

- [optimus](../optimus/SKILL.md) — den Boden laden, bevor irgendeine Schleife startet.
- [repair-loop](../repair-loop/SKILL.md) — der Hauptabnehmer dieser Obergrenzen.
- [fleet-ladder](../fleet-ladder/SKILL.md) — begrenzter Fallback über Modelle hinweg, statt eins zu hämmern.
- [session-handoff](../session-handoff/SKILL.md) — das, worin ein Checkpoint eskaliert.
