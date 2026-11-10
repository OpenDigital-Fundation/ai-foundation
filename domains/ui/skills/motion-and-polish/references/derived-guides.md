# Motion and polish — derived guides

Part of `ui:motion-and-polish`.

## GSAP & Framer Motion — Scroll Animations Skill

<!-- source: github/awesome-copilot skills/gsap-framer-scroll-animation/SKILL.md#the-5-most-common-scroll-patterns -->

### The 5 Most Common Scroll Patterns

Quick reference — full recipes with Copilot prompts are in the reference files.

#### 1. Fade-in on enter (GSAP)
```js
gsap.from('.card', {
  opacity: 0, y: 50, stagger: 0.15, duration: 0.8,
  scrollTrigger: { trigger: '.card', start: 'top 85%' }
});
```

#### 2. Fade-in on enter (Framer Motion)
```jsx
<motion.div
  initial={{ opacity: 0, y: 40 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: '-80px' }}
  transition={{ duration: 0.6 }}
/>
```

#### 3. Scrub / scroll-linked (GSAP)
```js
gsap.to('.hero-img', {
  scale: 1.3, opacity: 0, ease: 'none',
  scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
});
```

#### 4. Scroll-linked (Framer Motion)
```jsx
const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] });
const y = useTransform(scrollYProgress, [0, 1], [0, -100]);
return <motion.div style={{ y }} />;
```

#### 5. Pinned timeline (GSAP)
```js
const tl = gsap.timeline({
  scrollTrigger: { trigger: '.section', pin: true, scrub: 1, start: 'top top', end: '+=200%' }
});
tl.from('.title', { opacity: 0, y: 60 }).from('.img', { scale: 0.85 });
```

## Scroll Experience

<!-- source: davila7/claude-code-templates cli-tool/components/skills/creative-design/scroll-experience/SKILL.md#anti-patterns -->

### Anti-Patterns

#### ❌ Scroll Hijacking

**Why bad**: Users hate losing scroll control.
Accessibility nightmare.
Breaks back button expectations.
Frustrating on mobile.

**Instead**: Enhance scroll, don't replace it.
Keep natural scroll speed.
Use scrub animations.
Allow users to scroll normally.

#### ❌ Animation Overload

**Why bad**: Distracting, not delightful.
Performance tanks.
Content becomes secondary.
User fatigue.

**Instead**: Less is more.
Animate key moments.
Static content is okay.
Guide attention, don't overwhelm.

#### ❌ Desktop-Only Experience

**Why bad**: Mobile is majority of traffic.
Touch scroll is different.
Performance issues on phones.
Unusable experience.

**Instead**: Mobile-first scroll design.
Simpler effects on mobile.
Test on real devices.
Graceful degradation.

## Interaction Design

<!-- source: wshobson/agents plugins/ui-design/skills/interaction-design/SKILL.md#css-animation-patterns -->

### CSS Animation Patterns

#### Keyframe Animations

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}
.animate-pulse {
  animation: pulse 2s ease-in-out infinite;
}
.animate-spin {
  animation: spin 1s linear infinite;
}
```

#### CSS Transitions

```css
.card {
  transition:
    transform 0.2s ease-out,
    box-shadow 0.2s ease-out;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}
```
