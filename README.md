# OpenDigital AI Foundation

Coletânea curada de capacidades para agentes de IA: skills, agentes, workflows, regras, hooks, configurações MCP e referências. Cada capacidade tem um domínio dono e um caminho canônico. Cada domínio é um plugin instalável.

## Encontrar e usar

| Preciso de… | Comece por |
|---|---|
| Uma capacidade ou domínio | [Catálogo](docs/CATALOG.md) — artefatos, finalidade e acesso direto |
| Buscar por tecnologia, conhecimento, capacidade ou setor | [Facetas](docs/FACETS.md) |
| Um conjunto para meu trabalho | [Perfis de instalação](profiles/) |
| Conferir de onde veio um conteúdo | [Fontes e licenças](docs/SOURCES.md) |
| Alterar ou acrescentar conteúdo | [Guia de manutenção](docs/architecture/repository-layout.md) e [AGENTS.md](AGENTS.md) |

## Instalar

No Claude Code, adicione o marketplace e escolha o domínio:

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install workflow@opendigital-ai-foundation
```

A instalação de um domínio inclui todas as suas capacidades. Perfis escolhem vários domínios; não são plugins novos nem prometem instalação seletiva de arquivos dentro de um plugin. Consulte a lista efetiva com `uv run python -m tools.build profile fullstack-web`.

Os adaptadores para Agent Skills, Cursor, Gemini e OpenCode são gerados por `uv run python -m tools.build adapters` em `dist/`. A geração valida o formato; uso num agente real exige validação própria.

## Releases e pacotes individuais

A distribuição usa a versão em [VERSION](VERSION). Cada release contém um ZIP completo, bundles de Claude Code, Codex, Cursor, Gemini CLI, OpenCode e GitHub Copilot, o formato neutro Agent Skills e um ZIP por skill/workflow para cada IA. Os demais artefatos e os plugins nativos por domínio estão no pacote completo. As versões dos plugins continuam independentes.

Os nomes `bundle-<ia>` instalam a seleção completa; `skill-<ia>-<domínio>--<nome>` contêm uma única entrada pública e seus recursos. Leia `INSTALL.md` antes de copiar arquivos, incluindo diretórios ocultos. A distribuição mantém licenças e proveniência; não ativa hooks nem instala componentes globais.

Para construir a partir de um commit limpo, use um diretório de saída novo:

```sh
uv run python -m tools.build release dist/release
python dist/release/verify-release.py dist/release
```

O manifesto relaciona IDs, status, origem, IA, arquivo e SHA-256; `SHA256SUMS` permite conferir os downloads. O verificador offline exige o conjunto completo de assets baixados e não extrai nem executa os pacotes. Os testes validam empacotamento; as capacidades permanecem experimentais até avaliação de gatilho e tarefa em agentes reais.

## Organização do repositório

```text
domains/             conteúdo instalável, por domínio e tipo
profiles/            seleções entre domínios
evals/routing/       casos de roteamento entre capacidades
catalog/
  curation/          entradas editoriais, um manifesto por domínio
  inventory/         inventário upstream e hashes de conteúdo restrito
  overrides/         ajustes locais reaplicados ao conteúdo gerado
  schema/            contratos dos arquivos de dados
  taxonomy/          vocabulários de facetas
  catalog.yaml       registro público gerado
  exclusions.yaml    exclusões públicas geradas
  sources.lock.yaml  fontes fixadas, licenças e política de cópia
tools/               inventário, curadoria, geração, validação e avaliações
docs/                guias, specs, decisões e evidências de revisão
```

O [contrato completo de diretórios](docs/architecture/repository-layout.md) explica o que editar e o que regenerar. O [ROADMAP](docs/specs/ROADMAP.md) contém a ordem e as dependências das specs legadas e `docs/<domínio>/specs/ROADMAP.md` as do layout novo (ver [ADR](docs/foundation/adr/2026-11-21-docs-layout-domain-first.md)); o andamento de cada uma fica no seu `tasks.md`.

## Verificar uma contribuição

Com as dependências locais disponíveis:

```sh
uv run python -m tools.catalog rebuild
uv run python -m tools.build
uv run python -m tools.build docs
uv run pytest -q
uv run python -m tools.validate
```

Arquivos gerados devem continuar iguais depois da reconstrução. Os artefatos permanecem `experimental` até passarem pelas avaliações de gatilho e tarefa. Validação estática e testes de tooling não certificam o funcionamento de cada script importado nem o benefício operacional de uma capacidade.

Somente conteúdo de licença permissiva pode ser copiado; cada arquivo derivado tem origem no `PROVENANCE.yaml` do domínio. Veja os [avisos de terceiros](THIRD_PARTY_NOTICES.md) e as [regras de contribuição](AGENTS.md).
