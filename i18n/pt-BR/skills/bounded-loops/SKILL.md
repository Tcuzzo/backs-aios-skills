---
name: "bounded-loops"
description: "Use antes de iniciar qualquer loop que possa fazer retry, poll, iterar ou chamar uma API externa — loops de agente, loops de conserto, agendadores, watchers. Declara tetos de orçamento, faz checkpoint na exaustão e torna martelar estruturalmente impossível. Trigger words: bounded loop, budget, ceiling, retry, backoff, rate limit, throttle, kill-switch, checkpoint, runaway, infinite loop, spin, budget exhaustion, loop limitado, orçamento, teto, limite de taxa, loop infinito, exaustão de orçamento, loop descontrolado."
license: "MIT"
---

# Bounded Loops
**Effort:** free — tetos e checkpoints declarados antes de o loop começar; corta custo na raiz. Remove: gasto de loop descontrolado — cota queimada, rotas bloqueadas por 429 e progresso que um crash apaga.

Um loop sem limite é o bug mais caro que um agente pode entregar. Ele queima
orçamento, martela provedores até ser bloqueado, e esconde a própria falha dentro
do giro. Todo loop ganha um teto, um checkpoint e um jeito barulhento de morrer —
antes de começar.

## Quando rodar

Antes de iniciar qualquer loop: um loop de conserto, um wrapper de retry, um
poller, um agendador, uma execução autônoma multi-passo, qualquer coisa que possa
reemitir uma chamada ou tentar um passo de novo.

## Os passos

1. **Declare o orçamento primeiro.** Tokens, custo, tempo de relógio e máximo de
   tentativas — por escrito, antes da primeira iteração. Loop sem orçamento
   declarado é sem limite por definição e não começa.
2. **Limite as rodadas internas.** Um episódio interno (um ciclo LLM/tool sobre um
   problema) ganha um teto pequeno e fixo de rodadas (por volta de 4). O teto limita
   o episódio, não a missão — trabalho inacabado sobe de nível, não fica moendo.
3. **Checkpoint em cada iteração.** Estado durável em disco — manifesto da
   execução, log de evidências, passo atual — nunca memória de chat. Qualquer um
   (incluindo uma sessão nova) consegue retomar do último checkpoint.
4. **Na exaustão: checkpoint, depois escale.** Entregue o checkpoint ao loop
   externo ou ao seu humano com o que foi feito, o que falta e o bloqueio. Nunca
   continue em silêncio depois do orçamento. Nunca pare em silêncio, também —
   exaustão é barulhenta.
5. **Respeite toda API externa.** Antes da primeira chamada, aprenda o rate limit e
   a quota do provedor; quando desconhecidos, trate como estritos — uma chamada,
   espaçamento largo — até medir. Faça throttle em toda chamada, cacheie e reuse
   respostas, e segure um teto duro por janela.
6. **Recue exponencialmente quando levar pushback.** Um 429 ou 503 significa
   esperar, depois esperar mais. Zero retry instantâneo no mesmo endpoint. Um retry
   apertado contra um endpoint é como uma rota que funciona morre: queima quota e
   pode fazer bloquearem seu endereço de saída inteiro.
7. **Carregue um kill-switch barulhento e limitado.** Qualquer loop que possa
   reemitir uma chamada tem um número máximo de tentativas; quando bate, o loop
   para ALTO com a evidência — nunca um giro infinito ou silencioso.
8. **Pare e enfileire só em pontos seguros.** Parar significa checkpoint-depois-
   cancelar. Trabalho novo entra na fila para o próximo ponto seguro (uma fronteira
   de estado entre passos) — nunca injetado no meio de um passo. Uma instância de
   loop, um escritor, escritas de estado atômicas.

## Regras duras (o que reprova esta skill)

- Um loop que começa sem orçamento declarado de tokens / custo / tempo / tentativas.
- Continuar depois de um orçamento esgotado, em silêncio ou não, sem escalar.
- Retry instantâneo contra o mesmo endpoint, ou qualquer caminho de retry sem backoff.
- Loop de retry sem teto de tentativas, ou um teto que falha quieto quando bate.
- Estado de progresso guardado só na memória da conversa — um crash apaga a execução.
- Duas instâncias de loop escrevendo o mesmo estado, ou escritas de estado não atômicas.
- Escapar do loop enfraquecendo os próprios cheques de saída — um verde produzido
  abaixando a barra, apagando dados ou engolindo erros é falso verde, não saída.

## Combina bem com

- [optimus](../optimus/SKILL.md) — carregue o piso antes de qualquer loop começar.
- [repair-loop](../repair-loop/SKILL.md) — o principal consumidor destes tetos.
- [fleet-ladder](../fleet-ladder/SKILL.md) — fallback limitado entre modelos, não martelar um só.
- [session-handoff](../session-handoff/SKILL.md) — aquilo em que um checkpoint escala.
