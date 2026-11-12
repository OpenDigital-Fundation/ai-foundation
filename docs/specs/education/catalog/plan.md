# Plano — Educação

## Contratos

Registrar metadados em `catalog/curation/domains/education.yaml`. Os cinco arquivos procedurais por capacidade quando necessários (entrada, referência e casos de avaliação) são autorais e mantidos diretamente em domains, sem recipe/imports. PROVENANCE vazio significa ausência de conteúdo copiado de repositórios, não ausência de leituras consultadas; estas ficam nas referências e na revisão. Nenhuma mudança em sources.lock ou decisões de inventário.

## Implementação

1. Confirmar ausência de capacidades equivalentes no catálogo e criar ADR do domínio.
2. Escrever quatro entradas e referências específicas: plano de estudo, sessão, mapa Bloom/alinhamento, avaliação/rubrica.
3. Registrar domínio/plugin, facetas existentes e profile; criar casos positivos, negativos e tarefas adversariais sintéticas.
4. Reconstruir catálogo, marketplace e docs; validar ferramentas e gerar adaptadores em saída local nova.
5. Revisar fronteiras, fontes, links, licenças e linguagem de eficácia; preparar commit assinado e evidência para aprovação final.

## Verificação

Os gates estáticos demonstram integridade do pacote. Revisão manual aplica as instruções a exemplos sintéticos e registra achados sem simular execução independente. Casos de modelo são preparados, não executados e não promovem status para stable.
