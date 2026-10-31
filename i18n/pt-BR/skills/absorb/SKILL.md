---
name: "absorb"
description: "Use quando uma capacidade necessária puder existir em projeto open source, ou o operador pedir para absorver, adotar, portar, reengenheirar, ingerir um repo, avaliar arte prévia ou tornar nativa uma capacidade."
license: "MIT"
---

# Absorb — Adote a Arte Prévia, Não Reinvente
**Effort:** light — uma ingestão de repo (sonda de metadados + clone raso) e uma avaliação independente (assento não-autor, resolvido por capacidade) do código portado. Remove: reinventar uma capacidade que a arte prévia já resolveu — a duplicata feita do zero cujos bugs todos seriam dívida sua.

**Capacidade é rei.** Um repo é um veículo para uma capacidade. Quando você precisa
de algo que um projeto existente já faz, não construa uma cópia do zero, e não faça
clone-e-cola. Ache a melhor arte prévia, extraia a capacidade, reengenheire para
encaixar no seu harness e cite o scaffold (a estrutura emprestada). A citação é um
fato, não um enfeite.

## Quando rodar

- Pediram para você adicionar uma capacidade (uma tool, skill, agente, pipeline) que
  o open source provavelmente já resolveu.
- Você está prestes a dar `git clone` e copiar código na íntegra — pare; o caminho é este.
- Pule para um snippet isolado, um valor de config ou uma consulta de fato. Esses, só leia.

## Passos

Use o pacote atual do [BACKS Build Flow](../backs-build-flow/SKILL.md) e seu
responsável pela integração. Invocação direta cria esse pacote uma vez; chamada
aninhada devolve evidências de adoção ao chamador. Reutilize contexto válido,
essência do operador e corpos já carregados.
[bounded-loops](../bounded-loops/SKILL.md) cuida do prazo e cotas restantes da
missão; descoberta, construção, mutações, revisões, trocas de modelo e handoffs
gastam o mesmo orçamento. Fase ou trabalhador novo não o reinicia. Respeite
`task_mode`: revisão ou diagnóstico não autoriza edições nativas nem entrega.

1. **Cace a arte prévia primeiro.** Pesquise antes de construir. Uma cópia que você
   inventa é pior que um scaffold que você adota: você herda zero teste de campo e
   fica devendo todos os bugs.
2. **Descubra além do README.** Busque metadados do projeto (licença, atividade,
   linguagem) pela API da plataforma. Faça clone raso em diretório temporário.
   Leia código e tests. Para artefatos distribuídos ou comportamento solicitado
   que inspeção do código não resolva, chame
   [rea-investigation](../rea-investigation/SKILL.md) com alvo exato e pergunta
   limitada. REA devolve evidências a este chamador; não reinicia Absorb. Registre
   identidade original, observações, limites e incógnitas antes de escolher o que
   adotar. Achados estáticos não estabelecem comportamento de runtime.
3. **Rode os portões de confiança.**
   - *Licença:* permissiva (MIT / Apache / BSD / MPL) = seguro reengenheirar.
     Copyleft (GPL / AGPL) = só a técnica — reengenheire a ideia, nunca copie o
     código. Sem licença = trate como todos-os-direitos-reservados, só a técnica.
     Termos não-comerciais = bloqueio; leve para o seu humano.
   - *Varredura de coisa suspeita:* use `rg` para padrões de cloak / spam / fake-review /
     golpe. Sinalize alto.
   - *Nada de install selvagem:* nunca dê `pip install` / `npm install` numa
     dependência não auditada (typo-squatting é um ataque real de supply chain).
     Em vez disso, reengenheire como código fino por cima das suas próprias primitivas.
   - *A capacidade é real?* Verifique as alegações contra evidência independente. O
     blog de quem vende é alegação, não evidência. Veredito: real / hype / golpe /
     não-verificável.
   - *Egress limitado:* tudo que a versão adotada busca na rede precisa de throttle,
     cache e um jeito de matar.
4. **Desconstrua num mapa de capacidades.** Para cada habilidade que o projeto
   entrega, registre: o que faz, como, as costuras que sustentam o peso, o inchaço ou
   risco, o que você reaproveita do seu próprio stack, e se aterrissa nativa ou atrás
   de um adaptador fino. Cada capacidade é **preservada ou refutada com evidência**.
   Capacidade derrubada em silêncio é defeito.
5. **Escreva a spec de reengenharia.** As costuras a construir, o inchaço que você
   está cortando (registrado alto, nunca em silêncio), e um teste de contrato que
   falha por capacidade, afirmando um efeito colateral real — um arquivo, uma linha
   no banco, saída de verdade. Mocke só o transporte de uma API externa paga, nunca
   a lógica.
6. **Integração nativa.** Aplique [red-first](../red-first/SKILL.md): observe
   falha real e sele o contrato antes da correção mínima na costura responsável.
   Preserve intacto o test original. Delimite comandos reais de lint, tipos e tests
   do repo por [sniper-testing](../sniper-testing/SKILL.md), com `base_sha` fixado
   e `candidate_sha` atual, incluindo caminhos pendentes próprios. Registre
   verificações indisponíveis ou inaplicáveis; nunca instale verificador arbitrário
   nem invente aprovação. Rode [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
   no mesmo fluxo para evidências de qualidade/mutação. Lacuna recebe regressão
   suplementar separada, nunca edição do original selado. Tudo fica no orçamento
   compartilhado.
7. **Verifique a capacidade adotada.** Exercite resultado nativo contra mapa
   de capacidades e superfície real do usuário. Reutilize evidências de descoberta;
   solicite outra observação REA apenas para comparação concreta pendente, dentro
   dos limites existentes de provedor e execução. Escolha avaliador capaz pela
   matriz configurada para revisão nova separada do autor do candidato agregado
   exato; registre e exclua a execução autora. O builder nunca avalia a si mesmo.
   Execute a passagem exigida das suites afetadas e siga a entrega autorizada do
   projeto. Evidência estática original ou GREEN local não prova entrega nativa ao vivo.
8. **Cite e registre.** Preserve o crédito do scaffold onde vive a capacidade:
   autor, projeto, licença, o que foi emprestado e o que é reengenharia própria.
   Nunca invente nem apague crédito. Devolva mapa de capacidades, candidato exato,
   verificações, atribuição e lacunas ao responsável pela integração. Se o orçamento
   acabar ou gate obrigatório não puder rodar, salve **STILL-BUILDING** com trabalho
   restante e próxima ação; continue trabalho útil autorizado que não gaste a cota
   esgotada. Nunca fabrique **PROVEN** nem omita capacidade para obter aprovação.

## Regras duras — qualquer uma delas reprova a skill

- Copiar código na íntegra em vez de reengenheirar a capacidade.
- Construir uma cópia sem nunca ter procurado arte prévia.
- Confiar no README ou numa página de marketing mais que no código.
- Instalar uma dependência selvagem em vez de reengenheirar a técnica.
- Copiar código copyleft ou sem licença (só a técnica, sempre).
- Derrubar uma capacidade sem refutação por escrito.
- Teatro de mock num teste de capacidade — o teste tem que tocar um efeito colateral real.
- Entregar sem a citação do scaffold.

## Combina bem com

- [red-first](../red-first/SKILL.md) — os testes de contrato que guardam cada capacidade.
- [sniper-testing](../sniper-testing/SKILL.md) — efeitos colaterais reais, sem teatro de mock.
- [blind-tribunal](../blind-tribunal/SKILL.md) — avaliação independente, não-autor, do porte.
- [decision-bar](../decision-bar/SKILL.md) — bloqueios de licença e decisões de gosto vão para o seu humano; todo o resto executa.
