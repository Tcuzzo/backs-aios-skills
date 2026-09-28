---
name: "absorb"
description: "Use quando você precisa de uma capacidade que um projeto open source já entrega — adote e reengenheire como skill nativa em vez de inventar uma cópia. Trigger words: absorb, adopt, port, re-engineer, ingest a repo, prior art, capability port, make this native, absorver, adotar, portar, reengenharia, ingerir um repo, arte prévia, tornar nativo."
license: "MIT"
---

# Absorb — Adote a Arte Prévia, Não Reinvente
**Effort:** light — uma ingestão de repo (sonda de metadados + clone raso) e uma avaliação cross-family do código portado. Remove: reinventar uma capacidade que a arte prévia já resolveu — a duplicata feita do zero cujos bugs todos seriam dívida sua.

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

1. **Cace a arte prévia primeiro.** Pesquise antes de construir. Uma cópia que você
   inventa é pior que um scaffold que você adota: você herda zero teste de campo e
   fica devendo todos os bugs.
2. **Vá além do README.** Puxe os metadados do projeto (licença, atividade,
   linguagem) pela API da plataforma. Faça um shallow-clone num diretório de rascunho.
   Leia o código e os testes. O README é marketing; o código é a verdade.
3. **Rode os portões de confiança.**
   - *Licença:* permissiva (MIT / Apache / BSD / MPL) = seguro reengenheirar.
     Copyleft (GPL / AGPL) = só a técnica — reengenheire a ideia, nunca copie o
     código. Sem licença = trate como todos-os-direitos-reservados, só a técnica.
     Termos não-comerciais = bloqueio; leve para o seu humano.
   - *Varredura de coisa suspeita:* grep por padrões de cloak / spam / fake-review /
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
6. **Reconstrua red-first.** Commite os testes falhando, depois construa até ficar
   verde na costura inteira. Um modelo de família diferente da do builder avalia o
   resultado — o builder nunca avalia o próprio trabalho.
7. **Cite e registre.** Escreva o crédito do scaffold onde a capacidade agora vive:
   autor, projeto, licença, o que é emprestado (o scaffold) e o que é seu (a
   reengenharia). Nunca invente um crédito. Nunca apague um.

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
- [blind-tribunal](../blind-tribunal/SKILL.md) — avaliação cross-family do porte.
- [decision-bar](../decision-bar/SKILL.md) — bloqueios de licença e decisões de gosto vão para o seu humano; todo o resto executa.
