# Revisão — Educação e legal design

- **Baseline:** main `9813abf`, 137 artefatos/33 domínios.
- **Universo do lote:** cinco skills originais; quatro em education e uma em legal-compliance, sem novos itens upstream incorporados.
- **Estado:** implementado localmente; verificado localmente; não publicado; sem validação em campo.

## Escopo e proveniência

O domínio jurídico existente é preservado. As novas capacidades são autorais e mantidas diretamente em domains, sem recipes/imports, commits upstream fictícios ou mudanças em inventário/exclusões. PROVENANCE de education tem files vazio porque não há cópia/fusão de código/texto de repositório; a proveniência anterior de legal-compliance não é reescrita. As referências citam leituras acadêmicas/institucionais consultadas em 2026-11-11. Nenhum gráfico de Bloom/CAST, template jurídico, ícone ou rubrica de terceiros foi importado.

## Decisões conferidas

Bloom revisada distingue processos cognitivos e tipos de conhecimento; categorias descrevem tarefas e não pessoas ou uma escala numérica de domínio. Desenho reverso liga objetivo, evidência e prática. Recuperação, espaçamento, exemplos resolvidos, autoexplicação e práticas apoiadas aparecem com decisões contextuais, sem percentuais de eficácia ou intervalos universais. Métodos participativos têm alternativa de acesso e checagem individual. Rubricas não são chamadas validadas sem dados; não há notas ou credenciais automáticas. Legal design preserva fonte, condições, exceções e significado, com verificação profissional antes de uso jurídico real.

## Avaliação preparada

50 casos de gatilho (5 positivos e 5 negativos por skill), 13 casos de roteamento e 10 tarefas sintéticas são escritos. Casos de tarefa ficam marcados not-run; não existe alegação de execução independente, piloto com alunos/usuários ou eficácia educacional. Não executar avaliações com modelo, chamadas pagas nem instalar plugins nos clientes neste lote.

## Evidência executada em 2026-11-12

Na candidata conjunta de sete skills: 190 testes em tools passaram; 12 testes sintéticos do runtime de mensuração passaram; tools.validate retornou 0 erros/0 avisos. Catálogo/marketplace/docs foram reconstruídos duas vezes com hashes estáveis. Os quatro adaptadores gerados contêm 140 skills/workflows cada, incluindo as sete novas entradas e seus recursos, sem links relativos quebrados nessas entradas. Fixtures de eval não entram nos adaptadores; referências a elas foram retiradas das instruções distribuídas.

Universo final: 144 artefatos/34 domínios, contra 137/33 no baseline; todas as sete adições são experimentais. Não houve execução das avaliações de gatilho/tarefa com modelo nem piloto educacional/jurídico. Publicação depende da aprovação do commit/destino e da CI; limpeza depende do lote identificado.
