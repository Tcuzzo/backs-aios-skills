---
name: live-research
description: Use ao raciocinar sobre um codebase, API ou sistema cuja forma real importa. Roda um agente de pesquisa em paralelo que lê a verdade viva — os READMEs do próprio projeto, os docs de seção, a fonte de fato — para as conclusões se apoiarem no que existe de verdade, não na memória do modelo. Trigger words: live research, ground the reasoning, read the real source, check what is actually there, primary sources, background research, verify against the repo, what do the docs say, pesquisa ao vivo, ler a fonte real, fontes primárias, conferir no repo, o que dizem os docs.
license: MIT
---

# Live Research

Memória de modelo é um palpite sobre como um projeto era na época do treino. A
verdade viva é o que está no disco e nos docs oficiais agora. Esta skill roda
as duas pistas ao mesmo tempo: enquanto a pista principal raciocina sobre um
alvo, um agente de pesquisa lê a coisa real, e os achados entram no raciocínio
**antes** de qualquer conclusão.

## Quando rodar

- Você está prestes a raciocinar sobre a estrutura de um projeto, o contrato
  de uma API ou o comportamento de uma biblioteca — e não leu a fonte atual.
- Um design, um conserto ou uma alegação depende de fatos que podem ter
  mudado desde os seus dados de treino.
- Uma pergunta precisa de fatos do mundo real que o contexto de trabalho
  sozinho não responde.

## Os passos

1. **Dispare o pesquisador em paralelo.** No momento em que o raciocínio
   sobre um alvo começa, despache um agente de pesquisa em segundo plano no
   mesmo alvo. A pista principal segue trabalhando; o pesquisador lê. Nunca
   trave o trabalho por causa de perna que um agente faz sozinho.
2. **Leia a verdade viva, do mais perto primeiro.** O README do próprio
   projeto, depois os docs de seção mais próximos do alvo, depois a estrutura
   real da fonte — listagem real de diretórios, conteúdo real dos arquivos,
   assinaturas reais. Para fatos fora do projeto: docs oficiais, código-fonte,
   specs, APIs de primeira mão. Um blog que resume os docs não é fonte
   primária.
3. **Mande os achados de volta antes das conclusões.** Os achados fluem para
   a pista principal conforme chegam, e o raciocínio os incorpora e corrige o
   rumo. Uma conclusão tirada antes de o pesquisador reportar sobre aquele
   ponto é um palpite — marque assim até a verdade viva confirmar ou matar.
4. **Prenda cada alegação à fonte que é dona dela.** Cada achado carrega a
   fonte junto: um caminho de arquivo, uma linha citada, um link, um commit.
   Alegação que não dá para prender é marcada como não verificada, em voz
   alta — nunca vestida de fato.
5. **Escreva um arquivo citado.** Os achados vão para um único arquivo
   Markdown, cada alegação com sua fonte. Salve onde o projeto já guarda
   notas assim; se não houver convenção, escolha um lugar sensato e diga
   onde, para o próximo agente achar.
6. **Lembre antes de reler.** Cheque primeiro as notas de sessões anteriores —
   a mesma fonte pode já ter sido puxada. Reuse o achado em cache e cite a
   mesma fonte. Minutos de memória valem mais que horas de redescoberta.

## Regras duras

- **Nenhuma conclusão antes da fusão.** Se o pesquisador não reportou sobre
  um ponto, a pista principal não pode dar aquele ponto como resolvido.
- **Só fontes primárias.** Siga cada alegação de volta até a fonte que é dona
  dela. Um resumo de segunda mão é um ponteiro, não prova.
- **Headless, nunca assistido.** Pesquisa em segundo plano usa um caminho de
  busca headless (sem janela de navegador) — nunca um navegador ao vivo que
  um humano está olhando; isso é outra pista.
- **Não verificável significa dizer isso.** Um achado sem fonte primária sai
  sinalizado, nunca misturado em silêncio com o resto.
- **Zero atrito humano.** Esta skill não adiciona passo de aprovação nem
  portão. É disciplina de método, não checkpoint.

## O que volta

Um arquivo Markdown fundamentado e citado — mais uma pista de raciocínio que
foi corrigida em pleno voo, em vez de depois de a conclusão sair. A pista
principal lê o arquivo e segue.

## Funciona bem com

- [wayfinder](../wayfinder/SKILL.md) — tickets de pesquisa são o tipo agente-sozinho que esta skill resolve.
- [root-cause-first](../root-cause-first/SKILL.md) — a mesma disciplina de fonte primeiro, apontada para bugs.

> Crédito de scaffold: Matt Pocock, research (mattpocock/skills, MIT). A composição e as regras duras aqui são BACKS AIOS.
