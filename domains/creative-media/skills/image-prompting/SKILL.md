---
name: image-prompting
description: "Use when writing prompts for image-generation models: photographic direction (lens, light, composition), style control, and representation that avoids stereotyped or culturally inaccurate depictions of people."
license: MIT
metadata:
  domain: creative-media
  status: experimental
---
# Image prompting

Describe the image a photographer or illustrator would need to make it, and check the result for accuracy and bias.

## 1. Brief
Purpose and placement (hero, social, product), aspect ratio and resolution, brand constraints, and what must not appear.

## 2. Compose the prompt
Subject and action; setting and time; composition and camera (shot size, angle, lens, depth of field); light (quality, direction, colour temperature); style and medium; mood. Concrete nouns beat adjectives.

## 3. Represent people accurately
Specify people only as the brief requires; avoid defaulting to stereotypes of gender, age, ethnicity, disability or culture; get cultural dress, settings and symbols right. See the inclusive-visuals reference.

## 4. Iterate
Change one attribute per round, keep the seed when comparing, and record the prompt that worked.

## 5. Review
Check hands, text, logos and anatomy; confirm usage rights for the model and any reference images; never depict real, identifiable people without consent.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/inclusive-visuals.md`](references/inclusive-visuals.md) — covers Inclusive Visuals Specialist
- [`references/derived-guides.md`](references/derived-guides.md) — sections merged from other collections where this skill had no equivalent: Animated GIF Annotations; Image Diffing
