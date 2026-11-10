# Component styling — README

Part of `ui:component-styling`.

## HTML CSS Style Color Guide

<!-- source: github/awesome-copilot instructions/html-css-style-color-guide.instructions.md -->

Follow these guidelines when updating or creating HTML/CSS styles for browser rendering. Color names
represent the full spectrum of their respective hue ranges (e.g., "blue" includes navy, sky blue, etc.).

### Color Definitions

- **Hot Colors**: Oranges, reds, and yellows
- **Cool Colors**: Blues, greens, and purples
- **Neutral Colors**: Grays and grayscale variations
- **Binary Colors**: Black and white
- **60-30-10 Rule**
  - **Primary Color**: Use 60% of the time (*cool or light color*)
  - **Secondary Color**: Use 30% of the time (*cool or light color*)
  - **Accent**: Use 10% of the time (*complementary hot color*)

### Color Usage Guidelines

Balance the colors used by applying the **60-30-10 rule** to graphic design elements like backgrounds,
buttons, cards, etc...

#### Background Colors

**Never Use:**

- Purple or magenta
- Red, orange, or yellow
- Pink
- Any hot color

**Recommended:**

- White or off-white
- Light cool colors (e.g., light blues, light greens)
- Subtle neutral tones
- Light gradients with minimal color shift

#### Text Colors

**Never Use:**

- Yellow (poor contrast and readability)
- Pink
- Pure white or light text on light backgrounds
- Pure black or dark text on dark backgrounds

**Recommended:**

- Dark neutral colors (e.g., #1f2328, #24292f)
- Near-black variations (#000000 to #333333)
  - Ensure background is a light color
- Dark grays (#4d4d4d, #6c757d)
- High-contrast combinations for accessibility
- Near-white variations (#ffffff to #f0f2f3)
  - Ensure background is a dark color

#### Colors to Avoid

Unless explicitly required by design specifications or user request, avoid:

- Bright purples and magentas
- Bright pinks and neon colors
- Highly saturated hot colors
- Colors with low contrast ratios (fails WCAG accessibility standards)

#### Colors to Use Sparingly

**Hot Colors** (red, orange, yellow):

- Reserve for critical alerts, warnings, or error messages
- Use only when conveying urgency or importance
- Limit to small accent areas rather than large sections
- Consider alternatives like icons or bold text before using hot colors

### Gradients

Apply gradients with subtle color transitions to maintain professional aesthetics.

#### Best Practices

- Keep color shifts minimal (e.g., #E6F2FF to #F5F7FA)
- Use gradients within the same color family
- Avoid combining hot and cool colors in a single gradient
- Prefer linear gradients over radial for backgrounds

#### Appropriate Use Cases

- Background containers and sections
- Button hover states and interactive elements
- Drop shadows and depth effects
- Header and navigation bars
- Card components and panels

### Additional Resources

- [Color Tool](https://civicactions.github.io/uswds-color-tool/)
- [Government or Professional Color Standards](https://designsystem.digital.gov/design-tokens/color/overview/)
- [UI Color Palette Best Practices](https://www.interaction-design.org/literature/article/ui-color-palette)
- [Color Combination Resource](https://www.figma.com/resource-library/color-combinations/)

## Tailwind CSS v4+ Installation with Vite

<!-- source: github/awesome-copilot instructions/tailwind-v4-vite.instructions.md -->

Instructions for installing and configuring Tailwind CSS version 4 and above using the official Vite plugin. Tailwind CSS v4 introduces a simplified setup that eliminates the need for PostCSS configuration and tailwind.config.js in most cases.

### Key Changes in Tailwind CSS v4

- **No PostCSS configuration required** when using the Vite plugin
- **No tailwind.config.js required** - configuration is done via CSS
- **New @tailwindcss/vite plugin** replaces the PostCSS-based approach
- **CSS-first configuration** using `@theme` directive
- **Automatic content detection** - no need to specify content paths

### Installation Steps

#### Step 1: Install Dependencies

Install `tailwindcss` and the `@tailwindcss/vite` plugin:

```bash
npm install tailwindcss @tailwindcss/vite
```

#### Step 2: Configure Vite Plugin

Add the `@tailwindcss/vite` plugin to your Vite configuration file:

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
})
```

For React projects with Vite:

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
```

#### Step 3: Import Tailwind CSS

Add the Tailwind CSS import to your main CSS file (e.g., `src/index.css` or `src/App.css`):

```css
@import "tailwindcss";
```

#### Step 4: Verify CSS Import in Entry Point

Ensure your main CSS file is imported in your application entry point:

```typescript
// src/main.tsx or src/main.ts
import './index.css'
```

#### Step 5: Start Development Server

Run the development server to verify installation:

```bash
npm run dev
```

### What NOT to Do in Tailwind v4

#### Do NOT Create tailwind.config.js

Tailwind v4 uses CSS-first configuration. Do not create a `tailwind.config.js` file unless you have specific legacy requirements.

```javascript
// ❌ NOT NEEDED in Tailwind v4
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

#### Do NOT Create postcss.config.js for Tailwind

When using the `@tailwindcss/vite` plugin, PostCSS configuration for Tailwind is not required.

```javascript
// ❌ NOT NEEDED when using @tailwindcss/vite
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

#### Do NOT Use Old Directives

The old `@tailwind` directives are replaced by a single import:

```css
/* ❌ OLD - Do not use in Tailwind v4 */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ✅ NEW - Use this in Tailwind v4 */
@import "tailwindcss";
```

### CSS-First Configuration (Tailwind v4)

#### Custom Theme Configuration

Use the `@theme` directive in your CSS to customize your design tokens:

```css
@import "tailwindcss";

@theme {
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --font-sans: 'Inter', system-ui, sans-serif;
  --radius-lg: 0.75rem;
}
```

#### Adding Custom Utilities

Define custom utilities directly in CSS:

```css
@import "tailwindcss";

@utility content-auto {
  content-visibility: auto;
}

@utility scrollbar-hidden {
  scrollbar-width: none;
  &::-webkit-scrollbar {
    display: none;
  }
}
```

#### Adding Custom Variants

Define custom variants in CSS:

```css
@import "tailwindcss";

@variant hocus (&:hover, &:focus);
@variant group-hocus (:merge(.group):hover &, :merge(.group):focus &);
```

### Verification Checklist

After installation, verify:

- [ ] `tailwindcss` and `@tailwindcss/vite` are in `package.json` dependencies
- [ ] `vite.config.ts` includes the `tailwindcss()` plugin
- [ ] Main CSS file contains `@import "tailwindcss";`
- [ ] CSS file is imported in the application entry point
- [ ] Development server runs without errors
- [ ] Tailwind utility classes (e.g., `text-blue-500`, `p-4`) render correctly

### Example Usage

Test the installation with a simple component:

```tsx
export function TestComponent() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <h1 className="text-3xl font-bold text-blue-600 underline">
        Hello, Tailwind CSS v4!
      </h1>
    </div>
  )
}
```

### Troubleshooting

#### Styles Not Applying

1. Verify CSS import statement is `@import "tailwindcss";` (not old directives)
2. Ensure CSS file is imported in your entry point
3. Check Vite config includes the `tailwindcss()` plugin
4. Clear Vite cache: `rm -rf node_modules/.vite && npm run dev`

#### Plugin Not Found Error

If you see "Cannot find module '@tailwindcss/vite'":

```bash
npm install @tailwindcss/vite
```

#### TypeScript Errors

If TypeScript cannot find types for the Vite plugin, ensure you have the correct import:

```typescript
import tailwindcss from '@tailwindcss/vite'
```

### Migration from Tailwind v3

If migrating from Tailwind v3:

1. Remove `tailwind.config.js` (move customizations to CSS `@theme`)
2. Remove `postcss.config.js` (if only used for Tailwind)
3. Uninstall old packages: `npm uninstall postcss autoprefixer`
4. Install new packages: `npm install tailwindcss @tailwindcss/vite`
5. Replace `@tailwind` directives with `@import "tailwindcss";`
6. Update Vite config to use `@tailwindcss/vite` plugin

### Reference

- Official Documentation: https://tailwindcss.com/docs/installation/using-vite
- Tailwind CSS v4 Upgrade Guide: https://tailwindcss.com/docs/upgrade-guide

## Bulma v1

<!-- source: github/awesome-copilot instructions/bulma-v1.instructions.md -->

Bulma v1 is a rewrite of the Bulma CSS framework on Dart Sass and CSS variables. Most tutorials and older code show Bulma 0.9, so follow these rules when you write or review Bulma code.

### Key changes in Bulma v1

- **Same HTML, except tiles.** Class names did not change, so most 0.9 markup still renders. Tiles were removed.
- **Dart Sass only.** Build with the `sass` package. `node-sass` and LibSass can't compile it.
- **Sass modules.** Customize with `@use "bulma/sass" with (...)`. Setting variables and then calling `@import "bulma"` is the 0.9 pattern.
- **CSS variables.** Every component reads variables prefixed `--bulma-`, so you can theme with plain CSS and no build step.
- **Themes and dark mode.** A light theme and a dark theme ship by default. The dark theme follows the user's system setting.
- **Color palettes.** Each of the 7 main colors gets soft, bold, light, dark, invert and 21 numbered shades.
- **Grid.** The smart grid and fixed grid replace tiles.
- **Skeletons.** Loading placeholders, as standalone blocks and as an `is-skeleton` modifier.
- **Prefixed builds.** A prebuilt version prefixes every class with `bulma-`.

### Installation

```bash
npm install bulma
```

Import the compiled CSS once:

```js
import 'bulma/css/bulma.min.css';
```

Or load it from a CDN:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.4/css/bulma.min.css" />
```

Other builds live in `bulma/css/versions/`:

| File                            | Use it when                                          |
| ------------------------------- | ---------------------------------------------------- |
| `bulma-prefixed.css`            | Bulma has to share a page with another CSS framework |
| `bulma-no-helpers.css`          | You only want components, not the `has-*` helpers    |
| `bulma-no-helpers-prefixed.css` | Both of the above                                    |
| `bulma-no-dark-mode.css`        | The site should always render in the light theme     |

### Customizing with Sass

Pass variables through `@use ... with`:

```scss
@use "bulma/sass" with (
  $primary: #8a4d76,
  $link: #fa7c91,
  $family-primary: '"Nunito", sans-serif'
);
```

- Don't generate `$primary: ...;` followed by `@import "bulma";`. That is the 0.9 setup, and Sass has deprecated `@import`.
- Import only what you need by loading the utilities first and then single modules, for example `@use "bulma/sass/utilities" with (...)` and `@use "bulma/sass/form"`.
- Several component variables are now split into hue, saturation and lightness (`$input-h`, `$input-s`, `$input-background-l`). A variable name from a 0.9 tutorial may no longer exist. Check Bulma's list of Sass variables before using one.

### Customizing with CSS variables

You can change colors at runtime without Sass. Main colors are built from hue, saturation and lightness variables, so overriding those updates every shade derived from them:

```css
/* Load after Bulma */
:root {
  --bulma-primary-h: 280deg;
  --bulma-primary-s: 60%;
  --bulma-primary-l: 45%;
}
```

- Scope variables to a component to change one part only, for example `.button { --bulma-button-border-width: 2px; }`.
- In your own CSS, read Bulma's values with `var(--bulma-...)` instead of copying hex codes, so custom styles follow the theme.

### Dark mode

- The page is light by default and turns dark when the user's system prefers dark.
- Force a theme with `data-theme="dark"` or the `theme-dark` class, on `<html>` or on any element. `data-theme="light"` and `theme-light` force light.
- Use `bulma-no-dark-mode.css` if the site should never switch.
- Pair **soft** backgrounds with **bold** text, for example `has-background-primary-soft has-text-primary-bold`. Soft and bold swap in dark mode, so the contrast holds.
- Avoid fixed colors such as `has-background-white` or hard-coded hex values for page surfaces. In custom CSS use `var(--bulma-scheme-main)` for the page background so it follows the theme.

### Layout

Tiles (`tile is-ancestor`, `is-parent`, `is-child`) are gone from Bulma v1, so that markup gets no styles. Use the smart grid, which fits as many cells per row as their minimum width allows:

```html
<div class="grid">
  <div class="cell">One</div>
  <div class="cell">Two</div>
  <div class="cell is-col-span-2">Three, two columns wide</div>
</div>
```

For a set number of columns, wrap the grid in `fixed-grid`:

```html
<div class="fixed-grid has-3-cols">
  <div class="grid">
    <div class="cell">One</div>
    <div class="cell">Two</div>
    <div class="cell">Three</div>
  </div>
</div>
```

- Cells take `is-col-span-*`, `is-row-span-*`, `is-col-start-*` and `is-row-start-*`.
- `columns` and `column` (with sizes like `is-half` or `is-one-third`) still work for a single flex row.

### Skeletons

- Add `is-skeleton` to a component to show its loading state, for example `button is-skeleton`, `input is-skeleton` or `image is-64x64 is-skeleton`.
- Use `skeleton-block` for a plain placeholder box and `skeleton-lines` with empty child `div`s for text lines.

### Bulma has no JavaScript

- Bulma is CSS only. The navbar burger, dropdowns, modals and tabs need your own code to toggle `is-active`.
- In React or Vue, a Bulma component library such as [Bestax](https://bestax.io) or [Buefy](https://buefy.org) handles that state for you. Keep using the one the project already has.
- Don't add Bootstrap attributes such as `data-bs-toggle`. They do nothing in Bulma.
- Don't mix in Bootstrap or Tailwind classes. Use Bulma's own names: `button` not `btn`, `column is-half` not `col-md-6`, `is-flex` not `d-flex`, `mt-4` and `px-2` for spacing, `has-text-centered` for alignment.
