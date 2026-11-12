# Spec — Descoberta de skills

- **Domínio:** agent-engineering
- **Status:** implementado e verificado localmente; publicação pendente
- **Baseline:** main `9813abf`
- **Data:** 2026-11-12


## Requisitos

Reabrir a chave `vercel-labs/skills:skill:find-skills`, hoje excluída vendor-specific, sob `agent-engineering/skill-discovery`. A fonte já está fixada em sources.lock no commit `d3701c11b1101251af14c9d148f026e1a47ebe17`, MIT. Adaptar busca por domínio/tarefa, termos específicos, comparação de candidatos e fallback sem resultado. Consultar primeiro o catálogo local para melhorar dono existente quando apropriado.

## Aceite

- Uma decisão da chave; supersedes, imports e proveniência consistentes, sem duplicar skill-authoring.
- Descrição de descoberta/avaliação de skills para uma tarefa, não execução indiscriminada em todo pedido de ajuda.
- Ranking/estrelas/downloads não são prova de qualidade ou segurança; verificar arquivo, licença local, versão, dependências, escopo e teste relevante.
- Nenhum npx flutuante, instalação global, flags de confirmação automática ou atualização em massa no procedimento padrão; descoberta não autoriza instalação.
- Cinco gatilhos positivos/negativos, duas tarefas sintéticas e roteamento; pacote verificável com quatro adaptadores.

## Fora de escopo

Instalar extensões no cliente, adicionar registry como serviço de produção, criar marketplace remoto ou revisar todo o ecossistema externo.
