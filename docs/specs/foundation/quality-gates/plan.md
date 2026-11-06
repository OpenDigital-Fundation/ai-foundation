# Plano — Portões de qualidade

## Arquitetura

```
tools/validate/              # Python 3.12, sem dependência de rede
  schema.py                  # R1, R2 (jsonschema)
  names.py                   # R3
  similarity.py              # R4 (scikit-learn TF-IDF)
  license.py                 # R5 (hashes das fontes reference, gerados no fetch)
  hygiene.py                 # R6, R7
tools/evals/
  run_triggers.py            # R8, R11: roda o harness em modo não interativo e checa qual skill disparou
  run_tasks.py               # R9, R10
.github/workflows/validate.yml   # todo PR
.github/workflows/evals.yml      # label run-evals, promoção a stable, agendado semanal
```

## Contratos

```yaml
# domains/testing/skills/test-driven-development/evals/triggers.yaml
should_trigger:
  - "add a discount field to the checkout and make sure it's covered"
should_not_trigger:
  - "why is this test flaky?"          # pertence a debugging
```

```yaml
# domains/testing/skills/test-driven-development/evals/tasks.yaml
- id: red-first
  prompt: "Implement slugify() in src/text.ts"
  fixture: fixtures/ts-empty
  check: scripts/check_test_written_before_impl.sh
```

## Decisões

- Similaridade lexical primeiro (determinística, barata, sem chave de API); embeddings como modo opcional para auditoria.
- Os evals de gatilho usam o Claude Code em modo não interativo como harness de referência; adaptadores de outros harnesses entram quando houver demanda (spec `distribution`).
- Método de eval inspirado no `skill-creator` da Anthropic (Apache-2.0) e no `writing-skills` do superpowers (MIT).

## Riscos

- Limiar 0,80 errado gera falso positivo/negativo. Mitigação: calibrar com o próprio inventário (pares sabidamente duplicados × distintos) antes de ativar como bloqueante.
- Custo de evals. Mitigação: só sob demanda e na promoção.
