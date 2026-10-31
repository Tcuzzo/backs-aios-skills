---
name: human-calibration
description: "Use quando uma escolha de construção, design, comunicação ou UX importante precisar das preferências expressas e do contexto de trabalho do operador."
license: MIT
---

# Conheça seu humano

Aplique o pedido e as correções atuais do operador. Use evidências sobre suas
preferências de trabalho para escolher explicações úteis, atualizações de progresso
e decisões de design. Esse conhecimento é contexto revisável, nunca persona fixa
nem permissão.

## Uma única passagem de perfil

[operator-essence](../operator-essence/SKILL.md) cuida do arquivo privado de contexto
e de suas evidências. Reutilize seu recorte atual do
[Build Flow](../backs-build-flow/SKILL.md). Se faltar, execute uma única vez o fluxo
de insights disponível dessa skill, avalie o relatório/histórico fornecido e crie
contexto provisório quando as evidências forem escassas. Não reinicie a coleta de
insights em cada skill seguinte.

Um perfil existente indicado pelo operador pode fornecer evidências: preserve
fonte, data, confirmação e incerteza ao reconciliá-lo na essência. Não vasculhe
perfis alheios nem deduza quem é dono de um arquivo pelo nome de exibição.
Mantenha dados pessoais fora do código público do plugin. Uma tarefa somente
leitura pode passar um recorte em memória sem escrever perfil algum.

## Aplique o que se sabe

- Preferências e correções explícitas atuais prevalecem sobre observações
  históricas. Fatos do projeto e verificações de aceitação ainda precisam ser verificados.
- Diferencie escolhas observadas de tendências inferidas. Um design rejeitado ou
  pedidos repetidos de atualizações sustentam uma adaptação específica; não
  estabelecem personalidade, identidade, competência nem tolerância geral a risco.
- Use o menor recorte relevante: preferência ou observação, evidência de apoio,
  adaptação proposta e incerteza. Mostre ao operador de onde veio.
- Preserve os dois lados de uma tensão real, como profundidade do contexto e
  velocidade de execução. Resolva com condição concreta de prontidão e evidência,
  sem reduzir o objetivo.
- Uma pergunta opcional pode resolver uma incógnita material sobre gosto ou
  comunicação. Faça primeiro trabalho útil autorizado. Não exija questionário
  nem reconfirme preferências já fornecidas só porque uma nova sessão começou.
- Registre correções e contraexemplos quando a escrita do perfil estiver autorizada.
  Uma correção atualiza o contexto; nunca reescreve silenciosamente a tarefa nem
  concede autoridade para ações não relacionadas.

## Saída

Devolva um recorte conciso ao responsável existente pela tarefa. O usuário pode
inspecionar e corrigir. Adapte como o agente comunica e coleta evidências;
mantenha os mesmos padrões de fatos, qualidade e autorização para todo operador.

## Combina bem com

- [operator-essence](../operator-essence/SKILL.md) — evidências privadas e inicialização de insights.
- [human-voice](../human-voice/SKILL.md) — comunicação clara no registro solicitado.
- [intent-compiler](../intent-compiler/SKILL.md) — linguagem ambígua transformada em contrato de ação.
- [operator-intent-deduction](../operator-intent-deduction/SKILL.md) — escolhas a partir da intenção atual.
