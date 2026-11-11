# Revisão da integração restante

- Data: 2026-11-11
- Responsável: Codex, a pedido de Matheus Breguêz
- Baseline publicada: `bfb616c2a4394505ec8f19be08267d77c3ee3dd5`
- Escopo: sete commits locais de coleções, ciência, UX, negócios e derivações; conclusão da rodada parcial; reconciliação com as correções já publicadas na main.
- Estado: implementado e verificado localmente; publicação depende da aprovação específica do commit/destino. Sem validação em campo.

## Universo conferido

O catálogo passa de 116 para **123 artefatos experimentais**, distribuídos em **26 domínios**. As sete novas capacidades pertencem a science; o restante melhora os donos existentes. O lock fixa 38 fontes. O inventário contém 5637 observações e 5442 chaves distintas, todas decididas: 1435 incorporadas e 4007 excluídas, sem decisão sobreposta. Fontes: catalog/catalog.yaml, catalog/inventory/artifacts.csv, catalog/exclusions.yaml e sources.lock.yaml reconstruídos.

A rodada manual concluída incorpora 46 seções em 30 referências, de 30 chaves upstream para 18 donos em nove domínios. Cinco propostas foram rejeitadas: agent-skills.instructions, tdd-red, tdd-green, create-worktrees e bash-pro. Não foi criado um pacote Bash a partir do diretório de links languages/external-tools.

## Achados confirmados e correções

| Prioridade | Evidência | Tratamento |
|---|---|---|
| Alto — licença inline encoberta por MIT | Cabeçalhos de seis arquivos elsarticle em venue-templates declaram LPPL | Retirada autorizada de 113.730 bytes; exclusão por caminho exato, teste de preflight, remoção de proveniência órfã e indicação do pacote oficial externo |
| Alto — referências prometiam arquivos retirados | README, journals_formatting, current_sources e TEMPLATES no script query_template | Quatro overrides reproduzíveis; catálogo de modelos conferido por AST e existência de cada asset, sem executar o script |
| Alto — avisos MIT incompletos | Coleções novas e três pastas têm avisos próprios | THIRD_PARTY_NOTICES.md reproduz titulares de GitHub, Seth Hobson, VoltAgent, Daniel Ávila, K-Dense, Jeffallan e das três pastas específicas |
| Médio — dono não implementava a capacidade | Oito decisões chamavam um diretório de links de pacote de linguagem; GitLab apontava para GitHub | Linguagens reclassificadas como fora de escopo; GitLab como fornecedor, sem alegar incorporação |
| Médio — trechos pressupunham automação ou autorização | Dependências, segredos, scanner incompleto, MCP e blast radius | Referências limitadas a evidência, planejamento e ações explicitamente autorizadas; removidos helpers ausentes, instalação global e fórmulas jurídicas sem base |
| Médio — seleção e geração frágeis | Fragmentos vazios/ausentes; H1 em código; override README colidia com SKILL | Seletores recusados antes de escrever; títulos fora de fences; normalização antes do override canônico; regressões sintéticas |

## Verificação executada

- 190 testes de tooling passaram: python -m pytest -q -p no:cacheprovider tools.
- python -m tools.validate: zero erros e zero avisos.
- Duas execuções completas de tools.curation --all, tools.build, tools.catalog rebuild e tools.build docs: zero alteração na segunda execução, em 3406 caminhos conferidos por hash.
- Auditoria de 1714 origens alteradas: 1706 MIT e 8 Apache-2.0, com licença efetiva, caminho e aviso de modificação conferidos; sem divergência ou bloqueio pendente.
- 367 referências Python lidas por AST: sem erro sintático nem chamadas eval, exec, os.system ou shell=True na varredura. 23 chamadas subprocess.run observadas, sem execução. Os scripts empacotados continuam referências sujeitas à revisão antes do uso.
- As 38 fontes foram recuperadas nos commits fixados e verificadas com HEAD e status limpo. Fontes upstream foram lidas como dados.
- git diff --check: sem erro. Workflows de CI e dependências do projeto permanecem iguais à baseline.
- Os 57 arquivos da worktree parcial original foram preservados por hash em backup local ignorado pelo Git; todas as refs têm bundle de recuperação.

## Publicação e recuperação

Os commits locais antigos contêm os seis arquivos retirados. A branch de publicação terá a árvore saneada em um commit assinado cujo único pai é a main publicada; não enviará os sete commits antigos nem o merge local de reconciliação. As refs antigas e a worktree parcial permanecem preservadas para recuperação. Publicar requer PR, CI e aprovação específica do destino/commit; nenhuma nova remoção de worktree faz parte dessa autorização.

## Limites

A revisão é estática e dirigida aos riscos encontrados; não representa leitura humana integral de cerca de 465 mil linhas importadas. O gate reconhece licenças próximas e cabeçalhos conhecidos, não certifica a origem remota de toda afirmação. Os nomes não resolvidos que o curador imprime incluem papéis, exemplos e referências externas; os links locais passam no validador, sem instalar ferramentas implícitas.

Não foram executados código upstream, avaliações pagas, treinamento, instalação em agentes reais ou validação científica e operacional. Os 123 artefatos continuam experimentais; os casos de avaliação de ciência estão escritos e não são prova de desempenho. Esses limites não impedem publicar o catálogo experimental, mas impedem descrevê-lo como validado em campo.
