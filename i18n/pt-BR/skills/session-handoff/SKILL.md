---
name: "session-handoff"
description: "Use ao encerrar uma sessão, antes de compactar contexto, ao esgotar uma cota da missão ou quando trabalho pendente precisar continuar em outro agente ou harness."
license: "MIT"
---

# Session Handoff
**Effort:** free — um arquivo plano escrito antes de o contexto morrer; nenhuma chamada de modelo, e corta custo na raiz no início da próxima sessão. Remove: o agente novo re-derivando o estado, repagando armadilhas já pagas, e decisões perdidas numa janela de contexto morta.

Uma janela de contexto morre; o trabalho não pode morrer junto. Antes de uma
sessão terminar ou compactar, escreva um arquivo plano que um agente novo em
folha consiga ler frio e continuar — o que estava sendo feito, onde mora, o
que está pela metade e o próximo comando exato. O handoff precisa sobreviver ao
contexto. Use o registro existente do [BACKS Build Flow](../backs-build-flow/SKILL.md):
transfira a tarefa sem criar outro responsável, passagem de contexto nem missão.

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

Respeite `task_mode` e permissões de escrita da tarefa. Para revisão somente
leitura ou congelada, devolva o handoff na resposta ou registro externo já autorizado;
nunca escreva registro no repo protegido para satisfazer esta skill.

## Verifique o trabalho concorrente primeiro (antes de escrever uma palavra)

Cheque que o trabalho de OUTRAS sessões está preservado. Rode `git status`,
`git log` e `git worktree list`. Anote no doc, com honestidade, os arquivos
sujos e as branches não fundidas. Nunca altere o trabalho não commitado de
outra sessão para o handoff parecer limpo — esse é o defeito de perda de
dados. Um handoff que descreve um estado limpo enquanto outra sessão tem
trabalho em voo é uma alegação falsa.

## O que entra — uma seção curta cada

1. **Objetivo.** Trabalho em uma frase e definição de pronto. Preserve `mission_id`,
   `task_mode`, responsável pela integração, conclusão solicitada e ações de
   entrega já autorizadas.
2. **Estado.** Integrado (ids de commit), construindo, na fila. Referencie
   specs, planos, issues e diffs por caminho ou URL sem duplicar. Inclua `base_sha`
   fixado, `candidate_sha` atual, caminhos/commit/hashes do RED selado, comandos
   e resultados, e candidato exato coberto por cada recibo.
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
9. **Skills sugeridas.** O que carregar primeiro e por quê. Nomeie corpos/evidências
   já disponíveis, o que atualizar e fonte da essência do operador; não copie
   um segundo perfil.
10. **Orçamento restante.** Preserve prazo original e total/consumido/restante de
    tentativas, rodadas e outros limites de [bounded-loops](../bounded-loops/SKILL.md),
    chamadas pendentes e última hipótese/falha. Desconhecido continua desconhecido.
    Nunca reinicie orçamento ao transferir, compactar, mudar trabalhador ou modelo.

## Regras duras

- **Redija.** Nada de chave de API, senha, token ou dado pessoal. Nada de
  hostname real, IP interno ou caminho de home — só placeholders; aponte para
  os valores reais pelo nome da variável de ambiente. O handoff é o arquivo
  com mais chance de sair da máquina; um segredo que vaza por ele É o bug.
- **Alegações de ausência apodrecem mais rápido.** Antes de escrever "X não
  existe" ou "X não aterrissou", verifique de novo no commit atual —
  trabalho paralelo aterrissa enquanto você escreve.
- **Status sustentado por evidências por item.** Entrega de capacidade usa PROVEN
  só com revisão exigida e prova real de superfície; caso contrário, STILL-BUILDING
  nomeia a evidência ausente. Revisão ou patch local concluídos podem atender ao
  pedido sem serem apresentados como capacidade implantada.
- **Mantenha legível em dois minutos** (cerca de 120 linhas). Quando passar
  disso, arquive os blocos mais antigos movendo-os para uma seção de
  histórico — nunca apagando.

## Retomada (a outra metade)

Uma sessão que parte de um handoff o lê PRIMEIRO, depois verifica as duas ou
três alegações do topo contra `git log` e a árvore viva antes de agir sobre
elas. O handoff é um mapa, não a verdade — confie nele para ONDE olhar;
verifique O QUE ele diz.

Retome com o mesmo pacote e cotas restantes. Confira prazo antes de despachar;
sessão nova não é orçamento novo. Se uma cota acabou, preserve STILL-BUILDING e
conclua apenas trabalho útil autorizado que não a consuma. Mantenha selo RED e
base fixada; atualize identidade do candidato apenas ao mudar os bytes reais.

## Funciona bem com

- [root-cause-first](../root-cause-first/SKILL.md) — a investigação que a próxima sessão continua.
- [repair-loop](../repair-loop/SKILL.md) — passe o bastão no meio do loop sem perder a costura.
- [decision-bar](../decision-bar/SKILL.md) — como as decisões abertas chegam ao seu humano.

> Crédito de scaffold: Matt Pocock, handoff (mattpocock/skills). A composição e as regras duras aqui são BACKS AIOS.
