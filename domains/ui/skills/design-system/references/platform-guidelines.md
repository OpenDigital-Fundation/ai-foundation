# Platform guidelines and public design systems

Reference for `ui:design-system`. When a product targets a platform or a public-sector context, its guidelines set expectations users already have (Jakob's law). Follow them unless a tested reason says otherwise, and record the deviation.

## Which guideline applies

| Context | Primary reference | Notes |
|---|---|---|
| iOS, iPadOS, macOS, watchOS, visionOS | [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) | Navigation patterns, system controls, typography (Dynamic Type), safe areas |
| Android and Google products | [Material Design 3](https://m3.material.io/) | Components, design tokens, dynamic colour, adaptive layouts |
| Windows and Microsoft 365 | [Fluent 2](https://fluent2.microsoft.design/) | Desktop density, keyboard-heavy workflows |
| Enterprise dashboards, data tables, admin tools | [IBM Carbon](https://carbondesignsystem.com/) | Dense data, complex forms, data visualisation |
| Brazilian federal digital services | [Padrão Digital de Governo (GOV.BR DS)](https://www.gov.br/ds/) | Required look and behaviour for federal services; pairs with eMAG and ABNT NBR 17225 |
| UK public services | [GOV.UK Design System](https://design-system.service.gov.uk/) | Strong guidance on forms, questions one at a time, plain language |
| Collaboration and developer tools | [Atlassian Design System](https://atlassian.design/) | Content and voice guidance alongside components |
| Commerce admin | [Shopify Polaris](https://polaris.shopify.com/) | Merchant workflows, content guidelines |

Cross-platform products (React Native, Flutter, web apps installed on phones) should still respect each platform's navigation and system gestures; do not ship iOS back gestures on Android or the reverse.

## Minimum target sizes

| Source | Minimum | Status |
|---|---|---|
| WCAG 2.2, SC 2.5.8 Target Size (Minimum) | 24 × 24 CSS px, or enough spacing around smaller targets | Level AA, with exceptions (inline links, equivalent control elsewhere, essential) |
| WCAG 2.2, SC 2.5.5 Target Size (Enhanced) | 44 × 44 CSS px | Level AAA |
| Apple HIG | 44 × 44 pt hit area for controls | Platform guideline |
| Material Design | 48 × 48 dp touch target | Platform guideline |

Design to the platform size; treat the WCAG minimum as the floor that must never be broken.

## Using a public design system well

1. **Adopt tokens before components.** Colour, type, spacing and elevation tokens carry most of the consistency; map them to this skill's three-layer token model (`references/token-architecture.md`).
2. **Prefer the system's component over a custom one.** Custom components need their own accessibility work: keyboard support, focus order, ARIA roles and states.
3. **Keep the system's interaction rules,** not only its look: validation timing, error placement, loading and empty states.
4. **Check the licence** before copying code, icons or fonts from a design system; many publish code under open-source licences but keep brand assets and fonts under separate terms. Link to the guideline instead of copying its text.
5. **Version the dependency** and track upstream changes; public systems deprecate components.

## Related

- Heuristics and laws that justify following conventions: `ux:usability-review` (`references/heuristics-and-laws.md`).
- Accessibility standards and their legal weight: `accessibility:wcag-accessibility` (`references/standards-map.md`).
