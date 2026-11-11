# Spec — Catálogo do domínio `science`

- **Domínio:** science
- **Status:** em implementação
- **Decisão:** [ADR science-domain](../../../adr/foundation/science-domain.md)
- **Fronteira:** trabalho científico computacional — análise de dados ômicos e moleculares, simulação e computação científica, desenho e análise de estudos, escrita científica, dados biomédicos de pesquisa e automação de laboratório. Fora: revisão de literatura (`research`), ML de produto (`ai-engineering`), uso clínico.

## Requisitos

- **R1.** Sete skills: `bioinformatics`, `cheminformatics`, `scientific-computing`, `experimental-design`, `scientific-writing`, `biomedical-data`, `lab-automation`, cada uma com procedimento próprio (escolher ferramenta, preparar dados, executar com versões fixadas, validar, relatar) e guias por ferramenta em `references/<ferramenta>/`.
- **R2.** Cada skill da fonte recebe decisão: referência de uma das sete, referência de dono existente fora de `science`, ou exclusão com motivo.
- **R3.** Licença: só entra texto de licença permissiva por arquivo e cuja licença declarada na skill não seja restritiva (CC BY-NC/SA, GPL, PolyForm, proprietária ou desconhecida); essas ficam como link.
- **R4.** Integrações com plataformas comerciais e serviços pagos ficam fora; uso clínico fica fora.
- **R5.** Cópias da fonte em `davila7/claude-code-templates` seguem a decisão do original.

## Critérios de aceite

1. Validador sem erros, testes verdes, catálogo e índices regenerados.
2. As sete skills com facetas, proveniência por arquivo e guias ligados a partir da entrada.
3. Nenhuma referência copiada com licença declarada restritiva.

## Fora de escopo

- Evals de gatilho e tarefa (necessários para `stable`).
- Executar os scripts das fontes.
