# Accessibility audit — derived guides

Part of `accessibility:accessibility-audit`.

## Accessibility Auditor

<!-- source: davila7/claude-code-templates cli-tool/components/skills/creative-design/accessibility-auditor/SKILL.md#common-accessibility-issues-fixes -->

### Common Accessibility Issues & Fixes

#### 1. Missing Alt Text for Images

**❌ Problem:**
```html
<img src="/products/shoes.jpg">
```

**✅ Solution:**
```html
<!-- Informative image -->
<img src="/products/shoes.jpg" alt="Red Nike Air Max running shoes with white swoosh">

<!-- Decorative image -->
<img src="/decorative-pattern.svg" alt="" role="presentation">

<!-- Logo that links -->
<a href="/">
  <img src="/logo.png" alt="Company Name - Home">
</a>
```

**Rules:**
- Informative images: Describe the content/function
- Decorative images: Use empty alt (alt="")
- Functional images: Describe the action
- Complex images: Provide detailed description nearby

#### 2. Low Color Contrast

**❌ Problem:**
```css
/* Contrast ratio 2.5:1 - Fails WCAG */
.text {
  color: #767676;
  background: #ffffff;
}
```

**✅ Solution:**
```css
/* Contrast ratio 4.5:1+ - Passes AA */
.text {
  color: #595959;
  background: #ffffff;
}

/* Contrast ratio 7:1+ - Passes AAA */
.text-high-contrast {
  color: #333333;
  background: #ffffff;
}
```

**Requirements:**
- Normal text (< 18px): 4.5:1 minimum (AA), 7:1 enhanced (AAA)
- Large text (≥ 18px or ≥ 14px bold): 3:1 minimum (AA), 4.5:1 enhanced (AAA)
- UI components and graphics: 3:1 minimum

#### 3. Non-Semantic HTML

**❌ Problem:**
```html
<div class="button" onclick="submitForm()">Submit</div>
<div class="heading">Page Title</div>
<div class="nav-menu">...</div>
```

**✅ Solution:**
```html
<button type="submit" onclick="submitForm()">Submit</button>
<h1>Page Title</h1>
<nav aria-label="Main navigation">...</nav>
```

**Semantic Elements:**
- `<button>` for buttons
- `<a>` for links
- `<h1>` - `<h6>` for headings (hierarchical)
- `<nav>`, `<main>`, `<aside>`, `<article>`, `<section>` for landmarks
- `<ul>`, `<ol>`, `<li>` for lists
- `<table>`, `<th>`, `<td>` for tabular data

#### 4. Missing Form Labels

**❌ Problem:**
```html
<input type="email" placeholder="Enter your email">
```

**✅ Solution:**
```html
<!-- Explicit label -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email">

<!-- Implicit label -->
<label>
  Email Address
  <input type="email" name="email">
</label>

<!-- Hidden label (for tight layouts) -->
<label for="search" class="sr-only">Search</label>
<input type="text" id="search" placeholder="Search...">
```

**Best Practices:**
- Every form field must have an associated label
- Labels should be visible (don't rely on placeholder)
- Use aria-label only when visual label isn't possible
- Group related fields with `<fieldset>` and `<legend>`

#### 5. Keyboard Navigation Issues

**❌ Problem:**
```html
<div onclick="handleClick()">Click me</div>
<a href="javascript:void(0)" onclick="doSomething()">Action</a>
```

**✅ Solution:**
```html
<!-- Use proper button -->
<button onclick="handleClick()">Click me</button>

<!-- If div required, make it accessible -->
<div
  role="button"
  tabindex="0"
  onclick="handleClick()"
  onkeydown="handleKeyPress(event)"
>
  Click me
</div>

<script>
function handleKeyPress(event) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    handleClick();
  }
}
</script>
```

**Keyboard Requirements:**
- All interactive elements must be keyboard accessible
- Visible focus indicators (outline or custom styling)
- Logical tab order (matches visual flow)
- Skip links for repetitive content
- No keyboard traps (users can navigate away)

#### 6. Missing ARIA Landmarks

**❌ Problem:**
```html
<div class="header">...</div>
<div class="main-content">...</div>
<div class="sidebar">...</div>
<div class="footer">...</div>
```

**✅ Solution:**
```html
<header role="banner">
  <nav aria-label="Main navigation">...</nav>
</header>

<main role="main">
  <h1>Page Title</h1>
  <article>...</article>
</main>

<aside role="complementary" aria-label="Related articles">
  ...
</aside>

<footer role="contentinfo">
  ...
</footer>
```

**Common Landmarks:**
- `banner` - Site header
- `navigation` - Navigation menus
- `main` - Primary content (one per page)
- `complementary` - Supporting content
- `contentinfo` - Site footer
- `search` - Search functionality
- `form` - Form regions

#### 7. Inaccessible Modals/Dialogs

**❌ Problem:**
```html
<div class="modal">
  <div class="content">
    Modal content
    <button onclick="closeModal()">Close</button>
  </div>
</div>
```

**✅ Solution:**
```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-desc">Are you sure you want to delete this item?</p>

  <button onclick="confirmAction()">Confirm</button>
  <button onclick="closeModal()">Cancel</button>
</div>

<script>
// Focus management
function openModal() {
  const modal = document.querySelector('[role="dialog"]');
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );

  // Store previous focus
  previousFocus = document.activeElement;

  // Focus first element
  focusableElements[0].focus();

  // Trap focus
  modal.addEventListener('keydown', trapFocus);
}

function closeModal() {
  // Return focus
  if (previousFocus) previousFocus.focus();
}

function trapFocus(event) {
  if (event.key !== 'Tab') return;

  const focusableElements = Array.from(
    modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
  );

  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  if (event.shiftKey && document.activeElement === firstElement) {
    lastElement.focus();
    event.preventDefault();
  } else if (!event.shiftKey && document.activeElement === lastElement) {
    firstElement.focus();
    event.preventDefault();
  }
}
</script>
```

**Modal Requirements:**
- `role="dialog"` or `role="alertdialog"`
- `aria-modal="true"` to indicate modal behavior
- `aria-labelledby` pointing to title
- `aria-describedby` for description (optional)
- Focus management (trap and restore)
- Close on Escape key
- Prevent background scrolling

#### 8. Missing Skip Links

**✅ Solution:**
```html
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<header>
  <nav>...</nav>
</header>

<main id="main-content" tabindex="-1">
  <!-- Page content -->
</main>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
</style>
```

## Accessibility (a11y)

<!-- source: davila7/claude-code-templates cli-tool/components/skills/development/accessibility/SKILL.md#perceivable,understandable,robust -->

### Perceivable

#### Text alternatives (1.1)

**Images require alt text:**
```html
<!-- ❌ Missing alt -->
<img src="chart.png">

<!-- ✅ Descriptive alt -->
<img src="chart.png" alt="Bar chart showing 40% increase in Q3 sales">

<!-- ✅ Decorative image (empty alt) -->
<img src="decorative-border.png" alt="" role="presentation">

<!-- ✅ Complex image with longer description -->
<figure>
  <img src="infographic.png" alt="2024 market trends infographic" 
       aria-describedby="infographic-desc">
  <figcaption id="infographic-desc">
    <!-- Detailed description -->
  </figcaption>
</figure>
```

**Icon buttons need accessible names:**
```html
<!-- ❌ No accessible name -->
<button><svg><!-- menu icon --></svg></button>

<!-- ✅ Using aria-label -->
<button aria-label="Open menu">
  <svg aria-hidden="true"><!-- menu icon --></svg>
</button>

<!-- ✅ Using visually hidden text -->
<button>
  <svg aria-hidden="true"><!-- menu icon --></svg>
  <span class="visually-hidden">Open menu</span>
</button>
```

**Visually hidden class:**
```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

#### Color contrast (1.4.3, 1.4.6)

| Text Size | AA minimum | AAA enhanced |
|-----------|------------|--------------|
| Normal text (< 18px / < 14px bold) | 4.5:1 | 7:1 |
| Large text (≥ 18px / ≥ 14px bold) | 3:1 | 4.5:1 |
| UI components & graphics | 3:1 | 3:1 |

```css
/* ❌ Low contrast (2.5:1) */
.low-contrast {
  color: #999;
  background: #fff;
}

/* ✅ Sufficient contrast (7:1) */
.high-contrast {
  color: #333;
  background: #fff;
}

/* ✅ Focus states need contrast too */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

**Don't rely on color alone:**
```html
<!-- ❌ Only color indicates error -->
<input class="error-border">
<style>.error-border { border-color: red; }</style>

<!-- ✅ Color + icon + text -->
<div class="field-error">
  <input aria-invalid="true" aria-describedby="email-error">
  <span id="email-error" class="error-message">
    <svg aria-hidden="true"><!-- error icon --></svg>
    Please enter a valid email address
  </span>
</div>
```

#### Media alternatives (1.2)

```html
<!-- Video with captions -->
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="en" label="English" default>
  <track kind="descriptions" src="descriptions.vtt" srclang="en" label="Descriptions">
</video>

<!-- Audio with transcript -->
<audio controls>
  <source src="podcast.mp3" type="audio/mp3">
</audio>
<details>
  <summary>Transcript</summary>
  <p>Full transcript text...</p>
</details>
```

---

### Understandable

#### Page language (3.1.1)

```html
<!-- ❌ No language specified -->
<html>

<!-- ✅ Language specified -->
<html lang="en">

<!-- ✅ Language changes within page -->
<p>The French word for hello is <span lang="fr">bonjour</span>.</p>
```

#### Consistent navigation (3.2.3)

```html
<!-- Navigation should be consistent across pages -->
<nav aria-label="Main">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

#### Form labels (3.3.2)

```html
<!-- ❌ No label association -->
<input type="email" placeholder="Email">

<!-- ✅ Explicit label -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" 
       autocomplete="email" required>

<!-- ✅ Implicit label -->
<label>
  Email address
  <input type="email" name="email" autocomplete="email" required>
</label>

<!-- ✅ With instructions -->
<label for="password">Password</label>
<input type="password" id="password" 
       aria-describedby="password-requirements">
<p id="password-requirements">
  Must be at least 8 characters with one number.
</p>
```

#### Error handling (3.3.1, 3.3.3)

```html
<!-- Announce errors to screen readers -->
<form novalidate>
  <div class="field" aria-live="polite">
    <label for="email">Email</label>
    <input type="email" id="email" 
           aria-invalid="true"
           aria-describedby="email-error">
    <p id="email-error" class="error" role="alert">
      Please enter a valid email address (e.g., name@example.com)
    </p>
  </div>
</form>
```

```javascript
// Focus first error on submit
form.addEventListener('submit', (e) => {
  const firstError = form.querySelector('[aria-invalid="true"]');
  if (firstError) {
    e.preventDefault();
    firstError.focus();
    
    // Announce error summary
    const errorSummary = document.getElementById('error-summary');
    errorSummary.textContent = `${errors.length} errors found. Please fix them and try again.`;
    errorSummary.focus();
  }
});
```

---

### Robust

#### Valid HTML (4.1.1)

```html
<!-- ❌ Duplicate IDs -->
<div id="content">...</div>
<div id="content">...</div>

<!-- ❌ Invalid nesting -->
<a href="/"><button>Click</button></a>

<!-- ✅ Unique IDs -->
<div id="main-content">...</div>
<div id="sidebar-content">...</div>

<!-- ✅ Proper nesting -->
<a href="/" class="button-link">Click</a>
```

#### ARIA usage (4.1.2)

**Prefer native elements:**
```html
<!-- ❌ ARIA role on div -->
<div role="button" tabindex="0">Click me</div>

<!-- ✅ Native button -->
<button>Click me</button>

<!-- ❌ ARIA checkbox -->
<div role="checkbox" aria-checked="false">Option</div>

<!-- ✅ Native checkbox -->
<label><input type="checkbox"> Option</label>
```

**When ARIA is needed:**
```html
<!-- Custom tabs component -->
<div role="tablist" aria-label="Product information">
  <button role="tab" id="tab-1" aria-selected="true" 
          aria-controls="panel-1">Description</button>
  <button role="tab" id="tab-2" aria-selected="false" 
          aria-controls="panel-2" tabindex="-1">Reviews</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  <!-- Panel content -->
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  <!-- Panel content -->
</div>
```

#### Live regions (4.1.3)

```html
<!-- Status updates -->
<div aria-live="polite" aria-atomic="true" class="status">
  <!-- Content updates announced to screen readers -->
</div>

<!-- Urgent alerts -->
<div role="alert" aria-live="assertive">
  <!-- Interrupts current announcement -->
</div>
```

```javascript
// Announce dynamic content changes
function showNotification(message, type = 'polite') {
  const container = document.getElementById(`${type}-announcer`);
  container.textContent = ''; // Clear first
  requestAnimationFrame(() => {
    container.textContent = message;
  });
}
```

---

## Accessibility Audit

<!-- source: wshobson/agents plugins/ui-design/commands/accessibility-audit.md#target-and-level-configuration -->

### Target and Level Configuration

#### If argument provided:

- Parse for file path or component name
- Parse for `--level` flag (AA or AAA)
- Default to WCAG 2.1 Level AA if not specified

#### If no argument:

**Q1: Audit Target**

```
What would you like to audit?

1. A specific component (provide name or path)
2. A page/route (provide path)
3. All components in a directory
4. The entire application
5. Recent changes only (last commit)

Enter number or provide a file path:
```

**Q2: Compliance Level**

```
What WCAG compliance level should I audit against?

1. Level A   - Minimum accessibility (must-fix issues)
2. Level AA  - Standard compliance (recommended, most common target)
3. Level AAA - Enhanced accessibility (highest standard)

Note: Each level includes all requirements from previous levels.

Enter number:
```

**Q3: Focus Areas (optional)**

```
Any specific areas to focus on? (Press enter to audit all)

1. Color contrast and visual presentation
2. Keyboard navigation and focus management
3. Screen reader compatibility
4. Forms and input validation
5. Dynamic content and ARIA
6. All areas

Enter numbers (comma-separated) or press enter:
```

## Accessibility Expert

<!-- source: github/awesome-copilot agents/accessibility.agent.md#checklists -->

### Checklists

#### Designer Checklist

- Define heading structure, landmarks, and content hierarchy
- Specify focus styles, error states, and visible indicators
- Ensure color palettes meet contrast and are good for colorblind people; pair color with text/icon
- Plan captions/transcripts and motion alternatives
- Place help and support consistently in key flows

#### Developer Checklist

- Use semantic HTML elements; prefer native controls
- Label every input; describe errors inline and offer a summary when complex
- Manage focus on modals, menus, dynamic updates, and route changes
- Provide keyboard alternatives for pointer/gesture interactions
- Respect `prefers-reduced-motion`; avoid autoplay or provide controls
- Support text spacing, reflow, and minimum target sizes

#### QA Checklist

- Perform a keyboard-only run-through; verify visible focus and logical order
- Do a screen reader smoke test on critical paths
- Test at 400% zoom and with high-contrast/forced-colors modes
- Run automated checks (axe/pa11y/Lighthouse) and confirm no blockers
