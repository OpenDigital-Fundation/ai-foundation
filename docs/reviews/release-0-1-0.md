# Revisão — Release 0.1.0

- **Data:** 2026-11-14
- **Responsável:** Codex
- **Baseline do catálogo:** main 73c8463ace5a3bfa18283c349d9772eafaf190c1
- **Implementação revisada:** 1b4bc067c1af6e6160dccf82dee856f1c748a234, assinado por Matheus Breguêz
- **Contrato:** [release-packages](../specs/foundation/release-packages/spec.md)

## Universo e resultado local

O catálogo permanece com 144 artefatos em 34 domínios e 40 fontes fixadas. A distribuição projeta 139 skills e 1 workflow em seis clientes: Claude Code, Codex, Cursor, Gemini CLI, OpenCode e GitHub Copilot. O formato neutro Agent Skills recebe um bundle adicional; os demais quatro artefatos públicos estão na árvore nativa completa.

O build de implementação produziu 852 assets: 840 ZIPs individuais, 7 bundles, 1 ZIP completo, INSTALL.md, verify-release.py, manifest.json e SHA256SUMS. A origem desse ensaio é o commit 1b4bc06; seus bytes não são apresentados como uma release já publicada. O corte final precisa reconstruir após o commit deste registro, pois a origem e a árvore nativa mudam.

## Verificações executadas

- `python -m pytest -q -p no:cacheprovider`: **246 testes aprovados**, incluindo **24 casos de release** sintéticos; duração local da suíte: 87,63 s.
- `python -m tools.validate`: **0 erros, 0 avisos**.
- `git diff --check`: aprovado; YAML do workflow parseável e todos os blocos run aprovados por `bash -n`.
- `python -m tools.build release dist/release-initial`: aprovado em 61,33 s; hashes, CRC, matriz de seleção, licenças/metadados e composição do ZIP completo verificados sem executar seu conteúdo.
- Extração isolada de skill-discovery para cada cliente, em diretórios temporários vazios: uma entrada pública por pacote e busca autoral offline por “design instrucional” retornando education/instructional-design nas seis variantes.
- Comparação de todos os **3.768 arquivos** de native/ com o conjunto versionado do ensaio: bytes idênticos, sem caches, configurações pessoais ou metadados Git.
- Assinatura da implementação conferida com `git verify-commit`; chave B6FA8458D5176E83, autor e committer exigidos pelo AGENTS.

Logs e resumos locais estão em dist/local-review/release-0-1-0/evidence na worktree principal; não são conteúdo instalável nem assets públicos.

## Achado corrigido

Um caso de teste mostrou que a rotina de cópia dos adaptadores de desenvolvimento poderia seguir um symlink não versionado. O gerador de release agora recusa symlinks antes de montar pacotes e oferece aos adaptadores somente um snapshot dos arquivos versionados. Casos de arquivo pessoal não versionado dentro de uma skill e fora de domains comprovam sua ausência nos pacotes. Nenhuma mudança de curadoria ou conteúdo de capacidade foi necessária.

## Limites

Os testes verificam arquivos e busca lexical autoral, sem instalar plugins em contas pessoais nem executar scripts upstream. Não houve avaliação paga, ativação de Session Lens ou teste de tarefa em agentes reais; as capacidades permanecem experimentais. A distribuição versiona o conjunto, enquanto os plugins mantêm suas versões independentes.

O fluxo CI de PR constrói e verifica o transporte com token de leitura. Somente tags de versão correspondentes a VERSION, integradas à main, habilitam o job de publicação; ele envia um draft, compara nomes, tamanhos e digests fornecidos pelo GitHub e só então o publica. A execução remota e a publicação dependem da aprovação do corte final; não são inferidas do resultado local.
