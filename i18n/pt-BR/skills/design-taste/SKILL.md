---
name: "design-taste"
description: "Use antes de construir qualquer coisa visual — um site, app, dashboard, console ou deck — para que saia com gosto de verdade em vez dos defaults genéricos de IA. Trigger words: design, UI, taste, design tokens, design system, accessibility, WCAG, screenshot critique, dark mode, restyle, gosto, acessibilidade, crítica de screenshot, modo escuro, restilizar."
license: "MIT"
---

# Design Taste — Tokens Primeiro, Olhos no Resultado, Acessibilidade Dura
**Effort:** light — um arquivo de tokens antes de qualquer componente, mais uma passada screenshot → crítico de visão por superfície renderizada. Remove: reentregar os defaults genéricos de IA — o retrabalho de restilizar e o retrofit de acessibilidade depois da entrega.

UI genérica é bug de workflow, não bug de modelo. Conserte estruturalmente: leia o
brief como spec, fixe design tokens exatos antes de qualquer componente, proíba os
defaults pelo nome, dê olhos ao builder com um loop de screenshot, e feche o
portão na acessibilidade — duro.

## Quando rodar

- Qualquer pedido "constrói pra mim um / desenha pra mim um …" que renderiza pixels.
- Antes de montar um frontend ou uma entrega voltada a cliente.
- Quando uma superfície existente parece genérica e precisa de uma direção
  específica e defensável.

## Passos

1. **Leia o brief como spec.** Uma metáfora, uma cadência, uma era, artista ou
   lugar nomeado nas palavras do humano é restrição concreta de design, não
   decoração. A disciplina completa de ler o brief: [intent-compiler](../intent-compiler/SKILL.md).
2. **Escolha uma direção com chão.** Escolha uma referência *lead* (um design
   system ou biblioteca real que fixa a base estrutural) e uma referência *accent*
   (uma que carimba a assinatura por cima). As duas precisam ser reais e atuais,
   com assinatura de gosto verificável. Um clima inventado reprova o portão fechado.
3. **Emita tokens PRIMEIRO.** Antes de qualquer componente, escreva um arquivo de
   design tokens legível por máquina, em três camadas (primitivo → semântico →
   componente; formato W3C de tokens, `$value` + `$type`). Fixe de cara: uma rampa
   de cor perceptualmente uniforme (Oklch — um espaço de cor onde passos iguais
   parecem iguais), uma escala tipográfica de verdade numa fonte não-default, um
   incremento único de espaçamento (base 4px → 4/8/12/16/24/32/48/64), uma escala
   de raio, uma escala de elevação, e tokens de movimento nomeados (duração +
   easing por entrada / scroll / mudança de estado; honre `prefers-reduced-motion`).
   Dark e light são de primeira classe e ambos resolvem dos MESMOS tokens semânticos.
4. **Proíba os defaults genéricos pelo nome.** Proibição vence adjetivo: nada de
   fonte de reflexo default (Inter/Roboto), nada de gradiente roxo, nada de hero
   centralizado, nada de fileira de três cards iguais, nada de bloco cinza sobre
   branco. Adicione sua própria lista banida por projeto.
5. **Construa sob restrição.** Componentes consomem só tokens. Um hex cru, px ou
   família de fonte hardcoded dentro de componente é defeito.
6. **Feche o loop screenshot → crítico de visão.** Para qualquer coisa renderizada:
   renderize num navegador headless em larguras mobile e desktop, tire screenshot,
   e ponha um modelo de visão para pontuar — depois conserte, em passadas separadas
   (crítica → conserto estrutural → auditoria → polimento), nunca de uma vez só. O
   crítico é um avaliador: use um modelo de família diferente da do builder,
   pontuando eixos nomeados, nunca uma nota holística única. Resolva o modelo
   crítico da config na hora da chamada — um id de modelo pinado aposenta um dia e
   leva o loop inteiro junto.
7. **Pontue a rubrica de gosto de 8 eixos.** 0–3 por eixo, e todo eixo tem que
   pontuar ≥ 2: aderência-a-tokens · layout/hierarquia · tipografia ·
   cor/contraste · movimento · paridade dark-light · acessibilidade · o teste de
   estômago desenhado-vs-média ("isto parece desenhado, ou parece a média de
   tudo?"). Um eixo abaixo de 2 = não está pronto.
8. **Aplique o portão DURO de acessibilidade (WCAG 2.2).** Alvos de ponteiro
   ≥ 24×24 px CSS. Indicador de foco visível ≥ 2px de perímetro com contraste
   ≥ 3:1. Contraste de texto ≥ 4.5:1 normal, ≥ 3:1 texto grande e componentes de
   UI. Totalmente navegável por teclado. Contraste verificado nos DOIS temas. Isto
   é portão, não sugestão: falhou = não entrega.
9. **Teste o código atrás dos pixels.** Resolvedores de token, trocas de tema,
   calculadoras de contraste e reducers de estado ganham testes reais sobre DOM
   renderizado de verdade — uma comparação invertida num cheque de contraste
   entrega uma tela linda silenciosamente inacessível. Testes julgam o código; a
   rubrica e o portão WCAG julgam o gosto.

## Regras duras — qualquer uma delas reprova a skill

- Componente escrito antes de o arquivo de tokens existir.
- Hex cru / px / família de fonte dentro de componente.
- Qualquer item da lista de defaults banidos aparecendo na saída.
- Pular o loop screenshot → crítico para qualquer coisa renderizada.
- O builder avaliando os próprios visuais, ou uma nota holística única em vez de eixos.
- Qualquer eixo da rubrica abaixo de 2, ou qualquer cheque WCAG 2.2 falhando, na hora de entregar.
- Uma direção de gosto que não se ancora numa referência real e verificável.

## Combina bem com

- [intent-compiler](../intent-compiler/SKILL.md) — a disciplina completa de ler o brief.
- [blind-eval](../blind-eval/SKILL.md) — manter-ou-reverter quando a questão é gosto.
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — endurecendo o código atrás dos pixels.
- [blind-tribunal](../blind-tribunal/SKILL.md) — avaliação cross-family antes de aterrissar.

> Crédito de scaffold: W3C Design Tokens Community Group (formato de tokens);
> WCAG 2.2, W3C (portão de acessibilidade); UICrit, UIST 2024 (crítica de UI
> pontuada por eixos); AI Jason, & JackJack. (2025). superdesign: AI design agent
> [Computer software]. GitHub. https://github.com/superdesigndev/superdesign
> (AGPL-3.0; dual-licensed with a commercial enterprise license) — a ideia de
> proibir os defaults. A composição e as regras duras daqui são do BACKS AIOS.
