# Separar UI, UX, acessibilidade, marca e mídia
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** ui

## Contexto

`ui-ux-pro-max` mistura direção visual, diretrizes de UX, acessibilidade, gráficos e stacks; `design` (mesma fonte) junta marca, logo, CIP, slides, banners e ícones. Hallmark, `frontend-design` (Anthropic), `frontend-design-direction`/`taste` (ECC) e as personas UI/UX do agency-agents se sobrepõem em partes.

## Decisão

Cinco domínios: `ui` (visual e componentes), `ux` (pesquisa, fluxos, usabilidade, microcopy), `accessibility` (WCAG e auditoria), `brand` (identidade e voz) e `creative-media` (banners, slides, arte, GIF). A base de `ui/visual-design` são os portões em camadas do Hallmark (Floor/Reflex/Finish e revisor de contexto limpo), enriquecidos com a direção estética do `frontend-design` e as bases de dados (estilos, paletas, pares tipográficos) do ui-ux-pro-max como `knowledge/`. Diretrizes de UX do ui-ux-pro-max vão para `ux`; checagens de contraste/foco/movimento são referenciadas de `accessibility`, que é a dona delas.

## Consequências

- Cada pedido dispara uma skill clara.
- `ui/visual-design` depende de `accessibility` para o piso de qualidade, sem duplicar as regras.
