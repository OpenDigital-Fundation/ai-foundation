# Spec — Informação geográfica

- **Domínio:** geospatial
- **Status:** em implementação
- **Demanda:** solicitação explícita do mantenedor em 2026-11-11.
- **Decisão:** [ADR do domínio](../../../adr/foundation/geospatial-domain.md)

## Fronteira

Análise e engenharia de dados georreferenciados: sistemas de referência, geometria, raster/vetor, cartografia e serviços GIS. ETL genérico continua em data e modelos genéricos em ai-engineering.

## Capacidades

- `geospatial/geospatial-analysis` — Análise espacial, cartografia, raster/vetor, qualidade geométrica e incerteza.
- `geospatial/geospatial-engineering` — Pipelines e serviços GIS, índices espaciais, publicação de mapas e integração de formatos.

## Requisitos

- **R1.** Uma entrada por capacidade, nomes sem marca, procedimento executável em inglês e referências privadas por ferramenta/tema. Não duplicar donos existentes.
- **R2.** Reabrir as decisões relevantes do inventário fixado, somente após leitura do conteúdo e licença efetiva; registrar fonte, commit, caminho e modificação por arquivo.
- **R3.** Só copiar MIT, Apache-2.0 ou BSD. Texto restrito, desconhecido ou materiais proprietários ficam somente como link; uma biblioteca citada não transfere sua licença ao texto do guia.
- **R4.** Separar capacidade genérica de procedimento do harness de origem. Remover instalação remota, versões flutuantes executáveis, helpers não incluídos e aplicação de mudanças sem autorização.
- **R5.** Manter receita, supersedes, exclusões, facetas, plugin, catálogo e índices coerentes. Procedimentos gerais de outros domínios são referenciados, não copiados como nova capacidade.
- **R6.** Publicar como experimental; escrever casos de roteamento e de fronteira sem afirmar que avaliações de modelo foram executadas.

## Critérios de aceite

1. Todas as capacidades acima têm procedimento próprio, fontes selecionadas e links válidos.
2. Nenhuma chave é decidida duas vezes; decisões reabertas têm motivo verificável.
3. Reconstrução do domínio repetida sem diferença, validador 0/0 e suíte de tooling verde.
4. Revisão estática de comandos, licenças e limites registrada antes da aprovação de publicação.

## Fora de escopo

Executar código upstream, instalar produtos em máquinas reais, alterar sistemas externos, publicar sem aprovação específica, avaliações pagas ou certificação profissional/operacional.
