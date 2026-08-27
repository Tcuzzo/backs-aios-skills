---
name: wayfinder
description: Use quando você está perdido, o caminho à frente não está claro, ou é preciso decidir o que trabalhar em seguida. Traça um mapa de decisões até o destino em vez de estacionar uma pergunta no humano. Trigger words: wayfinder, the path, chart the route, map the work, what next, lost, fog of war, decision map, frontier, traçar a rota, mapear o trabalho, e agora, perdido, névoa de guerra, mapa de decisões, fronteira.
license: MIT
---

# Wayfinder
**Effort:** free — disciplina pura de traçado: um mapa de decisões montado com evidência que já está em disco, sem chamadas extras de modelo. Remove: perguntas estacionadas no humano que a evidência poderia responder, e trabalho de build começado antes de as decisões à frente dele serem tomadas.

Quando você não sabe o caminho, o movimento barato é parar e fazer ao humano
uma pergunta que ele te contratou para responder. O wayfinder traça a rota em
vez disso: monta um mapa de decisões, resolve as incógnitas a partir de
evidência e sobe só as escolhas que são genuinamente do humano.

## Quando rodar

- Você está perdido, ou o próximo passo não está claro.
- Um esforço grande precisa ser decomposto antes de alguém construir.
- Você sente a vontade de perguntar "o que você quer que eu faça?"

## Os passos

1. **Nomeie o destino.** Um objetivo nomeado no seu tracker, mais um
   predicado de fechamento: como você vai saber que está pronto. O destino
   fixa o escopo.
2. **Mapeie o que dá para ver.** Crie tickets na fronteira — as decisões
   prontas para resolver agora. Cada ticket resolve uma **decisão**, não uma
   fatia de trabalho de build.
3. **Deixe o resto na névoa.** Decisões que você sente vindo mas ainda não
   consegue cravar vão para uma seção **Ainda não especificado**: a pergunta
   suspeita, a área a revisitar. Não pré-fatie a névoa em pedaços de tamanho
   de ticket — ela é mais grossa que um ticket, e uma mancha pode virar
   vários tickets, ou nenhum.
4. **Exclua trabalho em voz alta.** Trabalho além do destino não é névoa —
   vai para uma seção **Fora de escopo** e nunca se gradua. Se um ticket vivo
   se revela além do destino, feche-o e deixe uma linha em Fora de escopo.
5. **Tipifique todo ticket** (veja Tipos de ticket abaixo).
6. **Resolva uma decisão a partir de evidência.** Leia o código, os docs, o
   registro — evidência determinística fecha um ticket sem palpite. Resolver
   um ticket limpa a névoa à frente dele: gradue o que agora é especificável
   em tickets novos, um de cada vez.
7. **Passe o bastão quando o caminho estiver claro.** O mapa está pronto
   quando não sobra nada a decidir antes de alguém ir lá e fazer a coisa. A
   vontade de simplesmente fazer o trabalho é o sinal de que você chegou à
   borda do mapa.

## Névoa ou ticket?

O teste é se você consegue formular a pergunta **com precisão** agora — não
se consegue respondê-la agora. Ticket quando a pergunta está afiada, mesmo
bloqueada. Ainda-não-especificado quando você ainda não consegue formular com
essa nitidez.

## Tipos de ticket

Todo ticket é **humano-no-loop** (trabalhado ao vivo com um humano) ou
**agente-sozinho**. Um ticket humano-no-loop só se resolve por troca ao vivo
— o agente nunca faz as vezes do lado do humano. Um agente respondendo às
próprias perguntas de sabatina quebrou isso.

- **Pesquisa** (agente-sozinho) — um agente de pesquisa em segundo plano
  resolve; os achados aterrissam numa branch de rascunho com um ponteiro a
  partir do ticket. Veja [live-research](../live-research/SKILL.md).
- **Protótipo** (humano-no-loop) — suba a fidelidade com um artefato tosco e
  barato ao qual o humano possa reagir.
- **Sabatina** (humano-no-loop) — conversa que puxa a decisão para fora. O
  tipo padrão.
- **Tarefa** (qualquer um) — trabalho manual que precisa acontecer antes de
  uma decisão: assinar um serviço, provisionar acesso, mover dados. O único
  tipo que *faz* em vez de decidir; ele ganha o lugar por desbloquear uma
  decisão.

## Regras duras

- **Nunca estacione no humano uma pergunta** que a evidência, o código ou as
  regras vigentes conseguem responder. Só sobem escolhas de gosto, visão e
  risco destrutivo — veja [decision-bar](../decision-bar/SKILL.md).
- **Refira-se ao trabalho pelo nome, nunca por um id seco.** Uma parede de
  #42, #43, #44 é ilegível; nomes se leem de relance. O id ou link viaja
  dentro do nome — nunca no lugar dele.
- **Uma decisão por sessão.** Resolva no máximo um ticket por sessão, tickets
  de pesquisa à parte. Mapear é o trabalho de uma sessão; ele não resolve
  nada na mão.
- **Planeje, não faça.** O mapa produz decisões, não entregáveis.
- **Quando o próprio pedido é a névoa** — o destino não está claro porque o
  pedido chegou como prosa ou metáfora — primeiro leia o pedido com
  [intent-compiler](../intent-compiler/SKILL.md), depois mapeie a partir do
  que ele realmente diz.

## Funciona bem com

- [live-research](../live-research/SKILL.md) — resolve os tickets de pesquisa agente-sozinho.
- [decision-bar](../decision-bar/SKILL.md) — quais decisões realmente chegam ao humano.
- [human-voice](../human-voice/SKILL.md) — como o mapa se lê para um humano.

> Crédito de scaffold: Matt Pocock, wayfinder (mattpocock/skills, MIT). A composição e as regras duras aqui são BACKS AIOS.
