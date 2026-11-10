# Plano — Estrutura dos arquivos auxiliares dos artefatos

## Arquitetura e contratos

`tools.curation.layout` normaliza nomes de referências e fontes locais após a montagem, atualiza referências de caminhos e retorna um mapa antigo → novo. Esse mapa atualiza destinos em PROVENANCE.yaml; `derived_from.path` continua identificando o upstream. A mesma função é aplicada à árvore atual e ao resultado de builds futuros.

O gerador de proveniência reconhece o caminho original de arquivos normalizados ao procurar correspondências upstream. O validador impede regressão do layout; exemplos sintéticos verificam nomes, links e proveniência. Agentes privados em `<skill>/agents/` permanecem locais à capacidade e são documentados; não são duplicados no catálogo público.

## Verificação

Testes unitários dos contratos alterados, suíte completa do tooling, validação estática do catálogo, conferência de links e comparação da projeção com a baseline. Sem execução de scripts upstream ou avaliações pagas.
