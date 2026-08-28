---
name: "red-first"
description: "Use ao despachar qualquer builder — um agente, um modelo ou você mesmo — para uma mudança que um teste deve provar. Commita um teste de contrato provado-falhando antes de o build começar, proíbe o builder de tocá-lo e põe um avaliador independente para verificar que o teste nunca foi editado. Trigger words: red first, failing test first, contract test, red baseline, tamper-proof test, test before build, teste falhando primeiro, teste de contrato, vermelho primeiro, linha de base vermelha, teste antes do build."
license: "MIT"
---

# Red-First, à prova de adulteração
**Effort:** free — disciplina pura de ordem: o teste que você escreveria de qualquer jeito é escrito primeiro, provado vermelho e selado com um commit; a checagem de adulteração é um único git diff. Remove: testes moldados depois do conserto para passar, e veredictos verdes que um builder entortou editando o teste.

Um teste escrito depois do conserto não prova nada — foi moldado para passar.
Um teste que o builder pode editar prova menos ainda — pode ser entortado para passar.
Então o teste vem primeiro, é trancado, e é avaliado intocado.

## Quando rodar

Antes de despachar qualquer build ou conserto em que um teste consegue
declarar o comportamento desejado. Este é o padrão tanto para conserto de bug
quanto para capacidade nova.

## Passos

1. **Escreva o teste de contrato que falha.** Ele declara o comportamento que
   você quer, na menor forma que pegaria a ausência dele. Ele tem que falhar
   agora.
2. **Prove que está vermelho.** Rode o teste e veja-o falhar — pelo motivo
   certo. Um teste que dá erro no import, ou que passa quieto, não está
   vermelho. Um teste vermelho que ninguém rodou é palpite, não linha de base.
3. **Commite o teste vermelho ANTES de despachar o builder.** Registre o id
   do commit. Esse commit é a linha de base vermelha — o lacre.
4. **Despache o builder com um trabalho só: deixar verde.** O builder é
   proibido de tocar no arquivo de teste. Diga isso no despacho.
5. **Avalie de forma independente.** Um avaliador que não escreveu a mudança
   checa duas coisas:
   - o teste agora passa;
   - o arquivo de teste está byte a byte idêntico à linha de base vermelha —
     `git diff <red-sha> HEAD -- tests/test_contract.py` não imprime nada.
   Qualquer diff no arquivo de teste reprova a avaliação. Sem exceção, nem
   "só arrumei um typo."
6. **Prefira um guarda estrutural a testes pontuais espalhados.** Um guarda
   estrutural é uma checagem (uma varredura de grep, um scan de AST, uma
   regra de lint) que falha no PRÓXIMO infrator, não só nesta instância. Um
   guarda vale mais que dez testes pontuais que fixam um caso cada.

## Regras duras

- **Vermelho tem que ser provado vermelho.** Rode, veja falhar, antes de
  contar.
- **O builder nunca edita o teste.** O diff vazio do arquivo de teste desde a
  linha de base vermelha é parte do portão de aterrissagem, não uma cortesia.
- **O builder nunca é o avaliador.** Use outra pessoa, outro agente ou um
  modelo de família diferente da do builder.
- **Verde sozinho não é prova.** Verde + teste intocado + avaliação
  independente é prova.
- **Quando uma classe inteira de defeito está em jogo, guarde a classe.**
  Testes pontuais param este bug; um guarda estrutural para o próximo.

## Funciona bem com

- [sniper-testing](../sniper-testing/SKILL.md) — rode só os testes que a
  mudança toca enquanto itera; uma passada completa na aterrissagem.
- [seam-engineering](../seam-engineering/SKILL.md) — a disciplina de conserto
  por classe à qual o guarda estrutural pertence.
- [blind-tribunal](../blind-tribunal/SKILL.md) — avaliadores independentes
  que nunca viram o autor.
- [repair-loop](../repair-loop/SKILL.md) — o loop que leva vermelho → verde
  → provado de ponta a ponta.
