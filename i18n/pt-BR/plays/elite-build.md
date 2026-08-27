# Elite Build — o play mestre

O play padrão para qualquer pedido de "constrói X", "conserta X" ou "melhora X".
O humano declara o objetivo uma vez; este play monta o ambiente inteiro para que
ele nunca precise re-explicar a base. Leia a intenção, carregue o humano, trave
o plano, prove o vermelho, construa, teste apertado, meça, avalie às cegas,
pouse com prova ao vivo.

## Quando rodar

Qualquer build, fix ou melhoria com risco real. Uma edição trivial de uma linha
pode pular direto para [sniper-testing](../skills/sniper-testing/SKILL.md) e
pousar.

## A cadeia

0. [optimus](../skills/optimus/SKILL.md) — suba o harness antes de qualquer
   edição. O piso carrega primeiro, toda sessão, toda vez.
1. [intent-compiler](../skills/intent-compiler/SKILL.md) — leia o pedido como a
   spec, inteiro. Deduza a intenção antes de levantar qualquer decisão de
   entrega ou de opção. Nunca apresente um menu de opções quando existe uma
   solução clara — resolva.
2. [human-calibration](../skills/human-calibration/SKILL.md) — carregue o perfil
   validado do humano e aplique. Nunca re-interrogue um humano que você já
   conhece.
3. [understanding-gates](../skills/understanding-gates/SKILL.md) — Design →
   Plano → Build → Teste → Entrega, cada etapa com gate. Antes de qualquer
   design: leia o que já existe via
   [live-research](../skills/live-research/SKILL.md), reutilize o que está
   escrito, mapeie a topologia inteira. A resposta quase sempre já está escrita.
4. [wayfinder](../skills/wayfinder/SKILL.md) — quando se perder em qualquer
   passo, trace a rota a partir da evidência. Nunca estacione no humano uma
   pergunta que a evidência responde.
5. [red-first](../skills/red-first/SKILL.md) — escreva o teste de contrato que
   falha e commite ANTES de qualquer builder rodar. O builder não pode tocar
   nesse teste.
6. Construa. Espalhe lanes paralelas por padrão — nunca serialize o que pode
   rodar junto. Cada lane ganha seu próprio branch de rascunho ou worktree.
   Sozinho, numa sessão só? Uma lane É o fan-out — construa num branch de
   rascunho e siga. (Um worktree é um segundo checkout do mesmo repositório em
   outra pasta, para dois builders nunca tocarem nos mesmos arquivos.) Resolva
   os builders por [fleet-ladder](../skills/fleet-ladder/SKILL.md); combine os
   rascunhos com [model-fusion](../skills/model-fusion/SKILL.md). Para um bug,
   rode o [repair-loop](../skills/repair-loop/SKILL.md) e feche a CLASSE na
   costura compartilhada, conforme
   [seam-engineering](../skills/seam-engineering/SKILL.md).
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — só execuções com escopo
   enquanto itera; o passe completo dos módulos tocados espera o pouso
   (passo 10).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — meça antes de
   pousar: suíte sniper, score de risco complexidade-vezes-cobertura abaixo do
   seu teto, depois teste de mutação até zero sobreviventes. Meça o código;
   nunca avalie no olho.
9. [blind-eval](../skills/blind-eval/SKILL.md), depois
   [blind-tribunal](../skills/blind-tribunal/SKILL.md) — um envelope com a
   autoria apagada vai para avaliadores de uma família de modelos diferente da
   do builder. Quem constrói nunca avalia o próprio trabalho. Cada achado de
   jurado vira um novo teste vermelho; reconvoque até todo jurado aprovar. Rig
   solo? Degrade conforme a regra "Solo rig" do blind-tribunal — e nomeie o gate
   enfraquecido no relatório de pouso.
10. Pouse — faça um merge limpo, rode UM passe completo das suítes dos módulos
    tocados, reinicie o serviço real e prove o comportamento na superfície do
    próprio humano (a página que ele carrega, o comando que ele roda) — nunca
    uma sonda proxy. Depois reporte.

## Gates duros (qualquer um vermelho bloqueia o pouso)

- O teste que falha foi commitado antes do build e está intocado — o avaliador
  verifica que o diff do arquivo de teste está vazio.
- Quem constrói nunca avalia, e o avaliador é de outra família de modelos.
- Todo achado levantado é fechado, ou adjudicado como "não é bug" com evidência
  registrada. Nunca adiado em silêncio. Fechamento da costura inteira — a
  costura é o ponto compartilhado do código onde essa classe de bug mora — ou
  não há pouso.
- Prova ao vivo na superfície real do humano. Teste verde com capacidade
  quebrada é fracasso, não sucesso.
- Reporte em duas palavras — PROVEN ou STILL-BUILDING — em
  [human-voice](../skills/human-voice/SKILL.md). Proven significa pousado, mais
  avaliado de forma independente, mais demonstrado ao vivo.
- Commite só os arquivos desta mudança — nunca o trabalho em andamento de outra
  sessão.

## Funciona bem com

- [optimus](../skills/optimus/SKILL.md) — re-suba o piso depois de uma compactação ou de um restart
- [invariant-floor](../skills/invariant-floor/SKILL.md) — o piso travado que todo pouso precisa cumprir
- [decision-bar](../skills/decision-bar/SKILL.md) — o que chega ao humano vs. o que executa direto
- [bounded-loops](../skills/bounded-loops/SKILL.md) — orçamentos e kill-switches em execuções longas
- [session-handoff](../skills/session-handoff/SKILL.md) — sele o estado antes de parar

**Weight:** a pilha completa — disciplina free, portões light e três passos heavy (model fusion, o gauntlet, o tribunal) — o gasto heavy se paga em qualquer coisa que vai para produção, que é exatamente para isso que este play existe.
