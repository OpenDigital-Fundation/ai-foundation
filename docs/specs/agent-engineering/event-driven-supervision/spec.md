# Spec — Supervisão orientada a eventos

- **Domínio:** agent-engineering
- **Data:** 2026-11-13
- **Baseline:** candidata local 9a7c743 (main permanece 9813abf).
- **Fonte solicitada:** deepseek-ai/dsh-superagent-prototype, commit 8c32a9dc5d72c033816c6a8110b37f40cf94fba4, MIT; única LICENSE na raiz.

## Resultado

Ampliar agent-engineering/harness-design com referência procedural revisada sobre entrada de eventos, autorização limitada, posse de follow-ups e retomada sem repetição de efeitos. A fonte é protótipo de pesquisa e sua documentação não comprova comportamento em produção. Não criar um superagente paralelo, outra skill de equipes ou novo runtime.

## Aceite

- Fixar fonte/commit/licença; proveniência e aviso por recurso adaptado, com receita/override reaplicável.
- Separar evento/contexto de autorização: bots, CI, citações e conversas anexadas não ampliam escopo. O host, não o texto do modelo, aplica permissões, cancelamento e operações permanentes.
- Revalidar escopo/política antes de retomar e conferir receipts/estado externo antes de repetir efeitos após interrupção. Readiness, espera, falha e necessidade de pessoa são estados distintos.
- Não transferir o preset upstream que executa comandos sem aprovação, nem tratar diretório, wrapper ou bloqueio por nome de comando como sandbox. Não transferir seus defaults de merge ou de autorização de atores não listados.
- Inventariar as duas skills upstream e excluí-las como vendor-specific: dependem de orchestrator_read/ack/report e identidades/configuração DSH. Aproveitamento genérico vem da documentação, sem declarar que os wrappers foram incorporados.
- Busca interna deve localizar o dono ao consultar dsh superagent/DeepSeek e manter universo de 144 artefatos. Validar projeções, links, licença e quatro pacotes; casos de tarefa ficam preparados, sem execução de modelo.

## Fora de escopo

Executar SETUP.md, pnpm/scripts/runtime upstream, instalar DeepSeek Harness, conectar GitHub/Feishu, adicionar credenciais, alterar controles do host ou prometer autonomia/segurança de produção.
