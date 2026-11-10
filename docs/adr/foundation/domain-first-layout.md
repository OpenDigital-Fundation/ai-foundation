# Domínio primeiro, tipo depois
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

Há dois layouts possíveis: por tipo na raiz (`agents/`, `skills/`, `prompts/`, `rules/`, `workflows/`, `mcps/`, `templates/`, `evals/`) ou por domínio na raiz. Por tipo é fácil de navegar, mas obriga a instalar tudo junto e não dá namespace aos nomes. O Claude Code instala plugins, e cada plugin dá namespace (`plugin:skill`).

## Decisão

O primeiro nível é o domínio (`domains/<domínio>/`), e cada domínio é um plugin. Dentro do domínio, as pastas são por tipo (`skills/`, `agents/`, `workflows/`, `prompts/`, `rules/`, `hooks/`, `mcps/`, `templates/`, `knowledge/`, `evals/`). Na raiz ficam só o que atravessa domínios: `catalog/`, `profiles/`, `evals/routing/`, `tools/`, `docs/`.

## Alternativas consideradas

- **Tipo na raiz:** rejeitado como primeiro nível porque impede instalação seletiva; aproveitado como segundo nível.
- **Um plugin único:** rejeitado; carrega centenas de descrições no contexto.

## Consequências

- Instalação seletiva e namespace grátis.
- Um artefato precisa de um domínio dono; casos ambíguos são decididos pela frase de fronteira da spec `catalog-governance`.
