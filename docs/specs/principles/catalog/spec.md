# Spec — Catálogo do domínio `principles`

- **Domínio:** principles
- **Status:** em implementação
- **Fronteira:** comportamento sempre ativo do agente ao programar: simplicidade, mudança cirúrgica, explicitar suposições, critérios verificáveis.

## Problema

Quatro fontes dizem a mesma coisa de formas diferentes e competem pelo mesmo gatilho ("qualquer tarefa de código"): `karpathy-guidelines`, `ponytail`, o agent *Minimal Change Engineer* e os rules `common/*` do ECC. Instalar mais de um gera instruções redundantes e, no caso do ECC, contraditórias (o ECC impõe imutabilidade e "muitos arquivos pequenos"; os demais mandam seguir o estilo existente).

## Matriz de curadoria

| Upstream | Decisão | Destino | Motivo |
|---|---|---|---|
| `DietrichGebert/ponytail:skill:ponytail` | merge (base) | `principles/coding-discipline` | Melhor procedimento: escada de decisão da menor mudança completa, lista "nunca corte", convenção `shortcut:` |
| `multica-ai/andrej-karpathy-skills:skill:karpathy-guidelines` | merge | `principles/coding-discipline` | Pensar antes de codar, critérios de sucesso verificáveis |
| `msitarzewski/agency-agents:agent:Minimal Change Engineer` | merge | `principles/coding-discipline` | Revisão linha a linha do diff; persona sem necessidade de contexto isolado |
| `affaan-m/ECC:rule:coding-style`, `patterns` | exclude (low-quality) | — | Contradiz "seguir o estilo existente"; regras absolutas sem contexto |
| `affaan-m/ECC:rule:performance` | exclude (low-quality) | — | Recomendações de modelo datadas; contexto pertence a `agent-engineering` |
| `affaan-m/ECC:rule:README` | exclude (source-internal) | — | Documentação da própria fonte |
| `ponytail-help`, `ponytail-gain` | exclude (source-internal) | — | Ajuda e marketing do próprio produto |
| `ponytail-review`, `ponytail-audit`, `ponytail-debt` | decidido em `code-quality` | — | Fora da fronteira deste domínio |

Rules `common/agents`, `code-review`, `development-workflow`, `git-workflow`, `hooks`, `security`, `testing` do ECC são decididos nos domínios donos.

## Requisitos

- **R1.** Uma única skill `coding-discipline` que dispara em qualquer tarefa de escrever, corrigir ou refatorar código.
- **R2.** Sem modos/níveis com estado (o `ponytail` usa hooks de rastreamento de modo): o comportamento é um só; o usuário pode pedir explicitamente uma versão maior.
- **R3.** Não pode contradizer `workflow` nem `testing`: exige teste para lógica não trivial, alinhado com TDD.
- **R4.** ≤ 150 linhas.

## Critérios de aceite

1. Validador sem erros; nenhuma outra skill do catálogo com similaridade ≥ 0,60 com ela.
2. `evals/triggers.yaml` com casos de disparo e de não disparo (inclui pedidos de review e de debugging, que pertencem a outros domínios).
