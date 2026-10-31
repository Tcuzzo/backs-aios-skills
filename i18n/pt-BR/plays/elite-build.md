# Elite Build — o play mestre

Use este play completo quando solicitado expressamente ou quando construção,
correção ou melhoria precisar de suas etapas compostas de design, construção,
qualidade e revisão. O humano declara o objetivo uma vez. Mudança focada pode
usar métodos pertinentes do BACKS Build Flow sem iniciar todo este play;
selecioná-lo preserva todos os gates aplicáveis abaixo.

## Uma tarefa, um responsável pela integração

[BACKS Build Flow](../skills/backs-build-flow/SKILL.md) cuida do pacote da tarefa,
`task_mode`, essência do operador e conclusão. Reutilize contexto atual, corpos
reais carregados e evidências; atualize etapa apenas quando entradas ou candidato
mudarem. Preserve `base_sha` fixado, `candidate_sha` atual e um responsável entre
todas as lanes. Chamar especialista não inicia outro ciclo de vida.

[bounded-loops](../skills/bounded-loops/SKILL.md) cuida do prazo original e cotas
restantes. Pesquisa, builders, lint/tipos/tests, mutação, revisões, modelos
alternativos e handoffs gastam os mesmos limites. Nunca os reinicie em play
aninhado. Ao esgotar, salve **STILL-BUILDING** com candidato, evidências, gates
pendentes e próxima ação; conclua trabalho útil autorizado que não consuma a cota
esgotada. Limite de orçamento não dispensa gate.

## A cadeia

0. [optimus](../skills/optimus/SKILL.md) — estabeleça piso e Build Flow uma vez
   por sessão. Reutilize os corpos reais ainda presentes no contexto e seus recibos
   de origem; um recibo sozinho não substitui um corpo ausente. Uma chamada aninhada
   não reinicia o ciclo nem afirma uma invocação que não ocorreu.
1. Use intenção e essência estabelecidas pelo Build Flow. Leia pedido inteiro e
   correções atuais; deduza a diretriz antes de apresentar decisões de entrega ou
   opções. Resolva diretamente o que pode ser resolvido com evidências.
2. [human-calibration](../skills/human-calibration/SKILL.md) — aplique o perfil
   validado já no pacote. Carregue apenas contexto aplicável ausente; nunca
   reinterrogue o humano nem reconstrua o mesmo perfil em cada etapa.
3. [turn-and-burn](../skills/turn-and-burn/SKILL.md) — preserve requisitos de
   composição da equipe e revisão do plano da missão. Consulte essência de cada
   modelo (know-thyself), `docs/BACKS_LESSONS_LEARNED.md` e `memory/MEMORY.md`
   quando disponíveis. São registros de capacidade e lições distintos da essência
   do operador. Reutilize evidências atuais do burn; qualquer Absorb necessário
   compartilha a missão e devolve resultado ao responsável pela integração.
4. [understanding-gates](../skills/understanding-gates/SKILL.md) — preserve gates
   Design → Plano → Construção → Tests → Entrega. Use
   [live-research](../skills/live-research/SKILL.md) para inspecionar caminho afetado,
   responsáveis, consumidores e costura de entrega. Siga dependências adicionais
   quando as evidências indicarem que podem mudar o resultado; não repita
   levantamento do sistema inteiro antes de cada edição. Comece o próximo passo
   executável ao atender à condição de contexto suficiente do Build Flow.
5. [architecture-engineer](../skills/architecture-engineer/SKILL.md) — se o diff
   tocar fronteira de módulo, direção de dependência ou costura compartilhada,
   aplique revisão estrutural e classificação de superfícies de autoridade.
   Cite regra local ou falha concreta por trás de cada violação; use ADR para
   decisões duradouras.
6. [wayfinder](../skills/wayfinder/SKILL.md) — trace com evidência uma rota realmente
   pendente. Não planeje novamente quando a rota já for conhecida.
7. [red-first](../skills/red-first/SKILL.md) — observe e commite contrato real
   falhando antes de executar seu builder. Registre selo e preserve arquivo original
   byte a byte. Achados posteriores recebem tests suplementares separados; não
   podem reescrever RED original.
8. Construa a menor mudança completa na costura responsável. Paralelize perguntas
   e trabalho independentes com propriedade explícita de arquivos ou worktrees
   isolados; preserve um responsável e as regras de concorrência do projeto.
   Resolva builders por [fleet-ladder](../skills/fleet-ladder/SKILL.md), usando
   [model-fusion](../skills/model-fusion/SKILL.md) quando a missão exigir.
   Para defeito, aplique [repair-loop](../skills/repair-loop/SKILL.md) dentro do
   fluxo e feche a classe na costura compartilhada com
   [seam-engineering](../skills/seam-engineering/SKILL.md). Devolva achados a esta
   tarefa sem reiniciar o play recursivamente.
9. [sniper-testing](../skills/sniper-testing/SKILL.md) — derive escopo do diff
   agregado de base a candidato mais caminhos próprios pendentes. Execute comandos
   reais de lint, tipos e tests focados do repo. Registre N/A com motivo e ferramentas
   obrigatórias ausentes como lacunas; não instale verificadores arbitrários nem
   invente aprovações. Mantenha execuções focadas durante a iteração.
10. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — aplique qualidade,
    complexidade/cobertura e mutação limitada no mesmo fluxo e candidato.
    Sobrevivente significativo ou achado retorna a RED suplementar e correção
    mínima dentro do orçamento restante. Reutilize evidência válida, nunca
    veredito desatualizado de bytes diferentes; não inicie outro ciclo completo.
11. [blind-eval](../skills/blind-eval/SKILL.md), depois
    [blind-tribunal](../skills/blind-tribunal/SKILL.md) — entregue pacote congelado
    de evidências sem autoria a revisores escolhidos ao vivo por capacidade e
    disponibilidade. Revisão usa execuções novas separadas do autor, sem conversa
    herdada do builder. Registre execução autora como proveniência e exclua-a.
    Cada achado fundamentado recebe RED separado, correção e nova revisão dentro
    da mesma cota. Todos os jurados exigidos precisam aprovar. Siga regra Solo rig
    do tribunal quando aplicável; registre configuração real e lacunas do runtime
    sem enfraquecer independência.
12. Conclua o resultado solicitado. Confira identidade do candidato, rode uma
    passagem completa das suites dos módulos tocados mais verificações obrigatórias,
    preserve trabalho concorrente e siga integração autorizada do projeto.
    Para implantação, verifique código instalado/em execução e superfície real
    do humano. Reinicie serviço apenas se entrega e procedimento exigirem.
    Patch local ou revisão não adquire escopo de publicação silenciosamente.

## Gates duros

- RED original observado falhando antes do fix e ainda intacto byte a byte;
  contratos suplementares têm evidências e selos próprios.
- Gates exigidos de qualidade, lint/tipos/tests e mutação aprovados no candidato
  exato, com N/A justificados e lacunas reais informadas honestamente.
- Revisão exigida em execução nova separada do autor; builder nunca avalia o
  próprio trabalho nem fornece ao revisor a conclusão desejada.
- Todo achado na costura própria é corrigido ou julgado com evidência. Achado
  aberto recebe checkpoint explícito e bloqueia integração; nunca é escondido.
- Requisitos aplicáveis de burn, essência, lições e revisão do plano satisfeitos
  por evidências atuais. Reutilizar evidência não autoriza pular gate obrigatório.
- Capacidade **PROVEN** significa integrada, avaliada independentemente e
  demonstrada na superfície real do humano. Caso contrário, relate
  **STILL-BUILDING** e a prova exata ausente com
  [human-voice](../skills/human-voice/SKILL.md). Declare conclusão de revisão ou
  patch solicitado separadamente de capacidade ao vivo.
- Commite somente arquivos desta tarefa. Preserve trabalho de outras sessões.

## Política da escada da frota

Use [fleet-ladder](../skills/fleet-ladder/SKILL.md) para despacho real, rotas
configuradas, sondagens, alternativas e independência da revisão. Leia
`config/fleet_ladder.yaml` e `config/gpu_nodes.yaml` da implantação quando
disponíveis; o pack não cria resolvedor. Preserve exigências de pesquisa prévia
para degraus fronteira e suas fontes permitidas de web, GitHub, Reddit e papers.
Respeite nível de raciocínio e política de eficiência de tokens configurados;
não fixe IDs de modelos nem trunque evidências para fabricar conformidade.

Use [session-handoff](../skills/session-handoff/SKILL.md) para preservar candidato,
selos, evidências, prazo e cotas restantes antes de uma interrupção.
