# Plano — Curadoria das fontes

## Arquitetura

```
catalog/sources.lock.yaml
tools/inventory/            # gera inventory.csv a partir dos clones fixados
  fetch.sh                  # clone raso no commit do lock, em diretório temporário isolado
  inventory.py              # extrai frontmatter (name, description), tipo, licença
  classify.py               # domínio sugerido por palavras-chave
domains/<d>/PROVENANCE.yaml
THIRD_PARTY_NOTICES.md
```

Os clones nunca entram no repositório; ficam em diretório temporário e são lidos como dados (scripts do upstream não são executados).

## Contratos

```yaml
# catalog/sources.lock.yaml
version: 1
sources:
  - id: obra/superpowers
    url: https://github.com/obra/superpowers
    commit: 22f0b46
    license: MIT
    policy: merge        # merge | reference
  - id: SecurityStandards/agent-pentester
    url: https://github.com/SecurityStandards/agent-pentester
    commit: 2468b67
    license: AGPL-3.0
    policy: reference
```

```yaml
# domains/testing/PROVENANCE.yaml
version: 1
files:
  - path: skills/test-driven-development/SKILL.md
    derived_from:
      - source: obra/superpowers
        commit: 22f0b46
        path: skills/test-driven-development/SKILL.md
        license: MIT
        modification: base        # base | merged-section | adapted | rewritten
      - source: mattpocock/skills
        commit: 4ae2317
        path: skills/engineering/tdd/SKILL.md
        license: MIT
        modification: merged-section
```

## Decisões

- Inventário reproduzível a partir do lock; o CSV versionado é o snapshot revisável.
- A decisão por item (R2) fica nos manifestos e exclusões de `catalog/curation/`; catálogo e exclusões públicos são projeções. O inventário em `catalog/inventory/` registra observações, não decisões.
- O classificador é deliberadamente simples; o trabalho de julgamento acontece na spec de cada domínio.

## Riscos

- Upstream renomeia artefatos: a chave `source:kind:name` quebra. Mitigação: o sync (spec `distribution`, tarefa de atualização) reporta chaves órfãs.
- `andrej-karpathy-skills` declara MIT só no README. Mitigação: registrar no lock com a observação e citar a fonte no NOTICE.
