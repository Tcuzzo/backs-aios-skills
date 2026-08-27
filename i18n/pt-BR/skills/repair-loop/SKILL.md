---
name: repair-loop
description: Use ao consertar um bug, fechar um issue reportado ou dar uplift numa costura de ponta a ponta. Roda o loop completo de reparo — aterrar no piso, reproduzir na verdade viva, teste de contrato vermelho, consertar a classe na costura, verificar no caminho real, avaliação independente, aterrissar — e itera até ser verdade. Trigger words: repair loop, dev mode, fix this, uplift, close the seam, dev build, loop de reparo, conserta isso, fechar a costura, modo dev.
license: MIT
---

# Repair Loop
**Effort:** light — o loop em si é disciplina mais uma passada de avaliação independente; os passos mais pesados que ele encadeia (gauntlet, tribunal) carregam os próprios selos e disparam só em mudanças que vão para produção. Remove: pousos verdes-mas-quebrados, e o retrabalho de bug reaberto que eles custam.

O loop padrão para qualquer conserto, fechamento de bug ou uplift. É um
comportamento, não maquinário de aprovação: adiciona zero portões e zero
atrito para o humano. Ele amarra o agente a uma disciplina que torna "verde
mas quebrado" estruturalmente difícil de sair.

## Carregue primeiro, antes de qualquer design ou edição

1. [invariant-floor](../invariant-floor/SKILL.md) — leia seu conjunto de regras antes de trabalhar.
2. [human-calibration](../human-calibration/SKILL.md) — aplique o perfil do humano; nunca o reinterrogue.
3. [understanding-gates](../understanding-gates/SKILL.md) — o planejador diagnóstico: Design → Plano → Build → Teste → Entrega.
4. [wayfinder](../wayfinder/SKILL.md) — quando perdido, trace a rota; nunca estacione uma pergunta no humano.
5. Se o pedido chega como prosa ou metáfora, rode [intent-compiler](../intent-compiler/SKILL.md) primeiro e itere sobre a diretiva deduzida.

## O loop

1. **Aterre no piso.** Carregue as regras e a verdade do próprio projeto
   (docs, fonte, tracker) antes de tocar em código. Trabalho feito de memória
   das regras não conta.
2. **Reproduza na verdade viva.** Veja a falha você mesmo, no caminho real
   que o humano usa — não uma sonda proxy, não a palavra do bug report. Sem
   reprodução, sem conserto.
3. **Teste de contrato vermelho.** Escreva um teste que falha capturando o
   defeito, e commite antes do conserto. Prove que está mesmo vermelho. O
   conserto o deixa verde; o conserto nunca edita o teste. Veja
   [red-first](../red-first/SKILL.md).
4. **Conserte a CLASSE na costura** — não um remendo pontual por sintoma. A
   fórmula completa vive em [seam-engineering](../seam-engineering/SKILL.md).
5. **Verifique no caminho real.** Confie, mas verifique. Capacidade se prova
   na superfície do próprio humano — a UI em que ele digita, o comando que
   ele roda — nunca num teste verde sobre uma costura mockada. Cheque toda
   alegação ("a outra branch já aterrissou isso", "aquele serviço está fora")
   contra a verdade viva antes de agir sobre ela.
6. **Meça o conserto.** No meio do loop, rode só os testes que cobrem a
   costura que você tocou — veja [sniper-testing](../sniper-testing/SKILL.md).
   Depois rode o [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) no
   código mudado: testes escopados, nota de complexidade-vs-cobertura, teste
   de mutação limitado. Um mutante que sobrevive ao seu conserto significa
   que o teste nunca alcançou o branch que você mudou — verde falso; continue
   iterando.
7. **Avaliação independente.** Um avaliador que não escreveu a mudança — de
   preferência um modelo de família diferente da do builder — precisa
   aprová-la. O builder nunca avalia o próprio trabalho. Veja
   [blind-tribunal](../blind-tribunal/SKILL.md).
8. **Cheque o trabalho concorrente.** Antes de alterar estado compartilhado,
   verifique que o trabalho em voo de qualquer outra sessão está preservado
   (numa branch ou commit). Nunca commite nem limpe trabalho que não é seu.
9. **Aterrisse.** Uma passada completa nas suítes dos módulos tocados na
   aterrissagem, depois commite. Feche todo achado que o loop levantou nesta
   costura — ou registre um veredicto explícito e com evidência de "não é
   bug" por achado. "Consertei o grande, adiei o resto" nunca aterrissa.

## Itere até ser verdade

Uma regra ainda não cumprida não para o loop — ela o move. Escale o modelo ou
o tier, remova o bloqueio, tente de novo, até cada passo acima ser verdade e a
mudança aterrissar. "Bom o bastante" não é status. Se travar de verdade duas
vezes na mesma costura, registre a evidência exata do bloqueio e vá para a
próxima peça desbloqueada — nunca moa em silêncio.

## Regras duras — qualquer uma derruba a skill

- Conserto entregue sem reprodução na verdade viva.
- Teste escrito depois do conserto, ou editado pelo conserto.
- Sintoma remendado enquanto a classe fica aberta na costura.
- Capacidade declarada verde por um proxy enquanto o caminho do próprio
  humano está quebrado.
- Builder avaliou a própria mudança.
- Um achado levantado adiado em silêncio na aterrissagem.
- Loop abandonado em "bom o bastante" em vez de escalado.

## Relatório

Duas palavras — **PROVEN** (provado) ou **STILL-BUILDING** (ainda construindo)
— mais a intenção em linguagem simples e a única decisão na frente do humano,
se houver. Perguntas vão ao humano só por gosto, visão ou risco destrutivo;
veja [decision-bar](../decision-bar/SKILL.md).

## Funciona bem com

- [incident-closure](../incident-closure/SKILL.md) — quando o humano reporta quebra, este loop roda dentro de um fechamento completo.
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
