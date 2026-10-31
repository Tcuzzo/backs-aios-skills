---
name: "clean-code-gauntlet"
description: "Use ao endurecer ou integrar mudanças executáveis que precisem de medidas de complexidade, cobertura, força de regressão e revisão de design independente."
license: "MIT"
---

# Clean Code Gauntlet
**Effort:** heavy — computação de verdade: rodadas de cobertura e complexidade mais uma passada limitada de mutação, depois um modelo de gosto; gaste em mudanças que vão para produção. Remove: review humano linha a linha de diffs inteiros, e os testes verde-falso atrás dos quais uma regressão se esconde.

## Por que isto existe

Código bagunçado faz agente patinar, e regra enterrada num prompt longo some no
meio do contexto — cheque determinístico nunca some. Então rode Clean Code como um
**gauntlet que o código tem que passar**, não prosa que o modelo tem que lembrar.

**Meça, não revise.** Feche o portão com números que uma ferramenta computa:
cobertura, complexidade ciclomática (uma contagem de caminhos independentes por
função), tamanho de módulo, mutantes mortos. Humanos e modelos auditam amostras —
nunca diffs inteiros.

## A corrente (rode em ordem; cada estágio para alto na falha)

Vincule `base_sha`, `candidate_sha`, responsável pela integração e cota restante
de [bounded-loops](../bounded-loops/SKILL.md) do pacote existente do
[Build Flow](../backs-build-flow/SKILL.md). Reutilize evidências ainda válidas;
rodadas de revisão e campanhas de mutação não reiniciam o orçamento.

1. **Lint, tipos e comportamento focados em verde.** Execute comandos aplicáveis
   do repo; veja [sniper-testing](../sniper-testing/SKILL.md). Registre verificações
   indisponíveis ou inaplicáveis sem chamá-las aprovadas. Baseline vermelha exige
   parar e corrigir; nunca mute nem avalie sobre vermelho.
2. **CRAP abaixo do limiar** com cobertura real (gate abaixo). Se falhar, refatore
   a função ou cubra por completo. Nunca reduza a barra.
3. **Mutação: nenhum sobrevivente sem explicação no escopo.** Sobrevivente não
   equivalente revela lacuna de regressão. Acrescente arquivo suplementar separado;
   preserve byte a byte o contrato original selado de [red-first](../red-first/SKILL.md).
   Refute mutantes equivalentes com evidências. Erro de ferramenta ou timeout é
   inconclusivo, nunca mutante morto.
4. **Review leve de gosto** — um modelo julga apenas o que os números não conseguem.

## Ferramentas que computam isso

| Stack | Ferramentas |
| --- | --- |
| Python | coverage.py + radon + mutmut |
| JS/TS | c8 (ou istanbul) + Stryker |
| Go | go test -cover + gocyclo + go-mutesting |
| Rust | cargo-tarpaulin + cargo-mutants |
| Java | JaCoCo + PIT |
| Outra | qualquer % de cobertura + qualquer contador de complexidade ciclomática |

Um formato de comando por estágio:
- Cobertura: `coverage run -m pytest <sniper files> && coverage report` (JS/TS: `npx c8 vitest run <files>`)
- Complexidade: `radon cc -s <changed files>`
- Mutação: `mutmut run --paths-to-mutate <changed files>` (JS/TS: `npx stryker run --mutate "<glob>"`)

Esses comandos são exemplos, não instruções de instalação nem garantias de CLI
estável. Use ferramentas fixadas e flags suportadas do repo. Para mudanças apenas
de documentação, valide links, estrutura, distribuição e cenários de comportamento;
complexidade e mutação podem ser inaplicáveis. Registre o motivo sem inventar métricas.

## O portão CRAP

```
CRAP(m) = comp(m)^2 * (1 - cov(m)/100)^3 + comp(m)
```

- Com 100% de cobertura o score colapsa para a própria complexidade.
- 30 é a linha clássica do "crappy" (complexidade 5 com cobertura zero já bate nela).
- Humanos seguram por volta de 4–5 de complexidade por função. Um agente pode
  carregar 6–8 SOMENTE com cobertura perto de 100% — a cobertura paga pela folga.
- Uma função com CRAP alto tem exatamente duas saídas: refatorar para baixo, ou
  cobrir por completo. **Nunca abaixe o limiar para passar.**

## De quem é a dívida — AUTHORED / WORSENED / UNCHANGED

Um score absoluto esconde de quem é a dívida. Divida todo delta de complexidade e
CRAP contra o `base_sha` fixado anterior à tarefa, com cobertura real comparável:

- **AUTHORED** — funções que esta mudança criou. A barra inteira se aplica.
- **WORSENED** — funções pré-existentes que esta mudança piorou. O delta é cobrado
  desta mudança; tem que voltar à baseline ou melhor.
- **UNCHANGED** — dívida pré-existente que a mudança nunca tocou. Reporte, arquive,
  nunca cobre desta mudança — e nunca use como desculpa para pular o gauntlet.

## Regras de mutação (limitadas, nunca imprudentes)

- **Nunca na árvore compartilhada.** Mute em checkout temporário do
  `candidate_sha` commitado exato. Alvos ou tests sujos exigem checkpoint e
  conclusão do candidato primeiro. Preserve trabalho alheio no checkout original.
- **Custo é medido, não presumido.** Cronometre uma vez a suite focada e informe
  ETA = baseline x quantidade de mutantes ANTES do gasto. Ofereça dry run.
- **Limitada e retomável.** Limite mutantes e minutos dentro da cota restante.
  Parada por orçamento registra mutantes não verificados e deixa o gate incompleto.
  Retome só com cota restante ou explicitamente ampliada.
- **Cobertura primeiro.** Mute apenas linhas cobertas; as descobertas são lacunas
  já detectadas pelo gate CRAP.
- **Só no escopo.** Mute o diff, nunca o repo inteiro.
- Mutante realmente equivalente pode ser refutado por escrito com evidência,
  nunca ignorado em silêncio.
- **Não há ferramenta de mutação para o stack?** Registre limitação e evidência
  substituta real. Aplique a política de aceitação do repo; gate obrigatório fica
  incompleto até seu responsável aceitar alternativa documentada.

## O review de gosto (por último, e leve)

Portões determinísticos vêm primeiro; gaste um modelo só onde raciocínio é a única
ferramenta. O revisor é escolhido ao vivo por capacidade e disponibilidade na
matriz configurada; a execução autora é registrada como proveniência e excluída.
A revisão usa sessão nova separada do autor, sem sua conversa nem contexto herdados;
o builder nunca avalia o próprio trabalho. Ele julga só design e gosto: nomes, preocupações
misturadas, largura de interface, e os seis cheiros — rigidez, fragilidade,
imobilidade, complexidade desnecessária, repetição desnecessária, opacidade. A
aritmética os portões já resolveram.

Piso de ofício que o review segura: funções pequenas, fazendo uma coisa, poucos
argumentos, sem argumentos de flag, nomes honestos; módulos profundos — uma
interface pequena escondendo lógica de verdade; testes rápidos, independentes,
repetíveis, um comportamento afirmado em cada.

## Regras duras (qualquer uma quebrada reprova a skill)

- Nunca abaixe um limiar nem enfraqueça o conjunto de mutação para forçar um pass.
- Nunca mute a árvore de trabalho compartilhada; nunca rode sem limite.
- Nunca cobre dívida UNCHANGED da mudança atual.
- Um teste que não consegue falhar é teatro — mutation testing é como você prova
  quais testes são reais.
- Diga o custo real — tempo de máquina é barato, regressão não é. Nunca finja verde
  para economizar a hora.

## Combina bem com

- [sniper-testing](../sniper-testing/SKILL.md) — escolhe o escopo de teste do estágio 1
- [red-first](../red-first/SKILL.md) — o contrato falhando que precede qualquer build
- [blind-eval](../blind-eval/SKILL.md) — manter-ou-reverter quando a questão é gosto
- [blind-tribunal](../blind-tribunal/SKILL.md) — um veredito avaliado mais completo antes de aterrissar

> Crédito de scaffold: Robert C. Martin, *Clean Code* (2008); Alberto Savoia &
> Bob Evans, a métrica CRAP (2007); John Ousterhout, módulos profundos
> (*A Philosophy of Software Design*, 2018); Pocock, M., & Martin, R. C.
> (2026, Aug 19). LIVE: Uncle Bob on Software Fundamentals in the Age of AI
> [Video]. YouTube. https://www.youtube.com/watch?v=zcLPGC-tvgk — fonte da
> banda CRAP para agentes e da mutação cobertura-primeiro. A composição e as
> regras duras daqui são do BACKS AIOS.
