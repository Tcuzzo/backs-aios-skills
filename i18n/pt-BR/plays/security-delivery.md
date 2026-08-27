# Play: Security & Delivery

O gate de entrega para qualquer coisa que um cliente ou outra máquina vai rodar.
Seguro por construção: o harness impõe as regras; nunca se confia que o modelo
vai lembrar delas.

## Quando rodar

- Um repo, agente ou app está prestes a ser entregue, publicado ou implantado.
- Um agente com ferramentas toca conteúdo não confiável — páginas web, issues,
  e-mail, input de fora.
- Você está adicionando dependências ou CI a algo que vai ser entregue.

## A cadeia

1. Gate de segredos — rode um scanner de segredos em modo só-verificados (ele
   checa cada credencial candidata contra o provedor ao vivo). Uma credencial
   confirmada viva reprova o build. Sem exceção.
2. Bloqueio de egress — negue a saída por padrão; roteie tudo por um proxy com
   allowlist de hostnames puros. Canonicalize e valide o hostname ANTES de
   comparar: rejeite null bytes, truques de percent-encoding e CRLF. O bypass de
   null byte `evil-host\x00.trusted.com` é real e já chegou em produção.
3. Quebre a trinca letal — arquitete todo caminho de execução para que pelo
   menos UM destes sempre falte: acesso a dados privados, exposição a conteúdo
   não confiável, comunicação externa. Não dá para bloquear prompt injection por
   completo; dá para torná-la incapaz de roubar.
4. Rastreamento de contaminação — ingerir conteúdo não confiável marca a sessão
   como contaminada. Enquanto contaminada, trave por política, no harness, toda
   ação capaz de exfiltrar (HTTP de saída, e-mail, criação de PR) — nunca deixe
   isso para o julgamento do modelo.
5. Cadeia de suprimentos — fixe cada dependência por hash e bloqueie scripts de
   instalação. Fixe cada action de CI num hash de commit completo, não numa tag.
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — código de
   segurança carrega a régua mais estrita. Rode teste de mutação sobre cada
   detector, parser e predicado de política, e leve os mutantes sobreviventes a
   zero. Uma comparação invertida dentro de um check de ameaça, com a suíte
   ainda passando, É a vulnerabilidade.
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — mocke SÓ a rede de
   saída, nunca o payload nem o parser sob teste: um detector mockado é um
   sensor cego em produção.
8. Sandbox antes de entregar — rode o artefato construído num sandbox efêmero,
   com toda a saída bloqueada e um hard-kill de recursos armado. Observe o que
   ele escreve e o que tenta chamar.
9. Proveniência — emita um SBOM (inventário de software), mais proveniência
   assinada se você tiver. E mesmo assim revise o código-fonte: proveniência
   assina fielmente código malicioso também.

## Proteções permanentes durante qualquer build

- Negue escrita em caminhos sensíveis: arquivos de inicialização do shell,
  config e hooks do git, config de DNS, chaves SSH.
- Ferramentas com privilégio mínimo. Um passo de confirmação fica reservado SÓ
  para operações genuinamente destrutivas ou irreversíveis — perda de dados,
  gasto, uma ação externa que não se desfaz. Nunca trave uma capacidade benigna,
  e nunca trave o seu humano.

## Gates duros — qualquer um reprova o play

- Uma credencial confirmada viva em qualquer lugar da entrega ou do histórico
  dela.
- Qualquer caminho de execução segurando as três pernas da trinca ao mesmo
  tempo.
- Uma dependência sem pin, um script de instalação, ou uma action de CI fixada
  por tag.
- Um mutante sobrevivente num detector, parser ou predicado de política.
- O artefato nunca ter rodado num sandbox antes da entrega.

**Weight:** disciplina de construção em sua maior parte free mais passadas light de scanner e sandbox; o passo heavy é mutação sobre cada detector e predicado de política — ele se paga em qualquer coisa que um cliente ou outra máquina vai rodar.
