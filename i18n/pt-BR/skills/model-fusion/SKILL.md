---
name: "model-fusion"
description: "Use quando comparar abordagens elaboradas independentemente ajudar a tarefa e couber no orçamento restante, ou quando o operador pedir um painel. Rascunhos, seleção ou síntese e verificação independentes do modelo; o mesmo modelo configurado pode assumir papéis separados em sessões isoladas."
license: "MIT"
---

# Model Fusion
**Effort:** heavy — rascunhos independentes, um avaliador e um escritor opcional; use o painel quando seu benefício para a tarefa justificar o custo dentro do orçamento restante.

O painel é opcional. Execuções separadas elaboram a mesma tarefa; um avaliador
que não participou dessas execuções escolhe ou combina candidatos. O resultado
é verificado contra o pedido original. O mesmo modelo configurado e capaz pode
rascunhar, avaliar e escrever em sessões separadas e isoladas. Não é necessário
trocar de modelo ou provedor. O avaliador não herda a conversa nem o contexto
de trabalho dos autores.

## Quando rodar

- Quando comparar abordagens puder resolver uma incerteza concreta e sua avaliação
  couber no orçamento restante da missão.
- Quando o operador pedir um painel; informe papéis disponíveis e limites.
  Uma tarefa grande, por si só, não exige um painel.
- Para mudanças simples, faça a implementação direta com a verificação adequada.

Vincule [bounded-loops](../bounded-loops/SKILL.md). Rascunhos, juiz, escritor e
rodadas de reparo compartilham prazo, tentativas restantes e recursos da missão
atual. Novos papéis ou sessões não reiniciam esses limites. Execute rascunhos
independentes em paralelo quando o host permitir; caso contrário, em sequência
dentro dos mesmos limites. Não alegue isolamento de sessão que o host não oferece.

## Os três estágios

### 1. Painel — rascunhos independentes

1. Dê a mesma tarefa e o mesmo pacote de contexto a cada sessão isolada de
   elaboração de rascunho.
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
     e uma execução de escrita separada compõe a resposta final a partir dessa
     análise. Mantenha papéis e sessões separados; o mesmo modelo configurado
     e capaz pode assumir ambos.
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

- Escolha tamanho do painel e papéis por capacidades necessárias, disponibilidade
  real, configuração atual e orçamento restante. Não fixe modelos, preferência
  de provedor nem diversidade obrigatória. Registre lacunas de configuração.
- Formato de config, papéis-não-nomes e resolução por sonda viva pertencem a
  [fleet-ladder](../fleet-ladder/SKILL.md).

## Regras duras — quebrou uma, a skill falhou

- **Quem constrói nunca julga.** A execução avaliadora não escreveu candidatos
  nem herdou a conversa ou o contexto de trabalho dos autores. O avaliador final
  trabalha em uma sessão nova e disjunta do autor.
- **Nenhum nome de modelo hardcoded** em nenhum ponto de chamada. Papéis no
  código, modelos na config.
- **Nenhuma degradação silenciosa.** Rascunhistas descartados, fallback do
  juiz, falhas de portão e esgotamento são todos em voz alta. Um resultado
  inavaliável nunca passa por padrão.
- **Reparo limitado.** As rodadas têm teto duro e consomem o orçamento restante
  da missão; respeite o limite alcançado primeiro. O esgotamento produz um
  checkpoint visível, nunca um loop infinito.
- **Testes verdes sozinhos não são "pronto".** O vencedor é provado em
  comportamento vivo.

## Funciona bem com

- [fleet-ladder](../fleet-ladder/SKILL.md) — resolva quais modelos estão de pé antes de o painel disparar.
- [blind-tribunal](../blind-tribunal/SKILL.md) — a corte de avaliação que falha fechada quando o avaliador primário morre.
- [red-first](../red-first/SKILL.md) — o teste que falha e que o rascunho vencedor precisa deixar verde.
- [blind-eval](../blind-eval/SKILL.md) — portão de gosto mantém-ou-reverte quando nenhum teste decide.
