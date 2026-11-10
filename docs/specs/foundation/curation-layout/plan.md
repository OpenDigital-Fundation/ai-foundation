# Plano — Organização das entradas de curadoria

## Arquitetura e contratos

O manifesto de domínio contém `version`, `domain`, `artifacts` e `imports`. Cada registro de artefato mantém os campos públicos do schema atual e pode conter `recipe` (montagem de bundle) ou `language_pack` (pacote de linguagem), nunca ambos. `imports` retém mapeamentos para proveniência de conteúdo portado. O registro público exclui esses campos de construção.

`tools.curation.manifests` centraliza leitura e validação. `tools.catalog.rebuild` prepara as duas projeções em memória antes de escrevê-las, sem upserts dependentes de ordem alfabética. `tools.curation.bundle` e `language_pack` deixam de emitir decisões intermediárias. `python -m tools.curation <sources-dir> --domain <domain>` executa receitas explícitas; não baixa nem executa fontes.

Dados: `catalog/inventory/artifacts.csv` e `restricted-hashes.txt`. Overrides continuam em `catalog/overrides/<domain>/<skill>/`, separados de conteúdo publicado.

Migração: arquivar cópias e hashes dos caminhos antigos fora do checkout, transpor registros e receitas por domínio, atualizar consumidores, verificar equivalência semântica e revisar diff. A implementação ocorre em cópia preparatória e só depois é aplicada na worktree própria.

## Verificação

Testes unitários dos contratos alterados, suíte completa do tooling, validação estática do catálogo, conferência de links e comparação da projeção com a baseline. Sem execução de scripts upstream ou avaliações pagas.

## Revisão antes da integração

Uma pré-validação comum resolve todas as fontes e receitas selecionadas antes de qualquer remoção de saída. Ela verifica existência e leitura das entradas, tópicos, padrões de reescrita e pertencimento dos itens usados ao campo supersedes do manifesto. As projeções recusam decisões de origem repetidas ou contraditórias antes de escrever arquivos. Testes com saída preexistente provam sua preservação quando falta uma fonte.
