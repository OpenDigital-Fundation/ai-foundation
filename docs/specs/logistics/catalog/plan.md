# Plano — Logística e cadeia de suprimentos

## Contratos e arquitetura

O manifesto `catalog/curation/domains/logistics.yaml` é a fonte editorial. Cada skill é montada pelo gerador existente, com corpo local e referências de arquivos/seções fixados; imports são usados apenas quando necessários. Não criar um agente por persona nem uma skill por fornecedor. O plugin registra só o domínio.

## Curadoria incremental

1. Conferir as capacidades existentes e a fronteira deste domínio.
2. Ler os candidatos do inventário e as licenças por arquivo/pasta; selecionar conteúdo concreto e descartar personas, promessas e protocolos de ferramentas ausentes.
3. Construir as entradas acima, ligar guias de referência, reclassificar exclusões e atualizar proveniência.
4. Registrar facetas e casos de roteamento; regenerar somente este domínio e os índices públicos.
5. Comparar saída por hash após rebuild, rodar validador e testes, revisar diff e deixar publicação para aprovação específica.

## Casos de verificação

Entradas positivas em português/inglês, fronteiras com operations, data, finance, licença local restritiva, chave repetida, referência ausente e reconstrução estável. Os testes de tooling existentes exercitam os gates; os casos de modelo ficam escritos e não executados.

## Decisões

A abertura do domínio é a decisão isolada do ADR. A seleção de fonte e seções fica na receita e na matriz de curadoria, sem um segundo plano ou cópia das projeções.
