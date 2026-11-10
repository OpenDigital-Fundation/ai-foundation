# Fronteiras entre tipos de artefato
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

As fontes misturam tipos: o ECC tem command, skill e agent para a mesma coisa (`/tdd`, `tdd-workflow`, `tdd-guide`); o agency-agents tem personas sem procedimento; o Claude Code já trata skills como invocáveis pelo usuário.

## Decisão

- **skill** é a unidade de capacidade.
- **agent** só existe quando precisa de contexto isolado, paralelismo ou restrição de ferramentas, e invoca skills em vez de copiá-las. Não há um agent por linguagem: um `code-reviewer` carrega o pacote da linguagem.
- **workflow** orquestra skills/agents com portões e é publicado como skill.
- **prompt**, **template** e **knowledge** são insumos sem gatilho próprio.
- **rule** é curta e sempre ativa.
- **hook** é guardrail determinístico e opt-in.
- **mcp** é recomendação com versão fixada.
- **profile** agrupa ids entre domínios.
- **command** não é escrito à mão; é gerado para harnesses que exigem.

## Consequências

- As famílias `orch-*`, `prp-*`, `multi-*`, `epic-*` do ECC viram poucos workflows.
- As personas do agency-agents só entram como agents se tiverem procedimento verificável; caso contrário, o conhecimento útil vai para a skill do domínio.
