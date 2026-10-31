---
name: rea-investigation
description: "Use quando executáveis distribuídos, pacotes ou comportamento solicitado de runtime precisarem de investigação REA para diagnóstico, descoberta de capacidades ou verificação de adoção nativa."
license: MIT
---

# Investigação de artefatos com REA

Use o motor REA instalado e sua skill independente para binários distribuídos,
pacotes ou comportamento solicitado de runtime. Para repositórios comuns de
código, use diretamente código e tests. Esta ponte não instala REA, Ghidra,
provedores nem servidor MCP e não afirma que estejam disponíveis.

Use o pacote do [BACKS Build Flow](../backs-build-flow/SKILL.md), responsável pela
integração e `task_mode` permitido do chamador. Investigação direta estabelece
o pacote uma vez. [bounded-loops](../bounded-loops/SKILL.md) cuida do prazo e cotas
restantes; retries de provedor, modelos e handoffs os herdam. Esta skill produz
evidências; não cria outro responsável pela adoção ou pelo reparo.

1. Resolva alvo exato, identidade/hash, pergunta e fase: **descoberta** do artefato
   original ou **verificação** de um resultado nativo específico. Leia a skill
   instalada `reverse-engineer-anything` e suas referências pertinentes no
   diretório de skills do host; evite selecionar esta ponte recursivamente.
   Se faltar, informe e continue investigação útil com ferramentas disponíveis
   dentro do orçamento existente.
2. Use ferramentas REA conectadas quando existirem ou a CLI instalada. Para
   binários nativos compatíveis, use provedor Ghidra existente; relate ausência ou
   indisponibilidade sem inventar resultados nem instalar dependências sem autorização.
3. Comece com inspeção estática somente leitura. Registre identidade do alvo,
   IDs de evidência, escopo, limites e incógnitas. Achados estáticos não provam
   comportamento de runtime; observe ao vivo apenas no escopo solicitado e nos
   limites declarados de execução e mutação da ferramenta.
4. Devolva ao chamador pacote com identidade, fase, comandos/recibos, IDs de
   evidência, observações, distinção estática/runtime, incógnitas e orçamento
   restante. O chamador controla o próximo passo: Absorb aplica gates de
   licença/dependências e integração nativa; o responsável pelo reparo aplica
   root-cause-first e repair-loop. Não inicie esses ciclos recursivamente a partir
   da ponte. Se a verificação encontrar defeito, devolva a observação para RED
   selado e ciclo limitado de correção/verificação; não afirme ter reparado.
5. Roteie por papel e capacidade pelo fleet-ladder configurado; nunca fixe IDs
   de modelos. Para avaliação independente exigida, use execução nova separada
   do autor de blind-tribunal e pacote sem autoria, conforme capacidades reais
   do host. Provedor ausente ou orçamento esgotado produz checkpoint
   **STILL-BUILDING** com observações úteis e próxima ação exata; nunca prova
   inventada de runtime. Mantenha investigação desbloqueada dentro da cota restante.

Scaffold: REA de morluto, licença MIT, https://github.com/morluto/rea.
Motor, skill original e provedores são instalações separadas.
