---
name: intent-compiler
description: "Use quando um pedido vier como prosa comprimida, metáfora, gíria, abreviação ou referência ambígua e o agente precisar de uma diretriz técnica fundamentada; também quando uma correção mudar a capacidade desejada ou a conclusão solicitada."
license: MIT
---

# Compile o pedido atual

Traduza o que o operador disse para um contrato executável, declare brevemente a
interpretação e continue o trabalho. Uma expressão comprimida pode conter uma
especificação completa. O operador não precisa reescrevê-la como ticket de engenharia.

## Uma interpretação para a tarefa atual

Se o pacote já contém uma diretriz e nenhuma instrução nova a altera, reutilize-a.
Esta skill interpreta a linguagem;
[operator-intent-deduction](../operator-intent-deduction/SKILL.md) resolve uma
decisão pendente dentro da diretriz. Nenhuma reinicia o fluxo completo da outra.

### 1. Analise as palavras reais

Extraia capacidade solicitada, ação, superfícies nomeadas, quantidades, restrições
e conclusão observável. Marque referências e metáforas não resolvidas. Repetição
pode sinalizar ênfase sem criar outra tarefa. O tom pode expressar urgência;
não estabelece permissão, tolerância a risco, competência nem identidade.

Interprete linguagem figurada no contexto real da tarefa. Pedir «queima tudo»
pode se referir a uma abordagem; por si só não autoriza apagar dados. Responda
com clareza sem imitar um dialeto nem inventar uma persona.

### 2. Resolva apenas incertezas que afetam a ação

Use esta ordem dentro das instruções vigentes:

1. Pedido explícito atual e correções do operador.
2. Escopo e autorização estabelecidos nesta conversa.
3. Fatos, alvos, contratos e estado atual verificados do projeto.
4. Preferências confirmadas e observações sustentadas relevantes de
   [operator-essence](../operator-essence/SKILL.md).
5. Inferência provisória claramente identificada quando as evidências forem poucas.

Se a essência estiver ausente ou desatualizada, seu responsável faz uma única
passagem suportada de insights e devolve um recorte provisório ou atual. Reutilize
esse resultado nas skills aninhadas; não colete histórico repetidamente.
Preferências históricas não podem anular instrução nova. Fatos do código podem
limitar a rota sem reduzir o objetivo.

Evidências qualitativas estabelecem significado e contexto de uma preferência.
Evidências quantitativas podem descrever resultados repetidos em sua população
declarada. Contagens isoladas não decidem o que o operador quis dizer; uma tendência
inferida em relatório não é uma instrução confirmada por ele.

### 3. Produza a diretriz

Carregue estes campos no pacote existente, sem criar um segundo plano:

| Campo | Conteúdo obrigatório |
| --- | --- |
| Capacidade desejada | O que o operador quer que exista ou aprender. |
| Limite atual | O que o estado verificado e as capacidades disponíveis permitem hoje. |
| Rota agora | A próxima ação útil sob a autorização existente. |
| Rota depois | Dependências restantes para a capacidade completa. |
| Contrato da tarefa | Modo, alvo, limites, conclusão solicitada e evidência de aceitação. |
| Incerteza | Incógnitas decisivas e evidências que podem resolvê-las. |

Mantenha visível a capacidade desejada completa quando uma dependência externa
limitar a rota atual. Uma revisão produz achados; não vira reparo silenciosamente.

## Declare a interpretação e aja

Use uma frase simples quando a interpretação importar:

> Leitura: atualizar a integração existente, preservar sua interface pública e verificar o consumidor real antes da publicação.

Identifique inferências frágeis quando necessário. Prossiga com trabalho reversível
justificado pela evidência. Resolva incerteza factual por inspeção ou experimento
focado. Se faltar autorização decisiva ou houver escolha realmente pendente do
operador, faça a preparação disponível e apresente uma recomendação concreta e
uma pergunta; consulte [decision-bar](../decision-bar/SKILL.md). Uma preferência
antiga não supre permissão ausente para uma nova ação importante.

Devolva a diretriz ao [Build Flow](../backs-build-flow/SKILL.md). Invoque dedução de
intenção apenas para uma decisão real restante. Uma correção posterior atualiza
o pacote e as evidências pertinentes da essência; não substitui silenciosamente
o objetivo nem reinicia o orçamento restante da missão.
