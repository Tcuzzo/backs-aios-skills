# Web App Builds

Como construir um app ou site web com estrutura limpa e cadeia de suprimentos
defendida. A maior parte do estrago em builds web entra pelas dependências e
pelas fronteiras, não pela sua própria lógica — então a higiene é o play, não
uma nota de rodapé.

## Quando rodar

Ao construir ou estender qualquer app web, site, API ou repo entregável que
outra pessoa vai instalar e rodar.

## A cadeia

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — leia o pedido inteiro
   antes de escolher stack ou estrutura.
2. [understanding-gates](../skills/understanding-gates/SKILL.md) — desenhe a
   estrutura primeiro: um entrypoint documentado, um manifesto de dependências
   explícito e um lockfile commitado. Nada de arquivo brotando sem plano.
3. Higiene de dependências (faça ANTES de qualquer install):
   - Valide cada pacote referenciado contra o registro: ele existe, é mais
     antigo que o seu projeto, e o publicador tem histórico. Nomes de pacote
     alucinados por IA são isca de squatting — pesquisa medida mostra que cerca
     de 43% dos nomes alucinados se repetem em re-execuções idênticas
     (Spracklen et al. (2025), USENIX Security 25), então um atacante pode
     registrá-los antes de você.
   - Fixe tudo por hash a partir de um lockfile compilado (ex.: `pip install
     --require-hashes`, `npm ci --ignore-scripts`); recuse qualquer divergência
     de integridade.
   - Bloqueie por padrão os scripts de ciclo de vida do install. Um pacote que
     só funciona rodando um postinstall é bandeira vermelha.
   - Fixe cada dependência de workflow de CI num SHA de commit completo de 40
     caracteres, nunca numa tag de versão mutável.
   - Minimize a contagem: cada dependência é uma decisão revisada, não um
     reflexo. Prefira a biblioteca padrão ou a primitiva da plataforma.
4. [red-first](../skills/red-first/SKILL.md) — testes de contrato falhando para
   rotas, loaders e caminhos de validação, antes de construí-los.
5. Construa seguindo a doutrina abaixo. Para qualquer superfície de UI, rode o
   método de [design-taste](../skills/design-taste/SKILL.md) — tokens primeiro,
   acessibilidade como gate duro.
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — nunca mocke sua própria
   validação ou serialização: uma fronteira web mockada entrega um app que
   aceita o que deveria rejeitar.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — handlers de
   rota, loaders de dados e caminhos de formulário/validação passam antes do
   deploy; rode mutação sobre os predicados de validação e de auth até nada
   sobreviver. Um check de fronteira cuja comparação invertida ainda passa na
   suíte é uma porta aberta numa superfície pública.
8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — avaliação entre
   famílias antes do deploy.

## A doutrina (o que o build precisa cumprir)

- Nenhum segredo no código-fonte: leia as credenciais do ambiente ou de um cofre
  de segredos. Uma chave commitada reprova o build.
- O tratamento de saída conhece o contexto: queries parametrizadas para SQL, e o
  encoding correto antes de qualquer valor chegar ao shell, ao banco ou ao DOM.
  Nunca concatene input não confiável como string.
- Emita um SBOM legível por máquina — um inventário de software (ex.:
  CycloneDX) — para o destinatário poder auditar a árvore de dependências
  inteira.
- Mantenha o build reproduzível: versões da toolchain fixadas, install
  determinístico e nenhum acesso de rede EXTERNO durante os testes (serviços
  locais em loopback — bancos, fixtures — são normais e esperados).

## Gates duros

- Uma dependência não validada ou sem pin bloqueia o install.
- Um segredo commitado reprova o build.
- Mutantes sobreviventes em predicados de validação ou de auth bloqueiam o
  deploy.
- Acesso de rede externo durante os testes bloqueia o pouso (loopback pode).

## Funciona bem com

- [seam-engineering](../skills/seam-engineering/SKILL.md) — conserte uma falha de fronteira como classe
- [bounded-loops](../skills/bounded-loops/SKILL.md) — chamadas de saída cientes de rate limit
