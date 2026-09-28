# Instalação — acople o pacote a um agente de verdade

> **v0.7 portable installer:** Registro atual em um passo para Claude Code, Codex, Cursor, OpenCode e agentes portáteis: `./install.sh --target all --locale pt-BR`. O script não sobrescreve nada; no PowerShell, use `./install.ps1`. A matriz completa de caminhos atuais está no [guia canônico de instalação](../../INSTALL.md).

O pacote é um conjunto de pastas de markdown. Cada skill é
`skills/<name>/SKILL.md`. Cada play é `plays/<name>.md`. Sem binários, sem
servidor, sem etapa de build. Instalar significa colocar o markdown onde o seu
agente procura por skills.

O frontmatter é, de propósito, o subconjunto mínimo de 3 chaves — `name`,
`description`, `license` — da convenção aberta Agent Skills (agentskills.io). A
spec exige só `name` e `description`, e runtimes compatíveis ignoram chaves que
não reconhecem. Então o pacote carrega nativamente onde a convenção carrega, e
lê como markdown puro em todo o resto.

## 1. Plugin do Claude Code (recomendado)

Dois comandos dentro do Claude Code:

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

Isso instala tudo de uma vez: as skills carregam, os comandos de barra ficam
disponíveis (digite `/optimus` para subir o piso), e o hook de aterramento já
vem ligado — ele bloqueia ferramentas de mutação até o harness carregar. O
kill-switch do hook é seu: defina `AIOS_GATE=off` no ambiente para desligá-lo,
com alarde. As atualizações fluem por `/plugin` quando o repo do marketplace
avança.

## 2. Claude Code, manual

O Claude Code também descobre skills em duas pastas (confirmado contra a
documentação oficial, 2026-08): a pessoal `~/.claude/skills/<name>/SKILL.md`
(todos os projetos da sua máquina) e a de projeto `.claude/skills/` (viaja com
um repo só).

Pessoal, em uma linha:

    git clone https://github.com/Tcuzzo/backs-aios-skills.git ~/backs-aios-skills && ln -s ~/backs-aios-skills/skills/* ~/.claude/skills/

Projeto: `cp -r ~/backs-aios-skills/skills/* .claude/skills/`

Use symlink se quiser que as atualizações do pacote fluam; copie se quiser a
versão pinada (ou se symlinks derem problema no seu runtime). Abra uma sessão
nova. Uma skill dispara quando a tarefa bate com a `description` dela — diga as
palavras-gatilho e o agente carrega o arquivo. No caminho manual, plays não são
skills: mantenha-os no clone e peça ao agente para ler um
(`read ~/backs-aios-skills/plays/elite-build.md`) no começo da sessão, ou cole o
seu play padrão no CLAUDE.md do projeto.

## 3. Qualquer runtime de Agent Skills (a convenção aberta)

A convenção é adotada bem além do Claude — OpenAI Codex, Gemini CLI, Cursor,
VS Code e mais (pelo ecossistema da spec, 2026-08). As regras que importam aqui:
o arquivo se chama exatamente `SKILL.md`; o nome do diretório é igual ao `name`
do frontmatter; só `name` + `description` são obrigatórios. Este pacote cumpre
as três. Instalar = copiar `skills/*` para onde o seu runtime guarda skills (o
Cursor usa `.cursor/skills/`, por exemplo). Não verificamos a pasta de todos os
runtimes — confira a documentação da sua plataforma para o caminho exato.

## 4. OpenClaw, Hermes, outros frameworks de agente

Confirmado contra a documentação atual deles (2026-08):

- **OpenClaw** descobre qualquer `SKILL.md` sob suas raízes de skill
  configuradas. Copie `skills/*` para a pasta `skills/` do seu workspace, ou
  para a global compartilhada `~/.openclaw/skills`. A CLI `openclaw skills`
  gerencia instalações e atualizações.
- **Hermes (Nous Research)** mantém uma pasta por skill em `~/.hermes/skills/`,
  e carrega o SKILL.md da skill no system prompt quando a tarefa a ativa. Copie
  `skills/*` para lá.

Qualquer outro framework — o padrão genérico, sem precisar de código:

1. Monte ou cole cada `SKILL.md` como contexto invocável por ferramenta (uma
   ferramenta de documentos, uma entrada de biblioteca de prompts, um índice de
   recuperação). Mantenha a linha `description` intacta — as palavras-gatilho
   dela são o contrato de invocação.
2. Carregue um play (`plays/*.md`) como contexto de sistema da sessão. Um play
   nomeia as skills que dispara, em ordem; o agente então puxa cada skill pelo
   nome.
3. Verifique o mecanismo de instalação atual do framework na documentação dele
   antes de confiar neste arquivo — mecanismos mudam rápido; só afirmamos o que
   confirmamos acima.

## 5. Loop de API puro (sem framework)

Você é o harness. A cada volta do loop:

1. Coloque `skills/invariant-floor/SKILL.md` no system prompt, sempre. Esse é o
   piso que toda mudança precisa cumprir.
2. Escolha o play que bate com o pedido — build → `plays/elite-build.md`, bug →
   `plays/bughunt.md`, avaliação → `plays/grading-verification.md` — e anexe.
3. Compare as palavras do usuário com as palavras-gatilho da `description` de
   cada skill. Nunca injete o pacote inteiro — injete só a uma a três skills que
   batem. O pacote é enxuto em tokens; mantenha assim.
4. Re-injete a cada reset de contexto. Uma regra que caiu do contexto não está
   carregada.

## Primeira sessão

Instalação via plugin: digite `/optimus` e passe a tarefa. Instalação manual:

    Você:   leia ~/.claude/skills/optimus/SKILL.md e suba. Esta sessão segue esse arquivo.
    Você:   tarefa — o total do checkout sai errado quando cupom e vale-presente se acumulam.
    Agente: [sobe: carrega invariant-floor, escolhe plays/bughunt.md, nomeia as skills que vai disparar]
    Você:   vai.
    Agente: [o play conduz: reproduzir, teste vermelho, consertar a classe, verificar ao vivo, avaliação cega, pousar]
