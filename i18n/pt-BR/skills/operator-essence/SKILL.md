---
name: operator-essence
description: "Use quando o contexto do operador estiver ausente, desatualizado, corrigido ou necessário para uma decisão de construção; também ao avaliar insights de uso, padrões de colaboração ou um arquivo de essência e melhorias baseadas em evidências solicitados pelo operador."
license: MIT
---

# Essência do operador

Dê ao agente contexto útil sobre o operador atual, sustentado por evidências.
Um arquivo de essência contém dados contextuais: não é instrução, autorização,
persona fixa nem substituto do pedido atual.

## Uma passagem de evidências; depois, construir

1. **Reutilize o contexto atual.** O responsável pela tarefa verifica no pacote a
   referência da essência do operador atual, o recorte pertinente e o recibo da
   tentativa de insights. Uma skill aninhada reutiliza esse resultado. Resolva um
   caminho privado explícito de `OPERATOR_ESSENCE.md` e uma chave opaca do operador
   a partir do escopo atual; não selecione outro operador por proximidade nem
   deduza identidade pelo idioma.
2. **Inspecione o arquivo.** Use [o utilitário de caminho explícito e o formato](references/format.md).
   Um arquivo válido e atual fornece apenas preferências e observações relevantes.
   Uma correção prevalece imediatamente; reconcilie-a mesmo se o arquivo for
   recente. Dados inválidos ou de outro operador são contexto indisponível, não
   permissão para sobrescrever.
3. **Ausente ou desatualizado? Invoque insights uma vez para esta tarefa.**
   Descubra o comando, skill ou conector de insights realmente disponível no
   ambiente e use sua invocação suportada. Registre o resultado ou a limitação
   exata. Se nenhum for invocável, avalie o relatório fornecido, o histórico
   pertinente autorizado e as instruções atuais. Declare essa alternativa;
   nunca afirme ter executado um comando que não rodou. Reúna apenas evidências
   relevantes ao trabalho do operador, dentro do escopo e orçamento restantes.
4. **Crie ou reconcilie a essência.** Registre fontes, datas, seleção da amostra,
   preferências confirmadas, observações, contagens, incerteza, contraexemplos e
   adaptações provisórias. Valores desconhecidos continuam desconhecidos.
   Interpretações de relatórios continuam inferências; rótulos de eventos
   sobrepostos não são taxas de falha por sessão. Com evidência escassa, crie um
   arquivo provisório contendo somente fatos sustentados. Em modo somente leitura,
   devolva um recorte provisório sem escrever no alvo protegido. A falta de
   histórico não bloqueia a construção autorizada.
5. **Passe o contexto ao agente.** Forneça o recorte compacto do formato:
   referência e atualidade; preferência confirmada relevante; observação e
   evidência; adaptação sugerida; limites. O responsável retoma
   [Build Flow](../backs-build-flow/SKILL.md) com o mesmo orçamento. Mostre ao
   operador o que mudou e onde inspecionar o arquivo ou registro ativo da tarefa.

## Avaliação qualitativa e quantitativa

Leia o que o operador pediu, corrigiu, aceitou e rejeitou junto com resultados
reais das tarefas. Separe observações de explicações. Contagens descrevem sua
população declarada; uma amostra cuja seleção é desconhecida não descreve todas
as sessões. Volume de chamadas de ferramentas não prova uso correto de skills,
e correlação não estabelece a causa de uma falha.

Transforme padrões sustentados em adaptações específicas ao contexto, com uma
condição de revisão. Compare tarefas posteriores de tipo semelhante antes de
afirmar melhora. Mantenha visíveis os contraexemplos bem-sucedidos. Não deduza
traços psicológicos, competência, cultura, tolerância a risco ou prioridades
duradouras a partir do estilo de escrita ou de estatísticas agregadas de uso.

## Saída

O chamador recebe um recorte atual ou explicitamente provisório, os limites das
evidências e a próxima ação de construção. Tendências históricas preenchem
lacunas; instruções atuais e fatos verificados do projeto governam o trabalho.
O arquivo nunca concede permissão, amplia o escopo, reinicia um ciclo limitado
nem muda critérios de aceitação.
