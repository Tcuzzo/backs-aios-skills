---
name: bounded-loops
description: "Use antes de trabalho que possa repetir tentativas, consultar periodicamente, iterar, despachar trabalhadores ou repetir chamadas externas, incluindo ciclos autônomos de construção, reparo, revisão e adoção."
license: MIT
---

# Ciclos limitados

Uma missão tem uma única cota restante. Retry, trabalhador, modelo alternativo,
rodada de revisão, reinício de contexto ou skill aninhada consome essa cota;
nunca a repõe. [Build Flow](../backs-build-flow/SKILL.md) controla as transições da
tarefa. Este método controla orçamento, retries, cancelamento e checkpoints.

## Declare e carregue o contrato

Antes da primeira ação repetitiva, registre no pacote existente:

- `mission_id`, responsável pela integração, objetivo e condição mensurável de aceitação.
- Prazo ou duração máxima, máximo de tentativas/rodadas e tetos de recursos/chamadas.
- Cota consumida e restante, limite menor de rodadas do episódio atual, assinatura
  da falha e próxima ação. Use um teto interno pequeno e explícito, muitas vezes
  três tentativas; escolha para esta tarefa sem tratar o exemplo como universal.
- Custos/tokens/chamadas medidos quando disponíveis. Marque contadores indisponíveis
  como desconhecidos; não invente zero, alocação ilimitada nem orçamento do provedor.
  Fixe limites executáveis de tempo e tentativas com os contadores que este
  ambiente realmente expõe.

Herde limites mais estritos do usuário/projeto. Se uma tarefa comum autorizada
não tiver limites fornecidos, escolha e declare limites proporcionais e aja sem
nova rodada de permissão. Pergunte apenas quando o compromisso real de recursos
precisar de autorização. Uma extensão proposta exige decisão explícita do dono
da missão e a autorização necessária do operador; mudar trabalhadores ou táticas
não é uma extensão.

## A iteração

1. Verifique a cota restante antes de emitir trabalho. Aloque tetos filhos dentro
   dela, inclusive para filhos paralelos: reserve seus máximos centralmente para
   que o gasto conjunto não ultrapasse o pai. Cada filho devolve consumo e sobra.
2. Execute uma ação orientada por hipótese. Para construir/corrigir, preserve RED
   real, aplique a menor correção completa, rode verificações focadas de
   lint/tipos/comportamento e devolva evidências de qualidade por
   [sniper-testing](../sniper-testing/SKILL.md) e
   [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md).
3. Salve resultados e cota restante em limites seguros. Um único escritor atualiza
   atomicamente o estado autorizado; trabalhadores devolvem evidências a ele.
   Para revisão estritamente somente leitura, use registro externo já autorizado
   ou a resposta. Escopo somente leitura não autoriza um registro no repositório.
4. Falha idêntica sem evidência nova exige outra hipótese ou tática, não outra
   execução cega. Encerre o episódio interno esgotado. Outro episódio pode usar
   a cota restante da missão com contabilização explícita.
5. Ao esgotar a missão, cancelar ou bloquear um gate obrigatório: salve checkpoint,
   explique o bloqueio e pare de repetir. Continue trabalho independente útil
   apenas se seu escopo e sua alocação restante permitirem. Relate capacidade
   inacabada como **STILL-BUILDING**; timeout ou gate pulado nunca é GREEN nem PROVEN.

## Chamadas externas e cancelamento

Respeite limites publicados do provedor e sinais Retry-After. Reutilize cache;
quando os limites forem desconhecidos, comece conservadoramente e meça. Use
backoff exponencial limitado para recusas transitórias, com duração e tentativas
máximas. Não repita falhas permanentes de autorização/entrada como transitórias.
Espera, backoff e alternativas contam contra o mesmo prazo da missão.

Pare em uma fronteira segura de estado: registre trabalho em andamento, salve
checkpoint e cancele. Não inicie um segundo escritor nem deixe um ciclo em segundo
plano após cancelar. Novos pedidos orientam a missão atual nessa fronteira;
contabilize mudanças de escopo explicitamente sem substituir o objetivo em silêncio.

## Handoff e saída

Quem recebe obtém a mesma identidade da missão, revisões base/candidata, identidade
dos tests selados, cota consumida/restante, evidências e próxima ação. Verifica
esse estado antes de retomar. Contexto novo não significa orçamento novo.

O sucesso exige as verificações originais de aceitação e a entrega solicitada.
Esgotar o orçamento exige checkpoint honesto, nunca tests enfraquecidos, erros
engolidos, dados apagados, aprovação inventada ou ciclo externo com contador reposto.

Veja [session-handoff](../session-handoff/SKILL.md) para continuar e
[fleet-ladder](../fleet-ladder/SKILL.md) antes de despachar modelos realmente configurados.
