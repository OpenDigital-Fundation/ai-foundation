# Plano — Descoberta de skills


## Implementação

Manter entrada original com adaptação explícita de find-skills na referência local `discovery-playbook.md`, import do arquivo fixado e override autoral; registrar MIT, commit, source path e modification. Remover somente a exclusão dessa chave e transferir a decisão para supersedes da skill. Não mudar as outras decisões do inventário.

Registrar facetas existentes, profile de operação de agentes e casos positivos/negativos. Reconstruir catálogo e docs e conferir unicidade, links, preservação do conteúdo e limites de instalação. Sem avaliar candidatos por popularidade isolada nem executar código do registry durante a revisão.

## Implementação incremental da busca interna

1. Acrescentar termos pt/en em assets/search-terms.json da skill. O índice não contém corpos de skills nem transcrições: só metadados públicos e termos autorais.
2. Gerar assets/catalog-index.json em tools/build/search.py a partir do catálogo, facetas e vocabulários existentes. Não registrar datas ou SHA do próprio commit na projeção.
3. Manter uma única lógica de ranking em scripts/find.py (biblioteca padrão); o CLI tools.catalog reutiliza essa lógica com índice construído em memória, sem escrever arquivos. O script portátil usa o snapshot distribuído.
4. Integrar geração no build de docs e verificação de frescor no validador. Documentar a diferença entre entrada do catálogo e instalação efetivamente disponível.
5. Testar resultados observáveis, filtros, dados ausentes e uso fora do checkout; gerar novamente adaptadores em caminho novo e preparar commit adicional assinado, sem reescrever o anterior.

Preservar as exclusões padrão de caches/distribuição do pytest, retirando somente o bloqueio ao nome build; confirmar por collect-only que os 19 casos novos e quatro casos preexistentes dessa pasta entram na suíte padrão.
