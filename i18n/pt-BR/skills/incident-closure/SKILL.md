---
name: incident-closure
description: Use quando o humano reporta quebra ou diz "conserta isso" — principalmente quando o plano de controle normal (API, CLI, serviço) está morto e você precisa alcançar por baixo dele. A resposta é um fechamento completo, entendimento primeiro — causa raiz com evidência, teste falhando primeiro, verde, prova ao vivo no caminho do próprio humano, commit — nunca um menu de opções de volta para ele. Trigger words: fix it, fix shit, full close, broken, wiped, down, it stopped working, recover, restore, conserta isso, quebrou, apagado, fora do ar, parou de funcionar, recuperar, restaurar, fechamento completo.
license: MIT
---

# Fechamento Completo

Quando o humano reporta quebra ou diz "conserta isso", existe exatamente uma
resposta certa: um fechamento completo, entendimento primeiro. Causa raiz com
evidência, um teste falhando primeiro, verde, prova ao vivo no caminho do próprio
humano, depois commit. Nunca um menu de opções de volta para ele, e nunca um
prompt de confirmação por passo — ele já disse conserta.

Onde skills irmãs exigem um sim explícito para atos destrutivos, esta regra vence
só a metade reversível: o "conserta isso" do humano É o sim vigente para escritas
de recuperação reversíveis que deixam trilha de backup; qualquer coisa
irreversível — destruição de dados, gasto, envios externos — ainda cruza a
[decision-bar](../decision-bar/SKILL.md), e a barra vence.

Peça algo ao humano só quando estiver provadamente perdido em todo outro lugar e
só ele puder fornecer. Todo outro insumo, você vai buscar.

## O método

1. **Sonde a superfície normal — depois pare de confiar nela.** Chame a API ou CLI
   uma vez. Se responde normal, isto não é situação de fechamento de incidente;
   passe adiante. Se retorna 401/403, conexão recusada, resultados vazios onde
   deveria haver dados, ou dados velhos, pare de tratar essa superfície como
   autoridade.
2. **Estabeleça a verdade do chão pelo disco, não pela API.** Nunca confie num
   serviço quebrado para descrever o próprio estado. Leia você mesmo os arquivos de
   dados, listagens de diretório e tempos de modificação, e compare com o que a API
   alega. Divergência é o sinal diagnóstico.
3. **Escaneie o raio de explosão.** Busque em cada diretório de dados de topo os
   arquivos tocados dentro da janela da falha (ex.: `find /data/volumes -newermt
   "<start>" ! -newermt "<end>"`). Mire numa resposta de uma tela para "o que foi
   tocado, o que não foi". Raio estreito (um volume, uma tabela) é recuperável
   aqui. Raio largo (muitos volumes, o diretório de dados inteiro) é disaster
   recovery — escale, não improvise.
4. **Inventarie sobreviventes vs perdas.** Classifique cada ativo afetado:
   - intacto no disco — recupere como está
   - reconstruível do repo — configs e backups commitados no git
   - reconstruível de env ou arquivos de credencial — tokens, senhas
   - perdido de vez — criptografado com chave sumida, estado só de runtime
   Só o último balde justifica perguntar ao humano. Todo o resto você reconstrói.
5. **Causa raiz com evidência, depois um teste red.** Nomeie por que quebrou, com
   prova do disco — não um chute. Onde o defeito é código, escreva o teste falhando
   que o captura antes do conserto, e deixe verde. Veja [red-first](../red-first/SKILL.md)
   e [root-cause-first](../root-cause-first/SKILL.md).
6. **Desça em cascata pelas camadas — nunca suba para o humano.** Quando o caminho
   preferido está quebrado, desça uma camada e tente de novo:
   API / SDK → CLI dentro do container → escritas diretas no banco → cirurgia de
   filesystem. Não pergunte ao humano enquanto restarem cascatas por tentar. Cada
   degrau para baixo é mais barato que perguntar.
7. **Presuma que as dependências também quebraram.** Código de recuperação usa só a
   biblioteca padrão da sua linguagem para HTTP e JSON — clientes de terceiros
   podem ser parte do que morreu.
8. **Escreva idempotente, com trilhas de backup.** Toda escrita em disco deixa uma
   cópia `.bak` com timestamp ao lado do alvo. Leia, confira, copie, escreva,
   recheque — nunca sobrescreva às cegas. Se você trocar uma credencial
   temporariamente para cunhar uma chave nova, faça backup da original antes e
   restaure antes de devolver: o login do próprio humano sobrevive intocado.
9. **Verifique com chamadas ao vivo no caminho do próprio humano.** Rode de novo a
   sonda do passo 1 e confirme que os números batem com o inventário pré-incidente
   ou com os backups do repo. Estado verde no banco não é prova; a superfície que o
   humano usa funcionando de novo é prova.
10. **Commite e reporte.** Commite só os arquivos do próprio conserto. Reporte: o
    que foi sondado, o raio de explosão, ações tomadas em ordem, contagens
    restauradas, o que ficou perdido de vez (vazio se nada), e qualquer passo que
    falhou sem ser fatal.

## Bandeiras vermelhas — pare e re-sonde

- "Vou perguntar ao humano por que quebrou" — não; descubra pelo disco primeiro.
- "A API diz que não tem nada aqui" — a visão de uma API quebrada sobre si mesma não é verdade.
- "Vou só reinstalar limpo" — você está descartando estado recuperável.
- "A chave sumiu, então as credenciais são inúteis" — valores em texto puro muitas
  vezes ainda vivem em env ou arquivos de credencial; recrie a credencial.
- "Confirmo antes de cada passo?" — o humano disse conserta; rode a cascata, reporte no fim.

## Regras duras — qualquer uma delas reprova a skill

- Opções apresentadas de volta ao humano quando existe uma solução clara.
- Uma escrita destrutiva sem trilha `.bak`.
- Pediram algo ao humano antes de a cascata e o inventário secarem.
- Um subsistema aposentado restaurado "por gentileza" — um serviço desativado
  continuar desligado é o estado desejado, e religar é decisão deliberada do humano.
- Recuperação dada como pronta a partir de estado interno em vez de uma sonda ao
  vivo no caminho dele.
- Conserto deixado sem commit (a menos que o humano tenha dito explicitamente sem commit).

## Combina bem com

- [repair-loop](../repair-loop/SKILL.md) — o loop de conserto de código que este fechamento roda quando o defeito é código.
- [root-cause-first](../root-cause-first/SKILL.md) · [red-first](../red-first/SKILL.md)
- [decision-bar](../decision-bar/SKILL.md) — o que pode chegar ao humano, e como.
