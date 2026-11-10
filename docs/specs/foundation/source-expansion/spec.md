# Spec — Expansão de fontes (2026-11)

- **Domínio:** foundation
- **Status:** em implementação
- **Depende de:** [source-curation](../source-curation/spec.md), [curation-layout](../curation-layout/spec.md)
- **Pedido:** ampliar o catálogo com coleções oficiais e de empresas, grandes coleções de agents e a coleção científica, aprovadas pelo mantenedor em 2026-11-07.

## Fatias

| Fatia | Fontes | Observações de licença |
|---|---|---|
| 1. Oficiais e empresas | `openai/skills`, `vercel-labs/skills`, `getsentry/skills`, `trailofbits/skills`, `anthropics/claude-cookbooks` | OpenAI declara licença por skill (Apache-2.0, MIT; Figma e Notion com termos próprios; algumas sem licença); Trail of Bits é CC BY-SA 4.0 (só referência) |
| 2. Agregador do GitHub | `github/awesome-copilot` | MIT; ~475 skills, ~231 agents, ~196 instructions |
| 3. Grandes coleções | `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `davila7/claude-code-templates`, `Jeffallan/claude-skills` | a verificar |
| 4. Ciência | `K-Dense-AI/claude-scientific-skills` | a verificar |

Frameworks de agentes (LangGraph, CrewAI, Mastra, smolagents, OpenAI Agents SDK, Google ADK, Microsoft Agent Framework, Agno) não são artefatos deste catálogo: ficam para o registro `opendigital-ai-landscape`.

## Requisitos

- **R1.** Cada fonte entra no lock com commit, licença e política; a licença por pasta é detectada pelo inventário e protege arquivos não permissivos.
- **R2.** Cada item novo do inventário recebe decisão (incorporar num artefato existente, novo artefato com spec do domínio atualizada, ou exclusão com motivo). O validador exige cobertura total.
- **R3.** Nenhum artefato duplicado: capacidade já coberta vira referência ou `supersedes` do artefato existente.
- **R4.** Conteúdo sob CC BY-SA, licença proprietária ou sem licença só entra como link.
- **R6.** Derivação a partir de exclusões (pedido do mantenedor em 2026-11-10): um item excluído como `duplicate-of`, de licença permissiva por arquivo, pode ceder ao dono as seções que o dono ainda não cobre. Só entram seções novas, com proveniência `merged-section` (o `path` registra `arquivo#seções`) e o item passa de exclusão a `supersedes` do dono. Nada de artefato novo; itens de fornecedor ou fora de escopo ficam para outra etapa.
- **R5.** Cada fatia termina com validador sem erros, testes verdes, índices regenerados e commit assinado.

## Critérios de aceite

1. As quatro fatias registradas no lock e com cobertura total no inventário.
2. `docs/SOURCES.md` mostra, por fonte, o que foi usado e o que foi excluído.
3. Derivação: cada seção derivada vem de arquivo permissivo, tem baixa sobreposição com o conteúdo atual do dono (medida e registrada) e é ligada a partir da entrada do dono; o gerador recusa seção inexistente.
