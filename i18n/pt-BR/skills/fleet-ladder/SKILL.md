---
name: "fleet-ladder"
description: "Guia de seleção por papel e capacidade antes do despacho; o pacote público não inclui resolvedor nem executável Fleet. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability, frota, escada, despacho, modelo fora, provedor fora, qual modelo, disponibilidade."
license: "MIT"
---

# Fleet Ladder
**Effort:** light — uma sonda viva, com cache, do degrau antes de qualquer despacho. Remove: despachos para provedores mortos, e nomes de modelo hardcoded nos pontos de chamada que quebram no dia em que o modelo se aposenta.

Esta skill descreve a seleção, mas não resolve modelos por conta própria. O pacote público não inclui resolvedor nem executável Fleet; registre qualquer função ausente como lacuna do runtime. Não fixe IDs de modelos em skills, prompts ou pontos de chamada.

## Quando rodar

- Antes de QUALQUER despacho para um modelo: build, avaliação, review ou job limitado de worker.
- Quando um provedor caiu e você precisa saber o que cai para o quê.
- No momento em que você se pega digitando um nome de modelo em código ou num template de prompt.

## Os passos

1. **Declare papel e capacidades.** Leia a escada configurada e sua ordem; escolha candidato adequado à tarefa, capacidade e disponibilidade. A configuração de exemplo é apenas um modelo. Esta skill não classifica nem filtra candidatos.
2. **Verifique a independência.** A revisão usa uma execução nova e separada do autor, com um pacote congelado sem contexto do autor. Escolha um revisor capaz pela escada configurada. Registre restrições adicionais como lacunas do runtime.
Qualquer revisor capaz pode realizar a revisão em uma sessão nova e separada da do autor; o modelo e o fornecedor não são restrições.
3. **Teste inferência real.** Uma lista de modelos não prova inferência, capacidade ou cota. Execute inferência real e limitada no candidato; mantenha o resultado em cache por prazo razoável e respeite o backoff. Verifique novamente a capacidade no fallback.
4. **Desça a escada, alto.** Despache para o melhor degrau DISPONÍVEL. Em falha de
   transporte, reporte a falha alto, depois tente o próximo degrau. Nunca pule em
   silêncio — o registro tem que mostrar quais degraus falharam e por quê.
5. **Exaustão falha alto.** Se todo degrau está fora, levante um erro claro
   nomeando o que foi tentado. Um job que não pode ser despachado nunca tem sucesso
   em silêncio, espera para sempre, nem degrada para uma resposta inventada.
6. **Registre a proveniência.** Anexe todo despacho a um log: papel, modelo
   escolhido, degraus pulados e por quê. Depois você tem que conseguir responder
   "quem de fato fez este trabalho?"

## Regras duras — quebrou uma e a skill falhou

- Não fixe IDs de modelos em skills, prompts ou chamadas; use papel e capacidades da configuração ativa.
- Uma inferência real e limitada é necessária; apenas o catálogo não basta.
- A revisão exige execução nova separada do autor e pacote congelado sem contexto do autor.
- Registre falhas e alternativas; reporte resolvedores ou isolamento ausentes como lacunas do runtime.


## Combina bem com

- [blind-tribunal](../blind-tribunal/SKILL.md)
- [bounded-loops](../bounded-loops/SKILL.md)
- [model-fusion](../model-fusion/SKILL.md)
