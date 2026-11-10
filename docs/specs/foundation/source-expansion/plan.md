# Plano — Expansão de fontes

- Clonar no commit fixado, registrar no lock, regenerar `catalog/inventory/` e ler a distribuição de licenças.
- Mapear itens a artefatos existentes pelo nome e descrição; o que é novo vira receita no manifesto do domínio dono; o resto vira exclusão em `catalog/curation/exclusions.yaml`.
- Reconstruir com `python -m tools.curation <sources-dir> --domain <domínio>`; regenerar catálogo e índices.

## Revisão antes da primeira integração em main

- Preservar o histórico assinado até `7767291` e a fatia 3 fora do lote.
- Remover instruções executáveis para hooks não distribuídos das referências importadas: manter políticas, contrato por host e exemplos de evidência, sem prometer bloqueio por `sessionEnd`. Ajustes de receitas ficam em `catalog/overrides/`; arquivos sem receita permanecem no domínio dono.
- Adaptar comandos com versões mutáveis para seleção explícita de versão compatível com o projeto; não inventar uma versão universal e não ocultar falhas do instalador. A transformação comum de referências deve preservar os avisos que citam `@latest` como antipadrão.
- Verificar a propagação de erro com um instalador sintético local; reconstruir apenas os donos afetados e comparar uma segunda reconstrução. Rodar testes de ferramentas e validador, sem executar código upstream nem avaliações pagas.
