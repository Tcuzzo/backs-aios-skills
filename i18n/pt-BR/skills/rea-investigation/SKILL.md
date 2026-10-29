---
name: rea-investigation
description: Use REA para investigar executável distribuído, pacote ou comportamento observado em execução quando isso ajudar a diagnosticar ou corrigir uma falha.
license: MIT
---

# Investigação de artefatos com REA

Use o motor REA instalado e sua skill independente para binários distribuídos, pacotes ou comportamento solicitado em execução. Para repositórios comuns de código, use diretamente o código e os testes. Esta ponte não instala REA, Ghidra, provedores ou servidor MCP e não afirma que estejam disponíveis.

1. Identifique o alvo exato e a pergunta. Leia a skill REA original instalada e as referências relevantes no diretório de skills do agente, sem selecionar esta ponte recursivamente. Se estiver ausente, informe e continue a investigação útil com as ferramentas disponíveis.
2. Use as ferramentas REA conectadas quando disponíveis ou a CLI instalada. Para binários nativos compatíveis, use um provedor Ghidra compatível já existente; informe ausência ou indisponibilidade sem inventar resultados ou instalar dependências sem autorização.
3. Comece com inspeção estática somente leitura. Registre identidade do alvo, IDs de evidência, escopo, limites e dúvidas. Achados estáticos não comprovam comportamento em execução; observe ao vivo apenas dentro do escopo solicitado e dos limites declarados de execução e alteração da ferramenta.
4. Leve os achados a root-cause-first e repair-loop. Para adotar uma capacidade de código aberto, use absorb e suas verificações de licença e dependências. Selecione por papel e capacidade pelo fleet-ladder configurado, sem fixar IDs de modelos. Para avaliação independente, use uma execução nova de blind-tribunal separada do autor e um pacote congelado sem dados do autor, conforme as capacidades reais do runtime.

Scaffold: REA by morluto, MIT license, https://github.com/morluto/rea.
O motor, a skill original e os provedores são instalações separadas.
