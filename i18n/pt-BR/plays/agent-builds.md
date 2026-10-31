# Agent Builds

Como construir um agente ou serviço que age por conta própria. A ideia central:
primitivas determinísticas fazem o trabalho pesado; o modelo só raciocina onde
raciocinar é a única coisa que funciona. Um design que é só LLM, com zero
primitivas, é inválido.

## Quando rodar

Ao construir qualquer agente, bot, worker ou serviço de longa duração — qualquer
coisa que segura ferramentas, chama a rede ou executa ações sem um humano
vigiando cada passo.

## Tarefa e limites compartilhados

Aplique este play dentro do pacote atual do
[BACKS Build Flow](../skills/backs-build-flow/SKILL.md). Mantenha um responsável
pela integração, `task_mode` solicitado, revisões base e candidata fixadas,
essência do operador e evidências atuais. Reutilize corpos pertinentes já carregados;
este play acrescenta gates do domínio sem reiniciar a tarefa.

[bounded-loops](../skills/bounded-loops/SKILL.md) cuida do prazo original e cotas
restantes entre retries, trabalhadores, modelos, revisões e handoffs. Nunca os
reinicie para um play aninhado. Ao esgotar, salve **STILL-BUILDING** com candidato,
evidências, gates pendentes e próxima ação. Continue trabalho útil autorizado só
dentro da cota restante; gate ausente não vira aprovação.

## A cadeia

1. Use intenção e essência do operador estabelecidas pelo Build Flow; missão
   e limites vêm do pedido inteiro e das correções atuais.

2. [understanding-gates](../skills/understanding-gates/SKILL.md) — na etapa de
   design, nomeie primeiro as PRIMITIVAS DE DOMÍNIO: toda capacidade central é
   uma função determinística, offline e fail-closed (falha fechado — nega em vez
   de deixar passar). Reserve o slot do LLM só para raciocínio de verdade.
3. [red-first](../skills/red-first/SKILL.md) — commite testes de contrato que
   falham para cada fronteira de IO tipada, antes de construí-la.
4. Construa seguindo a doutrina abaixo. Mantenha todo loop dentro de
   [bounded-loops](../skills/bounded-loops/SKILL.md): orçamentos, checkpoints,
   backoff e um kill-switch barulhento — nunca um retry martelando.
5. [sniper-testing](../skills/sniper-testing/SKILL.md) — derive escopo dos
   comandos reais de lint/tipos/tests pelo diff agregado fixado do candidato.
   Registre verificações ausentes e N/A justificados explicitamente. Só transporte
   de saída pode ser mockado, nunca roteamento, prompts nem parsing.

6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — os handlers de
   ferramenta e as funções de decisão do agente passam pelo gauntlet: score de
   risco abaixo do seu teto, depois mutação sobre os caminhos de decisão até
   zero sobreviventes. Lógica de branch que sobrevive a uma comparação invertida
   nunca foi testada de verdade.
7. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — painel independente
   aprova o agente antes da entrega. Escolha avaliadores ao vivo por capacidade
   e disponibilidade na matriz configurada; registre e exclua a execução autora.
   Revisam em sessões novas sem conversa nem contexto herdados do builder, que
   nunca avalia a si mesmo. Cada achado fundamentado recebe RED suplementar separado,
   preservando o original selado. Corrija e reconvoque dentro da mesma cota restante;
   todos os jurados exigidos precisam aprovar. Preserve passagem completa exigida
   das suites afetadas e prova real de entrega.

## A doutrina (o que o build precisa cumprir)

- Toda fronteira de IO declara um contrato tipado (entradas → saídas) e FALHA
  FECHADO — levanta erro ou nega diante de input ruim. Nunca falhe aberto, nunca
  engula um erro.
- Toda costura de rede é testável por cassete: embrulhe as chamadas de saída
  numa costura de gravação/replay, para a suíte rodar offline contra fixtures.
- Todo egress (tráfego de saída) passa por uma allowlist explícita de hostnames,
  negando por padrão. Host desconhecido levanta erro; nunca conecta em silêncio.
- Modele o agente como um fluxo de eventos tipado / máquina de estados, com
  estados de aprovação determinísticos (draft → review → ready → done) que o
  próprio agente calcula — uma primitiva, não fricção humana. Nenhuma ação pode
  pular seu estado.
- Confirme SOMENTE ações genuinamente destrutivas ou irreversíveis (gastar,
  apagar, um envio externo que não dá para desfazer) contra o estado commitado
  antes de disparar. Nunca trave uma ação benigna ou só de leitura, e nunca
  trave o humano — veja [decision-bar](../skills/decision-bar/SKILL.md).
- Persista o estado durável (objetivos, decisões, livro-razão) em disco, FORA da
  janela de contexto, e releia de lá. Nunca confie na memória em contexto ao
  longo de uma execução longa.
- Entregue um doc de operação que o agente carrega antes de cada tarefa — o
  arquivo mais próximo vence, com teto de tamanho — trazendo as regras que
  valem sempre.
- Falhas de ferramenta retornam um erro estruturado para o slot de raciocínio,
  para autocorreção. Um erro de ferramenta engolido é um bug.
- Privilégio mínimo: o agente carrega exatamente as ferramentas que a missão
  pede — nenhuma autoridade ambiente sobre filesystem ou rede.

## Gates duros

- Zero primitivas = design inválido; volte ao passo 2.
- Qualquer fronteira fail-open, fallback silencioso ou erro engolido bloqueia a
  entrega.
- Mutantes sobreviventes em caminhos de decisão bloqueiam a entrega.
- A revisão independente aprova em sessão nova separada do autor, sem conversa
  nem contexto herdados, escolhida ao vivo por capacidade e disponibilidade na
  matriz configurada. Registre e exclua a execução autora.


## Funciona bem com

- [root-cause-first](../skills/root-cause-first/SKILL.md) — quando o agente se comporta mal
- [session-handoff](../skills/session-handoff/SKILL.md) — estado durável do jeito certo

**Weight:** disciplina em sua maior parte free mais um portão light de design; o gasto heavy são as rodadas de mutação do gauntlet e o painel blind-tribunal — ele se paga em qualquer agente que vai agir sem ninguém olhando.
