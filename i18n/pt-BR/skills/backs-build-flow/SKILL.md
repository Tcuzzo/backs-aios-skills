---
name: backs-build-flow
description: "Use ao construir, corrigir, revisar, retomar ou entregar trabalho que exige coordenar contexto, skills e verificação sem perder o ritmo da execução."
license: MIT
---

# BACKS Build Flow

Um único responsável pela integração leva o pedido do contexto à entrega
verificada. As skills especialistas devolvem evidências a esse responsável;
não reiniciam o fluxo. Para uma resposta simples sem construção nem investigação,
use apenas os passos pertinentes.

## Reúna contexto suficiente para agir

1. Preserve o objetivo, as restrições, a autorização existente e o resultado
   solicitado pelo usuário. Escolha um modo: **construir/corrigir**, **revisão
   somente leitura**, **investigar** ou **retomar/entregar**. Uma revisão não
   autoriza edições, instalação nem implantação.
2. Reutilize um pacote de tarefa atual. Caso não exista, use
   [context-engineer](../context-engineer/SKILL.md) para verificar o alvo, as
   instruções vigentes, o caminho afetado de chamadas e consumidores, o trabalho
   existente e a verificação de aceitação.
   [building-with-backs](../building-with-backs/SKILL.md) resolve checkout e
   promoção. Fixe o `base_sha` anterior à mudança; atualize `candidate_sha` à
   medida que o trabalho recebe commits.
3. Aplique [operator-essence](../operator-essence/SKILL.md) ao operador atual:
   carregue o recorte relevante de contexto ou execute uma única vez a inicialização
   por insights para perfil ausente. Observações qualitativas e evidências
   quantitativas orientam comunicação e verificação; não concedem autoridade nem
   fixam uma persona. Marque evidências escassas como provisórias e continue o
   trabalho útil autorizado. Use [intent-compiler](../intent-compiler/SKILL.md)
   apenas para intenção ambígua; [operator-intent-deduction](../operator-intent-deduction/SKILL.md)
   decide se uma escolha material ainda pendente realmente precisa do operador.
4. **Comece a executar quando puder nomear o alvo, a próxima ação concreta, as
   restrições e uma verificação observável de aceitação.** Leitura adicional
   precisa resolver uma pergunta específica que possa mudar essa ação. Não mapeie
   todo o repositório repetidamente.

## Encaminhe as skills uma vez, com resultado e condição de saída

Carregue os corpos reais das skills pertinentes; um nome ou recibo isolado não
comprova aplicação. Reutilize corpos e evidências ainda presentes e atuais no
contexto. Após compactação, recarregue apenas o necessário para a próxima ação.
Para cada especialista, declare propósito, evidência esperada e condição de saída;
leia referências profundas sob demanda. Um único pacote atual acompanha
responsabilidade, estado e próxima ação
([formato do pacote e handoff](references/task-packet.md)). Evite registros duplicados.

Para adoção, [absorb](../absorb/SKILL.md) cuida do mapa de capacidades e da integração
nativa. [rea-investigation](../rea-investigation/SKILL.md) fornece evidências de
descoberta ou verificação quando pertinente; retorna ao chamador sem iniciar
Absorb recursivamente. Trabalho comum com código-fonte usa diretamente código e tests.

## Execute o ciclo limitado RED → GREEN

Vincule [bounded-loops](../bounded-loops/SKILL.md) antes dos retries: um
`mission_id`, prazo, cota de tentativas/rodadas e orçamento restante de recursos.
Trabalhadores filhos, trocas de modelo, achados de reparo e rodadas de revisão
consomem essa mesma cota.

1. **RED:** [red-first](../red-first/SKILL.md) estabelece uma verificação real de
   comportamento que falha antes da correção. Preserve o arquivo selado e a
   identidade da linha de base. Para revisão ou pesquisa, use o contrato de
   evidência sem fabricar edições.
2. **Construção:** implemente a menor mudança completa na costura responsável;
   atualize consumidores afetados e superfícies de compatibilidade. Preserve
   trabalho não relacionado.
3. **Lint e tests:** [sniper-testing](../sniper-testing/SKILL.md) deriva o escopo
   de `base_sha` até o candidato atual, incluindo trabalho pendente pertinente.
   Execute lint, verificação de formato, tipos e tests de comportamento aplicáveis
   do repositório. Registre comandos exatos, revisão, resultados e verificações
   indisponíveis ou inaplicáveis. Uma árvore limpa não apaga o escopo já commitado.
4. **Qualidade:** [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) usa o mesmo
   escopo e orçamento para qualidade medida, mutação isolada e limitada e revisão
   independente. Acrescente tests suplementares para novas lacunas sem reescrever
   o RED selado.
5. **Responda à evidência:** corrija um achado comprovado e execute novamente apenas
   verificações afetadas. Falhas idênticas repetidas exigem outra hipótese ou tática.
   Ao esgotar limites, salve um checkpoint do trabalho pendente; nunca reinicie o
   orçamento nem reduza as verificações.

Use os gates agregados de integração exigidos pelo repositório quando o candidato
estabilizar. Relate as capacidades reais deste ambiente; não invente ferramentas,
tests nem revisões.

## Conclua o resultado solicitado

Continue com empacotamento, commit, publicação e verificação autorizados quando
fizerem parte do pedido. Quando aprovação externa for realmente necessária,
prepare primeiro o resultado completo e revisável. Mantenha o usuário informado
sobre achados, ação atual, evidências e onde inspecionar o trabalho em andamento;
siga a cadência solicitada.

Diferencie **tarefa solicitada entregue** do estado de capacidade **PROVEN** do
piso de invariantes. Um patch local ou uma revisão concluídos não implicam
implantação em produção. Gates obrigatórios com falha ou indisponíveis continuam
visíveis: registre **STILL-BUILDING** com bloqueio exato, cota restante e próxima
ação. Em modo somente leitura, devolva o pacote na resposta ou em um registro
externo já autorizado; não crie implicitamente um registro no repositório nem
um arquivo de essência.
