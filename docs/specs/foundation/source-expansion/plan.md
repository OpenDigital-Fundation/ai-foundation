# Plano — Expansão de fontes

- Clonar no commit fixado, registrar no lock, regenerar `catalog/inventory/` e ler a distribuição de licenças.
- Mapear itens a artefatos existentes pelo nome e descrição; o que é novo vira receita no manifesto do domínio dono; o resto vira exclusão em `catalog/curation/exclusions.yaml`.
- Reconstruir com `python -m tools.curation <sources-dir> --domain <domínio>`; regenerar catálogo e índices.

## Derivação de exclusões (R6)

- **Contrato:** uma entrada de receita `"<owner>/<repo>:<path>#<seção>[,<seção>]"` copia só as seções cujo título (slug) corresponde, com os subtítulos delas. Sem `#`, o comportamento atual (arquivo inteiro). Seção ausente é erro no preflight. A proveniência registra `modification: merged-section` e `path: <arquivo>#<seções>`.
- **Seleção:** para cada exclusão `duplicate-of` permissiva, dividir o arquivo em seções (`##`/`###`), descartar seções curtas, de instalação ou de persona, e medir a similaridade máxima (TF-IDF) de cada uma contra as seções do dono. Entram as de similaridade baixa, em ordem de ganho; o que entra passa a contar no corpus do dono, para que duas fontes não acrescentem a mesma coisa.
- **Destino:** `references/derived/<tema>.md` do dono, montado pela receita (`references:`) e ligado no `SKILL.md`. Só donos com receita ou language pack nesta etapa; donos mantidos à mão ficam para depois.
- **Revisão:** ler uma amostra por dono antes do commit; varrer comandos mutáveis (`@latest`, `:latest`), instruções de instalação de ferramentas ausentes e menções a produtos.

## Revisão antes da primeira integração em main

- Preservar o histórico assinado até `7767291` e a fatia 3 fora do lote.
- Remover instruções executáveis para hooks não distribuídos das referências importadas: manter políticas, contrato por host e exemplos de evidência, sem prometer bloqueio por `sessionEnd`. Ajustes de receitas ficam em `catalog/overrides/`; arquivos sem receita permanecem no domínio dono.
- Adaptar comandos com versões mutáveis para seleção explícita de versão compatível com o projeto; não inventar uma versão universal e não ocultar falhas do instalador. A transformação comum de referências deve preservar os avisos que citam `@latest` como antipadrão.
- Verificar a propagação de erro com um instalador sintético local; reconstruir apenas os donos afetados e comparar uma segunda reconstrução. Rodar testes de ferramentas e validador, sem executar código upstream nem avaliações pagas.

## Conclusão das derivações em donos mantidos à mão

- Reconciliar os sete commits preservados com a main, preservando as correções anteriores, antes de aplicar a rodada parcial. As worktrees e a cópia de recuperação originais permanecem intactas.
- Conferir os 54 pares item/seção que realmente constam da seleção preservada, em vez de usar a contagem narrativa de 63. Rejeitar duplicatas sem contribuição nova e atribuição ao artefato errado; não criar pacote de linguagem para acomodar a seleção.
- Guias selecionados ficam em references/derived, com origem arquivo#seções, import e supersedes no dono, e saída correspondente das exclusões. Referências importadas são conteúdo mantido à mão; reescritas de risco são registradas como adaptação das seções selecionadas.
- Validação de provenance com fragmento deve recusar seção inexistente antes de registrar derivação; títulos Markdown dentro de código não são títulos do documento. Casos sintéticos cobrem esses contratos.
- Ler os blocos aproveitados e adaptar instaladores mutáveis, scripts não distribuídos, procedimentos que extrapolam o dono e estimativas sem evidência. Não executar fontes nem avaliações pagas; manter experimental.
- Regerar catálogo, curadoria e índices, testar e conferir estabilidade de uma segunda reconstrução antes do PR.
