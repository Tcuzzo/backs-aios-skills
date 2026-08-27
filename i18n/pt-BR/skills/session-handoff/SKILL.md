---
name: session-handoff
description: Use quando uma sessão está acabando, a janela de contexto vai compactar, ou o trabalho precisa continuar em outro agente ou harness. Compacta a sessão em um arquivo plano que um agente novo em folha lê frio e continua — estado, trabalho pela metade, o próximo comando exato, decisões abertas — com segredos redigidos e o trabalho concorrente verificado como preservado. Trigger words: handoff, hand off, compact, save state, continue in another session, portable handoff, before restart, passar o bastão, salvar estado, continuar em outra sessão, antes de reiniciar.
license: MIT
---

# Session Handoff

Uma janela de contexto morre; o trabalho não pode morrer junto. Antes de uma
sessão terminar ou compactar, escreva um arquivo plano que um agente novo em
folha consiga ler frio e continuar — o que estava sendo feito, onde mora, o
que está pela metade e o próximo comando exato. Handoff estacionado em prosa
de chat ou só na memória não existe.

## Quando escrever um

- Antes de a janela de contexto compactar ou ser limpa.
- Ao encerrar uma sessão com trabalho ainda aberto.
- Logo depois de aterrissar algo grande (registre o id do commit enquanto
  está fresco).
- No momento em que uma decisão de verdade vai para o seu humano (registre o
  que cada escolha significa).

## Onde ele vai

Um lugar conhecido onde o próximo agente vai olhar PRIMEIRO. Se o próximo
agente divide o seu projeto, use um arquivo de registro estável no repo e
commite a atualização, para ela sobreviver a um restart de máquina, não só a
uma limpeza de contexto. Se o próximo agente é outro harness ou um login
novo, escreva um arquivo plano portátil no diretório temporário — é andaime,
não artefato rastreado.

## Verifique o trabalho concorrente primeiro (antes de escrever uma palavra)

Cheque que o trabalho de OUTRAS sessões está preservado. Rode `git status`,
`git log` e `git worktree list`. Anote no doc, com honestidade, os arquivos
sujos e as branches não fundidas. Nunca altere o trabalho não commitado de
outra sessão para o handoff parecer limpo — esse é o defeito de perda de
dados. Um handoff que descreve um estado limpo enquanto outra sessão tem
trabalho em voo é uma alegação falsa.

## O que entra — uma seção curta cada

1. **Objetivo.** O trabalho em uma frase. O próximo agente não pode ter que
   adivinhar o que "pronto" significa.
2. **Estado.** Aterrissado (ids de commit), construindo, na fila. Referencie
   specs, planos, issues e diffs por caminho ou URL — nunca duplique o
   conteúdo deles.
3. **Onde o trabalho mora.** Branches, worktrees, arquivos sujos. Nomeie os
   arquivos exatos que o próximo agente deve ler primeiro.
4. **A trilha de veredictos.** Quem ou o quê avaliou cada peça e quais foram
   as pegadas reais. Um veredicto reprovado com defeitos nomeados vale MAIS
   que um verde — escreva os defeitos palavra por palavra.
5. **Trabalho pela metade e o próximo comando exato.** O que está em pleno
   voo, e o comando literal que continua dali.
6. **Decisões abertas.** Qualquer coisa esperando o seu humano, e o que cada
   escolha significa. Uma decisão nunca pode existir só numa janela de
   contexto morta.
7. **Contratos não cumpridos.** Testes ainda vermelhos, provas ainda
   faltando, promessas feitas e ainda não mantidas.
8. **Armadilhas.** Uma linha cada. Uma armadilha que você já pagou vale mais
   que um verde — escreva para a próxima sessão não pagar de novo.
9. **Skills sugeridas.** Quais skills o próximo agente deve carregar
   primeiro, e uma linha do porquê. É isso que torna o doc portátil entre
   harnesses.

## Regras duras

- **Redija.** Nada de chave de API, senha, token ou dado pessoal. Nada de
  hostname real, IP interno ou caminho de home — só placeholders; aponte para
  os valores reais pelo nome da variável de ambiente. O handoff é o arquivo
  com mais chance de sair da máquina; um segredo que vaza por ele É o bug.
- **Alegações de ausência apodrecem mais rápido.** Antes de escrever "X não
  existe" ou "X não aterrissou", verifique de novo no commit atual —
  trabalho paralelo aterrissa enquanto você escreve.
- **Status de duas palavras por item: PROVEN ou STILL-BUILDING.** Testes
  verdes sem prova viva é STILL-BUILDING, e o handoff diz exatamente qual
  prova falta.
- **Mantenha legível em dois minutos** (cerca de 120 linhas). Quando passar
  disso, arquive os blocos mais antigos movendo-os para uma seção de
  histórico — nunca apagando.

## Retomada (a outra metade)

Uma sessão que parte de um handoff o lê PRIMEIRO, depois verifica as duas ou
três alegações do topo contra `git log` e a árvore viva antes de agir sobre
elas. O handoff é um mapa, não a verdade — confie nele para ONDE olhar;
verifique O QUE ele diz.

## Funciona bem com

- [root-cause-first](../root-cause-first/SKILL.md) — a investigação que a próxima sessão continua.
- [repair-loop](../repair-loop/SKILL.md) — passe o bastão no meio do loop sem perder a costura.
- [decision-bar](../decision-bar/SKILL.md) — como as decisões abertas chegam ao seu humano.

> Crédito de scaffold: Matt Pocock, handoff (mattpocock/skills). A composição e as regras duras aqui são BACKS AIOS.
