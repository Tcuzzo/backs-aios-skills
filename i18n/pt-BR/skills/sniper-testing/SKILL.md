---
name: sniper-testing
description: "Use durante um ciclo de construção ou reparo, ou antes de confiar em um resultado verde, quando a verificação precisar cobrir o candidato real sem repetir desnecessariamente a suite inteira."
license: MIT
---

# Sniper Testing

Verifique o comportamento alterado pelo consumidor real. Use o diff completo da
tarefa para escolher verificações; depois repita apenas as afetadas pela próxima
mudança. Herde a mesma cota de missão de [bounded-loops](../bounded-loops/SKILL.md).

## 1. Fixe o escopo real

Preserve o `base_sha` verificado anterior à tarefa e o `candidate_sha` commitado
atual no pacote do [Build Flow](../backs-build-flow/SKILL.md). Uma árvore limpa
após commitar RED e a correção ainda tem um diff de tarefa. Usar apenas
`git diff HEAD` perde esse escopo.

Use o utilitário de escopo somente leitura incluído, a partir do diretório
resolvido desta skill:

```bash
python scripts/changed_files.py --repo <verified-repo> --base <base-sha> --candidate <candidate-sha>
```

Durante a iteração, acrescente `--include-worktree` apenas quando o candidato for
HEAD. Ele informa separadamente caminhos commitados, staged, unstaged e untracked,
preservando nomes incomuns. O escopo agregado inclui exclusões e os dois lados de
uma renomeação. Marque trabalho pendente alheio como preservado; não reivindique
todos os caminhos retornados. Base ausente ou revisão inválida é erro a resolver,
nunca escopo vazio que justifica pular verificações. O utilitário não busca nem
altera o histórico.

## 2. Escolha e execute verificações reais

Mapeie arquivos alterados e chamadas/consumidores afetados para tests de comportamento;
leia scripts, CI e configuração reais do repositório para encontrar os comandos.

| Verificação | Escopo e evidência |
| --- | --- |
| Lint e formato | Arquivos alterados compatíveis com a configuração existente; use modo de verificação antes de reformatar. |
| Tipos ou compilador | Fronteira do pacote/projeto afetado; dependências de tipos podem exigir alvo maior. |
| Comportamento | Caminho real alterado e regressão que falha se a capacidade quebrar. |
| Contrato/integração | Consumidores, aliases, empacotamento, preservação de configurações ou fronteiras de runtime alteradas. |
| Gates obrigatórios de integração | Suites exigidas pelo repositório quando o candidato estabilizar. |

Declare cada comando, por que cobre o risco, revisão/estado pendente, resultado
executado e falhas restantes. Linter/typechecker ausente é **indisponível** ou
**inaplicável**, com motivo; não invente aprovação. Não instale ferramenta nova
só porque um exemplo a cita. Lint verde não substitui tests de comportamento.

Durante a iteração, escolha o menor alvo útil. Verificação já aprovada não precisa
rodar de novo se código exercitado, entradas e ambiente pertinente não mudaram.
Um acoplamento concreto não resolvido ou gate obrigatório do projeto justifica
ampliar tests; registre o motivo. Ao integrar, rode uma vez as verificações
agregadas exigidas para o candidato final. Mudanças posteriores invalidam apenas
evidências afetadas e gates de commit exigidos.

## 3. Faça os tests detectarem falhas reais

Verifique efeito observável: artefato válido existente, dados lidos de um banco
local real, bytes reais de contexto recebidos pelo host ou elemento de UI renderizado.
Exercite arquivos, bancos e sockets locais sem mocks. A folha de transporte externo
pago pode ser substituída por fixture determinístico, mantendo reais a construção
da requisição, roteamento, parsing e consumidor local. Nunca afirme que o fixture
prova a execução do serviço externo.

Preserve byte a byte o arquivo RED selado de [red-first](../red-first/SKILL.md).
Quando surgir uma lacuna nova, acrescente um arquivo separado de regressão
suplementar seguindo as regras de evidência e selagem dessa skill. Nunca enfraqueça,
renomeie, substitua nem edite o arquivo selado original.

## Saída

Devolva escopo do candidato, resultados executados de lint/tipos/tests, evidências
de efeitos reais e gates pendentes ao mesmo responsável.
[clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) usa essas evidências como
primeira etapa, não como motivo para repetir verificações inalteradas.
