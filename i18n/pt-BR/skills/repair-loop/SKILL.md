---
name: "repair-loop"
description: "Use ao corrigir bug, fechar problema relatado ou melhorar uma costura de ponta a ponta com reprodução, RED selado, correção da classe, verificações focadas e entrega verificada dentro do orçamento da missão."
license: "MIT"
---

# Repair Loop
**Effort:** light — o loop em si é disciplina mais uma passada de avaliação independente; os passos mais pesados que ele encadeia (gauntlet, tribunal) carregam os próprios selos e disparam só em mudanças que vão para produção. Remove: pousos verdes-mas-quebrados, e o retrabalho de bug reaberto que eles custam.

O loop padrão para qualquer conserto, fechamento de bug ou uplift. É um
comportamento, não maquinário de aprovação: adiciona zero portões e zero
atrito para o humano. Ele amarra o agente a uma disciplina que torna "verde
mas quebrado" estruturalmente difícil de sair.

## Carregue primeiro, antes de qualquer design ou edição

Use [BACKS Build Flow](../backs-build-flow/SKILL.md) para pacote de tarefa,
essência do operador e um responsável pela integração. Reutilize regras aplicáveis,
contexto, corpos carregados e evidências já estabelecidos; atualize só o que mudou.
Invocação direta estabelece contexto ausente uma vez. Carregue piso de invariantes
e gates de entendimento obrigatórios se faltarem; use wayfinder apenas para rota
não resolvida. Achado de reparo não reinicia o play externo.

[bounded-loops](../bounded-loops/SKILL.md) cuida do prazo compartilhado e cotas
restantes de tentativas/rodadas. Preserve `mission_id`, `task_mode`, `base_sha`
fixado e `candidate_sha` atual por reprodução, edições, ferramentas, modelos,
revisões e handoffs. Chamada aninhada não reinicia orçamento. Revisão e diagnóstico
devolvem evidências sem editar nem promover; construir exige esse escopo.

## O loop

1. **Fundamente o caminho afetado.** Confira regras, código atual do projeto,
   contratos de chamadas e verificações existentes. Reutilize evidências atuais
   e pertinentes sem repetir auditoria do repo inteiro.
2. **Reproduza na verdade viva.** Veja a falha você mesmo, no caminho real
   que o humano usa — não uma sonda proxy, não a palavra do bug report. Sem
   reprodução, sem conserto.
3. **Teste de contrato vermelho.** Escreva um teste que falha capturando o
   defeito, e commite antes do conserto. Prove que está mesmo vermelho. O
   conserto o deixa verde; o conserto nunca edita o teste. Veja
   [red-first](../red-first/SKILL.md).
4. **Conserte a CLASSE na costura** — não um remendo pontual por sintoma. A
   fórmula completa vive em [seam-engineering](../seam-engineering/SKILL.md).
5. **Execute verificações focadas.** Use [sniper-testing](../sniper-testing/SKILL.md)
   para derivar escopo do diff agregado de `base_sha` a `candidate_sha` e caminhos
   próprios pendentes. Execute comandos reais de lint, tipos e tests do repo.
   Registre comando, resultado e revisão. Marque **N/A** com motivo para o inaplicável;
   ferramenta obrigatória ausente é lacuna. Não instale ferramentas arbitrárias
   nem invente aprovações. Test selado continua idêntico byte a byte.
6. **Meça dentro do fluxo.** Aplique [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
   para qualidade e mutação limitada do candidato. Investigue sobreviventes; se
   revelarem lacuna de test, acrescente arquivo suplementar separado preservando
   RED original. Corrija a costura responsável e repita verificações afetadas dentro
   da mesma cota restante; nunca reduza gates para obter GREEN.
7. **Avaliação independente.** Escolha avaliador capaz e disponível pela matriz
   configurada; registre e exclua a execução autora. Sessão nova separada do autor,
   sem conversa nem contexto herdados, precisa aprovar. O builder nunca avalia
   o próprio trabalho. Veja [blind-tribunal](../blind-tribunal/SKILL.md).
8. **Cheque o trabalho concorrente.** Antes de alterar estado compartilhado,
   verifique que o trabalho em voo de qualquer outra sessão está preservado
   (numa branch ou commit). Nunca commite nem limpe trabalho que não é seu.
9. **Verifique e integre dentro do escopo.** Uma passagem completa pelas suites
   dos módulos tocados na integração, mais verificações obrigatórias do projeto;
   siga a entrega autorizada. Confira comportamento na superfície real do humano
   (UI ou comando usado) e registre revisão exata candidata/instalada. Tests locais
   e evidência estática original não estabelecem entrega ao vivo. Feche cada achado
   na costura ou registre «não é bug» com evidência. «Corrigi o grande e adiei o resto»
   nunca aterrissa.

## Itere dentro do orçamento da missão

Verificação falha fornece a próxima hipótese limitada. Repita ou escolha rota
capaz configurada somente dentro da cota restante; mudar modelo não cria missão
nova. Aplique regras de estagnação e esgotamento de bounded-loops. Ao atingir
limite, salve **STILL-BUILDING** com candidato, tests selados, evidência da falha,
gates pendentes e próxima ação exata. Conclua trabalho útil autorizado que não
consuma cota esgotada. Achado aberto bloqueia integração, mas não apaga progresso
nem vira veredito **PROVEN** inventado.

## Regras duras — qualquer uma derruba a skill

- Conserto entregue sem reprodução na verdade viva.
- Teste escrito depois do conserto, ou editado pelo conserto.
- Sintoma remendado enquanto a classe fica aberta na costura.
- Capacidade declarada verde por um proxy enquanto o caminho do próprio
  humano está quebrado.
- Builder avaliou a própria mudança.
- Um achado levantado adiado em silêncio na aterrissagem.
- Ciclo reiniciado, abandonado em silêncio ou declarado verde com gate pendente.

## Relatório

Duas palavras — **PROVEN** (provado) ou **STILL-BUILDING** (ainda construindo)
— mais a intenção em linguagem simples e a única decisão na frente do humano,
se houver. Perguntas vão ao humano só por gosto, visão ou risco destrutivo;
veja [decision-bar](../decision-bar/SKILL.md).

## Funciona bem com

- [incident-closure](../incident-closure/SKILL.md) — quando o humano reporta quebra, este loop roda dentro de um fechamento completo.
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
