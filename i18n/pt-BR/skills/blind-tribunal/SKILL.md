---
name: "blind-tribunal"
description: "Use quando uma mudança autônoma precisa de avaliação independente antes de aterrissar e não há humano no loop. Convoca jurados cegos, cross-family — uma lente cada — sobre um envelope de arquivos inteiros com autoria removida; cada achado vira um teste novo falhando; repita até todos os jurados passarem. Trigger words: blind tribunal, grill tribunal, tribunal, jurors, cross-family grade, convene, blind grade, independent grade, grade before landing, tribunal cego, jurados, avaliação cega, avaliação independente, convocar, avaliar antes de aterrissar."
license: "MIT"
---

# Blind Tribunal
**Effort:** heavy — oito jurados, uma lente cada, roteados por camada para a família de modelo mais barata que basta, reconvocados sobre envelopes novos a cada rodada até a unanimidade; gaste em mudanças autônomas que pousam sem revisão humana. Remove: pousos desgovernados guardados por nada além da palavra do próprio builder.

O loop de avaliação que deixa o humano sair da sala sem o agente sair dos trilhos.
Um painel de jurados revisa a mudança às cegas, com a autoria arrancada. Cada
achado vira um teste novo falhando. O loop repete até todos os jurados passarem.
Nada aterrissa só na palavra do builder.

## Quando rodar

- Antes de aterrissar qualquer mudança autônoma que nenhum humano vai revisar.
- Qualquer mudança de alto raio de explosão: cara de segurança, toca dados, perto de autoridade.
- Quando um avaliador só não basta e você quer lentes independentes sobre o mesmo artefato.

## As cadeiras

Oito jurados, uma lente cada. Cada um é um modelo de uma família DIFERENTE da do builder
(mesmo fornecedor = mesma família). Jurado mandado checar tudo não checa nada direito.

| Jurado | Id da lente | Camada | A pergunta que ele faz |
| --- | --- | --- | --- |
| Defeito | `defect` | generalista | O que quebra de verdade? Falhas de lógica, erros de sintaxe, defeitos novos. |
| Proporção | `proportion` | generalista | Tem o tamanho certo? Superconstruído, ou na medida da intenção? |
| Consequência | `operator_consequence` | segurança do operador | Se um operador humano rodar isto, o que é destrutivo, inseguro ou danoso? |
| Reversibilidade | `reversibility` | estado profundo | Deixa efeitos irreversíveis? Se morre no meio, o sistema volta atrás limpo? |
| Continuidade | `state_continuity` | estado profundo | Órfãos, estado global sobrescrito, contexto perdido para os nós seguintes? |
| Economia | `resource_economy` | estrutural rápido | Loops sem otimizar, chamadas de rede/API redundantes, memória inchada? |
| Borda | `boundary_condition` | estrutural rápido | Com entrada nula, vazia, de tipo errado ou malformada — falha com graça? |
| Telemetria | `telemetry` | segurança do operador | Uma falha aqui se diagnostica pelos logs e pelo tratamento de erro? |

**Camadas de roteamento (primeiro a rota mais barata que basta):** estado profundo →
maior contexto e raciocínio mais fundo, de preferência por um harness que LÊ o repo
(nunca escreve); estrutural rápido → primeiro uma GPU local grátis, FUNDIDA com um
verificador de nuvem barato que julga o mesmo prompt: a lente passa só se os dois passam;
sem nuvem, o veredito local fica, marcado UNVERIFIED, nunca "verificado" em silêncio; e o
modelo local precisa ver TODO o artefato (dimensione `num_ctx` pelo prompt — o padrão do
Ollama, 4096, trunca em silêncio — e recuse antes de enviar o que não cabe); o verificador nunca é da mesma família do assento primário, e um assento UNVERIFIED é uma retenção (nunca unanimidade); jurados via harness rodam read-only, e cada convocação carrega um `run_id` e escreve seu resumo por último; depois os
modelos de nuvem de baixa latência; segurança do operador →
seu coder mais forte com base em segurança; generalista → um generalista grande e confiável.
Toda escada termina num degrau local de sobrevivência.

**Rig solo.** Quando só uma família de modelo está disponível, degrade
EXPLICITAMENTE: um contexto ou sessão nova que nunca viu a conversa do autor age
como avaliador cego, ou o humano revisa o envelope com autoria removida. O
relatório tem que nomear o portão enfraquecido — "avaliado cego-mesma-família, não
cross-family" — nunca fingir em silêncio que o portão cross-family segurou.

## O envelope

Jurados nunca veem o repo, o builder ou a conversa. Eles veem um envelope:

- **Arquivos atuais inteiros** para cada arquivo que a mudança tocou, mais seus
  arquivos de teste. Nunca trechos soltos de diff — um trecho esconde o contrato ao
  redor e induz achados falsos.
- **O contrato de revisão**: a intenção da mudança em uma linha, e os critérios de pass.
- **Zero autoria.** Sem nomes, sem ids de modelo, sem autores de commit, sem
  histórico de chat. Se identidade vazar, a montagem do envelope falha alto — nunca
  avalie sem o cego.
- **Sem prosa sobre o comportamento antigo.** Descrever o que o código "fazia antes"
  planta defeitos fantasma. Os arquivos falam por si.

## O veredito

JSON estrito, parseável por máquina, um objeto, sem prosa:

```json
{"verdict": "pass" | "refuse",
 "findings": [{"severity": "blocker|major|minor|info",
               "claim": "...", "evidence": "..."}]}
```

- Jurado que RESPONDEU mal — lixo, não-JSON, texto de recusa — conta como
  **refuse**; jurado que NUNCA respondeu (falha de transporte, inalcançável) é um
  **hold**: sente outro no lugar via [fleet-ladder](../fleet-ladder/SKILL.md),
  nunca um pass silencioso. Um tiro por jurado que responde por rodada — sem retry.
- Um pass seco com zero achados e sem evidência é um **voto de baixa informação**.
  Conta, mas nunca como a única prova — dois passes secos não vencem um refuse
  detalhado. Um pass forte nomeia o que checou.

## O loop

1. Red first: commite o teste de contrato falhando ANTES de construir o conserto, e
   registre esse commit. O builder não pode tocar no teste ([red-first](../red-first/SKILL.md)).
2. Construa até o verde.
3. Monte o envelope a partir dos arquivos ATUAIS.
4. Sente os oito jurados, por camada, — famílias diferentes da do builder
   ([fleet-ladder](../fleet-ladder/SKILL.md) resolve o que está vivo).
5. Cada jurado também verifica, não só lê: os testes novos passam; a suite de
   regressão não está pior que a baseline; e um cheque de falso verde — um teste que
   DEVERIA falhar (o bug reintroduzido) falha mesmo. Falso verde é refuse.
6. Em qualquer refuse: CADA achado — blocker, major e minor — vira um teste NOVO
   falhando, que falha pelo motivo real do achado. Conserte. Remonte o envelope
   sobre os arquivos revisados. Reconvoque TODOS os jurados. Veredito sobre arquivo
   velho não é veredito.
7. Aterrisse só com pass unânime. Achados minor levantados na rodada final também
   fecham, nunca ficam para depois — "consertei os blockers, minors depois" é
   exatamente o vazamento que esta skill existe para parar. Um achado termina
   CONSERTADO ou refutado com evidência registrada, nunca estacionado.

## Regras duras — qualquer uma quebrada anula a avaliação

- O builder nunca avalia o próprio trabalho: nem a mesma instância, nem a mesma família.
- **Um refuse de jurado vale o que o envelope vale.** Antes de escrever um teste a
  partir de um achado, verifique o achado contra os arquivos de verdade. Achado
  sobre código que o envelope nunca carregou significa consertar o envelope, não o código.
- Meça convergência pelos achados NOVOS por rodada, não pelo total bruto. Achados
  novos estáveis ou crescendo por duas rodadas seguidas: pare e escale para o
  humano. Nunca fique moendo.
- Nunca enfraqueça ou edite os testes falhando para alcançar um pass. Jurados
  verificam que os arquivos de teste estão intocados desde o commit red.
- Pass unânime abre o portão; não é a chegada. Aterrisse, depois prove a capacidade
  ao vivo na superfície real. Verde sem prova ao vivo não é pronto.

## Combina bem com

- [red-first](../red-first/SKILL.md) — o contrato falhando, commitado antes do builder rodar.
- [sniper-testing](../sniper-testing/SKILL.md) — efeitos colaterais reais, execuções com escopo, sem teatro de mock.
- [seam-engineering](../seam-engineering/SKILL.md) — conserte a classe, varra os irmãos, aterrisse uma guarda.
- [repair-loop](../repair-loop/SKILL.md) — o loop de construção que este tribunal avalia.
- [blind-eval](../blind-eval/SKILL.md) — o portão manter-ou-reverter mais leve quando a questão é gosto, não defeito.

> Scaffold credit: Matt Pocock, grill-me / grilling (mattpocock/skills, MIT). The
> cross-family blind adversarial tribunal design is BACKS AIOS.
