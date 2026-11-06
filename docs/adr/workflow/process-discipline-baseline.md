# Disciplina de processo como base do domínio workflow
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** workflow

## Contexto

Três fontes cobrem o ciclo de entrega: superpowers (brainstorming → plano → execução → verificação, com subagentes e worktrees), mattpocock (grilling, to-spec, to-tickets, wayfinder, handoff) e ECC (prp-*, orch-*, epic-*, blueprint, plan). O superpowers impõe uso obrigatório ("você DEVE usar antes de qualquer resposta"), o que conflita com instruções do usuário e de outros catálogos.

## Decisão

Superpowers é a base do processo (procedimentos verificáveis e testados); mattpocock contribui com interrogação do plano (grilling), decomposição em tickets e handoff; do ECC entram só ideias que não existam nas outras. Remove-se a linguagem de obrigatoriedade global: a prioridade é instrução do usuário > `AGENTS.md` do repositório > skill. Specs seguem o layout por domínio deste repositório.

## Consequências

- Um único caminho idea → spec → plano → tarefas → execução → revisão → conclusão.
- Perde-se a "ativação forçada" do superpowers; o gatilho depende de descrições boas, medidas pelos evals de roteamento.
