---
name: fix-shit
description: Diagnose and close a reported failure end to end with a reproducer, root cause, class-level repair, consumer tests, and real-path proof. Use when the operator says fix shit, stop swallowing errors, or finish a stubborn bug.
license: MIT
---

# Fix Shit

Use this as the fast entry point into `root-cause-first` and `repair-loop`.
It is a repair skill, not a permission to hide a failing signal.

1. Name the user's broken behavior and the exact surface where it appears.
2. Build a repeatable red signal from the real path. Trace the input and each
   boundary to find where actual behavior diverges from expected behavior.
3. Identify the root cause and all callers of the broken seam. Preserve the
   original error in logs or the operator-facing state; a fallback may protect
   the app, but it must not turn failure into false success.
4. Make the smallest change that closes the failure class. Add a test that fails
   on the old behavior and covers the seam that failed.
5. Run focused tests, the affected consumers, and the actual app path. Verify
   both the desired result and the explicit failure state. Ask an author-disjoint
   reviewer to inspect the change when available.
6. Report PROVEN or STILL-BUILDING, with the evidence and any remaining red bar.

If the error is intermittent, capture timing and a bounded reproduction rate;
do not infer a cause from one green rerun. For code-location ambiguity, start
with `building-with-backs` and its target check.


## Evidências e revisão independente

Para executáveis distribuídos, pacotes ou comportamento solicitado em execução, use [rea-investigation](../rea-investigation/SKILL.md) e a skill `reverse-engineer-anything` instalada separadamente quando sua análise for útil; use um provedor Ghidra existente para alvos nativos compatíveis. Evidência estática não prova comportamento ao vivo; não instale silenciosamente um provedor ausente. Para adotar capacidade de código aberto, use [absorb](../absorb/SKILL.md). Use [fleet-ladder](../fleet-ladder/SKILL.md) para escolher por papel e capacidade, sem fixar nomes de modelos. Quando houver tribunal, siga [blind-tribunal](../blind-tribunal/SKILL.md): uma execução nova separada do autor revisa um pacote congelado sem dados do autor. Informe resolvedor, revisor ou evidência ausente como lacuna do runtime.
