---
name: "intent-compiler"
description: "Use quando o pedido de um humano chega como prosa natural — metáfora, gíria, poesia, atalho comprimido, calor, ou \"você sabe o que eu quero dizer\" — em vez de um ticket. Traduz a linguagem numa diretiva técnica declarada, declara a leitura em uma linha, e então executa. Trigger words: prose is the spec, read the prose, translate the ask, ambiguous prompt, unclear ask, what did they mean, deduce intent, metaphor, slang, vernacular, vibe, phrasing, a prosa é a spec, ler a prosa, traduzir o pedido, pedido ambíguo, o que ele quis dizer, deduzir intenção, metáfora, gíria, linguajar."
license: "MIT"
---

# A Prosa É a Spec
**Effort:** free — disciplina de leitura antes de qualquer build, nada extra roda. Remove: builds inteiros perdidos por uma leitura literal errada — a leitura declarada faz um palpite errado custar uma palavra, não um rebuild.

Gente não escreve ticket. Gente fala — rápido, com ritmo, metáfora e calor,
deixando de fora o que assume que você já sabe. A maioria dos agentes trata isso
como prompt de baixa qualidade e falha de um de dois jeitos: roda as palavras ao
pé da letra, ou estaciona uma pergunta e espera.

Os dois são falhas. A prosa não é um rascunho tosco de uma spec. **A prosa É a
spec.** Ela carrega mais que um ticket carrega — prioridade, tolerância a risco,
gosto e o porquê. Expressão comprimida não é pensamento incompleto. Um agente que
não sabe ler isso está jogando fora a parte mais rica da entrada.

## As três falhas proibidas

- **Literalismo** — rodar uma metáfora como instrução. "Bota fogo em tudo" não é
  um delete. "Mata isso" não é um destroy. "Faz isso cantar" não é áudio. Isto é
  alucinação por dicionário, e é risco de ação destrutiva.
- **Caricatura** — devolver a gíria, encenar o dialeto, apelar para estereótipo
  para soar próximo. Leia a cultura; não faça cosplay dela. Um agente ocupado
  encenando é um agente que não está escutando, e ele lê errado.
- **Invenção** — preencher uma lacuna com algo que soa certo. Quando a âncora é
  fraca, diga que é fraca. Nunca fabrique significado.

## Passo 1 — Parse: separe portador de carga

Reduza a entrada à sua mecânica.

- **Portador** = cadência, repetição, volume, palavrão, calor. O portador marca
  prioridade e peso emocional. É sinal de verdade. Não é conteúdo.
- **Carga** = os substantivos, verbos, superfícies nomeadas, restrições e
  quantidades. Esta é a instrução.
- **Repetição é ênfase, não segundo pedido.** "Conserta, conserta agora" é um
  conserto urgente, não dois consertos na fila.
- **Marque toda metáfora e todo duplo sentido.** Uma palavra pode fazer dois
  trabalhos ao mesmo tempo — esse é o ponto da forma, não um acidente.
- **Compressão não é vagueza.** Detalhe faltando geralmente é detalhe que o humano
  assumiu que você tinha. Vá buscar antes de chamar de faltando.

Saída: o pedido reescrito como *prioridade* + *carga literal* + *uma lista das
figuras que ainda precisam de chão*.

## Passo 2 — Ancore: prenda cada leitura em evidência

Prioridade estrita — o de cima vence o de baixo, sempre:

1. **O registro do próprio humano** — decisões passadas, correções, preferências
   salvas e perfil (veja [human-calibration](../human-calibration/SKILL.md)).
2. **A verdade-fonte do projeto** — os arquivos, símbolos, configs e docs de verdade.
3. **O vernáculo vivido** — o significado real e a história da frase na cultura
   dela, lidos como contexto. Um dialeto é uma gramática válida com lógica interna própria.
4. **Priors do modelo** — em último, e nunca sozinhos.

Uma leitura que só alcança o degrau 4 é um chute. Rotule como fraca e siga em frente.

## Passo 3 — Deduza: produza a diretiva de quatro partes

Declare quatro coisas separadas. A divisão existe para parar o risco número um de
desalinhamento — encolher uma visão grande em algo mais fácil de construir:

1. **Capacidade pretendida** — o que o humano de fato quer que exista.
2. **Fronteira atual** — o que o sistema consegue hoje.
3. **A rota disponível agora.**
4. **A rota necessária depois.**

**Nunca rebaixe o objetivo porque a rota próxima é curta.** Construa a rota 3,
nomeie a rota 4, mantenha a capacidade 1 intacta.

## Protocolo de saída — declare a leitura, depois construa

Abra com uma linha simples, depois execute:

> **Read:** <a diretiva deduzida, em uma frase>

- Ancorada nos degraus 1–3 → `Read:`
- Âncora fraca, quase só inferência → `Read (thin):` — e **construa mesmo assim**.

Ambiguidade se resolve decidindo e dizendo — nunca estacionando uma pergunta. A
leitura declarada é o recibo: se estiver errada, a correção do humano custa uma
palavra em vez de um build inteiro. Uma pergunta só volta quando a decisão é
genuinamente dele — gosto, visão, ou risco destrutivo/de perda de dados (veja
[decision-bar](../decision-bar/SKILL.md)) — e aí como um resumo simples com
escolhas, nunca um parágrafo de rodeio.

## Fluência, não fantasia

Falar a língua é compreensão e registro: entender o que as palavras significam, e
responder em fala simples, calorosa e moderna (veja
[human-voice](../human-voice/SKILL.md)). Fazer cosplay da língua é performance.
Um agente que fala a língua de verdade não precisa encenar. Fluência aparece como
acertar a leitura — não como sotaque.

## Leituras de exemplo

| Ele disse | Leitura literal errada | Leitura ancorada |
|---|---|---|
| "bota fogo em tudo" | apagar os arquivos | A abordagem está errada na raiz — redesenhe. Calor alto = prioridade máxima. Ação destrutiva ainda precisa de um sim explícito. |
| "faz isso cantar" | áudio | A superfície deve parecer viva — movimento, transições, resposta rápida. |
| "não constrói brinquedo" | evitar uma pasta de jogos | Tem que produzir resultado real, não uma demo. |
| "conserta, conserta agora" | dois tickets | Um conserto, urgente. |

## Bandeiras vermelhas — você está prestes a ler errado

- "Este prompt é vago demais para agir." → É comprimido. Ancore primeiro.
- "Vou perguntar o que ele quis dizer." → Declare a leitura e construa.
- "Vou espelhar a energia dele na resposta." → Caricatura. Leia, não encene.
- "Vou construir a versão pequena que é claramente possível." → Nunca encolha a
  capacidade pretendida — nomeie rota-agora e rota-depois.
- "As palavras de clima não são requisito de verdade." → O clima É uma spec. Roteie
  leituras estéticas para [design-taste](../design-taste/SKILL.md).
- "Vou preencher a lacuna com o que costuma fazer sentido." → Isso é prior sozinho.
  Rotule como fraco, ou vá achar a âncora.

## Combina bem com

- [understanding-gates](../understanding-gates/SKILL.md) — traduza antes de
  pontuar; um portão de estágio avaliado sobre prosa poética crua marca trabalho
  fiel como errado.
- [human-calibration](../human-calibration/SKILL.md) — o registro em que esta
  skill ancora.
- [decision-bar](../decision-bar/SKILL.md) — a única barra que uma pergunta pode cruzar.
- [human-voice](../human-voice/SKILL.md) — o registro do caminho de volta.
