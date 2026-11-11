# Visual design — mobile ios design

Part of `ui:visual-design`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## iOS Mobile Design

<!-- source: wshobson/agents plugins/ui-design/skills/mobile-ios-design/SKILL.md#1-human-interface-guidelines-principles,5-visual-design -->

#### 1. Human Interface Guidelines Principles

**Clarity**: Content is legible, icons are precise, adornments are subtle
**Deference**: UI helps users understand content without competing with it
**Depth**: Visual layers and motion convey hierarchy and enable navigation

**Platform Considerations:**

- **iOS**: Touch-first, compact displays, portrait orientation
- **iPadOS**: Larger canvas, multitasking, pointer support
- **visionOS**: Spatial computing, eye/hand input

#### 5. Visual Design

**Colors and Materials:**

```swift
// Semantic colors that adapt to light/dark mode
Text("Primary")
    .foregroundStyle(.primary)
Text("Secondary")
    .foregroundStyle(.secondary)

// System materials for blur effects
Rectangle()
    .fill(.ultraThinMaterial)
    .frame(height: 100)

// Vibrant materials for overlays
Text("Overlay")
    .padding()
    .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
```

**Shadows and Depth:**

```swift
// Standard card shadow
RoundedRectangle(cornerRadius: 16)
    .fill(.background)
    .shadow(color: .black.opacity(0.1), radius: 8, y: 4)

// Elevated appearance
.shadow(radius: 2, y: 1)
.shadow(radius: 8, y: 4)
```
