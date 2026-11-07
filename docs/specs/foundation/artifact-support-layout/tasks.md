# Tarefas — Estrutura dos arquivos auxiliares dos artefatos

- [x] T1. Inspecionar a estrutura completa e definir contratos e critérios.
- [x] T2. Registrar spec e plano antes da implementação.
- [x] T3. Migrar a estrutura e seus consumidores.
- [x] T4. Executar verificações e revisar o diff.
- [x] T5. Registrar evidências e comunicar o outro agente.

## Evidências da preparação

- Baseline 908ad6c: 131 testes; zero erros/avisos no validador.
- Estrutura revisada: 147 testes, incluindo regressões de fontes editoriais, geração sintética, links e arquivos auxiliares.
- Catálogo e exclusões preservados semanticamente: 116 registros e as mesmas decisões upstream.
- 162 arquivos de fontes/licenças preservados byte a byte; todas as origens de proveniência preservadas.
- Reconstrução determinística: 32 arquivos conferidos, sem alteração.
- Sem execução upstream, avaliações pagas, instalação real, push, merge ou publicação.

## Entrega local inicial

- Lote aplicado na worktree própria; sem alterações na principal.
- Verificação no destino: 147 testes passaram; validador com zero erros e zero avisos.
- Aviso ao agente existente aceito pelo Orca; início de turno/leitura não comprovado.
- Alterações locais sem commit ou publicação; worktree e cópia de originais preservadas para revisão sob responsabilidade do Codex.

## Evidências da revisão para integração

- Suíte completa: 152 testes; validação estática sem erros ou avisos.
- Fontes ausentes preservam a saída existente; receitas conferem os itens declarados e projeções recusam decisões conflitantes.
- Catálogo e exclusões preservados; 32 arquivos gerados determinísticos.
- Integração local em spec/foundation solicitada pelo usuário; assinatura e integração serão registradas no histórico Git.
