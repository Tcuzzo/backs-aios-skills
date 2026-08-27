---
name: fleet-ladder
description: Use antes de entregar qualquer trabalho a um modelo — construir, avaliar ou um job limitado de worker — ou quando um provedor caiu e você precisa da ordem de fallback. Resolve a escada de modelos AO VIVO: sonda o que está de pé de verdade, escolhe o melhor disponível por uma ordem explícita de fallback, falha alto quando a escada esgota. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability, frota, escada, despacho, modelo fora, provedor fora, qual modelo, disponibilidade.
license: MIT
---

# Fleet Ladder

Nunca construa na mão uma chamada de provedor, e nunca hardcode um nome de modelo
num ponto de chamada. Um resolvedor só é dono da pergunta "qual modelo faz este
trabalho agora?" — e ele responde pela verdade ao vivo, não pela opinião de um
arquivo de config.

## Quando rodar

- Antes de QUALQUER despacho para um modelo: build, avaliação, review ou job limitado de worker.
- Quando um provedor caiu e você precisa saber o que cai para o quê.
- No momento em que você se pega digitando um nome de modelo em código ou num template de prompt.

## Os passos

1. **Declare o papel, não o modelo.** Todo job pede um papel — `builder`,
   `grader` ou `worker`. A escada mapeia papéis para candidatos ordenados de modelo.
   - `builder`: implementa e conserta.
   - `grader`: review independente — estruturalmente nunca o mesmo modelo que construiu.
   - `worker`: jobs limitados e bem especificados. Degraus mais baratos servem aqui.
2. **Leia a escada da config.** Um arquivo lista, por papel, os candidatos em ordem
   explícita de fallback: o mais forte primeiro, descendo até a sua cauda local de
   sobrevivência (o que você consegue rodar no seu próprio hardware quando todo
   provedor de nuvem apaga). Para mudar ou adicionar um modelo, edite esse arquivo —
   nunca o código. Formato inicial: [ladder.example.yaml](ladder.example.yaml) —
   copie e troque os placeholders.
3. **Sonde ao vivo antes de confiar.** Uma listagem de config é uma alegação, não
   verdade. Uma entrada velha lista modelos mortos; e também omite modelos vivos.
   Sonde o provedor antes de despachar para um degrau — uma chamada ao endpoint de
   modelos ou uma requisição de um token, por exemplo:
   `curl -s "$PROVIDER_BASE_URL/v1/models" -H "Authorization: Bearer $API_KEY"`
   (ou o mesmo formato contra o endpoint de chat com `"max_tokens": 1`).
   Cacheie o resultado da sonda por uma janela sensata — não martele provedores
   re-sondando a cada chamada. Renove o cache só quando você realmente precisar de
   verdade fresca.
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

- **Nenhum nome de modelo em ponto de chamada.** O código pede um papel; a escada
  responde com um modelo. Dê grep no seu código por literais de nome de modelo —
  cada um é um bug.
- **A sonda ao vivo vence a config.** Se o humano diz que um modelo existe e a
  config discorda, sonde. Checou-e-respondeu está resolvido; lista velha não está.
- **Builder e grader nunca resolvem para o mesmo modelo** para a mesma mudança.
  Se a escada os colapsaria num modelo só, o grader pega o próximo degrau
  independente — ou o job falha alto.
- **Sondagem limitada.** Sondas são baratas, cacheadas e com backoff. Loop
  apertado de retry contra um provedor morto é proibido.
- **Sem fallback silencioso.** Cada passo escada abaixo é visível no log e no
  relatório. Degradar quieto é como uma rota quebrada morre sem ninguém notar.

## Combina bem com

- [model-fusion](../model-fusion/SKILL.md) — o painel e o juiz resolvem seus modelos por esta escada.
- [blind-tribunal](../blind-tribunal/SKILL.md) — jurados vêm de famílias diferentes; a escada escolhe os vivos.
- [bounded-loops](../bounded-loops/SKILL.md) — cadência de sonda, backoff e kill-switches.
