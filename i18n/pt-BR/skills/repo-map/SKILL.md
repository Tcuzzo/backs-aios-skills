---
name: "repo-map"
description: "Use na primeira sessão em um repo frio sem índice e sempre que o mapa ficar velho. Percorre a árvore uma vez, escreve um CODE_MAP.md na raiz e faz toda sessão futura ler o mapa primeiro — mapa primeiro, árvore crua só quando o mapa não tiver a resposta. Trigger words: repo map, code map, map first, map-first, index the repo, cold repo, stale map, refresh the map, mapa do repo, mapa de código, indexar o repo, atualizar o mapa."
license: "MIT"
---

# Repo Map
**Effort:** light — uma caminhada na primeira vez, quase grátis depois. Remove: agentes redescobrindo a forma do repo em toda sessão — o maior imposto de latência e tokens num repo sem índice.

Um codebase indexado responde “onde X mora” de graça. A maioria dos repos não tem
índice, então cada sessão paga o mesmo imposto: percorre a árvore, redescobre o layout
e esquece tudo no fim. Esta skill paga uma vez. Percorra a árvore uma vez, escreva o
que aprendeu num mapa e faça toda pergunta futura ler o mapa antes de caminhar.

## Quando rodar

- Na primeira sessão em um repo frio — sem mapa e sem índice.
- Sempre que o mapa ficar velho (veja a regra abaixo).

## Os passos

1. **Percorra a árvore uma vez.** Uma passada na estrutura real: diretórios, pontos
   de entrada e onde as coisas moram. Essa deve ser a única caminhada completa que
   o repo precisa.
2. **Escreva um `CODE_MAP.md` na raiz do repo.** Ele carrega:
   - os pontos de entrada — onde a execução começa;
   - as seções e costuras, cada uma com seu propósito em uma linha;
   - onde ficam os testes;
   - os comandos de build, execução e teste;
   - os caminhos quentes — semeados pelo histórico (frequência de
     `git log --name-only`), ou vazios para sessões futuras preencherem.
3. **Mantenha enxuto.** É mapa, não documentação. Uma linha por fato. Se uma entrada
   vira parágrafo, está virando doc — corte de volta para um ponteiro.
4. **Registre a forma da árvore.** Guarde no mapa uma impressão digital barata,
   `git ls-files | sha256sum` (pega adições, movimentos e renomes), para uma sessão
   futura saber se a forma mudou.

## A lei mapa-primeiro

Pesquisa, orientação e plays leem o mapa ANTES de percorrer a árvore. A caminhada
crua é fallback quando o mapa não tem resposta — e tudo que ela aprende entra NO mapa
antes de a sessão seguir. O mapa absorve toda caminhada. A redescoberta é paga uma
vez, nunca por sessão.

## A regra de validade

Atualize o mapa só quando a forma da árvore mudar — arquivos adicionados, movidos ou
renomeados desde o estado registrado. Compare a impressão guardada
(`git ls-files | sha256sum`) com a árvore viva. Nunca atualize por relógio. Nunca em
toda sessão. Um mapa refeito por agenda é só o imposto por sessão com nome novo.

## Regras duras

- **Fatos e locais, nunca opiniões.** “Auth mora em `src/auth/`” pertence ao mapa;
  “o código de auth está bagunçado” não.
- **Ponteiro morto morre quando é encontrado.** Um caminho que não resolve mais é
  consertado ou cortado na hora. Um mapa mentiroso é pior que mapa nenhum.
- **O mapa nunca carrega segredos.** Sem keys, tokens, credenciais ou hostnames
  privados. É arquivo rastreado; trate como tal.

## Funciona bem com

- [live-research](../live-research/SKILL.md) — o pesquisador lê o mapa primeiro, depois a fonte.
- [wayfinder](../wayfinder/SKILL.md) — a orientação começa no mapa, não numa caminhada fria.
- [session-handoff](../session-handoff/SKILL.md) — o mapa é a parte do handoff que toda sessão compartilha.
