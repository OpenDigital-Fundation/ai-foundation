# Revisão da organização do repositório

- **Data:** 2026-11-07
- **Responsável:** Codex, a pedido de Matheus Breguêz
- **Baseline:** `908ad6c` em `spec/foundation`
- **Escopo:** estrutura completa versionada, fronteiras entre diretórios, domínio/tipo, entradas de curadoria, dados, proveniência, geradores, documentação e verificações.

## Universo e evidências da baseline

A árvore versionada tinha **1.691 arquivos**, dos quais **1.469 em domains/**, distribuídos por **25 domínios**. A descoberta e o registro concordavam em **116 artefatos públicos**: 111 skills, um agente, um workflow e três referências de conhecimento. Fonte: `git ls-files`, `tools.validate.repo.discover`, `catalog/catalog.yaml` e `catalog/domains.yaml` no commit acima.

O lock registrava **27 fontes**. O inventário tinha **1.378 observações** e **1.369 chaves distintas** de fonte/tipo/nome; nove observações adicionais repetiam uma chave, não uma decisão. As decisões cobriam as 1.369 chaves: **909 incorporadas** por `supersedes` e **460 excluídas**. Fonte: lock, inventário, catálogo e exclusões da baseline. Não usar a contagem antiga de 21 fontes e 1.118 itens do README como estado atual.

A baseline passou em **131 testes de tooling** e no validador com **zero erros e zero avisos**. Esses checks não distinguiam entradas de curadoria de saídas intermediárias nem impediam SKILL.md aninhado em referências.

## Achados confirmados e tratamento

| Achado | Evidência | Mudança |
|---|---|---|
| Entradas e resultados intermediários misturados | 29 YAMLs em `catalog/decisions/`, incluindo sete receitas agrupadas por lotes e domínios independentes; mapeamentos de proveniência, pacotes de linguagem e decisões no mesmo namespace | 25 manifestos editoriais por domínio em `catalog/curation/domains/`; sem decisões intermediárias geradas |
| Curadoria organizada pela história de importação | Receitas `business`, `gaps`, `data-platform`, `knowledge-work`; uma receita podia misturar seis domínios | Metadados, receitas e imports passam a ter o mesmo responsável do plugin |
| Dados operacionais em diretórios de outra responsabilidade | Inventário dentro da spec de source-curation; hashes ao lado de módulos Python | `catalog/inventory/artifacts.csv` e `restricted-hashes.txt`, com consumidores atualizados |
| Entradas públicas aparentes dentro de referências | 85 arquivos references/**/SKILL.md que o catálogo não descobria como capacidades | Guias passam a README.md; links, proveniência, exceções e geradores acompanham a mudança |
| Convenção própria para assets tipográficos | 162 arquivos nas duas árvores canvas-fonts | Assets movidos para assets/fonts; binários preservados byte a byte |
| Documentos divergiam da implementação | AGENTS dizia não existir tooling; README tinha contagens antigas; ROADMAP duplicava estados e citava nomes já substituídos | Runbook atual, README em português, ROADMAP restrito a sequência e dependências; estado por feature em tasks.md |
| Índices dificultavam seguir uma capacidade | IDs sem link direto em catálogo e facetas, sem acesso à fonte editorial do domínio | Sumários, links canônicos e origem editorial; facetas recolhíveis |
| Rebuild dependia de ordem e escrevia antes de terminar a leitura | Rebuild zerava projeções e fazia upsert por arquivo histórico | Validar e serializar fontes completas antes de escrever projeções; entradas duplicadas são recusadas |

## Revisão dos domínios

A estrutura pública por domínio continua sendo o contrato de instalação. A revisão conferiu cobertura do catálogo, arquivos públicos, metadados, entradas de curadoria e vínculo com o plugin para **todos os 25 domínios**, sem introduzir uma taxonomia adicional de grupos. As 66 receitas e os 11 pacotes gerados ficam no manifesto do próprio domínio. Os 39 registros restantes representam conteúdo sem receita de reconstrução automática, incluindo conteúdo portado e autoral.

| Domínio | Artefatos públicos | Receitas | Pacotes de linguagem | Fonte editorial |
|---|---|---|---|---|
| [accessibility](../../domains/accessibility/README.md) | 4 | 4 | 0 | [Manifesto](../../catalog/curation/domains/accessibility.yaml) |
| [agent-engineering](../../domains/agent-engineering/README.md) | 11 | 8 | 0 | [Manifesto](../../catalog/curation/domains/agent-engineering.yaml) |
| [ai-engineering](../../domains/ai-engineering/README.md) | 5 | 5 | 0 | [Manifesto](../../catalog/curation/domains/ai-engineering.yaml) |
| [architecture](../../domains/architecture/README.md) | 7 | 2 | 0 | [Manifesto](../../catalog/curation/domains/architecture.yaml) |
| [brand](../../domains/brand/README.md) | 2 | 2 | 0 | [Manifesto](../../catalog/curation/domains/brand.yaml) |
| [code-quality](../../domains/code-quality/README.md) | 6 | 1 | 0 | [Manifesto](../../catalog/curation/domains/code-quality.yaml) |
| [creative-media](../../domains/creative-media/README.md) | 6 | 6 | 0 | [Manifesto](../../catalog/curation/domains/creative-media.yaml) |
| [data](../../domains/data/README.md) | 3 | 3 | 0 | [Manifesto](../../catalog/curation/domains/data.yaml) |
| [debugging](../../domains/debugging/README.md) | 2 | 1 | 0 | [Manifesto](../../catalog/curation/domains/debugging.yaml) |
| [documents](../../domains/documents/README.md) | 4 | 4 | 0 | [Manifesto](../../catalog/curation/domains/documents.yaml) |
| [finance](../../domains/finance/README.md) | 3 | 3 | 0 | [Manifesto](../../catalog/curation/domains/finance.yaml) |
| [languages](../../domains/languages/README.md) | 13 | 1 | 11 | [Manifesto](../../catalog/curation/domains/languages.yaml) |
| [legal-compliance](../../domains/legal-compliance/README.md) | 2 | 2 | 0 | [Manifesto](../../catalog/curation/domains/legal-compliance.yaml) |
| [marketing](../../domains/marketing/README.md) | 5 | 5 | 0 | [Manifesto](../../catalog/curation/domains/marketing.yaml) |
| [operations](../../domains/operations/README.md) | 3 | 3 | 0 | [Manifesto](../../catalog/curation/domains/operations.yaml) |
| [platform](../../domains/platform/README.md) | 5 | 5 | 0 | [Manifesto](../../catalog/curation/domains/platform.yaml) |
| [principles](../../domains/principles/README.md) | 1 | 0 | 0 | [Manifesto](../../catalog/curation/domains/principles.yaml) |
| [product](../../domains/product/README.md) | 1 | 1 | 0 | [Manifesto](../../catalog/curation/domains/product.yaml) |
| [research](../../domains/research/README.md) | 3 | 3 | 0 | [Manifesto](../../catalog/curation/domains/research.yaml) |
| [sales](../../domains/sales/README.md) | 3 | 3 | 0 | [Manifesto](../../catalog/curation/domains/sales.yaml) |
| [security](../../domains/security/README.md) | 5 | 0 | 0 | [Manifesto](../../catalog/curation/domains/security.yaml) |
| [testing](../../domains/testing/README.md) | 4 | 2 | 0 | [Manifesto](../../catalog/curation/domains/testing.yaml) |
| [ui](../../domains/ui/README.md) | 4 | 2 | 0 | [Manifesto](../../catalog/curation/domains/ui.yaml) |
| [ux](../../domains/ux/README.md) | 2 | 0 | 0 | [Manifesto](../../catalog/curation/domains/ux.yaml) |
| [workflow](../../domains/workflow/README.md) | 12 | 0 | 0 | [Manifesto](../../catalog/curation/domains/workflow.yaml) |

## Duplicação de arquivos e limites de interpretação

A busca por hashes em arquivos maiores que 1.000 bytes identificou **82 grupos de cópias idênticas**, com **5.610.134 bytes** repetidos além da primeira ocorrência de cada grupo. Essa é uma medição de bytes da baseline, não prova de capacidade duplicada. A maior parte é de fontes tipográficas presentes em plugins instaláveis separadamente. Os assets foram reorganizados sem criar dependência entre plugins ou removê-los apenas por igualdade de hash.

Agentes privados de `codebase-audit/agents/` continuam ligados àquela skill. O agente público `code-quality/agents/code-reviewer.md` mantém seu registro. Scripts, dados e testes empacotados permanecem com a capacidade que os usa; transferi-los indiscriminadamente para tools/ quebraria instalação e contexto de execução.

## Critérios de preservação

- Registro público e exclusões comparados semanticamente com 908ad6c: mesmos 116 IDs, tipos, estados, responsáveis e decisões de origem.
- Profiles, lock de fontes, facetas e manifesto de marketplace conservam seus contratos.
- Os 162 arquivos de fontes e licenças movidos conservam bytes; origens, commits, licenças e caminhos upstream de todos os registros de proveniência foram conferidos após o remapeamento de destinos.
- Os 29 arquivos históricos de decisão têm cópia e hashes em diretório de revisão fora do checkout; não são uma segunda fonte de manutenção. O Git também mantém a baseline.

## Verificação da entrega

A evidência final de execução fica no tasks.md das três specs desta revisão. Os novos testes verificam preservação do registro, idempotência, rejeição de manifestos inválidos sem truncar as saídas, links e completude dos índices, normalização de assets e reconstrução com fontes sintéticas. A suíte existente continua cobrindo validadores e projeções dos adaptadores.

Não foram executados código upstream, avaliações pagas, instalação em agentes reais, push, merge ou publicação. Os 116 registros continuam experimentais; somente `principles/coding-discipline` já possui diretório de avaliações na baseline. Esta revisão organiza e verifica a estrutura; não certifica a qualidade semântica de todo texto importado ou o benefício operacional de cada capacidade. Essas validações são trabalho distinto da organização do repositório.

## Contratos e sequência

- [Organização da curadoria](../specs/foundation/curation-layout/spec.md)
- [Arquivos auxiliares dos artefatos](../specs/foundation/artifact-support-layout/spec.md)
- [Documentação e manutenção](../specs/foundation/repository-guide/spec.md)
- [Contrato operacional atual](../architecture/repository-layout.md)
- [ADR de manifestos por domínio](../adr/foundation/curation-manifests-by-domain.md)
- [ADR de referências e assets](../adr/foundation/reference-and-asset-layout.md)

## Revisão adicional antes da integração

Por solicitação do usuário, a entrega foi revisada novamente antes da integração local em `spec/foundation`. Foram corrigidos três casos no fluxo de curadoria:

1. Conferir todas as fontes selecionadas antes de remover qualquer saída gerada. Testes com uma skill preexistente comprovam sua preservação quando falta uma fonte, tanto no bundle quanto no pacote de linguagem.
2. Recusar itens utilizados por uma receita que não estejam declarados no `supersedes` do manifesto dono. A reconstrução não pode incorporar silenciosamente um item de outra capacidade.
3. Recusar uma decisão upstream repetida, inclusive incorporada e excluída simultaneamente, antes de escrever as projeções.

A revisão acrescentou cinco casos à suíte: **152 testes passaram** na preparação, com **zero erros e zero avisos** no validador. Registro e exclusões continuam semanticamente iguais à baseline; 32 arquivos gerados foram reconstruídos sem diferença de bytes. Os testes de geração usam fontes sintéticas, sem execução de código upstream ou avaliações pagas.

O destino autorizado para integração é a branch local `spec/foundation`, por avanço direto ao commit assinado da reorganização. Registro da assinatura e da integração: histórico Git e estado do Orca. O remoto não faz parte desta operação.
