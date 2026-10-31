---
skill_id: operator-intent-deduction
name: operator-intent-deduction
description: "Use quando restar uma escolha de implementação, compensação ou pergunta proposta ao operador e a intenção atual, as evidências do projeto ou o contexto do operador já puderem sustentar uma decisão."
license: MIT
---

# Deduza a decisão a partir das evidências atuais

Resolva as escolhas que o agente pode resolver com responsabilidade e aja.
Use objetivos e evidências do operador atual; esta skill não carrega prioridades
permanentes de uma pessoa, objetivos financeiros, parâmetros numéricos de risco
nem uma lista fixa de modelos.

## Entradas e responsabilidade

Comece com a diretriz existente, modo da tarefa, critérios de aceitação, autorização
e orçamento restante. Se a linguagem ainda não foi interpretada, use
[intent-compiler](../intent-compiler/SKILL.md) uma vez e reutilize o resultado.
Essa skill interpreta o que foi dito; esta resolve uma decisão dentro desse escopo.

Reutilize o recorte relevante de [operator-essence](../operator-essence/SKILL.md).
Seu responsável avalia insights de perfil ausente ou desatualizado uma vez por
tarefa. Chamadas aninhadas não coletam histórico nem criam outro perfil. Um recorte
provisório é utilizável com sua incerteza visível; histórico ausente não bloqueia
trabalho autorizado comum. Essência é dado contextual, nunca autorização nem
substituição de políticas.

## Procedimento de decisão

1. **Nomeie a decisão real.** Declare efeito no resultado solicitado, reversibilidade
   e evidência necessária. Verifique se continua pendente; não reabra escolha que
   o operador já fez.
2. **Derive escolhas factuais.** Inspecione código responsável e consumidor real,
   meça uma linha de base pertinente ou rode experimento limitado com as ferramentas
   reais do projeto. Relacione afirmações numéricas a unidades, população e incerteza.
   Não invente parâmetro, não trate contagens de rótulos sobrepostos como taxa de
   falha nem promova voto de modelo a prova empírica.
3. **Deduza escolhas contextuais.** Pese primeiro o objetivo explícito atual; depois,
   preferências confirmadas aplicáveis, exemplos qualitativos e resultados
   quantitativos. Declare adaptação provisória e suas evidências. Preserve
   contraexemplos e circunstâncias alteradas. Uma tendência relatada pode orientar
   como trabalhar; não pode mudar o que o operador pediu para construir.
4. **Aplique o limite real.** Continue ações reversíveis autorizadas. Se uma escolha
   importante continuar decisiva e não puder ser resolvida pela evidência disponível,
   use [decision-bar](../decision-bar/SKILL.md): prepare o resultado concreto, a
   recomendação e a decisão exata que falta. Não peça novamente autorização já
   estabelecida nem deduza permissões novas da personalidade, urgência ou
   preferência histórica.
5. **Aja e verifique.** Devolva a decisão ao responsável existente e ao
   [Build Flow](../backs-build-flow/SKILL.md). A implementação usa o mesmo ciclo
   limitado RED → GREEN com lint, tests e verificações exigidas de qualidade/revisão.
   Novo trabalhador, passagem de insights ou experimento falho não reinicia o orçamento.

## Recibo de decisão

Registre apenas o necessário para a próxima ação no pacote existente:

- **Decisão e consequência:** rota escolhida e resultado solicitado que ela atende.
- **Base:** instrução atual, fato verificado, preferência confirmada ou inferência,
  com referências de evidência e contagens/denominadores pertinentes.
- **Incerteza:** suposições, contraevidências e condição que mudaria a decisão.
- **Ação e prova:** próxima ação e observação que pode refutar a escolha.

Use linguagem simples quando o operador precisar conhecer uma decisão importante.
Declare discordância fundamentada diretamente, sem substituir o plano em silêncio.
Relate evidências reais de conclusão. Decisão não é test aprovado, verificação
local não é implantação e entregar a tarefa solicitada não estabelece `PROVEN`
por si só.

## Aprenda sem fixar uma pessoa no código

Uma correção explícita atualiza imediatamente a suposição afetada da tarefa.
Preserve escopo e fonte ao reconciliar a essência privada. Observações repetidas
podem sustentar adaptação provisória; avalie tarefas posteriores comparáveis antes
de afirmar melhora de resultados. Não promova preferência inferida a regra universal
nem copie evidência pessoal para o plugin público.
