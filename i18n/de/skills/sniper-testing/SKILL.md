---
name: sniper-testing
description: Für jede Fix- oder Build-Schleife, und bevor du irgendeinem grünen Test traust. Fährt nur die Tests, die abdecken, was du angefasst hast, und killt Mock-Theater — Tests, die bestehen, während die Fähigkeit kaputt ist. Trigger words: sniper testing, scoped tests, test scope, mock theater, fake green, full suite, test bloat, gezielte Tests, Test-Scope, falsches Grün, ganze Suite, Test-Blähung.
license: MIT
---

# Sniper Testing

## Warum es das gibt

Zwei Fehler-Muster verbrennen die meiste Testzeit. Test-Blähung: die ganze
Suite für eine winzige Änderung fahren. Mock-Theater: Tests, die bestehen,
während die echte Fähigkeit physisch kaputt ist. Dieser Skill killt beides.

## Regel 1 — der Diff definiert den Scope, nicht der Optimismus

Während der Fix/Build-Iterationsschleife ist es dir verboten, die ganze
Test-Suite zu fahren.

1. Fahr `git diff --name-only HEAD`, um exakt zu sehen, welche Dateien du
   angefasst hast.
2. Ordne jeder angefassten Datei die Test-Dateien zu, die sie direkt abdecken
   (z. B. `src/payments/refund.py` → `tests/test_refund.py`).
3. Benenn dein konkretes Test-Ziel, dann fahr NUR diese Dateien
   (z. B. `pytest tests/test_refund.py`).
4. Ein Test, der schon bestanden hat, wird nicht neu gefahren, außer deine
   nächste Änderung berührt Code, den er ausübt. Der Diff definiert den
   Scope — nicht Optimismus, nicht Angst.
5. Beim Landen — am Commit-Gate — fahr EINEN vollen Durchlauf über die Suite
   jedes angefassten Moduls. Dieser eine Durchlauf fängt indirekte Kopplungen
   genau einmal. Iterationstempo und eine solide Landung gehören beide zum Job.

## Regel 2 — Mock-Theater killen

Ein Fähigkeits-Test muss einen echten, physischen Nebeneffekt asserten:

- „erzeugt ein Video“ → eine echte Datei liegt auf der Platte, Größe > 0 Bytes.
- „speichert Erinnerung“ → die Zeile lässt sich aus einer echten lokalen
  Datenbank zurücklesen.
- „rendert das Widget“ → ein echtes DOM-Element existiert auf der Seite.

Mock nicht die Datenbank. Mock nicht das Dateisystem. Mock keine lokalen
Netzwerk-Sockets.

Der eine legale Mock ist das bezahlte externe Transport-Blatt — der HTTP-Call
an eine kostenpflichtige Dritt-API. Selbst dann muss der Test die ganze echte
Logik drumherum durchlaufen: Request bauen, Routing, Antwort parsen. Mock die
Leitung, nie das Hirn.

## Auditieren, bevor du traust

Bevor du dich auf irgendeinen Test verlässt, lies ihn. Ist er Mock-Theater —
grün wegen Mocks, ohne physische Assertion — lösch den Mock und schreib den
Test neu, sodass er einen echten Nebeneffekt assertet. Ein Test, der nicht
fehlschlagen kann, ist schlimmer als kein Test: er beglaubigt eine Lüge, und
du wirst auf dieser Lüge bauen.

## Harte Regeln (eine gebrochen, und der Skill ist gerissen)

- Kein Voll-Suite-Lauf während der Iteration.
- Keine Grün-Behauptung ohne Assertion eines echten Nebeneffekts.
- Kein Mock jenseits des bezahlten externen Transport-Blatts in einem
  Fähigkeits-Test.
- Kein Landen ohne den einen vollen Durchlauf über die angefassten Module.

## Passt gut zu

- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — der Sniper-Scope füttert sein erstes Gate
- [red-first](../red-first/SKILL.md) — schreib den fehlschlagenden Test vor dem Fix
- [seam-engineering](../seam-engineering/SKILL.md) — fix die Klasse, dann feg mit gescopten Tests
