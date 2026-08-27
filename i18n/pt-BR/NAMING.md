# Nomes — como este pacote nomeia as coisas, e por quê

Os nomes deste pacote carregam peso estrutural. Um agente escolhe uma skill
comparando a tarefa com o nome e a descrição, então um nome que diz a coisa
errada manda o trabalho para a disciplina errada. A convenção abaixo mantém o
roteamento honesto.

## Os três tipos de nome

- **Skills são disciplinas em forma de substantivo.** Uma skill é o contexto que
  um agente carrega para raciocinar — um corpo de regras, não uma ação. Por isso
  ela é nomeada como uma disciplina: `red-first`, `seam-engineering`,
  `sniper-testing`. Você carrega uma disciplina; não "roda" uma.
- **Comandos são imperativos.** Um comando é uma ação com começo e fim, então
  seu nome é um verbo, ou o nome do play ou skill que ele dispara: boot, build,
  hunt, grade, tribunal.
- **O piso de invariantes é lei.** `invariant-floor` é a única skill que todas
  as outras herdam. Ela leva o nome do que é — o piso — porque toda regra dura
  do pacote se apoia nela, e nenhuma skill pode pousar uma mudança abaixo dela.

## Os comandos incluídos

| Comando | Dispara |
| --- | --- |
| `/agent-build` | `plays/agent-builds.md` |
| `/bughunt` | `plays/bughunt.md` |
| `/design-taste` | `plays/design-taste.md` |
| `/elite-build` | `plays/elite-build.md` |
| `/grade` | `plays/grading-verification.md` |
| `/optimus` | `skills/optimus/SKILL.md` |
| `/parallel-work` | `plays/parallel-work.md` |
| `/secure-delivery` | `plays/security-delivery.md` |
| `/tribunal` | `skills/blind-tribunal/SKILL.md` |
| `/web-build` | `plays/web-app-builds.md` |

`design-taste` existir como skill, play e comando é de propósito — uma
disciplina, três formas de entrada: a skill é o contexto, o play é a receita, o
comando é o gatilho. Sem ambiguidade, porque o comando dispara o play; o play
aponta para a skill.

## Onde cada tipo de informação mora

Cada camada responde a uma pergunta diferente, e nada se duplica:

- **O nome diz o mecanismo.** `blind-tribunal` conta como funciona antes de
  você abrir o arquivo: jurados, cegos para o autor.
- **A descrição carrega as palavras-gatilho.** O runtime compara suas palavras
  com as descrições, então a descrição guarda toda frase que um humano diria
  quando precisa da skill — incluindo nomes antigos (veja abaixo).
- **O corpo carrega as regras.** Passos, regras duras que reprovam a skill e as
  skills com que ela combina. O corpo é a disciplina; o nome e a descrição são
  só o endereço dela.

## Renomear nunca quebra

Quando uma skill é renomeada, o nome antigo vira palavra-gatilho na descrição,
para que todo hábito e todo doc que usava o nome antigo continue roteando certo:

- **optimus** mantém o nome por inteiro — é a marca do boot, o único nome
  próprio do pacote, e o comando que você digita primeiro (`/optimus`).
- **"yoke"** sobrevive como palavra-gatilho em `human-calibration` — diga
  qualquer um dos dois, e a mesma disciplina carrega.

Um rename que quebra um gatilho existente é uma regressão, não uma limpeza.

## Justificativa por skill

| Nome | Por que esse nome |
| --- | --- |
| absorb | A disciplina de trazer uma capacidade externa para dentro e re-engenheirá-la como nativa, em vez de duplicá-la. |
| blind-eval | Avaliação com a autoria escondida — a cegueira é o mecanismo. |
| blind-tribunal | Um painel de jurados, cegos para o autor, de famílias de modelos diferentes. Tribunal = painel mais veredito. |
| bounded-loops | A propriedade imposta: todo loop carrega um limite — orçamento, checkpoint, kill-switch. |
| clean-code-gauntlet | Um gauntlet é uma sequência de provas duras; código limpo é o que sobrevive a ela. |
| decision-bar | Uma régua contra a qual toda decisão é medida antes de poder chegar ao humano. |
| design-taste | A disciplina do gosto no trabalho visual — travada e checada, não deixada no feeling. |
| fleet-ladder | A frota de modelos resolvida como uma escada de fallback, subida em ordem. |
| gpu-dispatch | A lei de despacho para trabalho em GPU: um modelo por placa, quente durante o loop. |
| guided-steps | Passos que só um humano consegue dar, guiados uma etapa por vez. |
| human-calibration | Calibrar o build para o humano que ele serve. (Era "yoke" — o nome antigo sobrevive como palavra-gatilho.) |
| incident-closure | Um incidente é fechado por completo — da causa-raiz à prova ao vivo — nunca triado de volta para o humano. |
| intent-compiler | Compila linguagem natural numa diretiva executável. A prosa é a fonte; a diretiva é a saída. |
| invariant-floor | O piso de leis numeradas que toda mudança precisa cumprir. Lei, não orientação. |
| leap-protocol | O protocolo para saltar trabalho grande entre builders paralelos e pousá-lo por uma só espinha. |
| live-research | Pesquisa contra fontes vivas — docs e código como estão agora — não a memória do modelo. |
| model-fusion | Vários modelos rascunham, um juiz independente escolhe — fusão de saídas, não votação. |
| optimus | A marca do boot, mantida como nome próprio. Ele sobe o piso; toda sessão começa aqui. |
| human-voice | Nomeada pelo que impõe: o agente escreve do jeito que uma pessoa fala, e as ideias difíceis ainda chegam inteiras. |
| red-first | O teste que falha (vermelho) vem primeiro, commitado antes de o build começar. |
| repair-loop | O ciclo de conserto completo, nomeado pela sua forma: ancorar, reproduzir, consertar, verificar, pousar. |
| root-cause-first | A ordem das operações é a regra: causa antes do conserto, sempre. |
| seam-engineering | Consertos pousam na costura — a primitiva compartilhada — nunca como remendos pontuais espalhados. |
| session-handoff | Nomeada pelo seu artefato: um arquivo de handoff que uma sessão fria consegue continuar. |
| sniper-testing | Um tiro, um alvo: rode só os testes que cobrem o que você tocou. |
| understanding-gates | Gates em cada etapa do build que checam entendimento, não só sintaxe. |
| wayfinder | Acha o caminho quando está perdido, em vez de estacionar uma pergunta no humano. |
