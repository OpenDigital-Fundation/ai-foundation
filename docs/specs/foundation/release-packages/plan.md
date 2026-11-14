# Plano — Pacotes de release

1. Adicionar tools/build/release.py usando as projeções portáteis existentes como fonte; montar mapas de membros ZIP sem 840 cópias temporárias da árvore.
2. Gerar layouts de projeto .claude/skills, .agents/skills, .github/skills, Cursor com regras e suporte local, extensão Gemini versionada e .opencode/skills. Índices compartilhados vão em metadados, sem sobrescrever AGENTS.md do consumidor.
3. Gerar ZIPs individuais, bundles e dist completo a partir dos mesmos mapas. Metadados de cada seleção carregam proveniência do domínio, inclusive suporte de outros domínios; conservar licenças locais byte a byte.
4. VERSION define a versão da distribuição, independente do versionamento de plugins por domínio. Tag e VERSION precisam corresponder. O CLI usa HEAD limpo como origem; build local não publica.
5. tools/build/release_verify.py usa apenas biblioteca padrão, não extrai nem executa conteúdo e é transportado junto. Conferir hashes, nomes seguros, contagem/identidade pública, manifests Gemini, regras e comandos, licenças e composição do completo.
6. Atualizar release.yml com build em PR e tag, verificação em job separado de leitura e publicação por draft no job de escrita. Manter ações fixadas e sem avaliações com modelo.
7. Testes sintéticos de dois artefatos cobrem seleção, suporte, determinismo, corrupção, traversal, symlink, limites e proteção de saída existente. Rodar tooling completo, validador e build real das 140 entradas antes do commit final/revisão.
8. Preparar commit assinado e pacote local revisável; solicitar aprovação específica do SHA/destino antes de push, integração e tag/release conforme AGENTS. Registrar publicação e limpeza separadamente.

## Evidência dos formatos consultada em 2026-11-14

- Claude Code: https://code.claude.com/docs/en/skills
- Codex: https://developers.openai.com/codex/skills/ (redireciona para https://learn.chatgpt.com/docs/build-skills)
- Cursor: https://cursor.com/docs/skills
- Gemini CLI: https://geminicli.com/docs/cli/skills/
- OpenCode: https://opencode.ai/docs/skills/
- Copilot: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- GitHub Releases: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
