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

## A cadeia

1. [red-first](../skills/red-first/SKILL.md) — confirme que a suíte falhou com
   exit diferente de zero ANTES de o fix existir. Uma suíte que nunca ficou
   vermelha não prova nada.
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — verifique que o builder
   usou testes com escopo durante a iteração e não fez teatro de mock na costura
   que mudou.
3. Avaliação entre famílias — entregue o trabalho a um modelo de família
   DIFERENTE da do builder. Avaliar dentro da mesma família infla as taxas de
   vitória de forma mensurável — avaliadores favorecem a própria linhagem;
   outra instância da mesma família não basta.
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — para mudanças de
   consequência, convoque jurados sobre um envelope com a autoria apagada. Cada
   achado vira um novo teste vermelho, e o tribunal reconvoca até todos os
   jurados aprovarem.
5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — o avaliador
   re-roda o gauntlet ele mesmo (cobertura-vs-complexidade, teste de mutação com
   limites). Nunca confie no relatório do builder sobre os próprios números.

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

- Builder e avaliador da mesma família de modelos.
- Não dá para mostrar a suíte vermelha antes do fix.
- Falta fail-to-pass ou pass-to-pass na execução avaliada.
- Qualquer sinal de verde falso acima está presente.
- O avaliador confiou no relatório do próprio builder em vez de re-rodar as
  verificações.
