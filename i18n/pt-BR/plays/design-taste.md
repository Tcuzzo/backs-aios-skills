# Design Taste

O play para construir qualquer UI que pareça desenhada, não gerada. UI genérica
é bug de WORKFLOW, não bug de modelo: separe a criação do gosto da
implementação, defina primeiro os design tokens exatos, dê olhos ao agente e
trave na acessibilidade.

## Quando rodar

Qualquer tela, página, componente, dashboard ou entrega visual que um humano vai
olhar. A primeira tela define o padrão de todas as que vêm depois — rode isto
antes dela.

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

1. Use intenção e essência estabelecidas pelo Build Flow para deduzir o gosto
   pedido nas palavras do humano. Declare a leitura uma vez antes de escrever.

2. [human-calibration](../skills/human-calibration/SKILL.md) — ancore a leitura
   no histórico do humano e em referências reais estudadas, nunca num chute
   demográfico.
3. Emita PRIMEIRO o arquivo de design tokens em três camadas, antes de qualquer
   componente — a spec completa de tokens e a lista de defaults banidos estão em
   [design-taste](../skills/design-taste/SKILL.md).
4. Construa os componentes com o arquivo de tokens injetado como restrição dura.
   Nunca chumbe um hex cru, um valor em pixel ou uma família de fonte dentro de
   um componente.
5. Execute o ciclo screenshot → crítico de [design-taste](../skills/design-taste/SKILL.md),
   resolvendo o modelo crítico ao vivo por [fleet-ladder](../skills/fleet-ladder/SKILL.md).
   Cada crítica e render consome o mesmo orçamento restante; devolva achados ao
   responsável atual.

6. Pontue a rubrica de gosto de 8 eixos conforme
   [design-taste](../skills/design-taste/SKILL.md).
7. Aplique o gate DURO de acessibilidade WCAG 2.2 conforme
   [design-taste](../skills/design-taste/SKILL.md).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — apenas código
   POR TRÁS dos pixels: resolvedores de tokens, trocas de tema, calculadoras de
   contraste e reducers de estado passam sem mutantes sobreviventes. Comparação
   invertida de contraste pode entregar tela linda e inacessível. O gauntlet não
   pontua gosto; rubrica e acessibilidade mantêm esse papel. Antes do gauntlet,
   use [sniper-testing](../skills/sniper-testing/SKILL.md) para comandos reais
   de lint/tipos/tests pelo diff agregado fixado. Declare N/A ou ausências honestamente.
   Renderize DOM real; render mockado não prova o que o humano vê. Preserve RED
   selado, acrescente tests suplementares separados para lacunas novas e mantenha
   revisão independente, passagem completa exigida das suites afetadas e prova
   real do render.

## Gates duros (específicos do play — as regras duras da própria skill valem por cima)

- O crítico trabalha em uma sessão nova e disjunta do autor; seu modelo é resolvido
  ao vivo pela fleet ladder; nunca um id de modelo fixado (um pin aposentado
  mata o crítico inteiro em silêncio).

## Funciona bem com

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — avalie a entrega inteira
- [sniper-testing](../skills/sniper-testing/SKILL.md) — dê escopo aos testes de componente

**Weight:** light ao longo do loop — a calibração e a passada do crítico de screenshot custam uma execução extra cada; o passo heavy é o gauntlet no código atrás dos pixels — ele se paga em qualquer tela que um humano vai olhar de verdade.
