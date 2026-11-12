# Revisão — Session Lens e descoberta de skills

- **Baseline:** main `9813abf`; fonte neokn/session-lens `8067dc0` (1.2.0), MIT.
- **Implementado:** runtime nativo privado opt-in e procedimento genérico de mensuração; find-skills reaberto como skill-discovery a partir da fonte MIT já fixada.
- **Universo importado:** 62 arquivos runtime/licença do Session Lens, 9 adaptados; find-skills com uma referência reescrita e uma licença.
- **Limites:** não instalado/ativado em clientes; sem coleta de sessões reais, piloto interativo ou execução de modelo. Nenhuma capacidade de telemetria Codex/Orca é alegada.

## Achados confirmados e tratamento

1. O plugin upstream declara dependência flutuante de session-report e oferece relatório com uso de modelo: dependência, controles e ação retirados; rotina residual retorna aviso sem chamar modelo.
2. Autocompactação oferece leitura ampla de logs e escrita de settings: comando/controles removidos e helpers substituídos por recusas locais; scripts não copiados.
3. O relatório upstream usa hardlinks e rm -rf no diretório de relatório: rotina substituída por recusa, sem shell de cópia/exclusão.
4. A tabela upstream omite Fable/Mythos 5.2, fazendo-os casar com o prefixo 5; cache read Sonnet 5.5 está em 0.20 em vez de 0.10 USD/MTok. Corrigidos contra [fonte oficial](https://platform.claude.com/docs/en/about-claude/pricing) consultada em 2026-11-12; modelo minor desconhecido não herda preço de família. Valores continuam estimativas padrão e datadas, sem rate modifiers específicos do contrato/plataforma.
5. O coletor mantém estado/links de filhos localmente e busca cabeçalhos para resolver sessões relacionadas: documentação declara esse escopo; não se afirma somente leitura do filesystem, nem ativação silenciosa. Não foram lidos logs pessoais nesta revisão.
6. find-skills upstream atrela recomendação a estrelas/downloads e sugere instalação global com auto-confirmação. A adaptação avalia conteúdo/licença e separa descoberta de instalação autorizada.

7. Fragmentos repetidos da mesma mensagem podiam contar novamente a mesma tool_use_id em totais por turno: deduplicação aplicada e testada com fixture repetida.
8. Exceções do observador podiam bloquear ou reenviar next(e) através de handlers gerais: observação protegida separadamente; erro original de downstream é propagado com uma única invocação. Teste sintético força falha no estado do observador e no downstream.

## Verificação executada em 2026-11-12

190 testes em tools e 12 testes sintéticos do runtime passaram (345 asserts). Fixtures cobrem aritmética/cache, preço desconhecido, snapshot versus estimativa, deduplicação, separação de uso, amostra pequena, resolução/transpilação de módulos e ausência de efeito nas ações desabilitadas. tools.validate retornou 0 erros/0 avisos. O CLI nativo retornou success=true, sem erro/aviso no manifesto/hooks; suas sugestões de ícone/marketplace e avaliação incompleta do diretório público não se aplicam à distribuição deste asset privado nem comprovam compatibilidade interativa. Os quatro adaptadores preservam o manifesto nativo oculto e os módulos, sem autoativação. Nenhuma avaliação com modelo ou dado pessoal foi executada. A versão local do executável Claude Code é 2.1.322; essa observação não equivale a plugin funcionando em sessão. A API de mods exige host habilitado e pode variar. Não reiniciar Claude para provar a integração.


Os casos escritos da candidata conjunta são 70 gatilhos (5 positivos/5 negativos por skill), 17 rotas e 14 tarefas sintéticas, sem execução com modelo. Imports mapeiam a origem dos recursos mantidos diretamente; não são uma instrução para substituir esta árvore cegamente por ferramentas de curadoria. Overrides guardam os nove arquivos adaptados para uma futura atualização revisada contra o mesmo pin.
