# Play: Grading & Verification

O play de avaliação adversarial. Sua única crença: um resultado verde é uma
alegação, não uma prova. O avaliador ataca, e o piso foi construído para não ter
como ser burlado.

## Quando rodar

- Qualquer mudança construída pede para pousar — código, config, docs, a saída
  de um agente.
- Uma suíte diz que está verde e ninguém a viu falhar antes.
- Um modelo construiu o trabalho e você precisa de um veredito honesto sobre
  ele.

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

1. [red-first](../skills/red-first/SKILL.md) — confirme que a suite falhou com
   saída diferente de zero ANTES do fix. Suite nunca vermelha não prova nada.
   O test falho fica commitado e o builder não pode tocá-lo; seus bytes exatos são
   o contrato.

2. [sniper-testing](../skills/sniper-testing/SKILL.md) — verifique comandos reais
   de lint/tipos/tests focados no diff agregado fixado e ausência de teatro de mocks
   na costura alterada. Confira motivos de N/A e verificações ausentes. Congele
   a identidade do candidato para esta revisão.

3. Avaliação independente — escolha ao vivo por capacidade e disponibilidade
   na matriz configurada (tarefa → capacidade → degrau → sondagem). Registre a
   execução autora quando o runtime suportar e exclua-a. Qualquer rota capaz
   configurada pode revisar em sessão nova e disjunta do autor (fresh author-disjoint review). É proibida sessão
   que viu a conversa ou herdou contexto do builder.

4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — para mudanças importantes,
   convoque jurados sobre pacote sem autoria em sessão nova sem conversa herdada.
   Devolva achados fundamentados ao responsável pela integração para RED suplementar
   separado e reparo limitado; o original continua selado. Reconvoque sobre o
   candidato revisado e congelado dentro do mesmo orçamento. Todos os jurados
   exigidos precisam aprovar antes de integrar.

5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — o avaliador
   re-roda o gauntlet ele mesmo (cobertura-vs-complexidade, teste de mutação com
   limites). Nunca confie no relatório do builder sobre os próprios números.

Respeite o alvo imutável da revisão. Execute verificações que criem cache, mutem
código ou exercitem serviços apenas em isolamento permitido; mutação nunca
reescreve fonte congelada. Falta de isolamento ou suporte de runtime é lacuna de
evidência, não permissão para corrigir durante revisão. Preserve evidência completa
exigida das suites afetadas e separe verificações locais de superfície real ou entrega.

## A prova de dois lados (as duas, ou não passa)

- **Fail-to-pass:** os testes que estavam vermelhos agora estão verdes — o fix
  está provado.
- **Pass-to-pass:** tudo que estava verde continua verde — sem regressão.
- Uma execução que só ADICIONA testes passando não satisfaz nenhuma das duas.
  Rode as duas de forma hermética.

## Guardas contra verde falso (qualquer uma é o sinal)

- Uma saída de emergência no exit code — um harness que sai limpo aconteça o que
  acontecer.
- Saídas chumbadas ou decoradas no lugar das computadas.
- Testes apagados, pulados ou enfraquecidos.
- Qualquer avaliador, timer ou pontuador editado. Um harness editado que fica
  verde É o sinal.
- Um mutante sobrevivendo sob uma suíte verde. O mutante é a prova de que as
  asserções nunca chegaram àquele branch — verde falso por definição.

## Tire o viés do juiz

O piso da mecânica de julgamento vive na seção "De-bias the judge" de
[blind-eval](../skills/blind-eval/SKILL.md) — aplique inteira.

## Gates duros — qualquer um reprova o play

- A revisão usou a execução autora ou sessão que viu sua conversa ou herdou
  contexto; sessão nova separada do autor é obrigatória.
- Um jurado do tribunal herdou contexto ou viu a conversa do autor.
- Não dá para mostrar a suíte vermelha antes do fix.
- Falta fail-to-pass ou pass-to-pass na execução avaliada.
- Qualquer sinal de verde falso acima está presente.
- O avaliador confiou no relatório do próprio builder em vez de re-rodar as
  verificações.

**Lacunas do runtime.** Selecione revisores capazes pela escada configurada e
exclua a execução autora. Informe restrições do runtime que bloqueiem revisor
capaz; não afirme silenciosamente que foram resolvidas nem as contorne.

**Weight:** checagens free de vermelho e de sniper na frente; o gasto heavy é o tribunal mais o avaliador re-rodando ele mesmo o gauntlet — ele se paga em qualquer mudança que pede pouso, porque um verde falso custa mais que todas as avaliações somadas.
