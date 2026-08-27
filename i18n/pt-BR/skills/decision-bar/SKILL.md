---
name: decision-bar
description: Use quando você está prestes a fazer uma pergunta ao seu humano, esperar aprovação ou estacionar uma decisão durante trabalho autônomo. Filtra toda decisão por uma barra só — apenas gosto, visão ou risco destrutivo chegam ao humano; todo o resto executa. Trigger words: ask-me bar, ask me, approval, permission, should I, decision, escalate, human in the loop, blocked on you, barra de decisão, aprovação, permissão, devo, decisão, escalar, humano no loop, travado em você.
license: MIT
---

# A Barra do Me-Pergunte
**Effort:** free — um teste de barra no momento em que você perguntaria; corta custo na raiz matando idas e vindas de interrupção. Remove: perguntas que as regras permanentes já respondem, e decisões reais estacionadas onde o humano nunca olha.

Agentes falham com seus humanos de dois jeitos: interrompem com perguntas que as
regras já respondem, ou "expõem" uma decisão real num lugar que ninguém nunca vai
ver. Esta skill fecha os dois.

## A barra

Uma decisão chega ao humano SOMENTE quando é genuinamente dele:

- **Gosto** — estilo, palavras, aparência, sensação; a escolha não tem resposta
  objetivamente certa.
- **Visão** — direção, escopo, intenção de produto; errar aqui entorta a missão.
- **Risco destrutivo** — perda de dados, ação irreversível, dinheiro de verdade,
  pessoas de verdade.

Tudo abaixo dessa barra EXECUTA — resolvido pelas regras vigentes, pela verdade do
próprio projeto, pela intenção conhecida do humano e por padrões sensatos. Zero
atrito adicionado.

## Passos

1. Pegue o momento. Você está prestes a perguntar, esperar ou adiar. Pare e rode a barra.
2. Teste: isto é gosto, visão ou risco destrutivo? Se nenhum — não é pergunta.
3. Abaixo da barra: procure antes de perguntar. Releia as regras vigentes e o
   código. A resposta quase sempre já está escrita. Resolva, execute, e anote a
   decisão no seu log de trabalho para o humano poder auditar depois.
4. Na barra: ENTREGUE a pergunta. Um resumo da situação em linguagem simples, depois
   as escolhas numa lista curta — como botões, se o canal do humano suportar — no
   canal que o humano de fato acompanha. Depois continue qualquer trabalho que não
   dependa da resposta.
5. Nunca estacione. Uma decisão deixada num doc, numa mensagem de commit, numa
   linha de ledger ou num parágrafo comprido não existe para o humano. Decisão
   estacionada é portão escondido.

## Regras duras (qualquer uma reprova a skill)

- Perguntar qualquer coisa respondível pelas regras vigentes, pelo código ou por
  padrões sensatos.
- Inventar maquinário novo de aprovação — uma flag, uma fila, um passo de
  assinatura — para trabalho abaixo da barra. Verificação pode ser adicionada;
  portão não.
- Fabricar uma aprovação para uma decisão que as regras vigentes do humano já tomaram.
- Estacionar uma decisão real em qualquer lugar que o humano não olha ativamente.
- Reportar "pronto" ou "verde" a partir de uma sonda proxy em vez da superfície do
  humano — a lei da prova mora em [invariant-floor](../invariant-floor/SKILL.md).

## Combina bem com

- [wayfinder](../wayfinder/SKILL.md) — trace a rota pelos desconhecidos abaixo da barra em vez de perguntar.
- [human-voice](../human-voice/SKILL.md) — o registro em que toda pergunta entregue é escrita.
- [invariant-floor](../invariant-floor/SKILL.md) — as regras vigentes a reler antes de qualquer pergunta subir.
