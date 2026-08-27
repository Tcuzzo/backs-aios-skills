---
name: understanding-gates
description: Use quando um build, conserto ou uplift está indo da intenção para a entrega e você precisa de prova de que ainda bate com o pedido original. Interroga Design, Plano, Build, Teste e Entrega com veredictos de aprovar/revisar/rejeitar, falhas nomeadas como alvos de reparo e uma nova rodada depois de cada reparo. Trigger words: understanding, stage gates, validate build, spec match, verdict, green but wrong, echo check, done means done, portões de estágio, validar o build, veredicto, verde mas errado, pronto é pronto.
license: MIT
---

# Understanding Gates

Uma disciplina de validação para builds. Ela interroga o trabalho em cinco
estágios — Design, Plano, Build, Teste, Entrega — sempre contra o pedido
ORIGINAL, nunca contra a reformulação que o próprio trabalho fez dele. Cada
portão devolve evidência: notas, um veredicto, falhas nomeadas e ações de
reparo. Ele amarra o agente, não o humano: nenhum passo novo de aprovação,
nenhum atrito para quem pediu.

## Quando rodar

- Qualquer build, conserto ou uplift que vai aterrissar em algum lugar real.
- Toda vez que você está prestes a dizer "pronto" e a única prova é um teste
  verde.
- Depois de cada reparo, no mesmo estágio que falhou.

## Estágio 0 — ancore a intenção

Antes de pontuar qualquer coisa, fixe a âncora de comparação: as palavras
ORIGINAIS do humano, mais uma diretiva traduzida de uma linha (veja
[intent-compiler](../intent-compiler/SKILL.md)). Todo portão pontua contra
essa âncora. Nunca pontue contra a sua própria paráfrase — paráfrase deriva,
e aí cada portão valida em silêncio a deriva em vez do pedido.

## Os cinco portões

Cada portão faz uma pergunta contra a intenção original:

| Estágio | Pergunta |
| --- | --- |
| Design | A spec está clara e fiel ao pedido original? |
| Plano | O plano responde à intenção e cabe na superfície onde vai entrar? |
| Build | O código satisfaz a spec sem deriva? |
| Teste | Os testes exercitam o comportamento real, não um substituto dele? |
| Entrega | Aplica limpo, falha em voz alta, e a alegação de entrega sobrevive a uma checagem de fatos? |

Pontue TODO portão nas mesmas cinco lentes, cada uma de 0–4: aderência à
spec, encaixe arquitetural, segurança de tipos, testabilidade, segurança —
formuladas para o estágio (no Design, "testabilidade" pergunta se a spec é
checável; na Entrega, se a alegação de entrega é). Consolidação: some as
cinco lentes (0–20), multiplique por 5 — essa é a nota de veredicto do
portão, de 0–100. Registre cada lente, não só o total — o total esconde qual
lente falhou.

## Veredictos

Consolide as lentes numa nota de 0–100 e enquadre:

- **Aprovar** (80+): evidência forte. Ainda não é prova de pronto — veja a
  segunda lei.
- **Revisar** (60–79): existem falhas nomeadas. Cada uma é um alvo de reparo.
- **Rejeitar** (abaixo de 60): o trabalho erra a intenção. Volte um estágio.

Um veredicto sem falhas nomeadas por trás é um veredicto de pouca informação.
Exija a lista.

## Disciplina de reparo

1. Mantenha a intenção original como âncora de toda nova rodada.
2. Registre as notas por lente, não só o número de cima.
3. Trate toda falha nomeada como alvo de reparo. Nenhuma falha é decoração.
4. Repare, depois RODE O MESMO PORTÃO DE NOVO. Reparo sem nova rodada é só
   alegação.
5. Nunca promova confiança a prontidão. Os testes e a superfície real
   decidem.

## As duas leis

**1. A lei do eco.** Uma checagem que só sabe concordar é um eco, não um
validador. A prova de honestidade é a refutação: alimente-a com uma alegação
que você sabe ser falsa e veja-a reprovar essa alegação. Se ela aprova a
mentira, a checagem é teatro. Corolário sobre mock: mocke só a folha externa
instável — uma API paga, uma rede instável. Nunca mocke o órgão cujo
comportamento É a prova; a pontuação, a extração de alegações e a lógica de
passa/falha dele precisam rodar de verdade.

**2. Necessário, não suficiente.** Um teste que passa é necessário, nunca
suficiente. Pronto significa que a superfície real — a que o humano de fato
usa — faz o trabalho sozinha. Nomeie essa superfície, dispare o caminho real
e veja o resultado correto chegar. Nunca promova um recibo de teste unitário
a alegação de capacidade viva.

## Regras duras (o que derruba esta skill)

- Pontuar contra uma paráfrase em vez do pedido original.
- Um veredicto de revisar ou rejeitar sem falhas nomeadas anexadas.
- Reparar sem rodar de novo o portão que falhou.
- Mockar o próprio validador, ou a exata costura sob mudança.
- Declarar pronto a partir de um teste verde sem prova na superfície real.

## Mantenha um registro do build

Para cada estágio guarde: a intenção, o artefato exato de entrada, as notas,
as falhas nomeadas, o reparo feito, o resultado da nova rodada e a evidência
da superfície real. Um registro que não aponta para evidência reproduzível é
uma faixa de propaganda, não um registro.

## Funciona bem com

- [intent-compiler](../intent-compiler/SKILL.md) — traduza o pedido antes de pontuar.
- [red-first](../red-first/SKILL.md) — o contrato do portão de Teste: teste falhando commitado primeiro.
- [sniper-testing](../sniper-testing/SKILL.md) — efeitos colaterais reais, sem teatro de mock.
- [blind-tribunal](../blind-tribunal/SKILL.md) — avaliadores independentes por cima destes portões.
- [repair-loop](../repair-loop/SKILL.md) — o loop que leva veredictos de revisar até o verde.
