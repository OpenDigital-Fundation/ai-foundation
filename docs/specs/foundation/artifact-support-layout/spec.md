# Spec — Estrutura dos arquivos auxiliares dos artefatos

- **Domínio:** foundation
- **Status:** implementada e verificada localmente
- **Baseline:** 908ad6c

## Problema

Há 85 arquivos `SKILL.md` dentro de `references/`, embora só a entrada imediata em `skills/<name>/SKILL.md` seja pública. Fontes tipográficas usam uma pasta própria fora do padrão de assets. Sem fronteira explícita, leitores confundem entradas executáveis, agentes privados e material auxiliar.

## Requisitos

- R1. A entrada de uma skill ou workflow é o `SKILL.md` na raiz do artefato. Guias sob `references/` usam `README.md`, preservando seus diretórios e conteúdo.
- R2. Fontes tipográficas empacotadas ficam em `assets/fonts/`; comandos e referências devem acompanhar a mudança.
- R3. Links relativos, registros de proveniência, exceções de higiene e reconstrução devem apontar aos caminhos novos. A origem upstream retém o caminho original.
- R4. Cada plugin continua instalável isoladamente; não criar symlinks nem referências entre diretórios de plugins para deduplicar assets.
- R5. Documentar distinção entre agentes públicos do domínio, agentes privados de uma skill, scripts, assets, dados e avaliações. Validar que novas referências não voltem a publicar SKILL.md aninhado.

## Critérios de aceite

1. Zero SKILL.md em references/ após migração e após reconstrução de uma receita sintética.
2. Os 116 IDs e entradas públicas permanecem iguais; conteúdo auxiliar movido preserva bytes, exceto atualização de caminhos.
3. Links, proveniência e testes de adaptadores passam.
4. Regeneração usa a mesma normalização dos arquivos versionados.

## Fora de escopo

Fundir capacidades por semelhança textual, retirar arquivos de terceiros, compartilhar assets entre plugins, mudar o significado de instruções ou certificar execução de scripts upstream.
