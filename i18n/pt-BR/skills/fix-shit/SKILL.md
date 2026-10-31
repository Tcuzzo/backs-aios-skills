---
name: fix-shit
description: "Use quando o operador relatar comportamento quebrado, disser fix shit ou para parar de engolir erros, ou pedir a conclusão de um bug persistente."
license: MIT
---

# Fix Shit

Entrada rápida para `root-cause-first` e `repair-loop` dentro da tarefa atual do
[BACKS Build Flow](../backs-build-flow/SKILL.md). Preserve seu único responsável,
essência do operador, `task_mode`, identidade do candidato e evidências; não
recarregue pacote válido nem inicie outro ciclo de vida. Invocação direta estabelece
o pacote uma vez. Orçamento restante e prazo de
[bounded-loops](../bounded-loops/SKILL.md) valem para toda reprodução, correção,
modelo alternativo e revisão. Esta skill não os reinicia nem esconde falhas.

1. Nomeie o comportamento quebrado do usuário e a superfície exata onde aparece.
2. Crie sinal vermelho repetível pelo caminho real. Trace entrada e cada fronteira
   até achar onde comportamento real e esperado divergem. Sele o contrato original
   com [red-first](../red-first/SKILL.md) antes de um builder mudar a costura
   responsável. Uma tarefa de diagnóstico devolve essa evidência.
3. Identifique causa raiz e todas as chamadas da costura quebrada. Preserve o erro
   original em logs ou estado visível; alternativa pode proteger o app, mas não
   transformar falha em sucesso falso.
4. Para correção autorizada, aplique [repair-loop](../repair-loop/SKILL.md) no fluxo:
   menor reparo da classe, comandos reais focados de lint/tipos/tests pelo diff
   agregado fixado e verificações de qualidade/mutação do clean-code-gauntlet.
   Preserve o original selado; lacuna nova recebe test suplementar separado.
   Reutilize etapas verificadas em vez de repeti-las.
5. Complete revisão exigida separada do autor (author-disjoint), gate de integração das suites
   afetadas e verificações do caminho real do app para a entrega solicitada.
   Verifique resultado desejado e estado explícito de falha. Capacidade de revisão
   ausente é lacuna do runtime, nunca aprovação independente emitida por si mesmo.
6. Devolva candidato e evidências ao responsável pela integração. Relate PROVEN
   apenas com revisão exigida e evidência real de entrega; caso contrário, salve
   STILL-BUILDING com bloqueio vermelho exato e próxima ação. Esgotar orçamento
   preserva trabalho e limites; continue trabalho útil desbloqueado somente dentro
   da cota restante.

Se o erro for intermitente, capture tempos e taxa de reprodução limitada; não
deduza causa de uma única repetição verde. Para ambiguidade de localização,
comece por `building-with-backs` e sua verificação de alvo.

## Evidências e revisão independente

Para executáveis distribuídos, pacotes ou comportamento solicitado de runtime,
invoque [rea-investigation](../rea-investigation/SKILL.md) e a skill independente
`reverse-engineer-anything` quando a análise for útil; use provedor Ghidra existente
para alvos nativos compatíveis. Não trate evidência estática como comportamento
ao vivo nem instale provedor ausente em silêncio. Para adotar capacidade open source,
invoque [absorb](../absorb/SKILL.md). Use [fleet-ladder](../fleet-ladder/SKILL.md)
para rotear por papel e capacidade, sem fixar modelos. Quando um tribunal for
necessário, siga [blind-tribunal](../blind-tribunal/SKILL.md): execução nova separada
do autor revisa pacote congelado sem dados de autoria. Relate resolvedores,
revisores ou evidências ausentes como lacunas do runtime.
