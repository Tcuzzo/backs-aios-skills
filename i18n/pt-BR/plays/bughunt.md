# Play: Bughunt

Uma caçada de bugs paralela e com limites. Trace a caçada como um mapa, espalhe
os caçadores por ele, verifique cada achado de forma adversarial e feche
costuras inteiras — nunca sintomas isolados.

## Quando rodar

- Uma auditoria, varredura ou caçada por muitas costuras — não um único bug
  reportado (para esse, use o repair loop).
- Um backlog de achados precisa ser atacado em paralelo, sem deriva e sem
  atropelo.

## A cadeia

1. [wayfinder](../skills/wayfinder/SKILL.md) — trace a caçada PRIMEIRO, como um
   mapa com um nó por costura ou achado. Os caçadores reivindicam nós de forma
   atômica na fronteira; fechar um nó escreve a pergunta do nó seguinte. Nada se
   inventa fora do mapa.
2. [leap-protocol](../skills/leap-protocol/SKILL.md) — cada nó é uma bola:
   objetivo, spec, escopo duro de arquivos, rodadas limitadas, resultado em três
   estados. Bolas relacionadas andam numa mesma fatia ordenada por dependência,
   com exatamente UM escritor.
3. [root-cause-first](../skills/root-cause-first/SKILL.md) — reproduza o bug e
   revise a evidência de causa-raiz ANTES de qualquer mudança no código. Nenhuma
   mutação na base do chute.
4. [repair-loop](../skills/repair-loop/SKILL.md) — a disciplina interna de cada
   bola: teste falhando commitado antes do fix, por
   [red-first](../skills/red-first/SKILL.md); execuções com escopo durante a
   iteração, por [sniper-testing](../skills/sniper-testing/SKILL.md); um passe
   completo dos módulos tocados no pouso.
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — todo achado é atacado
   de forma adversarial: um avaliador que não o escreveu ataca com recusa por
   padrão, e os jurados julgam um envelope com a autoria apagada. Quem constrói
   nunca avalia o próprio trabalho.
6. [seam-engineering](../skills/seam-engineering/SKILL.md) — feche a CLASSE na
   costura compartilhada, nunca o sintoma isolado.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — prova de
   fechamento: o branch corrigido tem que MORRER sob mutação. Um fechamento cujo
   mutante sobrevive não está provado, e o achado continua aberto.

## Uma bola fecha

Uma bola só fecha pelo gate de Score do
[leap-protocol](../skills/leap-protocol/SKILL.md) — verdade da fonte,
manter-ou-reverter, revisão cega, prova ao vivo, proveniência; evidência
faltando nunca vira aprovação por padrão. Estados terminais próprios da caçada:
todo achado termina FIXED (corrigido) ou REFUTED-WITH-EVIDENCE (refutado com
evidência).

## Regras da caçada

- Abaixe sua confiança. Reancore no livro-razão e no histórico de tentativas do
  nó, nunca na sua própria memória. Relançar significa reivindicar de novo na
  fronteira; passe o bastão por
  [session-handoff](../skills/session-handoff/SKILL.md).
- Transmita o progresso em voz humana enquanto trabalha. O desconhecido segue
  desconhecido — nunca vira "pass".
- Uma vez congelados os bytes candidatos, comandos, testes e veredito, o pouso é
  um replay determinístico. Nenhuma chamada de modelo re-decide um comando já
  decidido.
- Respeite a máquina: meça os recursos antes de criar processos, limite a
  concorrência, colete as lanes mortas, pare ALTO após a segunda morte no mesmo
  nó e aplique throttle em toda chamada externa. O kill-switch para novas
  reivindicações — nunca uma mutação em pleno voo.
- Nomeie o desperdício de cada fatia e meça o antes/depois. Só aceite um ganho
  de eficiência quando um comparador provar zero perda de capacidade; inchaço
  também é defeito.
- Reporte em duas palavras: PROVEN ou STILL-BUILDING.

## Gates duros — qualquer um reprova o play

- Uma mutação feita antes da revisão da evidência de causa-raiz reproduzida.
- Quem construiu avaliando o próprio achado.
- Um achado fechado enquanto um mutante sobrevive no branch corrigido.
- Uma rodada da suíte completa no meio da caçada — sniper só na costura do
  próprio achado.
- Teatro de mock num teste de fechamento: ele reabre o bug em silêncio enquanto
  o livro-razão diz que está fechado.
- Um achado estacionado em vez de corrigido ou refutado com evidência.
