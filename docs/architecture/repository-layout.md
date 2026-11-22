# Organização e manutenção do repositório

O repositório separa três responsabilidades: **conteúdo instalável** em `domains/`; **entradas e projeções de dados** em `catalog/`; **código de manutenção** em `tools/`. Documentação registra contratos e decisões, sem servir de depósito para dados operacionais.

## Responsabilidade de cada diretório

| Caminho | Responsabilidade | Como manter |
|---|---|---|
| `domains/<domain>/` | Plugin público, suas capacidades e arquivos auxiliares | Seguir a spec e o manifesto editorial do domínio |
| `profiles/` | Seleções de artefatos entre domínios | Editar os padrões de IDs; conferir os plugins efetivamente instalados |
| `evals/routing/` | Casos que escolhem entre capacidades públicas | Editar casos e expectativas; execução com modelo pode gerar custo |
| `catalog/curation/domains/` | Um manifesto editorial por domínio | Editar metadados, receitas e mapeamentos aqui |
| `catalog/curation/exclusions.yaml` | Decisões explícitas de não incorporação | Editar cada chave upstream e seu motivo |
| `catalog/inventory/` | Dados de levantamento upstream | Gerar a partir das fontes fixadas |
| `catalog/overrides/` | Ajustes locais de arquivos reconstruídos | Espelhar `<domain>/<skill>/<path>`; registrar proveniência da alteração |
| `catalog/schema/` | Formatos de dados aceitos | Alterar o contrato e seus validadores juntos |
| `catalog/taxonomy/` | Termos e hierarquias das facetas | Editar vocabulários; novos termos mantêm IDs estáveis |
| `tools/inventory/` | Leitura de fontes, inventário e relatório de mudanças | Código Python e testes do levantamento |
| `tools/curation/` | Montagem e adaptação de conteúdo | Código Python e testes de curadoria |
| `tools/build/` | Marketplace, documentação, profiles e adaptadores | Geradores e testes de distribuição |
| `tools/validate/` | Checagens estáticas do repositório | Validadores e testes de regressão |
| `tools/evals/` | Execução das avaliações de capacidades | Código do runner; resultados locais não são conteúdo publicado |
| `docs/<domínio>/specs/` | Requisitos, plano e tarefas de cada feature do domínio, mais o `ROADMAP.md` | Spec → plano → implementação → revisão |
| `docs/<domínio>/adr/` | Uma decisão arquitetural por documento, `AAAA-MM-DD-<decisão>.md` | Formato contexto, decisão, status e consequências |
| `docs/transversal/` | Specs e ADRs que atravessam domínios, mesma estrutura | Dono da spec contratual; os demais citam o caminho |
| `docs/specs/`, `docs/adr/` | Layout legado, aceito durante a transição | Não criar novos; migração em lote em issue própria |
| `docs/architecture/` | Contrato operacional atual | Atualizar junto das mudanças de estrutura |
| `docs/reviews/` | Evidências datadas de revisão | Identificar baseline, universo, achados e limites |
| `.claude-plugin/` | Índice público do marketplace | Gerar a partir dos plugins de domínio |
| `.github/` | Integração contínua, sync e distribuição | Versionar workflows e permissões mínimas |

Na raiz, `AGENTS.md` governa o trabalho; `CLAUDE.md` o referencia; `README.md` orienta o usuário. `pyproject.toml` e `uv.lock` definem o ambiente local. `LICENSE` e `THIRD_PARTY_NOTICES.md` registram licenças e atribuições. `.gitignore` separa ambientes, caches, resultados e `dist/` do conteúdo versionado. Pastas pessoais locais, como `.claude/`, não fazem parte do layout público.

## Qual arquivo é a fonte

| Quero mudar | Editar | Reconstruir |
|---|---|---|
| Metadados, estado ou origens absorvidas de uma capacidade | `catalog/curation/domains/<domain>.yaml` | `python -m tools.catalog rebuild` |
| Procedimento de uma skill com `recipe` | Campo `recipe` no manifesto | `python -m tools.curation <sources-dir> --domain <domain>` |
| Referências de um pacote de linguagem | Campo `language_pack` no manifesto de languages | Mesmo comando para `--domain languages` |
| Arquivo de uma skill gerada | `catalog/overrides/<domain>/<skill>/<path>` | Reconstruir o domínio para reaplicar o ajuste |
| Conteúdo autoral ou portado sem receita | Caminho canônico em `domains/` | Atualizar o manifesto e a proveniência quando aplicável |
| Exclusões | `catalog/curation/exclusions.yaml` | `python -m tools.catalog rebuild` |
| Proveniência de conteúdo portado | `imports` no manifesto e origens em `PROVENANCE.yaml` | `python -m tools.curation.provenance <sources-dir> <manifest.yaml>` recalcula correspondências; revisar o resultado |
| Facetas de uma capacidade | `catalog/facets.yaml`; vocabulários em `catalog/taxonomy/` | `python -m tools.build docs` |
| Índices de conteúdo | `tools/build/docs.py` e dados de origem | `python -m tools.build docs` |
| Plugins de domínio | `.claude-plugin/plugin.json` dentro do domínio | `python -m tools.build` para atualizar o marketplace |

`catalog/catalog.yaml` e `catalog/exclusions.yaml` são **projeções para leitura**, não entradas editoriais. O mesmo vale para `docs/CATALOG.md`, `docs/FACETS.md`, `docs/SOURCES.md` e `domains/*/README.md`. Cabeçalhos identificam o gerador. O manifesto descreve como construir; o pacote em `domains/` é a unidade distribuída. Manter ambos versionados permite instalar sem baixar as fontes originais.

## Fluxo dos dados

```text
sources.lock.yaml → fontes fixadas → catalog/inventory/
                                      ↓
manifestos + exclusões + overrides → curadoria → domains/ + PROVENANCE.yaml
               ↓                                  ↓
      catalog.yaml + exclusions.yaml       marketplace e adaptadores
               └──────────────────────────→ índices de documentação
```

O inventário registra o que foi encontrado, sem executar o código das fontes. Os manifestos registram a decisão editorial. `supersedes` identifica itens incorporados; exclusões identificam itens recusados. O validador cobra que cada chave inventariada tenha uma decisão única. Receita não deve escrever metadados concorrentes nem arquivos intermediários de decisão. Antes de reconstruir, os geradores conferem todas as fontes e o pertencimento dos itens ao `supersedes` do manifesto. Fontes ausentes, tópicos inválidos e caminhos de saída que escapam do artefato são recusados antes de substituir o conteúdo.

## Estrutura interna de uma capacidade

```text
domains/<domain>/
  .claude-plugin/plugin.json
  skills/<capability>/
    SKILL.md             entrada pública e gatilho
    references/          material carregado sob demanda
      <topic>/README.md  guia importado como referência
    scripts/             ferramentas auxiliares da capacidade
    assets/              arquivos utilizados na saída; fontes em assets/fonts/
    data/                bases consultadas por scripts
    templates/           modelos privados usados pela capacidade
    agents/              contextos privados invocados somente por esta capacidade
    evals/               casos de gatilho e tarefa da capacidade
  agents/<name>.md       agente público com contexto isolado
  workflows/<name>/     orquestração pública; entrada SKILL.md
  knowledge/            referência compartilhada dentro do domínio
  PROVENANCE.yaml       caminho local e origem upstream por arquivo
```

Os demais tipos públicos (`prompts`, `rules`, `hooks`, `mcps`, `templates`) seguem o [contrato de tipos](../specs/foundation/catalog-governance/spec.md). Só criar diretórios quando houver conteúdo. Arquivos auxiliares pertencem ao artefato que os usa; não ganham ID público por estarem num subdiretório chamado `agents` ou por terem sido skills no upstream. `references/` usa README.md para não simular entradas públicas adicionais.

Cada plugin e cada projeção de skill precisa carregar seus próprios arquivos auxiliares. Não criar caminhos relativos entre plugins, symlinks para uma biblioteca central de fontes nem deduplicar assets apenas por hash. Cópia byte a byte entre pacotes independentes pode ser necessária; duplicidade de capacidade é uma decisão semântica diferente.

## Busca interna de capacidades

`python -m tools.catalog find "design instrucional" --json` consulta os metadados locais sem rede ou instalação. Filtros `--domain`, `--type` e `--limit` reduzem o resultado. A skill skill-discovery inclui o mesmo mecanismo em scripts/find.py para clientes exportados.

O snapshot privado `domains/agent-engineering/skills/skill-discovery/assets/catalog-index.json` é gerado por `python -m tools.build docs` a partir de catálogo, facetas/vocabulários e termos autorais em assets/search-terms.json da skill. Não editar o índice; o validador recusa projeção desatualizada. A busca é lexical e informa disponibilidade no catálogo, sem presumir instalação no cliente.

## Antes de uma contribuição

1. Consultar o catálogo e a spec do domínio dono; melhorar uma capacidade existente quando ela já cobre a intenção.
2. Criar ou atualizar a spec, plano e tarefas antes de mudar arquitetura ou comportamento.
3. Escolher o ponto de edição pela tabela acima. Conteúdo importado mantém origem, commit, licença e modificação.
4. Reconstruir apenas o necessário, depois rodar testes, validador e os geradores de índices.
5. Revisar o diff e as limitações de validação. Commit assinado; push, PR, merge e publicação seguem a autorização do responsável.

Regerar curadoria substitui diretórios produzidos por receita. Conferir alterações locais e overrides antes de executar. A leitura de fontes não exige executar scripts delas; testes de código upstream e execução em agentes reais são verificações distintas. Avaliações pagas não fazem parte da checagem estática.

## Specs e decisões

O [ROADMAP](../specs/ROADMAP.md) lista sequência e dependências das specs legadas; no layout novo cada domínio tem o seu em `docs/<domain>/specs/ROADMAP.md` (ex.: [foundation](../foundation/specs/ROADMAP.md)). Cada `docs/<domain>/specs/<feature>/` (ou, no legado, `docs/specs/<domain>/<feature>/`) contém somente `spec.md`, `plan.md`, `tasks.md` e, quando necessário, evidências de design da própria feature. Inventários que mudam com a operação ficam em `catalog/inventory/`. O estado de execução fica no `tasks.md` de cada feature.

`python -m tools.validate` confere o layout novo (nome sem número, `spec.md`/`plan.md`/`tasks.md`, ADR datado, domínio conhecido) e recusa a mesma feature nos dois layouts. Ver o [ADR do layout](../foundation/adr/2026-11-21-docs-layout-domain-first.md). `docs/architecture/` serve ao contrato do repositório e ao domínio `architecture`; só `specs/` e `adr/` dentro dela seguem o layout por domínio.

Novos domínios exigem decisão arquitetural e uma frase de fronteira. Não resolver sobreposição criando agrupamentos adicionais ou copiando a mesma capacidade para dois plugins. [Facetas](../FACETS.md) e [profiles](../../profiles/) atendem busca transversal e instalação conjunta sem mudar o dono da capacidade.
