# Spec — Catálogo do domínio `accessibility`

- **Domínio:** accessibility
- **Status:** em implementação (Onda 2)
- **Fronteira:** conformidade e auditoria de acessibilidade (WCAG, ARIA, tecnologia assistiva).

## Resultado

| Artefato | Base | Fundidos |
|---|---|---|
| `wcag-accessibility` | ECC `accessibility` (WCAG 2.2 AA, web, iOS e Android) | ECC `frontend-a11y` (React/Next.js), agent `a11y-architect` (checklist e registro de decisão), rule `react-native/accessibility`; agency *Accessibility Auditor* (método com leitor de tela e relatório) |

`ui:visual-design` chama esta skill nos portões Floor; não duplica as regras. *Section 508 Accessibility Specialist* foi excluído (procurement federal dos EUA; coberto por WCAG 2.2 AA). *Inclusive Visuals Specialist* fica para `creative-media`.
