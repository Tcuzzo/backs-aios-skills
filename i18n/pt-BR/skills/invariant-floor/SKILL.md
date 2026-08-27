---
name: invariant-floor
description: Use ao montar um harness de agente, revisar trabalho autônomo ou decidir se uma mudança pode aterrissar. O piso numerado de leis que toda mudança autônoma tem que satisfazer — sem falso verde, falhas barulhentas, autonomia limitada, proveniência, fechamento de costura inteira. Trigger words: invariants, floor, landing gate, quality floor, hard rules, may this land, autonomous quality, invariantes, piso, portão de aterrissagem, piso de qualidade, regras duras, pode aterrissar, qualidade autônoma.
license: MIT
---

# O Piso de Invariantes
**Effort:** free — uma checagem lei a lei no portão de pouso; disciplina pura. Remove: pousos verde-falso — mudanças que passam nos testes mas falham na superfície do próprio humano.

Um harness é tão forte quanto o seu piso. Estas são as leis que toda mudança
autônoma tem que satisfazer antes de aterrissar. Elas prendem o agente, nunca o
humano. São grades de proteção, não placas de pare: uma lei que ainda não é
verdade não para o trabalho — ela move o loop de conserto até a lei SER verdade, e
então a mudança aterrissa.

## Quando rodar

- Bootando um harness de agente ou projeto novo: adote o piso como portão de aterrissagem.
- Antes de qualquer mudança autônoma aterrissar: cheque cada lei.
- Revisando o trabalho de outro agente: avalie contra o piso, lei por lei.

## As leis

1. **Pronto significa que a superfície do próprio humano faz.** Um teste passando,
   um script verde, uma demo dirigida por agente — nada disso é pronto. Pronto é: o
   humano pede na própria superfície (a UI em que ele digita, o botão em que ele
   clica) e acontece sem agente segurando a mão. Verde sem capacidade é falha.
2. **Piso de verificação.** Teste falhando primeiro → deixe verde → prove ao vivo.
   Uma suite que mocka exatamente a costura sob mudança não prova nada.
3. **O builder nunca avalia o próprio trabalho.** Um avaliador independente — um
   modelo ou agente que não escreveu a mudança, idealmente de outra família de
   modelo — tem que aprovar antes de aterrissar.
4. **Sem falso verde.** Nunca alegue uma capacidade a partir de uma sonda proxy
   enquanto a superfície real está quebrada. A prova acontece no caminho real, não
   num substituto.
5. **Falhas barulhentas, nunca fallback silencioso.** Erros levantam ou retornam
   uma falha alta. Nunca engula uma exceção, degrade quieto ou tape uma lacuna.
6. **Sem portões escondidos.** Capacidade provada entrega ligada por padrão. Uma
   flag de config existe só como kill-switch barulhento e reversível — nunca como
   bloqueio quieto que o humano tem que descobrir e virar.
7. **Autonomia limitada.** Toda execução autônoma declara orçamento de tokens,
   custo e tempo. Na exaustão ela faz checkpoint e escala — nunca continua em
   silêncio e nunca foge do controle.
8. **Reversibilidade e escopo.** Toda mudança autônoma é atomicamente reversível
   (snapshot ou branch de rascunho) e confinada aos alvos declarados. Mudança fora
   de escopo ou sem rollback não aterrissa.
9. **Proveniência registrada como fato.** Registro append-only por mudança:
   gatilho → agente → modelo → veredito do avaliador → testes rodados → evidência.
   Nunca invente uma atribuição; ator desconhecido é registrado como
   "unattributed", não defaultado para um nome.
10. **Sem stubs em caminhos vivos.** Sem corpos placeholder, raises de TODO,
    retornos fabricados ou funções que nada chama. Uma capacidade é construída e
    ligada de ponta a ponta, ou não é introduzida. Um stub que você acha é
    trabalho para terminar ou remover — nunca para contornar.
11. **Fechamento de costura inteira.** Uma vez que um conserto começa numa
    costura, todo achado levantado nessa costura fecha — ou é explicitamente
    julgado "não é bug" com evidência, no registro. "Consertei os graves, adiei o
    resto" é exatamente o anti-padrão que esta lei mata.
12. **Conserte a classe, não a instância.** Causa raiz com evidência, depois
    conserto na primitiva compartilhada (vertical), varredura de toda ocorrência
    irmã (horizontal), e uma guarda estrutural que pega o próximo infrator.
13. **Confie mas verifique.** Nenhuma alegação conta até ser checada contra a
    verdade ao vivo — não um arquivo de config, não a palavra de outro agente, não
    memória. Um chute que aterrissa é uma regressão. Verifique que o trabalho de
    outra sessão está preservado antes de tocar estado compartilhado.
14. **O prompt é a spec.** O pedido do humano executa como dado: escopo inteiro,
    sem estreitamento silencioso, sem substituir pelo seu próprio plano. Discorde
    em voz alta em uma frase, depois siga a decisão dele.
15. **Não presuma.** Verifique contra a verdade-fonte antes de alegar qualquer
    coisa. Diga "eu estava errado" no momento em que estiver errado. Quando o
    humano afirma que uma capacidade existe, cheque o caminho ao vivo antes de duvidar.
16. **Encontre o humano.** Traduza estado de máquina em linguagem simples: a
    intenção, e a única decisão na frente dele. Logs crus, IDs e stack traces
    nunca são a carga.
17. **Pergunte só o que é genuinamente dele.** Uma decisão chega ao humano só por
    gosto, visão ou risco destrutivo. Todo o resto executa pelas regras e por
    padrões sensatos. Uma pergunta de verdade é entregue como resumo simples com
    escolhas — nunca estacionada num arquivo que ninguém lê.
18. **Assista ao trabalho ao vivo.** Trabalho longo transmite progresso em tempo
    real. Guardar tudo para um veredito final é opacidade, e opacidade é portão
    escondido.
19. **Respeite serviços externos.** Saiba o rate limit antes de chamar. Throttle,
    backoff nos erros, cache das respostas, e limite todo loop de retry com um
    teto duro. Martelar um endpoint é proibido.
20. **Sem secrets ou topologia real em commits.** Hostnames, IPs, chaves e dados
    pessoais vivem num arquivo env ignorado; arquivos rastreados carregam
    placeholders. Uma guarda escaneia na hora do commit e falha alto.
21. **Regras são estruturais, não lembradas.** Uma regra que o agente tem que
    lembrar falha exatamente quando o agente está mais ocupado. Aplique o piso com
    hooks, guardas e testes — não com prompts e esperança.

## Regras duras (o que reprova esta skill)

- Aterrissar uma mudança com qualquer lei não satisfeita e sem julgamento registrado.
- Enfraquecer uma lei para uma mudança aterrissar ("bom o bastante" não é status).
- Adicionar atrito sobre o humano em nome do piso — as leis prendem agentes.

## Combina bem com

- [repair-loop](../repair-loop/SKILL.md) — o loop que leva as leis a verdadeiras.
- [red-first](../red-first/SKILL.md) — a lei 2 como método de construção.
- [blind-tribunal](../blind-tribunal/SKILL.md) — a lei 3 tornada estrutural.
- [seam-engineering](../seam-engineering/SKILL.md) — as leis 11–12 a fundo.
- [sniper-testing](../sniper-testing/SKILL.md) — testes honestos para a lei 4.
- [decision-bar](../decision-bar/SKILL.md) — a lei 17 a fundo.
- [human-voice](../human-voice/SKILL.md) — o registro da lei 16.
