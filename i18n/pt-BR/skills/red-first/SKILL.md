---
name: "red-first"
description: "Use antes de despachar builder para mudança de comportamento demonstrável, ou quando um achado de revisão ou lacuna de mutação precisar de contrato de regressão."
license: "MIT"
---

# Red-First, à prova de adulteração
**Effort:** free — disciplina pura de ordem: o teste que você escreveria de qualquer jeito é escrito primeiro, provado vermelho e selado com um commit; a checagem de adulteração é um único git diff. Remove: testes moldados depois do conserto para passar, e veredictos verdes que um builder entortou editando o teste.

Um resultado verde observado somente depois do conserto não demonstra a falha
original nem a capacidade do teste de detectá-la. Demonstre e sele o RED original
antes do conserto; o builder mantém esse arquivo intacto. Uma regressão suplementar
separada pode depois demonstrar falha contra um mutante controlado e aprovação
contra o candidato sem mutação, conforme descrito abaixo.

Use o pacote atual do [BACKS Build Flow](../backs-build-flow/SKILL.md). Esta skill
cuida do selo RED; não cria outro responsável nem ciclo de construção. Preserve
`base_sha` fixado, `candidate_sha` atual e identidade da missão. Prazo e tentativas
restantes de [bounded-loops](../bounded-loops/SKILL.md) cobrem reprodução, builders,
tests suplementares e revisões. Reutilize recibo RED válido em vez de fabricar
nova falha.

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
3. **Commite o test RED ANTES de despachar o builder.** Registre id do commit,
   caminhos e bytes exatos, comando/saída que falhou e motivo. Esse commit é a
   baseline RED e o lacre; não substitui o `base_sha` fixado da missão que delimita
   a mudança agregada.
4. **Despache o builder com um trabalho só: deixar verde.** O builder é
   proibido de tocar no arquivo de teste. Diga isso no despacho.
5. **Avalie de forma independente.** Um avaliador que não escreveu a mudança
   checa duas coisas:
   - o teste agora passa;
   - o arquivo de teste está byte a byte idêntico à linha de base vermelha —
     `git diff <red-sha> <candidate_sha> -- tests/test_contract.py` não imprime nada.
     Ao testar trabalho pendente, compare também bytes reais com o selo; diff
     commitado limpo não justifica edição staged ou unstaged.
   Qualquer diff no arquivo de teste reprova a avaliação. Sem exceção, nem
   "só arrumei um typo."
6. **Prefira um guarda estrutural a testes pontuais espalhados.** Um guarda
   estrutural é uma checagem (uma varredura de grep, um scan de AST, uma
   regra de lint) que falha no PRÓXIMO infrator, não só nesta instância. Um
   guarda vale mais que dez testes pontuais que fixam um caso cada.

## Um achado novo depois do selo original

Sobrevivente de mutação ou achado de revisão pode revelar asserção ausente.
Preserve byte a byte o arquivo RED original e acrescente **arquivo suplementar
separado**. Observe falha pelo novo defeito antes da correção; para lacuna de
mutação, demonstre falha no mutante controlado pertinente em isolamento e aprovação
no candidato sem mutação. Registre e sele essa evidência antes de o próximo builder
alterar a costura. Não afirme que era a baseline original. O avaliador verifica
ambos os selos e o candidato agregado exato. Adicionar test não autoriza enfraquecer,
renomear nem substituir o contrato original.

Se o orçamento compartilhado acabar ou RED não puder ser estabelecido, salve
**STILL-BUILDING** com lacuna e próxima ação exata. Não fabrique RED nem reinicie
a missão para forçar verde.

## Regras duras

- **Vermelho tem que ser provado vermelho.** Rode, veja falhar, antes de
  contar.
- **O builder nunca edita o teste.** O diff vazio do arquivo de teste desde a
  linha de base vermelha é parte do portão de aterrissagem, não uma cortesia.
- **O builder nunca é o avaliador.** Escolha por capacidade e disponibilidade na
  matriz configurada; registre e exclua a execução autora. Use sessão nova separada
  do autor, sem sua conversa nem contexto herdados.
- **Verde sozinho não é prova.** Verde + teste intocado + avaliação
  independente prova este contrato; capacidade ao vivo ainda exige evidência
  de superfície real e entrega do fluxo da tarefa.
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
