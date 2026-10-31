# Play: Parallel Work

Como espalhar trabalho entre agentes sem que eles se atropelem. A regra que paga
por todas as outras: uma só espinha de escrita, muitos leitores.

## Quando rodar

- Uma tarefa se divide em pesquisa, varredura, testes ou avaliação que podem
  rodar ao mesmo tempo.
- Mais de um agente vai mexer no mesmo repositório na mesma janela de tempo.
- Você está tentado a deixar dois agentes escreverem código em paralelo. Leia
  isto primeiro.

## Tarefa e limites compartilhados

Aplique este play dentro do pacote atual do
[BACKS Build Flow](../skills/backs-build-flow/SKILL.md). Mantenha um responsável
pela integração, `task_mode` solicitado, revisões base e candidata fixadas,
essência do operador e evidências atuais. Reutilize corpos pertinentes já carregados;
este play acrescenta gates do domínio sem reiniciar a tarefa.

[bounded-loops](../skills/bounded-loops/SKILL.md) cuida do prazo original e cotas
restantes entre retries, trabalhadores, modelos, revisões e handoffs. Nunca os
reinicie para um play aninhado. Ao esgotar, salve **STILL-BUILDING** com candidato,
evidências, gates pendentes e próxima ação. Continue trabalho útil autorizado só
dentro da cota restante; gate ausente não vira aprovação.

## A cadeia

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — divida trabalho em bolas
   com objetivos, specs e escopo estrito de arquivos ANTES de criar agentes.
   Entregue a cada lane pacote atual, base/candidato fixados, selos RED e cota
   restante alocada. Seu limite não pode ampliar prazo nem totais da missão.

2. Crie leitores, não escritores — espalhe subagentes SÓ para trabalho pesado em
   leitura, com poucas dependências cruzadas: pesquisa, rodar testes, varreduras
   de segurança, avaliação. Nunca para autoria de código interdependente.
3. Isole cada lane — cada agente paralelo ganha seu PRÓPRIO worktree (um
   checkout separado do mesmo repositório). Os conflitos então aparecem no merge
   como conflitos de merge de verdade, nunca como sobrescritas silenciosas que
   perdem dados sem aviso.
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — cada lane
   executa seu gauntlet no isolamento/worktree permitido antes de integrar. Use
   primeiro [sniper-testing](../skills/sniper-testing/SKILL.md) para comandos reais
   de lint/tipos/tests pelo diff agregado fixado; declare ausências ou N/A.
   Reutilize recibo válido só para o mesmo candidato e escopo; não aplique verde
   de outra lane a bytes diferentes. Cobertura ausente recebe arquivo suplementar
   separado, preservando originais selados.

5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — o agente revisor recebe
   um contexto LIMPO, nunca o do autor. Contexto compartilhado apodrece e
   concorda consigo mesmo.
6. Faça merge de uma lane por vez em workspace dedicado, com gate de tests por
   exit code. O responsável pela integração verifica candidato combinado, consumidores
   e passagem completa exigida das suites afetadas; aprovações independentes não
   provam a composição. Afirmar entrega exige evidência do alvo real.

## Regras de coordenação

- UM agente escreve código por workspace, num contexto coerente. Escritores
  paralelos tomam decisões implícitas conflitantes que nenhum merge reconcilia.
- Declare de saída a posse de arquivos por agente. Cada agente edita SÓ os seus
  arquivos nomeados.
- Coordene por um tracker (issues, tickets) — nunca por um arquivo de checklist
  compartilhado na árvore de trabalho. Esse arquivo é, ele mesmo, uma superfície
  de conflito de merge, e faz dois agentes pegarem a mesma tarefa.
- Cada subagente devolve um resumo destilado — fatos-chave, decisões,
  pendências, uma ou duas páginas — nunca a transcrição inteira.
- Persista o plano, a spec e as decisões em disco e releia de lá. Execuções
  longas compactam o contexto e derrubam instruções em silêncio; regras que
  devem valer sempre vivem no arquivo sempre-carregado, e em nenhum outro lugar.

## Disciplina de merge

- Trave TODO merge por exit code de teste antes de pousar. Suíte vermelha
  bloqueia o merge. Só isso já corta a maior parte da quebra causada por
  agentes.
- Faça o merge num espaço dedicado e depois verifique o resultado por stat:
  contagem de arquivos, diffstat, os arquivos nomeados de cada lane presentes.
  Um merge que derruba em silêncio os arquivos de uma lane é o pior merge que
  existe — cheque isso toda vez.

## Gates duros — qualquer um reprova o play

- Dois agentes escrevendo código no mesmo workspace ao mesmo tempo.
- Uma lane editando fora do escopo de arquivos que declarou.
- Um merge pousado sem exit code verde, ou sem a verificação por stat.
- Um revisor que compartilhou contexto com o autor.
- Uma lane pousando em cima dos resultados de teste de outra, ou mockando a
  costura que mudou.

**Weight:** heavy por projeto — decomposição leap, um gauntlet por lane e um tribunal de contexto limpo — o gasto só se paga quando o trabalho é grande o bastante para dividir, que é a única hora de rodar este play.
