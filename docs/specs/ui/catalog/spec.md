# Spec — Catálogo do domínio `ui`

- **Domínio:** ui
- **Status:** em implementação (Onda 2)
- **ADR:** [split-ui-ux-accessibility-brand](../../../adr/ui/split-ui-ux-accessibility-brand.md)
- **Fronteira:** interface visual — direção estética, tipografia, cor, layout, tokens, design system, componentes, acabamento.

## Resultado

| Artefato | Base | Fundidos |
|---|---|---|
| `visual-design` | Hallmark (portões Floor/Reflex/Finish, temas, lint em navegador real, revisor de contexto limpo, modos redesign/audit) | Anthropic `frontend-design` (direção estética, Apache-2.0, `LICENSE-frontend-design.txt` e aviso mantidos); ECC `frontend-design-direction`; agency *UI Designer*, *UI Finish-Gate Reviewer*; ui-ux-pro-max `design-review` |
| `design-system` | ui-ux-pro-max (motor de busca sobre CSVs de estilos, paletas, tipografia, gráficos, ícones, landing, stacks e diretrizes de interação; gera design system mestre com overrides) | ui-ux-pro-max `design-system` (tokens em três camadas), ECC `design-system` (extração de tokens de código existente) |

## Decisões de conteúdo

- O motor do ui-ux-pro-max fica inteiro: seus dados de "UX" são regras de implementação de interface (navegação, formulários, feedback), consultadas por `ux:usability-review` via `--domain ux`. O domínio `ux` cuida de pesquisa e avaliação.
- **Resíduo de marca aceito:** os scripts do Hallmark usam `.hallmark/`, `HALLMARK_*` e `hallmarkSlots` como identificadores, e as páginas geradas levam carimbos `/* Hallmark · ... */` que os scripts leem. Renomear exige reescrever e testar os scripts; fica para quando houver testes deles rodando aqui.
- Serviços externos: fotos referenciadas por URL do Wikimedia Commons (com crédito obrigatório CC BY/BY-SA), fontes do Google Fonts/Fontshare, e o passo opcional de *comp* via Together AI (só com `TOGETHER_API_KEY`, pago).

## Pendências

- Rodar os testes do Hallmark (`capture.test.mjs`, `theme.test.mjs`) e do motor de busca do ui-ux-pro-max (`scripts/tests`): é código do upstream, precisa de aprovação para executar.
- Decidir ECC `motion-foundations`/`motion-patterns`/`motion-advanced`, `make-interfaces-feel-better`, `taste*` e ui-ux-pro-max `ui-styling` (shadcn/Tailwind).

## Passada final (bundle [`gaps.yaml`](../../../../catalog/decisions/bundles/gaps.yaml))

Adicionados: `motion-and-polish` (base ECC `motion-foundations`; `motion-patterns`, `motion-advanced`, `make-interfaces-feel-better`, `taste*`, rule `web/design-quality`, *Whimsy Injector*) e `component-styling` (base ui-ux-pro-max `ui-styling`; *Frontend Developer*, CSS de *UX Architect*).
