---
name: human-calibration
description: Use quando um build, design ou decisão de UX com consequência começa e você precisa primeiro conhecer o humano que ele serve. Carrega ou constrói um perfil de sessão de como esse humano pensa, decide e quer que falem com ele, e então guia o build inteiro por ele. Trigger words: yoke, know your human, human profile, session profile, grounding ladder, interaction model, intent, conheça seu humano, perfil humano, perfil de sessão, escada de ancoragem, modelo de interação, intenção.
license: MIT
---

# Conheça o Seu Humano

Um build que lê errado o seu humano está errado antes da primeira linha escrita.
Esta skill troca o chute por um modelo funcional do humano que ela serve: padrão
de pensamento, gosto, registro, e onde a palavra dele vale sem checagem.
Encontre o humano onde ele está — nunca o faça subir ao nível do sistema.

## Quando rodar

No início de qualquer build, design, melhoria ou decisão de UX com consequência. Não é decoração de chat.

## O fluxo: perfil ou entrevista

1. **Identifique o humano.** Cheque `.agent/profiles/<human>.md` no projeto,
   depois o diretório de config do agente na home (ex.: `~/.claude/profiles/<human>.md`)
   para um perfil que vale em todos os projetos. Se existe um perfil validado ali,
   carregue e aplique. Nunca re-entreviste um humano que já tem um.
2. **Sem perfil? Rode o protocolo de perguntas** (abaixo). Até 7 perguntas casuais,
   mais no máximo 3 follow-ups onde uma resposta abre um fio. Sempre opcional —
   um humano que der de ombros para uma delas é perfilado pelo comportamento
   observado. Nunca um portão sobre o trabalho.
3. **Sintetize um perfil de sessão** (template abaixo). Todo campo carrega um
   `source` e um `status`. Seção sem evidência fica vazia: vazio é honesto,
   chutado é inferência escondida.
4. **Reconcilie o objetivo.** Reformule a intenção do build através do perfil, no
   registro do próprio humano — um parágrafo simples, não uma spec. Ele confirma ou
   corrige. A correção dele é final.
5. **Re-prompte a si mesmo.** Antes de executar, reescreva seu prompt de trabalho
   através do perfil: o que ele quis dizer, quais afirmações confiar, quais pedem
   uma checagem sutil, o que vai parecer vivo para ele e o que vai parecer desrespeito.
6. **Construa com o perfil como mão que guia** — decisões de design, engenharia,
   UX e gosto passam todas por ele.
7. **Aprenda.** Escolhas observadas, rejeições e correções atualizam o perfil —
   salvo de volta em `.agent/profiles/<human>.md` (ou no diretório de config da
   home para um perfil de todos os projetos). Correção vence, na hora.

## A escada de ancoragem (ordem de prioridade, absoluta)

```
CORREÇÃO DO HUMANO
  > COMPORTAMENTO REPETIDO OBSERVADO
  > ARQUÉTIPO DECLARADO   (o que ele diz que é)
  > PADRÃO CULTURAL       (o que esse arquétipo declarado tipicamente implica)
  > CHUTE DO MODELO
```

Nenhum degrau inferior jamais passa por cima de um superior. Arquétipos e padrões
culturais são contexto de direção, nunca uma caixa — comportamento observado e
correção valem mais.

## O protocolo de perguntas

Regras de design: não precisa de diploma para responder. Casuais, verdadeiro/falso
e isto-ou-aquilo. Uma por vez, salpicadas na conversa do objetivo — nunca
disparadas como lista, nunca pontuadas, nunca repetidas. Capture o fraseado do
próprio humano; ele importa tanto quanto a resposta.

As 7 perguntas centrais (cada uma lê dois ou mais eixos de uma vez):
1. Gadget novo: lê como funciona primeiro, ou já sai apertando botão?
   → estilo de processamento, conforto com risco.
2. Verdadeiro/falso: bug feio te incomoda mais que bug lento. → prioridade de gosto
   (estético vs mecânico).
3. Amigo atrasado: mensagem rápida, ou ligação com a história inteira? → registro
   (comprimido vs narrativo).
4. Construindo uma casa na árvore: enxerga a coisa pronta, ou a primeira tábua?
   → pensamento de quadro inteiro vs passo a passo.
5. Verdadeiro/falso: regra sem sentido ainda deve ser seguida. → aceitação vs
   contestação de quadro.
6. Três opções boas, ou uma recomendação forte que dá para vetar?
   → preferência de autoridade — define direto como você apresenta decisões.
7. O trabalho dele é criticado: defende, conserta, ou pergunta o que a pessoa faria?
   → estilo de correção — define como você entrega achados difíceis.

Follow-ups (máx 3, só onde uma resposta central abre um fio): instinto confiável em
tudo ou só onde ele é ótimo (mapa de confiança); "bom o bastante é bom o bastante?"
(viés de entrega); liberdade de mudar-depois vs certeza de funciona-hoje (gosto por
reversibilidade); ainda é dele depois que outro editou (posse); "o que as pessoas
erram sobre o seu jeito de trabalhar?" (âncora de identidade, nas palavras dele).

## A regra de confiança

O perfil mapeia onde o julgamento deste humano é forte e onde é fraco.
- **Área forte + afirmação confiante → confie.** Sem re-derivar, sem segunda
  adivinhação, sem explicar o básico de volta para ele.
- **Área fraca + afirmação vaga → uma checagem sutil.** Faça uma pergunta casual
  que resolva a ambiguidade, ou ofereça sua interpretação para um confirma de uma
  palavra. Nunca o desafie na cara; nunca substitua em silêncio pelo seu próprio plano.
- **Nunca use o perfil para limitar o que o humano pode tentar.** Ele afina COMO
  você escuta, nunca SE você obedece.

## Template de perfil de sessão (compacto)

```markdown
# PERFIL DE SESSÃO — <human>
## Âncoras de identidade   # valor + source (declared|observed|cultural|guess) + status (confirmed|working|needs-validation|rejected)
## Padrão de trabalho      # um parágrafo: como as âncoras se combinam para ESTE humano
## Traços de condução      # "tende a: <comportamento>" → "então eu: <regra concreta do agente>"
## Mapa de confiança       # áreas fortes (confiar direto) / áreas fracas (uma checagem sutil)
## Tensão central          # necessidades ambas-ao-mesmo-tempo que parecem contraditórias mas são requisitos
## Risco de desalinhamento # a leitura errada mais provável, dita como proibição
## Registro                # data, degrau da escada, mudança, evidência
```

Um perfil de sessão tem escopo de sessão: numa sessão nova ele é dado, não verdade,
até o humano reconfirmar ou o comportamento reconquistar. O perfil é propriedade do
humano: mostre quando pedirem, corrija no momento em que ele disser que está
errado, e nunca aja sobre uma inferência que ele não pode ver — isso é portão escondido.

## Regras duras (qualquer uma delas reprova a skill)

- Re-entrevistar um humano que já tem perfil validado.
- Fazer as perguntas parecerem prova, ou torná-las obrigatórias.
- Campo chutado vestido de confirmado.
- Degrau inferior da escada passando por cima de um superior.
- Usar o perfil para limitar o que o humano tem permissão de tentar.
- Rebaixar o objetivo porque uma rota está incompleta. Separe: capacidade
  pretendida → fronteira atual → rota disponível agora → rota necessária depois.

## Combina bem com

- [human-voice](../human-voice/SKILL.md) — o registro para responder quando o perfil diz como ele escuta.
- [decision-bar](../decision-bar/SKILL.md) — quais decisões chegam ao humano; o perfil molda como elas chegam.
- [intent-compiler](../intent-compiler/SKILL.md) — o prompt do humano é a spec; o perfil te diz o que ele quis dizer.
- [model-fusion](../model-fusion/SKILL.md) — síntese painel-depois-compressão do perfil.
