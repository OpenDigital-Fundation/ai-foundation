# Referências e assets dentro de artefatos

- **Status:** aceito na implementação; revisão e integração local solicitadas pelo usuário em 2026-11-07
- **Data:** 2026-11-07
- **Domínio:** foundation

## Contexto

A revisão estrutural da baseline 908ad6c identificou mistura de entradas editoriais com resultados gerados e convenções internas importadas de fontes distintas. O repositório precisa de fronteiras verificáveis sem alterar a instalação seletiva por domínio.

## Decisão

A entrada canônica usa SKILL.md na raiz do artefato. Referências copiadas com a mesma convenção são renomeadas para README.md dentro de references/. Fontes locais ficam em assets/fonts/. Assets repetidos entre plugins são mantidos quando necessários ao empacotamento independente.

## Consequências

A busca por SKILL.md identifica entradas reais. Caminhos publicados mudam somente dentro de referências e fontes; os IDs de catálogo e plugins continuam válidos. Atualizar links e proveniência é parte da migração e dos geradores.
