---
name: building-with-backs
description: "Use ao construir ou corrigir um projeto BACKS, resolver ambiguidade de pasta ou checkout, ou levar uma mudança autorizada do IDE ao runtime real."
license: MIT
---

# Construir com BACKS

Esta skill fecha uma falha recorrente: patch bom no checkout errado ou test verde
que nunca chega ao app do operador. O destino é o produto e o caminho solicitados.
Descubra o alvo antes de escrever.

Entre no pacote existente do [BACKS Build Flow](../backs-build-flow/SKILL.md);
invocação direta o estabelece uma única vez. Mantenha um responsável pela integração
e reutilize essência e contexto existentes. Respeite `task_mode` e carregue prazo
e cotas restantes de [bounded-loops](../bounded-loops/SKILL.md) entre trabalhadores,
modelos e handoffs. Resolver outro caminho não reinicia orçamento nem autoriza implantação.

1. **Resolva o destino.** Use o caminho exato nomeado pelo humano. Sem caminho
   explícito, inspecione workspace ativo, referências recentes e mapa do repo.
   Não substitua por clone próximo só porque o nome coincide. Execute
   `python scripts/resolve_target.py --repo <path> --target <file-or-directory>`
   a partir do diretório desta skill; acrescente `--expected-root <path>` se
   o humano nomeou o checkout. O comando retorna diferente de zero para raiz
   ausente, caminho fora dela, checkout divergente ou revisão Git ausente.
   Arquivo novo pode ainda não existir; o diretório pai precisa existir. Para
   projeto não Git explicitamente nomeado, acrescente `--allow-non-git` e
   registre que não há revisão disponível.
2. **Fixe a verdade inicial.** Registre raiz resolvida, branch ou HEAD destacado,
   `base_sha`, `candidate_sha` atual, estado do worktree, alvo solicitado,
   entrada do app/serviço e verificações. Mantenha a base original fixa após commits;
   atualize explicitamente a identidade do candidato e confira caminhos pendentes.
   Preserve edições alheias. Se outro checkout for mais recente, compare revisões
   e árvores reais antes de escolher; «mais recente» é uma afirmação medida.
3. **Mapeie a rota.** Trace ação do usuário até entrada, implementação, dados,
   saídas e costura de implantação. Nomeie o responsável existente pelo comportamento
   e consumidores dependentes. Use `repo-map`, `architecture-engineer` e
   `root-cause-first` quando essas costuras forem incertas.
4. **Construa no lugar resolvido.** Dê perguntas distintas a leitores paralelos
   e arquivos sem sobreposição ou worktrees isolados a escritores. Mantenha um
   responsável pela integração. Faça a menor mudança que fecha a classe de falha;
   aplique `repair-loop` dentro do fluxo atual. Siga o play completo `elite-build`
   quando selecionado ou pedido expressamente, reutilizando etapas válidas sem
   reiniciar. Revisão ou diagnóstico devolve achados sem editar.
5. **Prove o caminho.** Siga RED selado → correção mínima → verificações sniper
   de lint/tipos/tests → clean-code-gauntlet. Derive o escopo do diff agregado fixado;
   use comandos reais do repo e declare lacunas ou N/A honestamente. Preserve
   revisão separada do autor e a passagem completa obrigatória das suites afetadas
   na integração. Inspecione superfície real de app/CLI e logs dentro do escopo.
   Registre revisão/hash exato implantado e comportamento observado; nomeie
   tudo que não pôde ser exercitado.
6. **Promova pela rota própria do projeto.** Leia suas instruções de implantação
   e aprovação no próprio repo. Nunca transplante comando de outro projeto.
   Repita a verificação do alvo antes de instalar e confira depois que o processo
   em execução usa o código instalado.

Se o destino continuar ambíguo, avance na investigação somente leitura e pergunte
pelo caminho apenas depois de verificar as evidências disponíveis. Nunca afirme
instalação entre hosts só porque copiou arquivos; verifique descoberta em cada
host ou marque como não verificada.

Se uma cota acabar, salve **STILL-BUILDING** com alvo verificado, candidato,
evidência pendente e próxima ação exata. Preserve os limites originais; conclua
trabalho útil autorizado que não consuma a cota esgotada. Verificação local não
substitui evidência da entrega solicitada.
