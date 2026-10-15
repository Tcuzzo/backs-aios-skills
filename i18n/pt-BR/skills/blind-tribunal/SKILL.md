---
name: "blind-tribunal"
description: "Use quando uma mudança autônoma precisa de avaliação independente antes de aterrissar e não há humano no loop. Convoca jurados cegos, resolvidos por capacidade — uma lente cada — sobre um envelope de arquivos inteiros com autoria removida; cada achado vira um teste novo falhando; repita até todos os jurados passarem. Trigger words: blind tribunal, grill tribunal, tribunal, jurors, independent grade, convene, blind grade, independent grade, grade before landing, tribunal cego, jurados, avaliação cega, avaliação independente, convocar, avaliar antes de aterrissar."
license: "MIT"
---

# Blind Tribunal
**Effort:** heavy — oito jurados, uma lente cada, roteados por camada para o degrau de modelo mais barato que basta, reconvocados sobre envelopes novos a cada rodada até a unanimidade; gaste em mudanças autônomas que pousam sem revisão humana. Remove: pousos desgovernados guardados por nada além da palavra do próprio builder.

O loop de avaliação que deixa o humano sair da sala sem o agente sair dos trilhos.
Um painel de jurados revisa a mudança às cegas, com a autoria arrancada. Cada
achado vira um teste novo falhando. O loop repete até todos os jurados passarem.
Nada aterrissa só na palavra do builder.

## Quando rodar

- Antes de aterrissar qualquer mudança autônoma que nenhum humano vai revisar.
- Qualquer mudança de alto raio de explosão: cara de segurança, toca dados, perto de autoridade.
- Quando um avaliador só não basta e você quer lentes independentes sobre o mesmo artefato.

## As cadeiras

Oito jurados, uma lente cada. A execução autora que construiu o candidato é registrada
como proveniência e desqualificada; qualquer sessão que tenha herdado a conversa ou o
contexto do builder também. Jurado mandado checar tudo não checa nada direito.

| Jurado | Id da lente | Camada | A pergunta que ele faz |
| --- | --- | --- | --- |
| Defeito | `defect` | generalista | O que quebra de verdade? Falhas de lógica, erros de sintaxe, defeitos novos. |
| Proporção | `proportion` | generalista | Tem o tamanho certo? Superconstruído, ou na medida da intenção? |
| Consequência | `operator_consequence` | segurança do operador | Se um operador humano rodar isto, o que é destrutivo, inseguro ou danoso? |
| Reversibilidade | `reversibility` | estado profundo | Deixa efeitos irreversíveis? Se morre no meio, o sistema volta atrás limpo? |
| Continuidade | `state_continuity` | estado profundo | Órfãos, estado global sobrescrito, contexto perdido para os nós seguintes? |
| Economia | `resource_economy` | estrutural rápido | Loops sem otimizar, chamadas de rede/API redundantes, memória inchada? |
| Borda | `boundary_condition` | estrutural rápido | Com entrada nula, vazia, de tipo errado ou malformada — falha com graça? |
| Telemetria | `telemetry` | segurança do operador | Uma falha aqui se diagnostica pelos logs e pelo tratamento de erro? |

**Camadas de roteamento (primeiro a rota mais barata que basta):** estado profundo →
maior contexto e raciocínio mais fundo, de preferência por um harness que LÊ o repo
(nunca escreve); estrutural rápido → primeiro uma GPU local grátis; um veredito local
independente e suficiente pode PASSAR sem um verificador de nuvem ou fundido quando o
contrato da tarefa não o exige. Se um verificador opcional está FUNDIDO com o assento
primário, julga o mesmo prompt; se o verificador não está disponível (nenhum degrau de
nuva vivo), o veredito primário local se mantém por sua própria evidência, marcado
UNVERIFIED na revisão e no resumo — nunca "verificado" em silêncio. Um verificador
EXIGIDO pela tarefa que está ausente é uma RETENÇÃO independente de local/nuvem. O
modelo local precisa ver TODO o artefato (dimensione `num_ctx` pelo prompt — o padrão
do Ollama, 4096, trunca em silêncio — e recuse antes de enviar o que não cabe);
jurados via harness rodam read-only, e cada convocação carrega um `run_id` e escreve
seu resumo por último; depois os modelos de nuvem de baixa latência; segurança do
operador → seu coder mais forte com base em segurança; generalista → um generalista
grande e confiável. Toda escada termina num degrau local de sobrevivência.

**Rig solo.** Quando só um degrau de modelo está disponível, degrade
EXPLICITAMENTE: um contexto ou sessão nova que nunca viu a conversa do autor age
como avaliador cego, ou o humano revisa o envelope com autoria removida. Um
avaliador de mesmo modelo, degrau ou família em uma sessão nova e disjunta do
autor é permitido onde o runtime configurado o permita. O relatório tem que
nomear o portão enfraquecido — nunca fingir em silêncio que um portão mais
forte segurou.

## O construtor é declarado, e a exclusão é estrutural

"Família diferente do construtor" era uma regra que os jurados deviam lembrar. No próprio teste
do tribunal, o assento de segurança do operador foi liderado pelo mesmo modelo que construiu o
candidato, e nada o registrou ou excluiu: o autor avaliou o próprio trabalho por duas rodadas.
Então:

- **Convoque com o construtor nomeado** (`--builder <modelo-ou-família>`). O registro carrega
  `builder_family` como proveniência onde o runner o registra. A execução autora que construiu o
  candidato, e qualquer sessão que tenha herdado a conversa ou o contexto do builder, são
  desqualificadas em voz alta, antes de despachar, em cada escada. Uma lente sem degrau FICA EM
  ESPERA — nunca volta ao construtor. Proveniência, não um veto cego por modelo, degrau, família
  ou fornecedor.
- **Prove na escada viva, não num teste:** a tabela de rotas deve mostrar que os assentos caíram
  em degraus disponíveis vivos, e o relatório nomeia o degrau escolhido por lente. Senão a
  exclusão é enfeite.

## O envelope

Jurados nunca veem o repo, o builder ou a conversa. Eles veem um envelope:

- **Arquivos atuais inteiros** para cada arquivo que a mudança tocou, mais seus
  arquivos de teste. Nunca trechos soltos de diff — um trecho esconde o contrato ao
  redor e induz achados falsos.
- **O contrato de revisão**: a intenção da mudança em uma linha, e os critérios de pass.
- **Zero autoria.** Sem nomes, sem ids de modelo, sem autores de commit, sem
  histórico de chat. Se identidade vazar, a montagem do envelope falha alto — nunca
  avalie sem o cego.
- **Sem prosa sobre o comportamento antigo.** Descrever o que o código "fazia antes"
  planta defeitos fantasma. Os arquivos falam por si.

## O veredito

JSON estrito, parseável por máquina, um objeto, sem prosa:

```json
{"verdict": "pass" | "refuse",
 "findings": [{"severity": "blocker|major|minor|info",
               "claim": "...", "evidence": "..."}]}
```

- **Um pass que lista um achado `[blocker]` ou `[major]` não é um pass.** Contraditório; falha
  fechado em refuse, nomeando a severidade.
- **Um veredito para uma lente diferente da sentada** é um degrau recusado, não um veredito: anotado
  com as duas lentes, a marcha segue ao próximo degrau; só se todos responderem errado a lente
  fica em espera. Nunca um pass.
- **O diretório de saída é possuído antes de ser varrido.** O órgão carimba (stamp) o diretório que
  reivindica; um com essas formas de arquivo SEM o carimbo é recusado, arquivos e remédio nomeados,
  nada apagado. Um só com arquivos alheios nunca correu risco e não é bloqueado.
- **Uma lente que explode nunca descarta os vereditos já pagos.** Cada falha é registrada por
  lente; vereditos e resumo são escritos ANTES de lançar o erro.
- **A evidência de mutação nomeia um arquivo reescrito** (`changed_paths`).
- **Tudo que o órgão escreve é só do dono (0600).**
- **Um modelo local derramado só é descarregado pelo ÚLTIMO detentor.** Duas lentes podem
  compartilhar uma placa; a primeira a terminar não tira o modelo da outra no meio da chamada.
- **Um degrau que não cabe o artefato é pulado antes da chamada**, razão anotada; uma recusa por
  capacidade é um TIPO e a marcha continua — nunca um halt.
- Jurado que RESPONDEU mal — lixo, não-JSON, texto de recusa — conta como
  **refuse**; jurado que NUNCA respondeu (falha de transporte, inalcançável) é um
  **hold**: sente outro no lugar via [fleet-ladder](../fleet-ladder/SKILL.md),
  nunca um pass silencioso. Um tiro por jurado que responde por rodada — sem retry.
- Um pass seco com zero achados e sem evidência é um **voto de baixa informação**.
  Conta, mas nunca como a única prova — dois passes secos não vencem um refuse
  detalhado. Um pass forte nomeia o que checou.

## O loop

1. Red first: commite o teste de contrato falhando ANTES de construir o conserto, e
   registre esse commit. O builder não pode tocar no teste ([red-first](../red-first/SKILL.md)).
2. Construa até o verde.
3. Monte o envelope a partir dos arquivos ATUAIS.
4. Sente os oito jurados, por camada, escolhidos ao vivo por capacidade e
   disponibilidade na matriz de degraus configurada
   ([fleet-ladder](../fleet-ladder/SKILL.md) resolve o que está vivo). A execução
   autora que construiu é desqualificada, e qualquer sessão que tenha herdado a
   conversa ou o contexto do builder também; um avaliador de mesmo modelo, degrau
   ou família em uma sessão nova e disjunta do autor é permitido onde o runtime
   configurado o permita.
5. Cada jurado também verifica, não só lê: os testes novos passam; a suite de
   regressão não está pior que a baseline; e um cheque de falso verde — um teste que
   DEVERIA falhar (o bug reintroduzido) falha mesmo. Falso verde é refuse.
6. Em qualquer refuse: CADA achado — blocker, major e minor — vira um teste NOVO
   falhando, que falha pelo motivo real do achado. Conserte. Remonte o envelope
   sobre os arquivos revisados. Reconvoque TODOS os jurados. Veredito sobre arquivo
   velho não é veredito.
7. Aterrisse só com pass unânime. Achados minor levantados na rodada final também
   fecham, nunca ficam para depois — "consertei os blockers, minors depois" é
   exatamente o vazamento que esta skill existe para parar. Um achado termina
   CONSERTADO ou refutado com evidência registrada, nunca estacionado.

## O rodapé nomeia a lente, um degrau rejeitado guarda suas palavras, e a profundidade de rota é uma capacidade medida

A rodada 4 deixou duas lentes em espera com zero recusas, e cada elo ficou no registro. Três leis saíram dela:

- **Declare a forma da resposta ao lado da resposta.** O rodapé do protocolo carrega o nome literal da lente (`"lens": "defect"`), nunca o marcador `<your lens>`. Um jurado que devia lembrar a lente declarada 350 KB antes, dentro de um artefato que nomeia as oito lentes, respondeu a lente errada três vezes em duas rodadas. Preencha o marcador ao renderizar.
- **Um degrau rejeitado deixa suas palavras no registro.** Uma resposta com lente errada ou um veredito anulado carrega um `raw_tail` limitado na entrada rejeitada, para a próxima rodada ler a causa em vez de inferi-la.
- **A profundidade de rota é uma capacidade medida, não um piso mágico de "três degraus de nuvem".** Cada nível mantém degraus suficientes para o artefato que precisa carregar (`context_tokens` e `num_ctx` no Ollama; o padrão 4096 trunca em silêncio). Uma lente errada mais uma anulação nunca devem deixar uma lente em espera.
- **O canal de raciocínio e o orçamento seguem a rota e a forma da resposta.** Um modelo raciocinador, ao qual se pediu um veredito JSON seco, gastou seu orçamento sobre um artefato de 131k tokens e não emitiu nada (`finish_reason=length`); o teto de tempo do papel então matou o degrau seguinte no meio do caminho. Algumas nuvens desativam raciocínio para JSON (`reasoning_effort: none`), outras mantêm medium; o incidente histórico fica registrado como evidência, não como regra universal.
- **Nada mais escreve no repo do tribunal enquanto ele se reúne.** O arquivo de estado de um avaliador concorrente dentro do checkout mudou bytes sob um assento, e o órgão anulou aquele veredito com honestidade: ele não consegue atribuir uma mudança. Serialize os escritores, ou reúna em um worktree separado do mesmo commit.

## Regras duras — qualquer uma quebrada anula a avaliação

- O builder nunca avalia o próprio trabalho: a execução autora que construiu, e
  qualquer sessão que tenha herdado a conversa ou o contexto do builder, são
  desqualificadas; um avaliador de mesmo modelo, degrau ou família em uma
  sessão nova e disjunta do autor é permitido onde o runtime configurado o
  permita.
- **Um refuse de jurado vale o que o envelope vale.** Antes de escrever um teste a
  partir de um achado, verifique o achado contra os arquivos de verdade. Achado
  sobre código que o envelope nunca carregou significa consertar o envelope, não o código.
- Meça convergência pelos achados NOVOS por rodada, não pelo total bruto. Achados
  novos estáveis ou crescendo por duas rodadas seguidas: pare e escale para o
  humano. Nunca fique moendo.
- Nunca enfraqueça ou edite os testes falhando para alcançar um pass. Jurados
  verificam que os arquivos de teste estão intocados desde o commit red.
- **Um sobrevivente é uma alegação; uma prova verde é uma alegação.** Rode de novo à mão cada
  mutante sobrevivente, numa árvore isolada, com um teto que sobreviva à carga. Um timeout não é
  sobrevivente; um erro de coleta não é kill. Todo caminho de veredito deve poder dizer INVALID, e
  um harness cuja linha de base sem mutação não esteja verde limpo se recusa a emitir vereditos.
- Pass unânime abre o portão; não é a chegada. Aterrisse, depois prove a capacidade
  ao vivo na superfície real. Verde sem prova ao vivo não é pronto.

## Combina bem com

- [red-first](../red-first/SKILL.md) — o contrato falhando, commitado antes do builder rodar.
- [sniper-testing](../sniper-testing/SKILL.md) — efeitos colaterais reais, execuções com escopo, sem teatro de mock.
- [seam-engineering](../seam-engineering/SKILL.md) — conserte a classe, varra os irmãos, aterrisse uma guarda.
- [repair-loop](../repair-loop/SKILL.md) — o loop de construção que este tribunal avalia.
- [blind-eval](../blind-eval/SKILL.md) — o portão manter-ou-reverter mais leve quando a questão é gosto, não defeito.

> Scaffold credit: Matt Pocock, grill-me / grilling (mattpocock/skills, MIT). The
> blind adversarial tribunal design is BACKS AIOS.
