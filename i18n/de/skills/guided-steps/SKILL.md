---
name: guided-steps
description: Nutze das, wenn ein Setup Schritte braucht, die nur ein Mensch tun kann — Dashboards von Drittanbietern, Credentials, CI-Secrets, Provisionierung, einmalige Migrationen, Cutovers. Verfasst ein interaktives Skript Etappe für Etappe, das jede URL öffnet, sagt, was zu klicken und zu kopieren ist, Werte einfängt und sie dorthin schreibt, wo sie hingehören. Trigger words: wizard, human-only steps, provision, credentials, dashboard setup, CI secrets, cutover, Assistent, Zugangsdaten, manuelle Schritte, Einrichtung, provisionieren.
license: MIT
---

# Wizard für menschliche Schritte
**Effort:** free — Autoren-Disziplin plus ein statischer Syntax-Check; keine Modell-Calls. Beseitigt: denselben Nur-Mensch-Klickpfad bei jedem Lauf neu erklären zu müssen, und Secrets, die unterwegs in versionierte Dateien geklebt werden.

Manche Schritte kann nur ein Mensch tun: sich durch ein Drittanbieter-Dashboard
klicken, Credentials anlegen, einen Provisionierungs-Screen freigeben. Sie sind
mühsam von Hand, und mühsam, jedes Mal neu zu erklären. Der Wizard macht daraus
einen geführten Lauf: ein interaktives Shell-Skript, Etappe für Etappe, das jede
URL öffnet, genau sagt, was zu klicken und zu kopieren ist, die Werte einfängt
und sie dorthin schreibt, wo sie hingehören.

## Wann einsetzen

- Ein Setup braucht einen Menschen an einer UI, die keine API erreicht —
  Dashboards, Konsolen, Credential-Screens, CI-Secret-Seiten, einmalige
  Migrationen, Cutovers.
- Der Weg ist lang genug, dass es wehtut, ihn jedes Mal neu zu erklären.

Wann NICHT: Eine API kann den Schritt (dann automatisiere ihn — ein Wizard ist
der letzte Ausweg), oder die Prozedur hat ein, zwei Schritte (dann sag es dem
Menschen einfach in klaren Worten).

## Die Form

Ein Skript, zwei Teile:

- **Eine Helfer-Bibliothek oben** — identisch in jedem Wizard, nie von Hand
  editiert. Sie liefert: Etappen-Header mit Fortschritt („Etappe 3 von 7“),
  Erzählung in menschlicher Stimme, plattformübergreifendes URL-Öffnen, verdeckte
  Eingabe für Secrets, idempotente `.env`-Upserts (Key aktualisieren, wenn
  vorhanden, sonst anhängen), Writes in den Secret-Store deines CI-Providers,
  einen Bestätigen/Pause-Schritt und eine Abschluss-Zusammenfassung von allem
  Eingefangenen.
- **Die Etappen unter einer Markierung** — der einzige Teil, den du verfasst.
  Eine Etappe pro menschlichem Schritt: die URL öffnen, sagen, was zu klicken und
  was zu kopieren ist, den Wert einfangen, ihn an sein Ziel schreiben. Setze die
  Gesamt-Etappenzahl, damit die Fortschrittsanzeige ehrlich ist.

## Prozess

1. **Scope.** Lies die Env-Beispieldatei, das README, die Deploy-Config und die
   CI-Workflows. Jedes Secret und jede Variable, die sie referenzieren, ist ein
   Wert, den der Wizard produzieren muss. Zeig dem Menschen die geordneten
   Etappen und die Werte vorab — bestätige den Plan vor dem Verfassen.
2. **Kartiere den Weg jeder Etappe.** Eine Zeile pro Etappe: URL → Aktion →
   Wert → Ziel. Der Mensch sieht den ganzen Weg, bevor er startet.
3. **Verfassen.** Kopiere das Template. Schreibe nur die Etappen; fasse nie die
   Bibliothek an. Halte die Erzählung in klaren Worten — die Person, die das
   ausführt, ist vielleicht kein Engineer.
4. **Statisch verifizieren.** Syntax-Check (`bash -n`, shellcheck), ausführbar
   machen, dann jede Etappe von Hand durchgehen: Stimmt jede URL, ist jede
   Anweisung klar, ist jedes Schreibziel korrekt? Führe es NICHT Ende-zu-Ende
   aus — es öffnet Browser und blockiert auf menschliche Eingabe.

## Harte Regeln

- **Secrets berühren nie getrackte Dateien.** Eingefangene Werte landen in der
  gitignorierten `.env` oder im CI-Secret-Store. Das Skript selbst trägt nur
  Platzhalter; der Mensch fügt echte Werte zur Laufzeit ein. Ein echter Key,
  Hostname oder ein persönliches Detail im verfassten Skript IST der Bug.
- **Jeder Remote-Write ist Single-Shot und begrenzt.** Ein Write in den
  Secret-Store ist ein API-Call: keine Retry-Schleifen, kein Hämmern. Laut
  scheitern und den Menschen die Etappe neu fahren lassen.
- **Standardmäßig kurzlebig.** Ein Wizard wird für einen Lauf gebaut und danach
  gelöscht. Committe ihn nur, wenn der Mensch einen wiederholbaren Setup-Pfad
  will — und auch ein committeter Wizard trägt nur Platzhalter.
- **Der Bestätigungsschritt ist der eigene Pauseknopf des Menschen, kein Gate.**
  Er existiert, damit er seine Arbeit prüfen kann — nie, um ihm Freigabe-Reibung
  aufzubürden.

## Passt gut zu

- [session-handoff](../session-handoff/SKILL.md) — festhalten, welche Etappen liefen, wenn der Lauf geteilt wird.
- [human-voice](../human-voice/SKILL.md) — das Register, in dem jede Etappe erzählt.
- [bounded-loops](../bounded-loops/SKILL.md) — die Kein-Hämmern-Regel hinter Remote-Writes.

> Gerüst-Credit: Matt Pocock, wizard (mattpocock/skills). Die Komposition und die harten Regeln hier sind BACKS AIOS.
