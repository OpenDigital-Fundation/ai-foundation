# Spec — Curadoria das fontes

- **Domínio:** foundation
- **Status:** proposta para revisão
- **Depende de:** [catalog-governance](../catalog-governance/spec.md)
- **ADRs:** [license-and-provenance](../../../adr/foundation/license-and-provenance.md), [pinned-upstream-snapshots](../../../adr/foundation/pinned-upstream-snapshots.md)

## Problema

Precisamos tirar "o melhor" de dez fontes sem copiar duplicatas, sem violar licenças e sem perder a rastreabilidade de onde cada trecho veio.

## Fontes e licenças (snapshot de 2026-11-06)

| Fonte | Commit | Licença | Uso permitido | Pontos fortes observados |
|---|---|---|---|---|
| `obra/superpowers` | `22f0b46` | MIT | copiar/fundir | Disciplina de processo: brainstorming, planos, TDD, debugging sistemático, verificação, subagentes, worktrees |
| `mattpocock/skills` | `4ae2317` | MIT | copiar/fundir | Skills curtas e afiadas: grilling, domain modeling, deep modules, triage, to-spec/to-tickets, handoff, writing-for-agents |
| `affaan-m/ECC` | `b38be6a` | MIT | copiar/fundir | Amplitude: 314 skills, 71 agents, 98 commands, rules por linguagem, hooks; muita duplicação interna |
| `multica-ai/andrej-karpathy-skills` | `2c60614` | MIT (README) | copiar/fundir | 4 princípios de comportamento ao programar |
| `msitarzewski/agency-agents` | `b859c51` | MIT | copiar/fundir | 283 personas por divisão (engenharia, design, marketing, vendas...) |
| `anthropics/skills` | `ca45fc4` | Apache-2.0 por skill; **docx/pdf/pptx/xlsx proprietárias** | copiar Apache com NOTICE; proprietárias só referenciar | skill-creator, mcp-builder, frontend-design, webapp-testing, doc-coauthoring, formato Agent Skills |
| `nextlevelbuilder/ui-ux-pro-max-skill` | `b7d5353` | MIT | copiar/fundir (dividindo) | Bases de dados de estilos, paletas, pares tipográficos, diretrizes de UX por stack |
| `Nutlope/hallmark` | `407fa68` | MIT | copiar/fundir | Portões anti-"cara de IA" em camadas (Floor/Reflex/Finish), lint em navegador real, revisor de contexto limpo |
| `DietrichGebert/ponytail` | `96608e0` | MIT | copiar/fundir | Menor mudança que resolve, níveis de rigor, review/audit em linguagem simples, ledger de atalhos (`shortcut:`) |
| `SecurityStandards/skill-security-audit` | `c1c8a8c` | MIT (Cloudflare) | copiar/fundir | Auditoria de segurança multi-fase com achados verificados e legíveis por máquina |
| `SecurityStandards/agent-reverse-engineer` | `f254f5a` | MIT | referenciar (é um produto/MCP, não skill) | Engenharia reversa com agentes |
| `SecurityStandards/agent-pentester` (Shannon) | `2468b67` | **AGPL-3.0** | **só referenciar** | Pentest autônomo de web/API |
| `SecurityStandards/security-standards` | `3bd356a` | sem licença declarada | **só referenciar** | Políticas, frameworks, questionários |
| `SecurityStandards/CTOSecurityChecklist`, `DevOpsSecurityChecklist` | `aeea8c3`, `568f21f` | **CC BY-NC-SA 4.0** | **só referenciar** (uso comercial vedado) | Checklists de SaaS e DevOps |

## Inventário

[`catalog/inventory/artifacts.csv`](../../../../catalog/inventory/artifacts.csv) lista as observações upstream com fonte, tipo, nome, caminho, licença, **domínio sugerido** e descrição. O universo atual é calculado a partir do arquivo, distinguindo observações de chaves únicas de decisão (`source:kind:name`); rules sem frontmatter são distinguidas pelo caminho.

O domínio sugerido vem de uma classificação por palavras-chave, **não revisada**. Distribuição: 243 fora de escopo, 163 agent-engineering, 79 code-quality, 62 workflow, 56 languages, 48 testing, 37 platform, 32 ai-engineering, 32 security, 28 debugging, 27 sem domínio, e os demais domínios com menos de 30 cada. Cada spec de domínio confirma ou corrige a classificação dos itens dela.

## Requisitos

- **R1.** `catalog/sources.lock.yaml` registra cada fonte com URL, commit, licença e política (`merge` | `reference`).
- **R2.** Cada artefato upstream recebe exatamente uma decisão: `keep` (adotar com ajustes mínimos), `merge` (fundir em outro), `split` (dividir entre domínios), `reference` (link externo) ou `exclude` (com motivo de `exclusions.yaml`).
- **R3.** Critério de escolha da base numa fusão, em ordem: (1) licença permissiva; (2) procedimento verificável (passos e critério de saída) acima de lista de dicas; (3) menor tamanho para a mesma cobertura; (4) evals ou testes já existentes na fonte; (5) manutenção ativa.
- **R4.** Todo arquivo copiado ou fundido gera entrada em `domains/<d>/PROVENANCE.yaml`: fonte, commit, caminho original, licença, tipo de modificação. Arquivos Apache-2.0 mantêm o aviso de modificação exigido pela licença; o repositório tem `THIRD_PARTY_NOTICES.md`.
- **R5.** Conteúdo `reference` aparece só como link e descrição própria, nunca como texto copiado.
- **R6.** Remover de toda cópia: telemetria, auto-update, instruções de autopromoção ("use sempre esta skill antes de qualquer resposta"), referências a produtos da fonte e caminhos absolutos.

## Critérios de aceite

1. `sources.lock.yaml` com todas as fontes da tabela.
2. Cada linha de `inventory.csv` tem decisão registrada em `catalog.yaml` (`supersedes`) ou `exclusions.yaml`.
3. Nenhum arquivo de fonte `reference` (AGPL, NC, proprietária, sem licença) está copiado no repositório (verificado por hash no CI).
4. `THIRD_PARTY_NOTICES.md` lista todas as fontes `merge`.

## Fora de escopo

Escrever o conteúdo final das skills (specs de domínio).
