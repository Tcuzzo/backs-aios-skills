---
name: guided-steps
description: Use quando um setup precisa de passos que só um humano consegue fazer — dashboards de terceiros, credenciais, secrets de CI, provisionamento, migrações pontuais, cutovers. Escreve um script interativo estágio a estágio que abre cada URL, diz o que clicar e copiar, captura valores e escreve onde eles pertencem. Trigger words: wizard, human-only steps, provision, credentials, dashboard setup, CI secrets, cutover, assistente, passos humanos, provisionar, credenciais, configurar dashboard, segredos de CI, virada.
license: MIT
---

# Wizard de Passos Humanos
**Effort:** free — disciplina de autoria mais uma checagem estática de sintaxe; nenhuma chamada de modelo. Remove: reexplicar a cada execução o mesmo caminho de cliques que só um humano faz, e segredos colados em arquivos rastreados pelo caminho.

Alguns passos só um humano consegue fazer: clicar por um dashboard de terceiro,
criar credenciais, aprovar uma tela de provisionamento. São chatos de fazer na mão
e chatos de re-explicar toda vez. O wizard transforma isso numa execução guiada:
um shell script interativo, estágio a estágio, que abre cada URL, diz exatamente o
que clicar e copiar, captura os valores e escreve onde eles pertencem.

## Quando usar

- Um setup precisa de um humano dirigindo uma UI que nenhuma API alcança —
  dashboards, consoles, telas de credencial, páginas de secret de CI, migrações
  pontuais, cutovers.
- O caminho é longo o bastante para doer re-explicar toda vez.

Quando NÃO usar: uma API consegue fazer o passo (automatize — o wizard é o último
recurso), ou o procedimento tem um ou dois passos (só diga ao humano em palavras
simples).

## O formato

Um script, duas partes:

- **Uma biblioteca auxiliar no topo** — idêntica em todo wizard, nunca editada na
  mão. Ela fornece: cabeçalhos de estágio com progresso ("estágio 3 de 7"),
  narração em voz humana, abertura de URL multiplataforma, entrada oculta para
  secrets, upserts idempotentes no `.env` (atualiza a chave se existe, anexa se
  não), escritas no cofre de secrets do seu provedor de CI, um passo de
  confirmar/pausar, e um resumo final de tudo que foi capturado.
- **Os estágios abaixo de um marcador** — a única parte que você escreve. Um
  estágio por passo humano: abra a URL, diga o que clicar e o que copiar, capture o
  valor, escreva no destino. Defina o total de estágios para o mostrador de
  progresso ser honesto.

## Processo

1. **Escopo.** Leia o arquivo de exemplo de env, o README, a config de deploy e os
   workflows de CI. Todo secret ou variável que eles referenciam é um valor que o
   wizard tem que produzir. Mostre ao humano os estágios ordenados e os valores
   logo de cara — confirme o plano antes de escrever.
2. **Mapeie a jornada de cada estágio.** Uma linha por estágio: URL → ação →
   valor → destino. O humano vê o caminho inteiro antes de começar.
3. **Escreva.** Copie o template. Escreva só os estágios; nunca toque na
   biblioteca. Mantenha a narração em palavras simples — a pessoa rodando isto
   pode não ser engenheira.
4. **Verifique estaticamente.** Cheque a sintaxe do script (`bash -n`,
   shellcheck), torne-o executável, e depois percorra cada estágio na mão: cada
   URL está certa, cada instrução clara, cada alvo de escrita correto? NÃO rode de
   ponta a ponta — ele abre navegadores e trava esperando entrada humana.

## Regras duras

- **Secrets nunca tocam arquivos rastreados.** Valores capturados aterrissam no
  `.env` gitignorado ou no cofre de secrets do CI. O script em si carrega só
  placeholders; o humano cola os valores reais na hora de rodar. Uma chave real,
  hostname ou dado pessoal no script escrito É o bug.
- **Toda escrita remota é tiro único e limitada.** Uma escrita no cofre de secrets
  é uma chamada de API: sem loops de retry, sem martelar. Falhe alto e deixe o
  humano rodar o estágio de novo.
- **Efêmero por padrão.** Um wizard é feito para uma execução e apagado depois.
  Commite só quando o humano pedir um caminho de setup repetível — e um wizard
  commitado continua carregando só placeholders.
- **O passo de confirmar é o botão de pausa do próprio humano, não um portão.**
  Existe para ele conferir o próprio trabalho — nunca para pôr atrito de aprovação
  em cima dele.

## Combina bem com

- [session-handoff](../session-handoff/SKILL.md) — registre quais estágios rodaram se a execução for dividida.
- [human-voice](../human-voice/SKILL.md) — o registro em que cada estágio narra.
- [bounded-loops](../bounded-loops/SKILL.md) — a regra de não-martelar atrás das escritas remotas.

> Scaffold credit: Matt Pocock, wizard (mattpocock/skills). The composition and hard rules here are BACKS AIOS.
