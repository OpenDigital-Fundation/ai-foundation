# Spec — Portões de qualidade

- **Domínio:** foundation
- **Status:** proposta para revisão
- **Depende de:** [catalog-governance](../catalog-governance/spec.md)
- **ADRs:** [evals-required-for-stable](../../../adr/foundation/evals-required-for-stable.md)

## Problema

As regras de unicidade e de formato só valem se forem verificadas por máquina a cada PR. Além disso, "o melhor de cada fonte" precisa ser medido: uma fusão pode piorar a skill.

## Requisitos

### Validação estática (todo PR)

- **R1. Formato.** Frontmatter de skill/agent/workflow valida no schema; `name` igual ao nome do diretório; `description` entre 50 e 1.024 caracteres, começando pelo gatilho ("Use when..."); `SKILL.md` ≤ 500 linhas; links relativos existem.
- **R2. Catálogo.** Bijeção entre `domains/**` e `catalog.yaml`; todo `supersedes` aponta para chave existente no inventário; profiles só referenciam ids existentes.
- **R3. Nomes.** Únicos no repositório; sem termos de `catalog/naming.yaml`.
- **R4. Duplicata.** Similaridade entre `description` de artefatos do mesmo tipo (TF-IDF + cosseno; embeddings opcionais) acima de 0,80 falha; entre 0,60 e 0,80 gera aviso no PR. Exceções em `catalog/similarity-allowlist.yaml` com justificativa.
- **R5. Licença.** Bloqueia cópia de fonte `reference` (hash); exige entrada em `PROVENANCE.yaml` para arquivo derivado.
- **R6. Higiene.** Sem segredos (gitleaks), sem caminhos absolutos de máquina, sem URLs de telemetria, sem instruções de autopromoção (lista de padrões).
- **R7. Hooks e MCP.** Hooks sem rede por padrão; MCP sem versão flutuante (revisão estática no estilo do `mcp-dependency-review` do ECC).

### Evals (para `stable` e em mudanças de conteúdo)

- **R8. Gatilho.** Cada skill tem `evals/triggers.yaml` com ≥ 5 prompts que devem disparar e ≥ 5 que não devem (incluindo prompts da skill vizinha mais parecida).
- **R9. Tarefa.** Cada skill tem ≥ 2 casos de tarefa com critério de correção verificável (script ou rubrica LLM-as-judge versionada em `prompts/`).
- **R10. Comparação na fusão.** Ao fundir, a skill resultante é avaliada contra a melhor fonte original nos mesmos casos; não pode perder taxa de acerto.
- **R11. Roteamento global.** `evals/routing/` contém prompts realistas com a skill esperada; roda com o catálogo inteiro instalado para detectar colisão de gatilhos entre domínios.

## Critérios de aceite

1. Um PR que adiciona uma skill `ui-ux-pro-max` falha em R3.
2. Um PR que adiciona uma segunda skill de TDD com descrição parafraseada falha em R4.
3. Um PR que copia `skills/docx/SKILL.md` da Anthropic falha em R5.
4. Promover a `stable` uma skill sem `evals/` falha.
5. A suíte estática roda em < 2 min no CI.

## Fora de escopo

Executar evals pagos em todo PR: evals de modelo rodam sob demanda (label `run-evals`) e na promoção para `stable`.
