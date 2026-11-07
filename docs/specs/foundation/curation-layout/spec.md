# Spec — Organização das entradas de curadoria

- **Domínio:** foundation
- **Status:** implementada e verificada localmente
- **Baseline:** 908ad6c

## Problema

As decisões estão agrupadas por onda de importação, fonte ou lote, com entradas manuais, receitas, mapeamentos e resultados gerados na mesma pasta. Um domínio pode depender de cinco arquivos sem relação visível. O inventário operacional está dentro de uma spec e hashes de licenças estão junto ao código do validador.

## Requisitos

- R1. Cada domínio tem exatamente um manifesto editorial em `catalog/curation/domains/<domain>.yaml`, com seus metadados de catálogo, receitas e mapeamentos de importação. Nenhum artefato pode ser declarado duas vezes ou num domínio diferente do prefixo do ID.
- R2. `catalog/catalog.yaml` e `catalog/exclusions.yaml` são projeções geradas, com fonte explícita. Exclusões são editadas em `catalog/curation/exclusions.yaml`; não há arquivos de decisão intermediários gerados.
- R3. Inventário e hashes operacionais ficam em `catalog/inventory/`. Dados não pertencem a specs nem a módulos Python.
- R4. A migração preserva exatamente os 116 registros públicos, decisões upstream, receitas, ajustes locais e origens; a ordenação histórica não determina precedência silenciosa.
- R5. Geradores de bundles, pacotes de linguagem e referências usam os manifestos; um comando de curadoria executa as receitas de um domínio. Entradas malformadas falham antes de escrever os registros.
- R7. Antes de reconstruir conteúdo, conferir arquivos-fonte, receitas e vínculo de cada item inventariado ao manifesto; fontes ausentes e itens sem declaração não podem apagar a saída existente.
- R6. As cópias históricas são movidas para o diretório de revisão fora do checkout, com mapa de migração e hashes, antes da retirada dos caminhos antigos. Nenhum conteúdo é descartado.

## Critérios de aceite

1. Registro e exclusões gerados são semanticamente idênticos à baseline 908ad6c.
2. Todos os 25 manifestos têm domínio e IDs válidos e não duplicados.
3. Testes rejeitam declarações inválidas sem modificar as projeções; geração é determinística.
4. Nenhuma ferramenta ou runbook ativo depende dos caminhos antigos.

## Fora de escopo

Alterar IDs, taxonomia de domínios, conteúdo das capacidades, estabilidade, novas fontes, instalação global, push ou publicação.
