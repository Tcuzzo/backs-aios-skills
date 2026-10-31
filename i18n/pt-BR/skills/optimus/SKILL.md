---
name: "optimus"
description: "Use ao iniciar ou retomar uma sessão, trabalho ou ciclo autônomo que precise do harness BACKS e das skills pertinentes."
license: "MIT"
---

# Harness Boot
**Effort:** light — uma passada de boot por sessão para carregar o piso e as skills do job, mais um hook determinístico que não custa nada para rodar. Remove: edições sem aterramento — mutações feitas antes de as regras serem lidas, e o refazer que vem depois que elas são.

Uma regra: **nenhum código e nenhum job até o harness carregar.** O harness é
o piso de invariantes do pack mais as skills que cobrem este job. Toda sessão,
todo runtime, toda vez. O porquê: uma regra que o agente precisa lembrar falha
exatamente quando o agente está mais ocupado — então carregar as regras é o
primeiro ato, e um hook torna isso estrutural em vez de consultivo.

## Quando rodar

No início de uma sessão ou trabalho novo; revalide após reinício de contexto ou
handoff. Retry interno reutiliza o aterramento atual e o mesmo pacote de tarefa.
Recarregue corpos ausentes ou alterados; não reinicie o ciclo de vida a cada iteração.

## A sequência de boot

1. **Carregue o piso de invariantes.** Leia [invariant-floor](../invariant-floor/SKILL.md)
   antes de tocar em qualquer coisa. É o piso da sessão inteira.
2. **Aplique [Build Flow](../backs-build-flow/SKILL.md).** Ele controla modo da tarefa,
   prontidão para agir, seleção de skills, RED/GREEN limitado com lint e tests
   focados, evidências do gauntlet e entrega. Reutilize pacote verificado; reúna
   apenas fatos ausentes necessários à próxima ação concreta. Especialistas
   retornam a um único responsável.
3. **Aplique contexto humano** ([human-calibration](../human-calibration/SKILL.md))
   quando pertinente. [operator-essence](../operator-essence/SKILL.md) cuida do
   arquivo de contexto sustentado por evidências e da passagem de insights quando
   ele falta; não execute um segundo ciclo de perfil.
4. **Carregue a sessão.** O hook entrega os corpos reais de Optimus, Yoke e Build
   Flow, mais o harness nativo comprovado quando disponível. A compactação recarrega
   os corpos sem revogar aterramento adquirido. Marcador ausente diante de ferramenta
   mutante dispara carregamento, nunca recusa da ferramenta. Hosts sem hook de
   contexto podem usar:
   ```bash
   node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
   ```
   Em shell Codex, passe o `CODEX_SESSION_ID` ativo como argumento final.
   A variante Python está no loader `aios_gate.py`. Skills desconhecidas retornam
   diferente de zero sem inventar recibo.
5. **Aplique as skills necessárias à próxima ação.** Nomeie propósito, resultado
   e condição de saída. Skill nomeada mas não invocada não aconteceu. Reutilize
   corpos reais ainda presentes no contexto; resumo de memória ou hash de arquivo
   não os substitui.
6. Só então escreva código, execute comandos mutantes ou altere algo.

## Aterramento automático

O hook existente lê arquivos fundamentais e entrega seus corpos pelo contexto
do host. Registra hashes da fonte somente após a entrega. Recibos de carregamento
de contexto são distintos de evidência real de eventos Skill; carregar um ponteiro
ou calcular hash não invoca essa skill.

- Início de sessão e compactação recarregam o piso sem tirar ferramentas.
- Marcador de sessão ausente dispara carregamento automático na próxima ferramenta correspondente.
- Corpos ausentes ou ilegíveis produzem diagnóstico visível e nenhum recibo falso;
  operador e agentes mantêm suas ferramentas.
- `--rearm <session_id>` solicita outra carga. Nunca bloqueia a sessão.
- `AIOS_GATE=off` continua sendo o interruptor reversível existente do operador.
- Hooks são locais e determinísticos. Não se acrescenta chamada a modelo nem dependência de rede.

## Regras duras (o que reprova esta skill)

- Qualquer mutação antes de carregar o harness.
- Skill nomeada em relatório que nunca foi invocada na sessão.
- Aterramento na memória da sessão, conhecimento prévio do LLM ou «eu lembro» em
  vez do harness BACKS. BACKS independe de modelo e contexto, com canais robustos
  de memória: o harness (arquivos de memória, plays, registros e YAML da escada)
  carrega o conhecimento, não a cabeça do modelo (decisão do operador 2026-09-26).
- Hook que recuse ferramenta, revogue aterramento adquirido ou relate carga inexistente.
- Segundo gate ou fricção nova para o humano. O interruptor continua sendo dele.

## Combina bem com

- [invariant-floor](../invariant-floor/SKILL.md) — o piso carregado primeiro.
- [human-calibration](../human-calibration/SKILL.md) — contexto humano do boot.
- [repair-loop](../repair-loop/SKILL.md) — reparo após o boot.
- [bounded-loops](../bounded-loops/SKILL.md) — orçamentos para cada ciclo.
- [wayfinder](../wayfinder/SKILL.md) — quando falta conhecer a rota.

## Política dos degraus da frota (referência breve)

Antes de despachar modelos ou elevar design/raciocínio à fronteira, invoque
[fleet-ladder](../fleet-ladder/SKILL.md). Exige **ler**
`config/fleet_ladder.yaml` e `config/gpu_nodes.yaml` (caminhos da implantação),
respeitar o posto ativo do builder e exigir pesquisa atual (web, GitHub, Reddit
e papers) quando o degrau marcar fronteira / `research_seams`. Não fixe IDs
de modelos; Patch controla o YAML.
Referência: `observe/SECURITY_OPERATOR_BUILDER_SEAT_ORDER_20260926.md`.

Respeite [fleet-ladder](../fleet-ladder/SKILL.md): raciocínio de nível médio ou
superior quando suportado, pesquisa antes de tarefas pesadas e contexto sem truncar.
