---
name: clean-code-gauntlet
description: Use ao endurecer ou aterrissar qualquer build — um agente, um serviço, uma biblioteca — quando você quer uma barra de qualidade determinística em vez de review linha a linha. Roda sniper tests, o score CRAP (complexidade x cobertura) e mutation testing limitado, depois um review leve de gosto. Trigger words: clean code, gauntlet, unc, uncle bob, crap score, crap, mutation testing, harden, complexity, coverage, quality bar, código limpo, teste de mutação, endurecer, complexidade, cobertura, barra de qualidade.
license: MIT
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

1. **Sniper tests verdes.** Rode só os arquivos de teste que cobrem o que o diff
   tocou — veja [sniper-testing](../sniper-testing/SKILL.md). Baseline vermelha
   significa parar e consertar; nunca mute ou avalie em cima de vermelho.
2. **CRAP abaixo do limiar** sobre dados reais de cobertura (veja o portão abaixo).
   Estourou → refatore a função para baixo, ou cubra por completo. Nunca abaixe a barra.
3. **Mutation testing: zero sobreviventes no escopo.** Um sobrevivente condena os
   TESTES, não o código — fortaleça o teste que deveria tê-lo pego.
4. **Review leve de gosto** — um modelo julga só o que números não alcançam.

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
CRAP contra a baseline pré-mudança:

- **AUTHORED** — funções que esta mudança criou. A barra inteira se aplica.
- **WORSENED** — funções pré-existentes que esta mudança piorou. O delta é cobrado
  desta mudança; tem que voltar à baseline ou melhor.
- **UNCHANGED** — dívida pré-existente que a mudança nunca tocou. Reporte, arquive,
  nunca cobre desta mudança — e nunca use como desculpa para pular o gauntlet.

## Regras de mutação (limitadas, nunca imprudentes)

- **Nunca a árvore de trabalho compartilhada.** Mute num checkout de rascunho
  cortado do HEAD commitado. Arquivos alvo ou de teste sujos = recuse; commite primeiro.
- **Custo é medido, nunca presumido.** Cronometre a suite com escopo uma vez,
  reporte ETA = baseline x número de mutantes ANTES de gastar qualquer coisa.
  Ofereça um dry run.
- **Limitado e retomável.** Limite mutantes e minutos. Parada por orçamento é uma
  pausa com checkpoint, não uma falha — retome para terminar.
- **Cobertura primeiro.** Mute só linhas cobertas; linha descoberta é lacuna de
  cobertura que o portão CRAP já pegou.
- **Só no escopo.** Mute o que o diff tocou, nunca o repo inteiro.
- Um mutante genuinamente equivalente pode ser refutado em vez de morto — com a
  refutação por escrito, nunca pulado em silêncio.
- **Não existe ferramenta de mutação para o seu stack?** Registre isso no relatório
  de aterrissagem e apoie-se no portão CRAP — nunca pule em silêncio.

## O review de gosto (por último, e leve)

Portões determinísticos vêm primeiro; gaste um modelo só onde raciocínio é a única
ferramenta. O revisor é um modelo de família diferente da do builder — o builder
nunca avalia o próprio trabalho. Ele julga só design e gosto: nomes, preocupações
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
