# Spec — Pacotes de release

- **Domínio:** foundation
- **Status:** implementada localmente; publicação pendente
- **Baseline:** main 73c8463; 144 artefatos, dos quais 139 skills e 1 workflow distribuíveis
- **Depende de:** [distribution](../distribution/spec.md)

## Objetivo

Publicar v0.1.0 com distribuição completa, downloads por IA e downloads de uma única skill por IA, preservando arquivos privados, licença e origem sem instalar ou executar conteúdo.

## Requisitos e aceite

1. Seis destinos explícitos: Claude Code, Codex, Cursor, Gemini CLI, OpenCode e GitHub Copilot; manter também o formato neutro Agent Skills.
2. Um ZIP completo inclui o catálogo nativo por domínio, os sete bundles e todos os ZIPs individuais. Cada skill/workflow não deprecated recebe seis ZIPs individuais; não transformar referências privadas em novas capacidades.
3. Cada pacote individual contém uma só entrada pública, seus recursos e suporte público referenciado, LICENSE, THIRD_PARTY_NOTICES, PROVENANCE e metadados de origem. Índices e comandos devem listar só a seleção instalada.
4. Manifesto JSON relaciona ID canônico, tipo, status, IA, versão, commit, arquivo, tamanho e SHA-256; SHA256SUMS e verificador offline acompanham a release.
5. ZIPs determinísticos: ordem, timestamps e permissões normalizados; rejeitar symlinks, traversal, saída existente, arquivos inesperados, hashes divergentes e versões inválidas. Nenhum cache, checkout Git, clone upstream ou diretório pessoal no pacote.
6. Respeitar 1.000 assets por release e arquivo menor que 2 GiB; abortar antes de criar saída quando o catálogo ultrapassar o limite.
7. CI de PR constrói e transporta os pacotes com token de leitura; publicação só por tag v<versão>, após verificação. Falha de upload mantém draft; nunca substituir assets ou tags existentes automaticamente.
8. Validar estrutura, integridade, seleção individual e busca interna offline; distinguir testes de pacote de validação em agentes reais. O estado experimental continua preservado.

## Fora de escopo

Instalação em contas pessoais, ativação de hooks/Session Lens, avaliações pagas, novas fontes, promoção de skills para stable e publicação em registries externos.
