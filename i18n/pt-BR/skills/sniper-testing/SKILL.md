---
name: "sniper-testing"
description: "Use durante qualquer loop de conserto ou build, e antes de confiar em qualquer teste verde. Roda só os testes que cobrem o que você tocou, e mata o teatro de mock — testes que passam com a capacidade quebrada. Trigger words: sniper testing, scoped tests, test scope, mock theater, fake green, full suite, test bloat, testes escopados, teatro de mock, verde falso, suíte inteira, inchaço de teste."
license: "MIT"
---

# Sniper Testing
**Effort:** free — disciplina pura, nenhuma execução extra; corta o custo líquido na raiz ao apagar re-execuções da suíte inteira durante a iteração. Remove: inchaço de teste (rodar a suíte inteira para um diff minúsculo) e os verdes de teatro de mock sobre os quais você construiria.

## Por que isso existe

Dois modos de falha queimam a maior parte do tempo de teste. Inchaço de
teste: rodar a suíte inteira para uma mudança minúscula. Teatro de mock:
testes que passam enquanto a capacidade real está fisicamente quebrada. Esta
skill mata os dois.

## Regra 1 — o diff define o escopo, não o otimismo

Durante o loop de iteração de conserto/build, você está proibido de rodar a
suíte de testes inteira.

1. Rode `git diff --name-only HEAD` para ver exatamente quais arquivos você
   tocou.
2. Mapeie cada arquivo tocado para os arquivos de teste que o cobrem
   diretamente (ex.: `src/payments/refund.py` → `tests/test_refund.py`).
3. Declare seu alvo de teste específico, depois rode SÓ aqueles arquivos
   (Python: `pytest tests/test_refund.py`;
   JS: `npx vitest run tests/refund.test.js`;
   Go: `go test ./payments/ -run TestRefund`).
4. Um teste que já passou não roda de novo, a menos que a próxima mudança
   toque código que ele exercita. O diff define o escopo — não o otimismo,
   não o medo.
5. Na hora de aterrissar — o portão do commit — rode UMA passada completa na
   suíte de cada módulo tocado. Essa passada única pega acoplamentos
   indiretos exatamente uma vez. Velocidade de iteração e uma aterrissagem
   sólida são as duas partes do trabalho.

## Regra 2 — mate o teatro de mock

Um teste de capacidade precisa assertar um efeito colateral real, físico:

- "produz um vídeo" → um arquivo real existe no disco com tamanho > 0 bytes.
- "guarda memória" → a linha volta na leitura de um banco local real.
- "renderiza o widget" → um elemento DOM real existe na página.

Não mocke o banco de dados. Não mocke o sistema de arquivos. Não mocke
sockets de rede local.

O único mock legal é a folha de transporte externo pago — a chamada HTTP para
uma API de terceiro cobrada por uso. Mesmo aí, o teste precisa atravessar
toda a lógica real ao redor: montar a requisição, rotear, parsear a resposta.
Mocke o fio, nunca o cérebro.

## Audite antes de confiar

Antes de se apoiar em qualquer teste, leia-o. Se for teatro de mock — verde
por causa de mocks, sem asserção física — delete o mock e reescreva o teste
para assertar um efeito colateral real. Um teste que não consegue falhar é
pior que nenhum teste: ele certifica uma mentira, e você vai construir em
cima dela.

## Regras duras (quebrou uma, a skill falhou)

- Nada de rodar a suíte inteira durante a iteração.
- Nenhuma alegação de verde sem asserção de efeito colateral real.
- Nenhum mock além da folha de transporte externo pago num teste de
  capacidade.
- Nenhuma aterrissagem sem a passada completa única nos módulos tocados.

## Funciona bem com

- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — o escopo sniper alimenta seu primeiro portão
- [red-first](../red-first/SKILL.md) — escreva o teste que falha antes do conserto
- [seam-engineering](../seam-engineering/SKILL.md) — conserte a classe, depois varra com testes escopados
