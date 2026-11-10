# Plano — Expansão de fontes

- Clonar no commit fixado, registrar no lock, regenerar `catalog/inventory/` e ler a distribuição de licenças.
- Mapear itens a artefatos existentes pelo nome e descrição; o que é novo vira receita no manifesto do domínio dono; o resto vira exclusão em `catalog/curation/exclusions.yaml`.
- Reconstruir com `python -m tools.curation <sources-dir> --domain <domínio>`; regenerar catálogo e índices.

## Derivação de exclusões (R6)

- **Contrato:** uma entrada de receita `"<owner>/<repo>:<path>#<seção>[,<seção>]"` copia só as seções cujo título (slug) corresponde, com os subtítulos delas. Sem `#`, o comportamento atual (arquivo inteiro). Seção ausente é erro no preflight. A proveniência registra `modification: merged-section` e `path: <arquivo>#<seções>`.
- **Seleção:** para cada exclusão `duplicate-of` permissiva, dividir o arquivo em seções (`##`/`###`), descartar seções curtas, de instalação ou de persona, e medir a similaridade máxima (TF-IDF) de cada uma contra as seções do dono. Entram as de similaridade baixa, em ordem de ganho; o que entra passa a contar no corpus do dono, para que duas fontes não acrescentem a mesma coisa.
- **Destino:** `references/derived/<tema>.md` do dono, montado pela receita (`references:`) e ligado no `SKILL.md`. Só donos com receita ou language pack nesta etapa; donos mantidos à mão ficam para depois.
- **Revisão:** ler uma amostra por dono antes do commit; varrer comandos mutáveis (`@latest`, `:latest`), instruções de instalação de ferramentas ausentes e menções a produtos.
