# Design Taste

O play para construir qualquer UI que pareça desenhada, não gerada. UI genérica
é bug de WORKFLOW, não bug de modelo: separe a criação do gosto da
implementação, defina primeiro os design tokens exatos, dê olhos ao agente e
trave na acessibilidade.

## Quando rodar

Qualquer tela, página, componente, dashboard ou entrega visual que um humano vai
olhar. A primeira tela define o padrão de todas as que vêm depois — rode isto
antes dela.

## A cadeia

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — deduza QUAL gosto as
   palavras do próprio humano pedem, e declare essa leitura em uma linha antes
   de escrever.
2. [human-calibration](../skills/human-calibration/SKILL.md) — ancore a leitura
   no histórico do humano e em referências reais estudadas, nunca num chute
   demográfico.
3. Emita PRIMEIRO o arquivo de design tokens em três camadas, antes de qualquer
   componente — a spec completa de tokens e a lista de defaults banidos estão em
   [design-taste](../skills/design-taste/SKILL.md).
4. Construa os componentes com o arquivo de tokens injetado como restrição dura.
   Nunca chumbe um hex cru, um valor em pixel ou uma família de fonte dentro de
   um componente.
5. Rode o loop screenshot → crítico conforme
   [design-taste](../skills/design-taste/SKILL.md), resolvendo o modelo crítico
   ao vivo por [fleet-ladder](../skills/fleet-ladder/SKILL.md).
6. Pontue a rubrica de gosto de 8 eixos conforme
   [design-taste](../skills/design-taste/SKILL.md).
7. Aplique o gate DURO de acessibilidade WCAG 2.2 conforme
   [design-taste](../skills/design-taste/SKILL.md).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — só no código
   POR TRÁS dos pixels: resolvedores de token, trocas de tema, calculadoras de
   contraste e reducers de estado passam com zero mutantes sobreviventes. Uma
   comparação invertida num check de contraste entrega uma tela linda e
   inacessível. O gauntlet nunca pontua gosto — a rubrica e o gate de
   acessibilidade seguem sendo os juízes do visual. Renderize DOM de verdade nos
   testes; um render mockado não prova nada sobre o que o humano vê.

## Gates duros (específicos do play — as regras duras da própria skill valem por cima)

- O crítico é de uma família de modelos DIFERENTE da de quem constrói, resolvido
  ao vivo pela fleet ladder — nunca um id de modelo fixado (um pin aposentado
  mata o crítico inteiro em silêncio).

## Funciona bem com

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — avalie a entrega inteira
- [sniper-testing](../skills/sniper-testing/SKILL.md) — dê escopo aos testes de componente
