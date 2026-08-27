# BACKS AIOS Skills

**Leia isto em:** [English](../../README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Deutsch](../de/README.md) · [हिन्दी](../hi/README.md) · [简体中文](../zh-CN/README.md)

> Esta é a tradução em português (Brasil). O [README em inglês](../../README.md) é a versão canônica.

Um harness de agente destilado em 27 skills portáteis e 8 plays nomeados,
extraído de uma plataforma de agentes em produção e reconstruído como markdown
puro que qualquer agente consegue carregar.

## Missão

Este pacote existe para as pessoas que, sem ele, ficariam de fora dos resultados
de elite com agentes — devs, designers e criadores que não são engenheiros de
plataforma. O harness e as skills são o equalizador: eles carregam os humanos
que não podem pagar pelos maiores modelos, e fazem o tamanho do modelo importar
menos. Essa é a aposta deste pacote: um modelo pequeno dentro de um harness
forte pode vencer um modelo grande correndo solto. Você não precisa saber como o
harness foi construído para usá-lo — você diz as palavras-gatilho, e a
disciplina dispara.

## Filosofia

Três crenças atravessam cada arquivo deste pacote.

**Programado, não "prompted".** O agente por trás deste pacote se comunica com
clareza e recusa jogadas ruins porque essas propriedades foram engenheiradas no
harness como regras estruturais — hooks, gates, testes — e não sugeridas num
prompt. Uma regra que o agente precisa lembrar falha exatamente quando o agente
está mais ocupado. Então as regras que importam são impostas onde esquecer é
impossível: no harness, não na memória do modelo.

**Máquinas não pensam — elas destilam.** Dê a um modelo nada de real para
trabalhar e ele comprime o ar — uma resposta errada dita com confiança. Dê ao
mesmo modelo o contexto certo e ele acerta. O que chamamos de raciocínio é
destilação sobre contexto: o modelo comprime o que recebeu numa resposta.
Raciocínio sem pesquisa é alucinação. É por isso que skills existem. Uma skill é
o contexto COM o qual um agente raciocina enquanto raciocina SOBRE uma coisa —
ela leva o agente do entendimento de alto nível até a profundidade do assunto,
para que a destilação tenha algo real para destilar.

**Raciocine só onde raciocinar é a única ferramenta que funciona.** Tudo que é
determinístico pertence ao harness — gates, testes, hooks, orçamentos. O
raciocínio do modelo é gasto só onde ele paga o próprio custo: julgamento,
design, leitura de intenção. Essa divisão é o que torna o pacote um equalizador
de modelos: o harness faz o trabalho pesado, e o tamanho do modelo deixa de
decidir o resultado.

## Começo rápido

### Opção 1 — plugin do Claude Code

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

Depois digite `/optimus` para subir o piso. As skills carregam, os comandos dos
plays ficam disponíveis, e o hook de aterramento já vem ligado (kill-switch:
`AIOS_GATE=off`).

### Opção 2 — manual

Copie as pastas de `skills/` para o diretório de skills do seu agente e diga as
palavras-gatilho. Os caminhos por agente — Claude Code, qualquer runtime de
Agent Skills, OpenClaw, Hermes, um loop de API puro — estão em
[INSTALL.md](INSTALL.md).

| Quando você quer... | Diga... |
| --- | --- |
| Algo quebrou | "repair loop" ou "ciclo de reparo" |
| Construir uma feature | `/elite-build` (plugin) ou leia `plays/elite-build.md` (manual) |
| Isso está bom o bastante para entregar? | "clean code gauntlet" ou "gauntlet de código limpo" |
| Confira meu trabalho, às cegas | "blind tribunal" ou "tribunal cego" |
| Estou perdido — e agora? | "wayfinder" ou "traça a rota" |
| O pedido é prosa vaga | "prose is the spec" ou "a prosa é a spec" |

## Como funciona

- **Skills** são disciplinas isoladas. Cada uma tem palavras-gatilho na
  descrição, passos numerados, regras duras que reprovam a skill e links para as
  skills com que ela combina. Um arquivo cada: `skills/<name>/SKILL.md`.
- **Plays** são combos nomeados. Um play dispara skills numa ordem definida e
  lista os gates duros que bloqueiam um pouso. Um arquivo cada:
  `plays/<name>.md`.
- **Comandos** são as entradas de barra que o plugin instala — cada um carrega
  um play ou uma skill e roda. Um arquivo cada em `commands/`.
- **A convenção de nomes** — por que skills são substantivos, comandos são
  verbos e o piso é lei — está em [NAMING.md](NAMING.md).
- **Selos de esforço** — a afirmação de custo de uma linha de cada skill
  (free / light / heavy) e a linha **Weight:** que fecha cada play são
  decodificadas em [NAMING.md](NAMING.md#selos-de-esforço).

## As skills

| Skill | O que ela faz |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | Adota uma capacidade open-source existente e a re-engenheira como skill nativa, em vez de construir uma cópia. |
| [blind-eval](skills/blind-eval/SKILL.md) | Julga uma mudança pelos méritos, com a autoria escondida, e então mantém ou reverte. Só melhoria provada pousa. |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | Jurados cegos, de famílias de modelos diferentes, avaliam a mudança, uma lente cada. Todo achado vira um teste que falha. Repete até todos aprovarem. |
| [bounded-loops](skills/bounded-loops/SKILL.md) | Tetos de orçamento, checkpoints e kill-switches em todo loop. Torna martelar uma API estruturalmente impossível. |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | Uma régua de qualidade determinística: testes sniper, o score CRAP (complexidade x cobertura), teste de mutação com limites, depois uma revisão leve de gosto. |
| [decision-bar](skills/decision-bar/SKILL.md) | Uma régua para toda decisão: só gosto, visão ou risco destrutivo chegam ao humano. Todo o resto executa. |
| [design-taste](skills/design-taste/SKILL.md) | Entrega trabalho visual que parece desenhado, não gerado: design tokens primeiro, crítica por screenshot, um gate duro de acessibilidade. |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | Resolve a escada viva de modelos: sonda o que está no ar, faz fallback em ordem, falha alto quando a escada acaba. |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | Um modelo por GPU, sem vazar para a RAM do sistema, placa quente durante o loop inteiro, descarrega no fim do loop. |
| [guided-steps](skills/guided-steps/SKILL.md) | Roteiriza os passos que só um humano consegue fazer — dashboards, credenciais, segredos — etapa por etapa, capturando cada valor. |
| [human-calibration](skills/human-calibration/SKILL.md) | Constrói um perfil de como esse humano pensa, decide e quer que falem com ele, e conduz o build inteiro por esse perfil. |
| [incident-closure](skills/incident-closure/SKILL.md) | "Conserta" significa fechamento completo — causa-raiz com evidência, teste falhando, verde, prova ao vivo — nunca um menu de opções de volta para o humano. |
| [intent-compiler](skills/intent-compiler/SKILL.md) | Lê a linguagem natural do humano — dialeto, metáfora, atalho — como uma spec completa, e a executa inteira. Todo dialeto é uma gramática válida; a skill lê cultura como contexto com lógica interna própria, nunca como estereótipo. |
| [invariant-floor](skills/invariant-floor/SKILL.md) | As leis numeradas que toda mudança autônoma precisa cumprir antes de pousar. O piso onde o pacote inteiro se apoia. |
| [leap-protocol](skills/leap-protocol/SKILL.md) | Divide trabalho grande em bolas de dono único, distribui para builders paralelos em worktrees isolados, reconcilia por uma só espinha de escrita. |
| [live-research](skills/live-research/SKILL.md) | Um agente de pesquisa paralelo lê a fonte viva — READMEs, docs, o código de verdade — para o raciocínio se apoiar no que existe, não na memória. |
| [model-fusion](skills/model-fusion/SKILL.md) | Um painel de modelos rascunha em paralelo, um juiz independente escolhe, e o vencedor é validado contra a intenção original. |
| [optimus](skills/optimus/SKILL.md) | Nenhum código antes de o harness carregar. Um hook determinístico bloqueia ferramentas de mutação até o agente ter lido as regras. |
| [human-voice](skills/human-voice/SKILL.md) | A régua sem-diploma: se ler exige diploma, reescreva. Mantém a ideia inteira enquanto tira os cacoetes de máquina. |
| [red-first](skills/red-first/SKILL.md) | Commita um teste comprovadamente falhando antes de o build começar. O builder não pode tocá-lo. Um avaliador verifica que ele nunca se moveu. |
| [repair-loop](skills/repair-loop/SKILL.md) | O ciclo de conserto completo: ancorar no piso, reproduzir, teste vermelho, consertar a classe, verificar no caminho real, avaliação independente, pousar. |
| [root-cause-first](skills/root-cause-first/SKILL.md) | Nenhum conserto sem investigação. Reproduza sob demanda, instrumente as fronteiras, rastreie os dados de volta até a origem. |
| [seam-engineering](skills/seam-engineering/SKILL.md) | Conserta a classe da falha uma vez, na primitiva compartilhada, varre cada irmão, e planta uma guarda que pega o próximo infrator. |
| [session-handoff](skills/session-handoff/SKILL.md) | Compacta uma sessão num arquivo único que um agente novo em folha lê a frio e continua. Segredos redigidos. |
| [sniper-testing](skills/sniper-testing/SKILL.md) | Rode só os testes que cobrem o que você tocou. Mate o teatro de mock — testes que passam com a capacidade quebrada. |
| [understanding-gates](skills/understanding-gates/SKILL.md) | Trava Design, Plano, Build, Teste e Entrega com vereditos aprovar/revisar/rejeitar, para o build seguir batendo com o pedido. |
| [wayfinder](skills/wayfinder/SKILL.md) | Quando perdido, traça um mapa de decisão até o destino, em vez de estacionar uma pergunta no humano. |

## Os plays

| Play | O que ele roda |
| --- | --- |
| [elite-build](plays/elite-build.md) | O play mestre para qualquer build, conserto ou melhoria: ler a intenção, travar o plano, provar o vermelho, construir, testar apertado, avaliar às cegas, pousar com prova ao vivo. |
| [agent-builds](plays/agent-builds.md) | Construção de agentes e serviços: primitivas determinísticas fazem o trabalho pesado; o modelo só raciocina onde raciocinar é a única coisa que funciona. |
| [web-app-builds](plays/web-app-builds.md) | Apps e sites web com estrutura limpa e cadeia de suprimentos defendida — higiene de dependências é o play, não uma nota de rodapé. |
| [design-taste](plays/design-taste.md) | UI que parece desenhada, não gerada: separar a criação do gosto da implementação, definir tokens primeiro, dar olhos ao agente, travar na acessibilidade. |
| [grading-verification](plays/grading-verification.md) | Avaliação adversarial: um resultado verde é uma alegação, não uma prova. O avaliador ataca, e o piso não pode ser burlado. |
| [parallel-work](plays/parallel-work.md) | Espalhar trabalho entre agentes sem que se atropelem: uma só espinha de escrita, muitos leitores. |
| [security-delivery](plays/security-delivery.md) | O gate de entrega para qualquer coisa que um cliente ou outra máquina vai rodar. Seguro por construção, não por memória. |
| [bughunt](plays/bughunt.md) | Uma caçada de bugs paralela e com limites: traçar o mapa, espalhar caçadores, verificar cada achado de forma adversarial, fechar costuras inteiras. |

## Funciona melhor com

Estas skills são a camada portátil do **BACKS AIOS**, uma plataforma de agentes
construída por [Tcuzzo](https://github.com/Tcuzzo) — um sistema indexado por
grafo e imposto por gates, onde o harness, não o modelo, segura a disciplina. O
sistema completo — seu design de memória, seus perfis de comportamento de
modelo, seu grafo de código — não está neste pacote. As skills ainda ficam de pé
sozinhas em qualquer agente: Claude Code, OpenClaw, Hermes, Codex, Cursor, ou um
loop de API puro. Quanto maior a autonomia do seu agente, mais o piso se paga.

## Créditos

Composição e conversão por [Tcuzzo](https://github.com/Tcuzzo). Algumas skills
carregam créditos de scaffold pelos trabalhos publicados que enxertam; eles
estão anotados no próprio texto e reunidos em [NOTICE.md](../../NOTICE.md).
Licença [MIT](../../LICENSE). Contribuições são bem-vindas — mantenha os
créditos intactos.
