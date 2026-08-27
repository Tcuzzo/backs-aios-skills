---
name: seam-engineering
description: Use ao reparar um bug ou fechar uma auditoria ou caça a bugs. Conserta a classe da falha uma vez no primitivo compartilhado, varre cada irmão, aterrissa um guarda que pega a próxima instância e fecha todo achado levantado — sem adiamento silencioso. Trigger words: seam, class fix, whole-seam closure, point patch, structural guard, do it right the first time, costura, conserto de classe, remendo pontual, guarda estrutural, fazer certo de primeira.
license: MIT
---

# Seam Engineering
**Effort:** free — disciplina pura de reparo: um conserto de classe no primitivo compartilhado em vez de N remendos pontuais. Remove: o mesmo bug consertado de novo em cada ponto irmão, e o achado médio adiado que vira o bug misterioso que ninguém acha em seis meses.

Uma costura fecha certo e completa, ou não fechou.
Um remendo rápido hoje é o bug que ninguém acha daqui a seis meses.
Esta skill transforma um bug report em uma classe fechada de bugs.

## Quando rodar

Qualquer reparo: um bug reportado, um teste que falhou, uma lista de achados
de auditoria ou caça a bugs. Principalmente quando bate a vontade de "só
remendar aqui".

## Passos

1. **Causa raiz com evidência.** Conserte a causa, não o sintoma. Antes de
   escrever o conserto, mostre a prova: uma repro que falha, uma linha de
   log, um trace apontando para a costura real. Conserto sem evidência é
   palpite.
2. **Nomeie a CLASSE da falha.** Pergunte: que família de erro é esta, e onde
   mais o mesmo erro pode morar? Escreva a classe em uma frase.
3. **Conserte na vertical — uma vez, no primitivo compartilhado.** O
   primitivo compartilhado é a única função ou módulo por onde toda
   ocorrência passa. Conserte ali. Nunca N remendos pontuais. Nunca
   marcar-o-caso-ruim-e-compensar.
4. **Varra na horizontal.** Cace toda ocorrência irmã da classe e conserte na
   mesma mudança, não "depois".
5. **Aterrisse um guarda estrutural.** Um teste ou checagem automática que
   falha na PRÓXIMA instância da classe. A classe fica fechada porque algo a
   vigia, não porque todo mundo lembra.
6. **Feche a costura inteira.** Liste todo achado que a caça levantou. Antes
   de aterrissar, cada um está ou consertado e verde, ou carrega um veredicto
   explícito e registrado de "não é bug" com evidência. Nunca um adiamento
   silencioso. Nunca "estacionado num doc".

## Regras duras

- **Um reparo que adiciona uma condição nova de falha é, ele mesmo, um bug.**
  Um helper de rollback que pode quebrar, uma limpeza que abandona estado, um
  teste editado para abençoar o defeito que devia pegar — tudo bug. Redesenhe
  a mudança como uma unidade atômica, ou como uma máquina de estados
  explícita e à prova de crash. Nunca passe pano.
- **"Consertei os graves; o resto vira follow-up" derruba a skill.** Esse é
  exatamente o hábito que esta skill existe para matar. Um bug médio adiado é
  o futuro bug misterioso. Todo achado na costura conta igual.
- **"Bom o bastante para aterrissar" não é status.** Se a costura não está
  certa, continue iterando — remova o bloqueio, escale para um modelo ou
  revisor mais forte, tente de novo — até estar.
- **Um remendo pontual ao lado de um primitivo compartilhado existente
  derruba a skill.** Se um primitivo já é dono da costura, o conserto anda
  nele; um conserto por fora recria a classe.
- **Um "não é bug" adjudicado precisa de evidência,** não de voto. Registre o
  que foi checado e por que o achado não se sustenta.

## Funciona bem com

- [root-cause-first](../root-cause-first/SKILL.md) — a disciplina de
  investigação por trás do passo 1.
- [red-first](../red-first/SKILL.md) — o teste que falha e prova o conserto,
  e o padrão de guarda estrutural do passo 5.
- [sniper-testing](../sniper-testing/SKILL.md) — testes escopados enquanto
  itera; uma passada completa na aterrissagem.
- [repair-loop](../repair-loop/SKILL.md) — o loop de ponta a ponta dentro do
  qual esta disciplina roda.
- [incident-closure](../incident-closure/SKILL.md) — "conserta isso" significa
  fechamento completo, nunca um menu de opções.
