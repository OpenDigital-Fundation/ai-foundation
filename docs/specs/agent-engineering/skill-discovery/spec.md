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

## Busca interna executável — ampliação solicitada em 2026-11-12

O procedimento precisa oferecer busca local concreta, além de orientar leitura manual. A interface será `python -m tools.catalog find <consulta>`, com filtros de domínio/tipo, limite e saída JSON. Uma versão portátil, somente biblioteca padrão, acompanha a skill e consulta um snapshot gerado dos mesmos metadados, funcionando após exportação para os quatro adaptadores.

- Buscar IDs, capacidades, domínios, nomes de facetas pt/en e termos editoriais explícitos. Normalizar acentos e caixa; classificação lexical determinística, sem prometer busca semântica.
- Retornar ID canônico, tipo, estado, caminho no repositório fonte, motivo da correspondência e universo consultado. Instalação local não é inferida de presença no índice.
- Dar prioridade ao ID exato; nenhuma correspondência retorna lista vazia. Filtros desconhecidos e limites fora de 1–50 falham com mensagem clara.
- Não executar comandos candidatos, instalar pacotes, consultar rede, varrer diretório pessoal ou reabrir o registro externo para uma busca interna.
- Índice é projeção gerada; termos de busca são entrada editorial privada da skill. Validador detecta índice ausente/desatualizado, ID inválido ou termo sem dono. Build docs atualiza a projeção sem timestamps instáveis.
- Testar consultas reais como design instrucional, Bloom, legal design, aprender/ensinar e Session Lens; testar filtros, ausência de resultado, snapshot portátil e a estabilidade do índice. A coleta padrão do pytest deve incluir tools/build, que era ignorada pelo padrão de nome de diretório do pytest.

## Fora de escopo

Instalar extensões no cliente, adicionar registry como serviço de produção, criar marketplace remoto ou revisar todo o ecossistema externo.
