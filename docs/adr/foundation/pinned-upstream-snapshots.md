# Snapshots fixados das fontes, sem submódulos
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

As fontes mudam rápido (o ECC teve centenas de mudanças em meses). Submódulos ou dependência viva trariam mudanças não revisadas e o conteúdo inteiro das fontes, inclusive o que foi descartado.

## Decisão

`catalog/sources.lock.yaml` fixa o commit de cada fonte. Conteúdo é copiado/fundido uma vez, com proveniência. Um job semanal compara o HEAD das fontes com o lock e abre uma issue com o diff dos artefatos relevantes; a incorporação passa por PR normal.

## Consequências

- O repositório é autocontido e estável.
- Melhorias upstream chegam com atraso, mas revisadas.
