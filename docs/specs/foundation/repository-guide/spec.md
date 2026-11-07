# Spec — Contrato de manutenção e documentação do repositório

- **Domínio:** foundation
- **Status:** implementada e verificada localmente
- **Baseline:** 908ad6c

## Problema

README, AGENTS.md e ROADMAP descrevem estados diferentes do código. A lista de domínios não explica a separação entre produto instalável, dados de catálogo, entradas editoriais, código de manutenção e documentos de decisão. Os índices gerados exibem IDs sem links diretos em alguns pontos.

## Requisitos

- R1. README e guias de manutenção em português explicam o layout real, instalação, descoberta, edição e verificação.
- R2. Um guia arquitetural descreve todos os diretórios de primeiro nível, entradas autorais versus geradas, pipeline de dados, fronteiras dos tipos e pontos de extensão.
- R3. Catálogo e facetas têm sumário e links aos caminhos públicos; READMEs de domínio mantêm conteúdo, instalação, origem e um link ao manifesto editorial do próprio domínio.
- R4. O ROADMAP só lista specs, ordem e dependências. Estado de execução fica em tasks.md, com evidências; não manter uma segunda tabela de status global.
- R5. Integração contínua e runbook incluem as projeções e novos validadores. Documentar os limites: validação estática não certifica a utilidade da capacidade nem o funcionamento em um harness real.

## Critérios de aceite

1. Todos os diretórios versionados da raiz têm responsabilidade documentada.
2. README, guias e índices gerados têm links locais válidos e descrevem os comandos implementados.
3. Duas gerações de índices produzem exatamente os mesmos bytes.
4. Revisão registra escopo, baseline, achados confirmados, decisões e limites de validação.

## Fora de escopo

Redesenhar a taxonomia em grupos novos, traduzir conteúdo upstream, avaliações pagas, roadmap de produtos externos, release ou aprovação humana de ADRs.
