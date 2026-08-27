---
name: gpu-dispatch
description: Use ao despachar modelos locais para GPUs — agendar inferência, escolher uma placa ou gerenciar residência de modelo. Um modelo por GPU, sem derramar para a RAM do sistema, quente durante o loop, descarrega no fim do loop, admissão por verdade medida. Trigger words: gpu, vram, gpu dispatch, model loading, keep alive, resident model, local inference, spill, warm, despacho de gpu, carregar modelo, modelo residente, inferência local, derramar, aquecido.
license: MIT
---

# Lei de Despacho de GPU
**Effort:** free — regras impostas pelo despachante, lidas do estado vivo do próprio nó; corta custo na raiz. Remove: execuções derramadas da VRAM rodando 10x mais lentas em silêncio, churn de partida fria entre jobs, e placas paradas por cercas presumidas.

Quatro regras para rodar modelos locais em GPUs. Elas existem porque os dois modos
comuns de falha são opostos e igualmente caros: surrar placas com cargas e
derramamentos, e cercar demais o hardware até ele ficar parado. Os dois são
capacidade perdida. Aplique isto no dispatcher como código — nunca como regra que
um modelo tem que lembrar.

## Quando rodar

- Antes de despachar qualquer job de inferência para uma GPU local.
- Ao projetar ou revisar um dispatcher, agendador ou roteador de modelos.
- Quando uma execução local está misteriosamente lenta, ou uma placa misteriosamente "indisponível".

## As quatro regras

1. **Um modelo residente por placa, por vez.** Antes de qualquer despacho, leia o
   estado ao vivo de modelos carregados do nó pela API do próprio runtime. Se um
   modelo diferente está residente, use-o ou descarregue-o primeiro. Nunca carregue
   um segundo modelo ao lado.
2. **Sem derramar para a RAM do sistema — aborte, não rode devagar.** Verifique que
   o modelo cabe inteiro na VRAM livre da placa antes do despacho, e afirme que ele
   permanece todo em VRAM durante o trabalho. Qualquer derramamento para a RAM do
   sistema é ABORT, não execução degradada — um modelo derramado fica 10x mais
   lento em silêncio e envenena todo job atrás dele. Um modelo que não cabe acima
   do piso reservado da placa não é despachado para essa placa; escolha um modelo
   menor ou outra placa.
3. **Mantenha a placa quente pelo loop de trabalho inteiro.** Segure o modelo
   residente com um keep-alive limitado — um piso e um teto que você configura,
   nunca ilimitado — e renove enquanto o loop roda. Sem churn de cold start entre
   jobs do mesmo loop.
4. **Descarregue só quando o loop completa.** Liberação explícita no fim do loop —
   não depois de cada job. Descarregar por job é churn de cold start; nunca
   descarregar é vazamento. Liberação no fim do loop é a costura.

## Admissão por verdade medida

Se uma placa pode receber trabalho é decidido por medição ao vivo, nunca por suposição:

- Uma **sonda real** do nó — não uma nota velha de "inalcançável" numa config.
- **VRAM livre real** acima do piso reservado da placa — o piso é o único limite
  vigente; tudo acima dele é livre para usar.
- Um **cheque real de processo rodando** para cargas interativas. Um jogo, stream
  ou sessão de edição ao vivo na placa vence na hora — mas a presença é medida,
  nunca presumida de um arquivo marcador ou de uma lista "cold" hardcoded.

Defaults fail-closed, negações por "propósito desconhecido" e arquivos marcadores
cuja ausência significa "cerca ligada" são todos o mesmo bug: o runtime recusando
hardware que o humano é dono. Cercar demais hardware próprio é capacidade perdida,
e capacidade perdida é defeito. Só a palavra ao vivo do humano põe ou tira uma cerca.

## Regras duras (o que reprova esta skill)

- Carregar um segundo modelo numa placa que já tem um residente.
- Continuar uma execução depois de detectar derramamento de VRAM em vez de abortar.
- Um keep-alive ilimitado, ou descarregar entre jobs dentro de um loop.
- Negar uma placa com base em nota de config, arquivo marcador ou suposição em vez
  de uma sonda ao vivo.
- Aplicar qualquer parte disto por prompt em vez de no código do dispatcher.

## Combina bem com

- [invariant-floor](../invariant-floor/SKILL.md) — verdade medida e falhas
  barulhentas são leis do piso; esta skill as aplica a GPUs.
- [fleet-ladder](../fleet-ladder/SKILL.md) — resolva qual modelo despachar antes
  de decidir onde ele roda.
- [bounded-loops](../bounded-loops/SKILL.md) — o loop de trabalho a que keep-alive
  e liberação de fim de loop estão amarrados.
