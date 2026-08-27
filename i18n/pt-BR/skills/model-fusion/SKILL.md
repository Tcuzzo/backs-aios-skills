---
name: model-fusion
description: Use quando a resposta de um modelo só não é confiável o bastante — um build, conserto ou design difícil em que você quer vários modelos competindo e um juiz independente escolhendo. Um painel rascunha em paralelo, um juiz funde o vencedor, o resultado é validado contra a intenção original. Trigger words: fusion, panel, judge, multi-model, ensemble, draft and merge, builder not grader, fusão, painel, juiz, multimodelo, rascunhar e fundir, quem constrói não avalia.
license: MIT
---

# Model Fusion
**Effort:** heavy — um painel completo rascunhando em paralelo mais um juiz independente (e um escritor opcional); gaste em builds e consertos difíceis que vão para produção, nunca em mudanças de uma linha. Remove: apostar a mudança no rascunho de um modelo só, e o retrabalho quando esse rascunho está errado.

Muitas vozes independentes vencem uma voz só. Um painel de modelos rascunha a
mesma tarefa em paralelo. Um juiz — um modelo que não escreveu nenhum dos
rascunhos — escolhe ou funde o melhor. O vencedor é então conferido contra o
que foi pedido de fato.

## Quando rodar

- Qualquer build, conserto ou uplift substancial em que qualidade importa mais
  que velocidade.
- Quando você quer um par específico de avaliadores independentes, não
  confiança cega num modelo.
- NÃO para mudanças triviais de uma linha. Faça a mudança direta e verifique.

## Os três estágios

### 1. Painel — rascunhos em paralelo

1. Mande a mesma tarefa, com o mesmo contexto, para todos os modelos do
   painel de uma vez.
2. Cada rascunhista trabalha sozinho. Nenhum vê o trabalho do outro.
3. Um rascunhista que dá erro, estoura o tempo ou devolve vazio é registrado
   e descartado. Ele nunca mata a rodada. Registre o descarte em voz alta —
   nunca engula.
4. Colete todo candidato não vazio.

### 2. Juiz — um de fora escolhe e funde

1. Antes de julgar, rode um portão mecânico barato em cada candidato: ele
   aplica limpo? Ele parseia? Rode a sonda numa cópia descartável, nunca na
   árvore viva. Candidatos que falham no portão saem antes de o juiz os ver.
2. Duas formas de juiz — escolha uma por config:
   - **Síntese:** o juiz analisa cada candidato (forças, defeitos, conflitos),
     e um modelo escritor separado compõe a resposta final a partir dessa
     análise. Escritor e juiz são papéis diferentes; mantenha modelos
     diferentes quando puder.
   - **Seleção:** o juiz escolhe o melhor candidato que passou no portão.
     Mais barato. Use quando fundir não acrescenta nada.
3. Se o juiz ou o escritor está indisponível, degrade EM VOZ ALTA para
   seleção sobre os mesmos candidatos. Nunca desperdice o painel em silêncio;
   nunca finja que houve síntese.
4. Se nenhum candidato sobrevive ao portão, anexe o melhor erro ao prompt e
   rode o painel de novo — limitado, no máximo 2 rodadas de reparo. Esgotou,
   devolva falha com a lista completa de erros. Nunca devolva um resultado
   vazio ou nulo como sucesso.

### 3. Validar — conferir o vencedor contra a intenção

1. Releia o pedido original. O vencedor faz o que foi pedido — tudo, e nada
   além do que foi pedido?
2. Cheque a correção semântica, o encaixe de estilo com o código ao redor, e
   que ele ainda aplica limpo.
3. Confiança baixa vira uma bandeira de escalada, não algo escondido. Depois
   prove do jeito normal: teste que falha primeiro, verde, comportamento
   vivo. Um rascunho fundido que nunca rodou é um palpite.

## A escada

- A forma dos degraus da fusão: um painel largo de modelos baratos embaixo,
  painéis mais apertados e orçamentos de saída mais apertados subindo — um
  degrau mal configurado falha em voz alta na hora de carregar.
- Formato de config, papéis-não-nomes e resolução por sonda viva pertencem a
  [fleet-ladder](../fleet-ladder/SKILL.md).

## Regras duras — quebrou uma, a skill falhou

- **Quem constrói nunca julga.** O juiz não escreveu candidato nenhum. O
  avaliador final é um modelo diferente (de preferência de outra família) de
  quem construiu o vencedor.
- **Nenhum nome de modelo hardcoded** em nenhum ponto de chamada. Papéis no
  código, modelos na config.
- **Nenhuma degradação silenciosa.** Rascunhistas descartados, fallback do
  juiz, falhas de portão e esgotamento são todos em voz alta. Um resultado
  inavaliável nunca passa por padrão.
- **Reparo limitado.** As rodadas extras do painel têm teto duro. Esgotamento
  é falha em voz alta, não loop infinito.
- **Testes verdes sozinhos não são "pronto".** O vencedor é provado em
  comportamento vivo.

## Funciona bem com

- [fleet-ladder](../fleet-ladder/SKILL.md) — resolva quais modelos estão de pé antes de o painel disparar.
- [blind-tribunal](../blind-tribunal/SKILL.md) — a corte de avaliação que falha fechada quando o avaliador primário morre.
- [red-first](../red-first/SKILL.md) — o teste que falha e que o rascunho vencedor precisa deixar verde.
- [blind-eval](../blind-eval/SKILL.md) — portão de gosto mantém-ou-reverte quando nenhum teste decide.
