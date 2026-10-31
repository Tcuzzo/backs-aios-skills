<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/reflex-seam-dark.svg">
  <img alt="O Reflex Seam. À esquerda, um runtime determinístico é dono do estado, dos arquivos, das regras e dos testes. À direita, um kernel de julgamento do modelo é dono da inferência, da política, da reversibilidade e da prioridade. Entre eles corre uma costura serrilhada. Os sinais de decisão cruzam do modelo para o runtime, e as atualizações de estado cruzam de volta. Uma mudança de estado sem permissão é recusada em voz alta." src="../../assets/reflex-seam-light.svg">
</picture>

# BACKS AIOS Skills

**Leia isto em:** [English](../../README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Deutsch](../de/README.md) · [हिन्दी](../hi/README.md) · [简体中文](../zh-CN/README.md)

**O modelo decide. O runtime é dono do estado, dos arquivos e das regras — e se o modelo
tentar pegar um estado que não é dele, o sistema falha em voz alta em vez de adivinhar.**

Essa linha é o **Reflex Seam**, e este pack a leva a um agente que você já usa.
O hook entrega os corpos reais do piso, Optimus, Yoke e Build Flow ao contexto do
host. Se faltar contexto, ele carrega e comunica qualquer diagnóstico; não recusa
ferramentas nem revoga aterramento adquirido. Recibos de carregamento não são
apresentados como invocações de skills que nunca ocorreram.

Duas regras vêm junto. **Sem teatro de mocks:** um teste que passa enquanto a coisa está
quebrada é mentira, então os testes afirmam efeitos reais. **Quem constrói não avalia:** o
teste que falha é escrito primeiro, e algo que não escreveu o código precisa aprová-lo.

> Esta é a tradução em português (Brasil). O [README em inglês](../../README.md) é a versão canônica.

O pack contém **62 pastas de skills**: **54 métodos e aliases traduzidos** e
8 entradas de comando, além de **8 plays e 15 adaptadores de comando**. Os métodos
portáteis são distribuídos como Markdown que o agente consegue carregar.

Para aprender visualmente, consulte o [guia das skills e dos loops](../../docs/FLOWCHARTS.md).

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
- **Plays** combinam métodos e gates do domínio dentro do pacote atual do Build
  Flow. Um responsável pela integração conduz trabalho com orçamento compartilhado;
  cada especialista devolve evidências sem reiniciar a tarefa. Um arquivo por play:
  `plays/<name>.md`.
- **Comandos** são as entradas de barra que o plugin instala — cada um carrega
  um play ou uma skill e roda. Um arquivo cada em `command-adapters/`.
- **A convenção de nomes** — por que skills são substantivos, comandos são
  verbos e o piso é lei — está em [NAMING.md](NAMING.md).
- **Selos de esforço** — a afirmação de custo de uma linha de cada skill
  (free / light / heavy) e a linha **Weight:** que fecha cada play são
  decodificadas em [NAMING.md](NAMING.md#selos-de-esforço).

## Integração de Build Flow e essência do operador

[backs-build-flow](skills/backs-build-flow/SKILL.md) mantém uma tarefa e um responsável:
contexto suficiente → RED selado → correção mínima → lint, tipos e tests reais →
[clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) → revisão e entrega
autorizada. O escopo vai do `base_sha` fixado ao candidato atual, mesmo após
commits, e todos os trabalhadores e retries gastam o mesmo orçamento. Lacuna nova
recebe test separado; o RED original permanece intacto.

[operator-essence](skills/operator-essence/SKILL.md) fornece recorte privado
baseado em evidências qualitativas e quantitativas. Se o arquivo faltar, usa uma
vez os insights suportados do host ou declara a alternativa disponível. Dados
escassos ficam provisórios; não bloqueiam trabalho autorizado. Pedido e correções
atuais prevalecem sobre tendências históricas. Essência não é persona fixa,
política financeira/de risco nem autorização.

## As skills

| Skill | O que ela faz |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | Adota uma capacidade open-source existente e a re-engenheira como skill nativa, em vez de construir uma cópia. |
| [architecture-engineer](skills/architecture-engineer/SKILL.md) | Revisa fronteiras, dependências e responsabilidades contra regras do projeto e registra decisões de arquitetura. |
| [backs-build-flow](skills/backs-build-flow/SKILL.md) | Um responsável coordena contexto suficiente, essência do operador, RED/GREEN limitado, lint/tipos/tests, gauntlet e entrega verificada. |
| [backs-pack-sync](skills/backs-pack-sync/SKILL.md) | Compara cobertura privada e pública sem revelar dados privados; adiciona capacidades somente por pontes públicas revisadas. |
| [backs-session-rollover](skills/backs-session-rollover/SKILL.md) | Preserva objetivo, correções, evidências e passo pendente ao compactar contexto e continuar em sessão nova. |
| [blind-eval](skills/blind-eval/SKILL.md) | Julga uma mudança pelos méritos, com a autoria escondida, e então mantém ou reverte. Só melhoria provada pousa. |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | Jurados em sessões novas sem contexto do autor revisam pacote sem autoria; achados retornam a RED suplementar e revisão dentro do orçamento. |
| [bounded-loops](skills/bounded-loops/SKILL.md) | Um único orçamento restante da missão limita retries, trabalhadores, modelos e revisões; esgotamento preserva checkpoint honesto. |
| [building-with-backs](skills/building-with-backs/SKILL.md) | Resolve checkout e caminho exatos e leva mudança autorizada à superfície real com evidências de revisão e entrega. |
| [cam-iot-inventory](skills/cam-iot-inventory/SKILL.md) | Inventaria câmeras, IoT e Wi-Fi com identidade estável e evidência honesta; distingue inventário de imagem disponível. |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | Uma régua de qualidade determinística: testes sniper, o score CRAP (complexidade x cobertura), teste de mutação com limites, depois uma revisão leve de gosto. |
| [co-health](skills/co-health/SKILL.md) | Observa evidências do harness e watchdog e comunica achados preservando ferramentas e código. |
| [conscientious-objector](skills/conscientious-objector/SKILL.md) | Observa evidências do harness e watchdog sem retirar ferramentas nem alterar código do operador. |
| [context-compiler](skills/context-compiler/SKILL.md) | Alias compatível de context-engineer; preserva o mesmo método e pacote de execução. |
| [context-engineer](skills/context-engineer/SKILL.md) | Reconstrói apenas contexto ausente, verifica alvo e próxima ação e preserva orçamento, evidências e essência pertinente. |
| [context_engineer](skills/context_engineer/SKILL.md) | Alias compatível de context-engineer com conteúdo idêntico. |
| [debugging-engineer](skills/debugging-engineer/SKILL.md) | Investiga regressões difíceis, falhas silenciosas e corridas com hipóteses refutáveis e sondagens decisivas antes de editar. |
| [decision-bar](skills/decision-bar/SKILL.md) | Uma régua para toda decisão: só gosto, visão ou risco destrutivo chegam ao humano. Todo o resto executa. |
| [design-critique](skills/design-critique/SKILL.md) | Critica a superfície real pela tarefa do usuário, hierarquia, acessibilidade, movimento e coerência visual. |
| [design-taste](skills/design-taste/SKILL.md) | Entrega trabalho visual que parece desenhado, não gerado: design tokens primeiro, crítica por screenshot, um gate duro de acessibilidade. |
| [fix-shit](skills/fix-shit/SKILL.md) | Entrada direta para diagnóstico e reparo limitado da classe de falha, com RED selado e prova real de entrega. |
| [fleet-dispatch](skills/fleet-dispatch/SKILL.md) | Despacha por papel pela escada configurada e devolve resultados com proveniência real. |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | Resolve a escada viva de modelos: sonda o que está no ar, faz fallback em ordem, falha alto quando a escada acaba. |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | Um modelo por GPU, sem vazar para a RAM do sistema, placa quente durante o loop inteiro, descarrega no fim do loop. |
| [guided-steps](skills/guided-steps/SKILL.md) | Roteiriza os passos que só um humano consegue fazer — dashboards, credenciais, segredos — etapa por etapa, capturando cada valor. |
| [harness-optimizer](skills/harness-optimizer/SKILL.md) | Compara baseline e candidato por experimentos limitados, dados reservados e verificações de vazamento e sobreajuste. |
| [human-calibration](skills/human-calibration/SKILL.md) | Aplica preferências expressas e corrigidas do operador pela essência existente, sem questionários duplicados nem persona fixa. |
| [human-voice](skills/human-voice/SKILL.md) | A régua sem-diploma: se ler exige diploma, reescreva. Mantém a ideia inteira enquanto tira os cacoetes de máquina. |
| [incident-closure](skills/incident-closure/SKILL.md) | "Conserta" significa fechamento completo — causa-raiz com evidência, teste falhando, verde, prova ao vivo — nunca um menu de opções de volta para o humano. |
| [intent-compiler](skills/intent-compiler/SKILL.md) | Interpreta o pedido atual em contrato executável; separa fatos, preferências e inferências e reutiliza a diretriz vigente. |
| [invariant-floor](skills/invariant-floor/SKILL.md) | As leis numeradas que toda mudança autônoma precisa cumprir antes de pousar. O piso onde o pacote inteiro se apoia. |
| [karpathy](skills/karpathy/SKILL.md) | Experimenta em clone descartável com meta, métricas, arquivos permitidos e orçamento explícitos; mantém melhorias comprovadas. |
| [leap-protocol](skills/leap-protocol/SKILL.md) | Divide trabalho grande em bolas de dono único, distribui para builders paralelos em worktrees isolados, reconcilia por uma só espinha de escrita. |
| [live-research](skills/live-research/SKILL.md) | Um agente de pesquisa paralelo lê a fonte viva — READMEs, docs, o código de verdade — para o raciocínio se apoiar no que existe, não na memória. |
| [model-fusion](skills/model-fusion/SKILL.md) | Um painel de modelos rascunha em paralelo, um juiz independente escolhe, e o vencedor é validado contra a intenção original. |
| [operator-essence](skills/operator-essence/SKILL.md) | Fornece contexto privado qualitativo e quantitativo com fontes, limites e incerteza; usa insights ou alternativa disponível uma única vez. |
| [operator-intent-deduction](skills/operator-intent-deduction/SKILL.md) | Resolve decisões pendentes pelo pedido atual, fatos verificados e contexto sustentado, sem fixar identidade nem política de risco. |
| [operator_intent_deduction](skills/operator_intent_deduction/SKILL.md) | Alias compatível de operator-intent-deduction com conteúdo idêntico. |
| [optimus](skills/optimus/SKILL.md) | Carrega corpos reais do piso, Yoke e Build Flow no contexto; o hook não recusa ferramentas nem reinicia a tarefa. |
| [osha-bot](skills/osha-bot/SKILL.md) | Observa evidências do harness e watchdog e preserva ferramentas, código e controle do operador. |
| [rea-investigation](skills/rea-investigation/SKILL.md) | Devolve evidências REA de descoberta ou verificação ao responsável atual sem reiniciar adoção ou reparo. |
| [red-first](skills/red-first/SKILL.md) | Commita um teste comprovadamente falhando antes de o build começar. O builder não pode tocá-lo. Um avaliador verifica que ele nunca se moveu. |
| [reload-vsc-and-verify](skills/reload-vsc-and-verify/SKILL.md) | Detecta instalação local, conecta skills ausentes e recarrega VS Code com verificação de descoberta. |
| [repair-loop](skills/repair-loop/SKILL.md) | O ciclo de conserto completo: ancorar no piso, reproduzir, teste vermelho, consertar a classe, verificar no caminho real, avaliação independente, pousar. |
| [repo-map](skills/repo-map/SKILL.md) | Mapeie primeiro a estrutura real do repositório, pontos de entrada, configuração e caminhos de execução antes de alterar código. |
| [root-cause-first](skills/root-cause-first/SKILL.md) | Nenhum conserto sem investigação. Reproduza sob demanda, instrumente as fronteiras, rastreie os dados de volta até a origem. |
| [scrub-plugin-pack-literals](skills/scrub-plugin-pack-literals/SKILL.md) | Detecta e remove literais privados do pack público sem enfraquecer higiene de publicação. |
| [seam-engineering](skills/seam-engineering/SKILL.md) | Conserta a classe da falha uma vez, na primitiva compartilhada, varre cada irmão, e planta uma guarda que pega o próximo infrator. |
| [session-handoff](skills/session-handoff/SKILL.md) | Transfere o mesmo pacote, candidato, selos RED, evidências, prazo e orçamento restante respeitando modo somente leitura. |
| [sniper-testing](skills/sniper-testing/SKILL.md) | Deriva lint, tipos e tests reais do diff completo entre base fixada e candidato, incluindo pendências pertinentes. |
| [truth-audit](skills/truth-audit/SKILL.md) | Verifica em somente leitura o que realmente executa e converte achados comprovados em especificação de reparo. |
| [turn-and-burn](skills/turn-and-burn/SKILL.md) | Coordena preparação da missão, revisão do plano e capacidades ausentes por pesquisa e adoção. |
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
