# Evals obrigatórios para status stable
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

"Pegar o melhor" exige medir. Sem eval, uma fusão pode piorar o gatilho ou a qualidade, e conflitos entre domínios só aparecem em uso. `skill-creator` (Anthropic) e `writing-skills` (superpowers) já tratam skill como código testável.

## Decisão

Todo artefato nasce `experimental`. Para `stable`, precisa de evals de gatilho (deve/não deve disparar, incluindo a vizinha mais parecida) e de tarefa, e, se for fusão, não pode perder para a melhor fonte original. Evals de roteamento globais rodam com o catálogo inteiro.

## Consequências

- Custo de modelo na promoção e em execuções agendadas.
- Profiles de produção só incluem artefatos `stable`.
