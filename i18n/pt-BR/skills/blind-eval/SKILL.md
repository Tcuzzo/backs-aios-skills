---
name: blind-eval
description: Use antes de aterrissar qualquer coisa em que gosto ou qualidade de saída é a questão e um teste não consegue decidir. Julga a mudança pelo mérito com a autoria escondida, e mantém ou reverte — empate reverte, só ganho provado aterrissa. Trigger words: blind eval, karpathy, keep or revert, quality gate, taste call, blind judge, A/B judge, prove uplift, avaliação cega, manter ou reverter, portão de qualidade, decisão de gosto, juiz cego, provar ganho.
license: MIT
---

# Blind Eval

Um portão de qualidade manter-ou-reverter para decisões que um teste não decide —
qualidade de prosa, texto de UI, legibilidade de um refactor, saída de um prompt,
a sensação de um design. Julgue a mudança pelo mérito com a autoria escondida, e
depois MANTENHA ou REVERTA. Empate reverte. Só ganho provado aterrissa.

## Quando rodar

- Antes de aterrissar qualquer mudança em que "ficou melhor?" é questão de gosto ou qualidade.
- Como o portão dentro de um loop de melhoria: propor → tentar → medir → manter ou descartar.
- Sempre que o autor sentir a tentação de declarar o próprio trabalho uma melhoria.

## O método

1. **Escreva o que é "melhor" ANTES de olhar.** Um objetivo em linguagem simples.
   Uma medida primária ou eixo de rubrica com uma barra dura — um nível a superar,
   não um número a empurrar. Eixos secundários em ordem de prioridade (custo,
   tamanho, latência).
2. **Congele as duas versões.** A baseline e a candidata, como artefatos reais —
   nunca uma descrição delas.
3. **Arranque a autoria.** Rotule A e B, embaralhe a ordem, tire todo nome, id de
   modelo e o raciocínio do autor. O juiz vê só os artefatos e a rubrica.
4. **Sente um juiz que não escreveu nenhuma das duas** — um modelo de outra família,
   ou um humano. O autor nunca avalia o próprio trabalho.
5. **Julgue pelo mérito.** Pontue cada eixo da rubrica. Cite evidência do artefato
   para cada nota — veredito sem evidência é chute.
6. **MANTENHA só se a candidata passa a barra E vence a baseline com folga estrita.**
   Empate não é ganho — reverta.
7. **Reverta limpo.** Restaure a árvore byte a byte idêntica ao estado pré-mudança
   (um branch de rascunho ou stash faz disso um comando só). Registre o veredito de
   qualquer forma.

## Regras que matam o jogo sujo

- **A barra vem primeiro, e os eixos valem em ordem.** Regressão num eixo de
  prioridade mais alta é fatal mesmo que todos os eixos abaixo melhorem. E passar a
  barra com folga extra não compra nada — você não pode estourar a primária para
  "pagar" uma regressão de custo.
- **Nunca abaixe a barra depois de ver o resultado.** Consertar a nota enfraquecendo
  a avaliação é proibido. Mantenha a rubrica e a avaliação fora dos arquivos que a
  mudança pode tocar.
- **Sem auto-avaliação.** O juiz nunca vê a justificativa do autor — um juiz que lê
  o discurso de venda avalia o discurso, não o trabalho.
- **Tire o ruído de um juiz estocástico.** Leituras cegas variam de rodada em
  rodada, e juízes preferem a primeira opção que veem. Rode cada comparação várias
  vezes com a ordem embaralhada e pegue o voto da maioria — o embaralho mata o viés
  de posição e as repetições matam o ruído, num movimento só. Se a melhoria real é
  menor que a oscilação do juiz entre rodadas, o portão não separa sinal de sorte —
  adicione leituras ou escolha uma medida mais estável.
- **Rig solo.** Sem segunda família de modelo disponível? Uma sessão cega nova, que
  nunca viu a conversa do autor, julga — e o relatório nomeia o portão enfraquecido
  ("julgado cego-mesma-família, não cross-family").
- **Sem barra confiável? Use dominância.** Quando o nível da baseline é desconhecido
  ou ruidoso, derrube a barra absoluta e mantenha só o que vence o campeão atual com
  folga estrita. Uma regressão nunca domina, então não precisa de piso.
- **Nunca pontue um eixo de custo sobre falhas.** "Menos passos" computado sobre
  tentativas falhas premia desistir rápido. Compute custo e esforço só sobre sucessos.

## Tire o viés do juiz

O piso da mecânica de julgamento. Estas moram aqui e em nenhum outro lugar:

- **Suite held-out.** Avalie numa suite mantida FORA do alcance de escrita do
  builder — o builder nunca vê os testes avaliados, então não consegue codificar
  para eles.
- **Strip de commit fresco.** Reduza o workspace a um commit fresco e bloqueie a
  saída de rede antes de uma rodada avaliada, para que um pass seja DERIVADO — não
  recuperado do histórico do git ou do conserto de outra pessoa.
- **Normalize por tamanho.** Juízes preferem fortemente a resposta mais longa —
  corrija o tamanho antes de comparar notas.
- **Critérios de holdout rotativos.** Use uma rubrica de eixos nomeados, sim/não,
  com critérios de holdout escondidos que rodam entre rodadas. Uma nota holística
  visível vira teatro de citação.
- **Avaliação de estado final.** Avalie trabalho multi-passo pelo estado FINAL, não
  cada passo intermediário.
- **Calibração do juiz.** Calibre o juiz num conjunto pequeno rotulado por humanos —
  reporte as taxas de verdadeiro-positivo e verdadeiro-negativo — antes de confiar
  nele no seu domínio.

O embaralho de ordem faz parte da regra de ruído acima — uma lei, dita uma vez.

## A variante em loop

O mesmo portão move um loop autônomo de melhoria: propor uma mudança pequena →
rodar um experimento curto → medir às cegas → manter se melhor, reverter se não →
repetir, num orçamento fixo de rodadas. Alimente o propositor com os traces de
falha da rodada anterior, não só o objetivo — um propositor que não vê por que
falha edita no escuro. Até um loop que não mantém nada paga o próprio custo: os
traces que ele coleta apontam bugs concretos e consertáveis que nenhuma nota
agregada revela.

## Combina bem com

- [blind-tribunal](../blind-tribunal/SKILL.md) — o painel de jurados mais pesado quando a questão é defeito, não gosto.
- [red-first](../red-first/SKILL.md) — quando um teste CONSEGUE decidir, escreva o teste.
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — portões medidos de qualidade de código para parear com a decisão de gosto.

> Crédito do nome: Andrej Karpathy. Inspiração do nome; a disciplina de
> manter-ou-reverter tem um paralelo independente no autoresearch de Karpathy
> (2026, github.com/karpathy/autoresearch, MIT). O aspecto cego (autoria
> oculta) e a composição e as regras duras daqui são do BACKS AIOS.
