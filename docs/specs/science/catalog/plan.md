# Plano — Catálogo do domínio `science`

- Registrar `K-Dense-AI/claude-scientific-skills` no lock; reincluir no inventário a pasta científica de `davila7` adiada na fatia 3.
- Classificar as 177 skills por capacidade numa tabela explícita (nome → destino), com o motivo das exclusões.
- Cada skill do domínio é uma receita com corpo original e `reference_dirs` apontando para as pastas da fonte (o `SKILL.md` vira `README.md` da referência).
- Licença declarada no frontmatter de cada skill é lida antes de copiar; restritiva ou ambígua vira exclusão `license`.
- Cópias da davila7 com o mesmo nome herdam a decisão; as demais seguem as mesmas regras.
- Reconstruir, validar, varrer comandos mutáveis e caminhos de máquina, commit assinado.

## Licença declarada em arquivos auxiliares

- O cabeçalho de licença reconhecido no próprio arquivo prevalece sobre LICENSE da pasta/raiz. LPPL e expressões SPDX fora da lista aprovada não podem herdar MIT por omissão.
- A receita pode declarar exclusões de arquivos exatos por reference_dir; preflight valida existência e contenção de cada exclusão e verifica todos os demais arquivos. O copiador deve aplicar a mesma lista.
- Seis arquivos Elsevier sob LPPL serão omitidos do guia venue-templates, conforme autorização específica do mantenedor; os demais arquivos MIT permanecem. A proveniência de saídas que deixaram de existir deve ser retirada.
- Os originais e os commits locais são preservados; a publicação partirá da main com uma árvore limpa para que o histórico enviado não carregue as cópias retiradas.

- Overrides espelham os caminhos finais canônicos: aplicar depois da normalização de SKILL.md para README.md nas referências e antes de remover links ausentes. Testar a origem registrada e a preservação do ajuste.
