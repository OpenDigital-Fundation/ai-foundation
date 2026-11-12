# Spec — Mensuração de sessões de agentes

- **Domínio:** agent-engineering
- **Status:** implementado e verificado localmente; publicação pendente
- **Baseline:** main `9813abf`
- **Data:** 2026-11-12


## Requisitos

Adicionar `agent-engineering/session-observability`: mensurar sessões selecionadas, agente principal/subagentes, invocações de skills, ferramentas/MCP, tokens e custos com escopo, período, unidade, origem e limites explícitos. A skill é procedimento genérico; uma cópia adaptada e fixada de neokn/session-lens `8067dc061bd89affd2893afdba9b34f2ca847346` (MIT) fica como asset privado e opt-in para Claude Code. Não prometer suporte nativo a Codex/Orca, causalidade, qualidade ou eficácia pela contagem de uso.

Context-management mantém o caminho de consulta rápida ao medidor nativo; agent-evaluation mede desempenho em tarefas controladas; agent-debugging investiga falhas. Esta feature produz instrumentação e leitura descritiva de uso, sem repetir essas capacidades.

## Aceite

- Fonte/commit/licença/modificações por arquivo, aviso MIT e imports reproduzíveis; nenhuma fonte é carregada automaticamente.
- Pacote local sem dependência flutuante de session-report e sem caminhos de executar relatório pago, alterar autocompactação ou apagar/criar hardlinks de transcrições.
- SDK nativo de mods permanece específico do Claude Code, com versão mínima 2.1.308 e ativação opt-in. Declarar leituras de transcrições/configuração/processos e metadados locais gravados pelo plugin antes de habilitar.
- Corrigir rates confirmados contra tabela oficial em 2026-11-12: Fable/Mythos 5.2 e cache read de Sonnet 5.5. Expor limite de estimativa de tabela fixa, modelo desconhecido e diferença da fatura/plano contratado.
- Casos sintéticos verificam deduplicação, separação ferramenta/skill/MCP, estimativa versus snapshot e modelos desconhecidos. Testes não usam sessões pessoais nem modelos pagos.
- Validar manifesto/plugin e import graph, ferramentas do repositório e presença nos quatro adaptadores. Não instalar globalmente nem alterar controles/permissões.

## Fora de escopo

Dashboard agregado próprio, adapter Codex/Orca em tempo real, acesso a credenciais, coleta/exportação externa, reativação de Claude, piloto com logs pessoais e comprovação de benefício operacional.
