# Spec — Governança do catálogo

- **Domínio:** foundation
- **Status:** proposta para revisão
- **ADRs:** [domain-first-layout](../../../adr/foundation/domain-first-layout.md), [one-capability-per-domain](../../../adr/foundation/one-capability-per-domain.md), [artifact-type-boundaries](../../../adr/foundation/artifact-type-boundaries.md), [unbranded-naming](../../../adr/foundation/unbranded-naming.md), [language-packs](../../../adr/foundation/language-packs.md), [english-artifacts-portuguese-governance](../../../adr/foundation/english-artifacts-portuguese-governance.md)

## Problema

As fontes avaliadas somam 1.275 artefatos (1.007 após remover cópias idênticas). A sobreposição é alta: TDD aparece em ~15 variantes, code review em ~25, planejamento em ~20. Fontes distintas usam nomes diferentes para a mesma capacidade (`systematic-debugging` × `diagnosing-bugs`), uma mesma fonte duplica por linguagem (`go-reviewer`, `rust-reviewer`, `python-reviewer`...), e há "megaskills" que juntam domínios distintos (`ui-ux-pro-max`, `design`). Instalar tudo gera conflito de gatilho: o agente não sabe qual skill usar e o contexto se enche de descrições redundantes.

## Objetivo

Definir as regras que fazem do repositório uma coletânea **sem duplicatas e sem sobreposição dentro do domínio**, de forma verificável por máquina.

## Requisitos

### R1. Taxonomia de domínios

O catálogo é dividido nestes domínios, cada um com uma frase de fronteira. Um artefato pertence a exatamente um domínio.

| Domínio | Fronteira (o que é dono) |
|---|---|
| `principles` | Comportamento sempre ativo do agente ao programar: simplicidade, mudança cirúrgica, explicitar suposições, critérios verificáveis. |
| `workflow` | Ciclo de entrega: ideação, spec, plano, execução, worktrees, conclusão de branch, handoff, retrospectiva, tickets. |
| `architecture` | Desenho de sistema e de código: módulos, domínio, ADR, API, fronteiras. |
| `code-quality` | Avaliar e melhorar código existente: review (dar e receber), simplificação, refatoração, dívida, auditoria de repositório. |
| `testing` | Provar comportamento: TDD, estratégia de testes, E2E/navegador, verificação antes de concluir. |
| `debugging` | Achar a causa de falha: diagnóstico, erros de build, falhas silenciosas. |
| `security` | Segurança de aplicação e de agente: auditoria, threat modeling, segredos, supply chain, hardening. |
| `languages` | Conhecimento idiomático por linguagem e framework (um pacote por linguagem). |
| `data` | Bancos de dados, migrações, modelagem e engenharia de dados. |
| `ui` | Interface visual: direção estética, tipografia, cor, layout, tokens, design system, componentes, acabamento. |
| `ux` | Experiência: pesquisa com usuário, fluxos, arquitetura de informação, heurísticas de usabilidade, microcopy. |
| `accessibility` | Conformidade e auditoria de acessibilidade (WCAG, ARIA, leitores de tela). |
| `brand` | Identidade e voz de marca, guias de estilo. |
| `creative-media` | Peças visuais e mídia: banners, slides, arte generativa, GIF, imagens. |
| `ai-engineering` | Construir produtos com LLM: APIs de modelo, MCP servers, RAG, prompts, evals de produto, custo. |
| `agent-engineering` | Configurar e operar agentes de código: autoria de skills, harness, orquestração, subagentes, loops, memória, contexto. |
| `platform` | Git/GitHub, CI/CD, containers, deploy, observabilidade, SRE, incidentes. |
| `documents` | Documentos de escritório e escrita técnica/corporativa. |
| `research` | Pesquisa com fontes e citações, revisão de literatura. |
| `product` | Gestão de produto: PRD, priorização, síntese de feedback, experimentos. |
| `marketing` | SEO/AEO, conteúdo, social, e-mail, mídia paga. |
| `sales` | Prospecção, qualificação, propostas, pipeline. |
| `finance` | Contabilidade, FP&A, precificação, impostos. |
| `legal-compliance` | Contratos, conformidade regulatória, privacidade jurídica. |
| `operations` | Gestão de projetos, pessoas, suporte ao cliente, processos. |

| `science` | Ciência computacional e dados biomédicos de pesquisa; apoio clínico pertence a healthcare. |
| `games` | Regras, loops, progressão, níveis e implementação de jogos em engines, incluindo estado, cena, desempenho, áudio e multiplayer. Arte e interface genéricas continuam em creative-media/ui; programação genérica continua em languages. |
| `geospatial` | Análise e engenharia de dados georreferenciados: sistemas de referência, geometria, raster/vetor, cartografia e serviços GIS. ETL genérico continua em data e modelos genéricos em ai-engineering. |
| `extended-reality` | Aplicações imersivas AR/VR/XR: coordenadas espaciais, interação corporal, conforto, percepção e integração com runtimes espaciais. Jogos ficam em games; estilos visuais genéricos continuam em ui. |
| `healthcare` | Sistemas e interoperabilidade de saúde, preparação de evidência para profissionais e documentação clínica rastreável. Dados biomédicos para pesquisa continuam em science; revisão de literatura genérica em research; privacidade jurídica em legal-compliance. |
| `web3` | Construção e verificação de contratos e protocolos blockchain/DeFi. Auditoria genérica continua em security; contabilidade em finance; não oferece recomendação de investimento nem executa transações de valor real. |
| `infrastructure` | Infraestrutura de rede e laboratórios auto-hospedados: conectividade, segmentação, DNS, VPN, hardware, recuperação e operação local. CI/CD, deploy de aplicações e SRE genérico continuam em platform. |
| `logistics` | Planejamento de suprimentos e operação física de transporte, exceções, transportadoras, estoque e logística reversa. Gestão de projeto genérica fica em operations; segurança de dependências de software não é logística. |

Domínios novos exigem ADR. Outros nichos verticais vão para `catalog/exclusions.yaml` até haver demanda (ver ROADMAP).

### R2. Unicidade: uma capacidade, um artefato

- A chave do catálogo é `domínio/capacidade`. **Capacidade** é uma intenção de usuário distinta, expressa pelo gatilho da `description` ("use quando...").
- Dois artefatos do mesmo tipo com gatilhos sobrepostos são **duplicatas**, mesmo com nomes diferentes. Resolução: fundir no melhor, nunca manter os dois.
- Uma skill não pode atravessar domínios. Se cobre dois, é dividida (ex.: `ui-ux-pro-max` → conteúdo de UI em `ui`, diretrizes de UX em `ux`, acessibilidade em `accessibility`).
- Variações por linguagem/framework de uma mesma capacidade não são artefatos separados: viram `references/` do pacote da linguagem (R5).

### R3. Fronteira entre tipos de artefato

| Tipo | Quando existe | Proibido |
|---|---|---|
| **skill** | Unidade canônica de capacidade: procedimento, conhecimento ou checklist carregado sob demanda. | Duplicar outra skill; ter >500 linhas no `SKILL.md` (o excesso vai para `references/`). |
| **agent** | Só quando a capacidade precisa de contexto isolado, paralelismo ou restrição de ferramentas (ex.: revisor independente, explorador de código). O agent invoca skills; não copia o conteúdo delas. | Persona sem procedimento; agent que replica uma skill; um agent por linguagem. |
| **rule** | Orientação curta e sempre ativa (domínio `principles` e pacotes de linguagem). | Procedimento longo (vira skill). |
| **hook** | Guardrail determinístico e opt-in (bloquear comando destrutivo, formatar após edição). | Hook que injeta instruções de marketing/telemetria; hook ligado por padrão. |
| **workflow** | Orquestração declarativa de várias skills/agents com portões entre etapas (ex.: `feature-delivery`: ideação → spec → plano → TDD → review → conclusão). Substitui as famílias `orch-*`, `prp-*`, `multi-*` e `epic-*` do ECC. | Repetir o conteúdo das skills que orquestra; workflow de uma etapa só (isso é skill). |
| **prompt** | Texto reutilizável que **não** dispara sozinho: prompt de despacho de subagente, system prompt de produto, prompt de avaliação (LLM-as-judge). | Prompt que deveria ser skill (tem gatilho próprio). |
| **template** | Arquivo-modelo que o agente copia e preenche: `spec.md`, `plan.md`, `tasks.md`, ADR, `AGENTS.md`, corpo de PR, relatório de auditoria. Fica em `templates/` do domínio dono ou em `assets/` da skill que o usa. | Template sem skill/workflow que o use. |
| **knowledge** | Material de referência estático e citável que várias skills consultam (ex.: mapa OWASP/ASVS, catálogo de heurísticas de Nielsen, tabela de contraste WCAG). | Copiar material de licença não permissiva (vira link). |
| **eval** | Casos de teste de um artefato: gatilho (deve/não deve disparar) e tarefa (saída esperada). Cada artefato tem os seus em `evals/`; o `evals/` da raiz guarda os **evals de roteamento** entre domínios. | Artefato `stable` sem eval. |
| **profile** | Conjunto nomeado de artefatos de vários domínios para instalar junto (ex.: `fullstack-web`, `security-review`, `product-team`). Só referencia ids do catálogo. | Conter artefato próprio. |
| **command** | Não é artefato de fonte. Skills são invocáveis pelo usuário; comandos para harnesses que exigem (ex.: `.toml` do Gemini) são gerados na distribuição. | Comando escrito à mão que duplica skill. |
| **mcp** | Recomendação de servidor MCP com versão fixada e escopo de permissão documentado. | Empacotar servidor de terceiros; versão flutuante (`@latest`). |

Layout resultante por domínio: `domains/<domínio>/{skills,agents,workflows,prompts,rules,hooks,mcps,templates,knowledge,evals}/`. Pastas vazias não são criadas. Na raiz: `profiles/` e `evals/` (roteamento entre domínios).

### R4. Nomes

- kebab-case, em inglês, descritivo da capacidade (`test-driven-development`, `visual-design`), sem marca, sem superlativo (`pro`, `max`, `ultimate`, `v2`) e sem nome de autor.
- Único no repositório inteiro, não só no domínio (harnesses sem namespace colidem).
- No Claude Code o nome final fica `<domínio>:<skill>` pelo namespace do plugin.

### R5. Pacotes de linguagem

Cada linguagem tem **uma** skill (`<linguagem>`, ex.: `typescript`) com `references/` para padrões, testes, segurança, build e frameworks (`references/frameworks/django.md`). Skills genéricas de `testing`, `code-quality`, `debugging` e `security` carregam a referência da linguagem quando relevante. Isso substitui as ~80 variantes por linguagem do ECC.

### R6. Registro único

`catalog/catalog.yaml` lista cada artefato com: `id` (`domínio/nome`), `type`, `capability` (uma frase), `status` (`experimental` | `stable` | `deprecated`), `owner` e `supersedes` (ids das fontes fundidas). Nenhum arquivo em `domains/` existe sem entrada no catálogo, e vice-versa.

### R7. Exclusões explícitas

`catalog/exclusions.yaml` registra cada artefato upstream descartado com o motivo: `duplicate-of:<id>`, `out-of-scope`, `license`, `source-internal` (ferramenta da própria fonte), `low-quality` ou `vendor-specific`.

## Critérios de aceite

1. Todo artefato em `domains/` tem entrada em `catalog.yaml` e vice-versa (verificado no CI).
2. Nenhum par de skills do catálogo excede o limiar de similaridade de gatilho definido em `quality-gates` sem uma exceção registrada.
3. Nenhum nome publicado contém termos da lista de marcas/superlativos.
4. Toda entrada upstream do inventário aparece em `catalog.yaml` (`supersedes`) ou em `exclusions.yaml`.
5. Cada domínio de R1 tem um diretório em `domains/` com `plugin.json`, mesmo que vazio no início.

## Fora de escopo

- Escolher o conteúdo de cada domínio (cada `docs/specs/<domínio>/catalog/`).
- Tooling de CI (spec `quality-gates`) e empacotamento (spec `distribution`).
