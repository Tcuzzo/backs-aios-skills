---
name: "root-cause-first"
description: "Use diante de um bug difícil, uma falha silenciosa, uma caça a regressão ou uma mudança arriscada que pode quebrar sem barulho um consumidor a jusante. Nada de conserto sem investigação — leia o erro, reproduza sob demanda, cheque as mudanças recentes, instrumente as fronteiras dos componentes, rastreie o fluxo de dados de trás para frente até a fonte. Trigger words: debug, root cause, why is this failing, silent failure, regression, works in tests but fails live, systematic debugging, causa raiz, por que está falhando, falha silenciosa, regressão, passa no teste mas quebra ao vivo."
license: "MIT"
---

# Root Cause First
**Effort:** free — disciplina pura de investigação que em geral corta custo na raiz: uma sonda decisiva substitui disparar o pipeline inteiro para ver o que acontece. Remove: remendos na coisa errada — o conserto de sintoma que esconde o bug real e quebra um consumidor a jusante.

Nada de conserto sem investigação. Um remendo feito antes de você entender a
falha conserta a coisa errada, esconde o bug de verdade e quebra algo a
jusante. Seu produto não é um remendo — é uma causa raiz provada por uma sonda
decisiva, e um conserto provado que não regride nada.

Duas leis governam tudo abaixo:

1. **Sem suposições — o código, os dados e o sistema vivo são a verdade;
   notas são só pistas.** Um comentário, uma memória, uma conclusão anterior,
   até a sua última frase é hipótese até uma sonda confirmar. As palavras
   "todos / cada / nenhum" disparam uma checagem em três pontos: o ambiente,
   uma busca no repo inteiro e uma varredura de todo chamador.
2. **Um contraexemplo verificado mata a conclusão anterior na hora.** Quando
   uma sonda contradiz o que você acreditava, diga com clareza "eu estava
   errado — na verdade é X", e siga a partir do fato novo. Nunca passe pano.

## O loop (rode em ordem; não pule)

1. **Leia o erro.** Declare o sintoma em uma frase precisa. Leia a mensagem
   real, não a que você espera que ela diga. Nomeie o raio de explosão: o que
   depende da coisa que você suspeita?
2. **Reproduza.** Faça a falha acontecer sob demanda — ao vivo, ou num teste
   que falha. **Cronometre.** Uma "falha" que volta em milissegundos quando o
   trabalho real leva segundos é uma exceção engolida cedo, não trabalho real
   falhando. A diferença de tempo é, por si, uma pista.
3. **Cheque as mudanças recentes.** Faça o diff do que mudou desde a última
   vez que funcionou — código, config, ambiente, dependências. Se o histórico
   é longo, bissecte.
4. **Mapeie os consumidores.** Para um bug numa superfície compartilhada,
   liste cada chamador e como cada um a usa (comparação exata de string?
   booleano? lista?). A regressão de verdade costuma se esconder numa
   comparação exata a jusante, não no botão que você está girando.
5. **Instrumente as fronteiras.** Logue ou sonde em cada costura de
   componente — o que entra, o que sai. Rastreie o dado ruim de trás para
   frente, fronteira por fronteira, até chegar à fonte. Conserte a fonte,
   nunca o sintoma.
6. **Cause-raiz por hipótese.** Forme uma hipótese falsificável. Ache a ÚNICA
   sonda decisiva que a separa das alternativas, e rode só ela. Não dispare o
   pipeline inteiro "pra ver o que acontece".
7. **Conserte cirurgicamente, na costura certa.** A menor mudança que resolve
   a causa raiz. Prefira a fonte compartilhada única (um normalizador, um
   runner) a editar N pontos de chamada. Quando possível, faça o conserto
   inerte no caminho que funciona — provadamente não muda nada ali e só ativa
   no quebrado. Nenhum refactor adjacente de carona.
8. **Prove.** Escreva o teste que falha reproduzindo o bug; veja ficar
   vermelho; conserte; veja ficar verde. Depois rode os testes de cada
   caminho de consumidor que você mapeou no passo 4 — verde ali é seu piso de
   zero regressão. Uma suíte que mocka exatamente a costura que falhou não
   prova nada.
9. **Verifique ao vivo.** Dirija o sistema real — requisições reais, banco
   real, logs reais. Nunca um script de carona que importa o código no seu
   próprio processo. Capture evidência de antes/depois.
10. **Aprenda.** Anote o sintoma, a sonda decisiva, a causa raiz e o
    antipadrão que a escondeu, para o próximo bug com essa cara sair mais
    barato.

## Construa o loop de reprodução ANTES de teorizar

Se você se pegar lendo código para montar teoria antes de existir um comando
capaz de ficar vermelho — pare. Sem comando capaz de vermelho, sem teoria. Um
sinal apertado de passa/falha que fica vermelho NESTE bug é o maior uplift de
debugging que existe. Gaste esforço desproporcional aqui.

Jeitos de construir um, mais ou menos em ordem: um teste que falha; um script
HTTP contra um servidor de dev; uma execução de CLI com uma entrada fixa,
comparada por diff com um snapshot sabidamente bom; um script de navegador
headless; um payload real capturado e reexecutado pelo caminho do código
isolado; um harness descartável que chama uma função; um loop de fuzz sobre
entradas aleatórias; um harness de bissecção para o bisect automático
funcionar; um loop diferencial (a mesma entrada pelas versões velha e nova,
diff das saídas).

Depois aperte: mais rápido (cacheie o setup, estreite o escopo), mais afiado
(asserte o sintoma específico, não "não quebrou"), determinístico (pine o
tempo, semeie o RNG, congele a rede). Um loop determinístico de dois segundos
é um superpoder.

Para bugs intermitentes, persiga uma taxa de reprodução maior, não uma repro
limpa: rode o gatilho 100 vezes em loop, adicione stress, estreite as janelas
de timing. Uma falha intermitente de 50% é debugável; uma de 1% não é.

Se você realmente não consegue construir um loop, pare e diga isso. Liste o
que tentou e peça ao seu humano acesso, um artefato capturado ou
instrumentação temporária. Não teorize sem loop. E se não existe costura que
replique o padrão real de chamada, essa ausência É um achado — sinalize a
lacuna de arquitetura depois que o conserto aterrissar.

## Antipadrões (como bugs difíceis ficam vivos)

- Concluir de uma nota ou comentário sem sonda.
- Consertar antes de reproduzir.
- Confiar numa suíte verde que mocka exatamente a costura que falha ao vivo.
- Verificação de carona — importar o código em vez de dirigir o sistema vivo.
- Mudar um botão de config sem mapear os consumidores de comparação exata que
  ele alimenta.
- Refactors largos de carona com um conserto.
- Dizer "todos / cada / nenhum" sem a checagem em três pontos.

## Funciona bem com

- [red-first](../red-first/SKILL.md) — commite o teste que falha antes do conserto.
- [sniper-testing](../sniper-testing/SKILL.md) — testes escopados enquanto itera.
- [seam-engineering](../seam-engineering/SKILL.md) — conserte a classe, não a instância.
- [repair-loop](../repair-loop/SKILL.md) — o ciclo completo de consertar e aterrissar.

> Crédito de scaffold: Matt Pocock, diagnosing-bugs (mattpocock/skills). A composição e as regras duras aqui são BACKS AIOS.
