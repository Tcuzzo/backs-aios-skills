---
name: optimus
description: Use ao iniciar qualquer sessão, job ou loop de agente — antes de escrever qualquer código. Boot harness-first: carregue o piso de invariantes e as skills que o job precisa, para o agente ler as regras antes de trabalhar; inclui o padrão de hook do portão de aterramento que bloqueia ferramentas mutantes até o harness carregar. Trigger words: optimus, harness-boot, harness first, load the harness, boot the floor, grounding gate, read the floor, no code without harness, session start, boot sequence, carregar o harness, início de sessão, ler o piso, sem código sem harness.
license: MIT
---

# Harness Boot
**Effort:** light — uma passada de boot por sessão para carregar o piso e as skills do job, mais um hook determinístico que não custa nada para rodar. Remove: edições sem aterramento — mutações feitas antes de as regras serem lidas, e o refazer que vem depois que elas são.

Uma regra: **nenhum código e nenhum job até o harness carregar.** O harness é
o piso de invariantes do pack mais as skills que cobrem este job. Toda sessão,
todo runtime, toda vez. O porquê: uma regra que o agente precisa lembrar falha
exatamente quando o agente está mais ocupado — então carregar as regras é o
primeiro ato, e um hook torna isso estrutural em vez de consultivo.

## Quando rodar

No começo de toda sessão, job, missão e loop. De novo depois de um reset de
contexto ou de um handoff. Carregar o harness uma vez e passar uma semana no
piloto automático não é carregar o harness.

## A sequência de boot

1. **Carregue o piso de invariantes.** Leia [invariant-floor](../invariant-floor/SKILL.md)
   antes de tocar em qualquer coisa. Esse é o piso onde a sessão inteira se apoia.
2. **Carregue o mapa deste job.** Nomeie quais arquivos, quais regras e quais
   skills do pack governam este trabalho específico. Se você não consegue
   nomeá-los, não está pronto para editar.
3. **Carregue o perfil humano** ([human-calibration](../human-calibration/SKILL.md))
   quando o job toca o gosto, a superfície ou o fluxo de trabalho de um humano.
4. **Invoque as skills que o job precisa — em tempo real, nesta sessão.** Uma
   skill nomeada mas não invocada não aconteceu. Trabalhar "de memória de uma
   skill" não é invocá-la.
5. Só então: escreva código, rode comandos mutantes ou mude qualquer coisa.

## O padrão do portão de aterramento

Torne o passo 4 estrutural com um **hook pré-uso-de-ferramenta** determinístico
— um script pequeno que o runtime do seu agente chama antes de cada chamada de
ferramenta:

- Toda sessão começa **RED** (vermelha).
- Em RED, ferramentas só-leitura (read, grep, search, fetch) sempre passam. O
  agente se aterra livremente.
- Em RED, o hook **bloqueia ferramentas mutantes** (edit, write, delete) e os
  verbos mutantes primários do shell (commit, push, rm, install, restart de
  serviço, edições in-place).
- Invocar qualquer skill do harness **vira a sessão para GREEN** (verde; pego
  por um hook pós-uso-de-ferramenta). Aí o agente pode agir.
- **Rearme:** o estado volta a RED em todo início de sessão. Em sessões
  longas, rearme por job ou por ação, para um GREEN velho nunca carregar
  trabalho sem aterramento.

Regras de design do próprio hook:

- **Determinístico e de graça.** Sem chamada de modelo, sem rede, sem
  dependências. O estado é um arquivo pequeno por sessão, escrito
  atomicamente.
- **Ele força aterramento, não é um sandbox.** Case só os verbos mutantes
  primários; deixe em paz wrappers de duplo uso e ferramentas de cópia, para
  os comandos de aterramento não caírem na armadilha.
- **Falha aberto, mas em voz alta.** Um hook que quebrou nunca pode brickar a
  sessão — e nunca pode permitir em silêncio. Imprima o erro onde o humano
  veja.
- **Nunca prenda uma sessão.** Identidade de sessão desconhecida permite, com
  uma linha alta de aviso. Uma sessão que nunca pode virar GREEN nunca pode
  ser bloqueada em RED.
- **Um kill-switch do humano** (uma variável de ambiente), padrão LIGADO,
  loga alto quando desligado. O portão amarra agentes, nunca o humano. Nunca
  adicione um segundo portão.

Hook genérico (pseudocódigo, ~25 linhas):

```python
HARNESS_SKILLS = {"optimus", "repair-loop", "invariant-floor"}  # o conjunto do seu pack
MUTATING_TOOLS = {"Edit", "Write", "Delete"}
MUTATING_SHELL = r"^\s*(sudo\s+)?(git (commit|push|reset|checkout)|rm|pip install|" \
                 r"npm install|systemctl (restart|stop)|sed .*-i)"

def handle(event, session_id, tool, args):
    if kill_switch_off():                    # variável de ambiente do humano, ex.: HARNESS_GATE=off
        return ALLOW                         # desligado em voz alta, nunca em silêncio
    if not session_id:
        warn("sem id de sessão — permitindo; o portão nunca prende uma sessão")
        return ALLOW
    if event == "SessionStart":
        set_state(session_id, "RED")         # toda sessão rearma para RED
        return ALLOW
    if event == "PostToolUse":
        if tool == "Skill" and args.get("skill") in HARNESS_SKILLS:
            set_state(session_id, "GREEN")   # harness invocado -> o agente pode agir
        return ALLOW
    if event == "PreToolUse":
        mutating = tool in MUTATING_TOOLS or (
            tool == "Bash" and matches(MUTATING_SHELL, args.get("command", "")))
        if not mutating or get_state(session_id) == "GREEN":
            return ALLOW                     # só-leitura sempre passa
        return BLOCK("RED: invoque uma skill do harness primeiro, depois aja")
    return ALLOW
```

## Regras duras (o que derruba esta skill)

- Qualquer mutação antes de o harness carregar.
- Uma skill nomeada num relatório que nunca foi invocada na sessão.
- Um hook que bloqueia ferramentas só-leitura, prende uma sessão em RED ou
  falha em silêncio.
- Um segundo portão, ou qualquer atrito novo posto sobre o humano. O
  kill-switch continua sendo dele.

## Funciona bem com

- [invariant-floor](../invariant-floor/SKILL.md) — o piso que o boot carrega primeiro.
- [human-calibration](../human-calibration/SKILL.md) — o passo de perfil do boot.
- [repair-loop](../repair-loop/SKILL.md) — o que um job de conserto roda depois do boot.
- [bounded-loops](../bounded-loops/SKILL.md) — orçamentos para todo loop que o boot inicia.
- [wayfinder](../wayfinder/SKILL.md) — quando o boot mostra que você não sabe a rota.
