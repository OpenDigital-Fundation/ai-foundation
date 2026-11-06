# Motion and polish — taste

Part of `ui:motion-and-polish`.

## Taste

<!-- source: affaan-m/ECC skills/taste/SKILL.md -->

Most AI video advice stops at *how to render frames*. This skill is the layer above
that: **what the frames should look like, in what order, cut to what rhythm, so the
result reads as one intentional thing instead of a pile of generations.**

It encodes a specific taste — the **angelcore / cloud-trance / hyperpop** family
(Bladee "Silver Surfer"-era ethereal trance crossed with heavy angelcore) — distilled
from a corpus of saved Reels and a tour through a ~70-entry visual-genre library. It
is opinionated on purpose. Taste is a point of view, not a menu.

> The companion file `references/genre-taxonomy.md` holds the full named-genre catalog.
> This file is the actionable layer: mood, grammar, pipeline, and a beat-mapped shot plan.

### When to Activate

- Building a **music video**, lyric video, fancam, or visualizer.
- Making a short-form **edit / reel** where the *feel* matters more than the information.
- Driving **AI b-roll generation** (fal.ai, Veo, Kling, etc.) and the prompts need a
  coherent direction instead of one-off vibes.
- Assembling a **moodboard** or choosing a visual genre before any rendering.
- The user says "taste", "make it feel like X", "give it a direction", "angelcore",
  "cloud trance", "hyperpop edit", "Bladee", "dreamcore", or names a saved reference.
- The current edit works but reads as flat, generic, AI-slop, or stylistically incoherent.

This skill sits **on top of** `video-editing` (the mechanics) and `remotion-video-creation`
(the renderer). Use those for *how*. Use this for *what and why*.

### Core Thesis

1. **Taste is the last layer, and it must be decided first.** `video-editing` correctly
   says taste is the final human pass. The trap: if you only decide taste at the end, every
   generation and cut upstream was a guess. Pick the direction *before* the first prompt,
   then let it constrain everything.
2. **Coherence beats novelty.** One look executed across 30 shots beats 30 looks. A named
   genre (below) is a constraint that buys coherence for free.
3. **Cut to the song, not to the footage.** In a music video the timeline is the waveform.
   Every hard cut lands on a beat or a transient. Frame math is in the pipeline section.
4. **Generate selectively, edit ruthlessly.** AI makes b-roll that does not exist; it does
   not make taste. You still throw away 80%.

### The Aesthetic Vocabulary (distilled)

The reference corpus tours a large library of *named* visual genres. The full list lives in
`references/genre-taxonomy.md`. The useful move is not memorizing 70 names — it is seeing
that **a genre name is a complete prompt-and-grade preset.** When you pick one, you inherit
its palette, texture, lighting, and subject matter as a unit.

The genres cluster into families. Pick a **primary** family and at most **one accent**:

| Family | Genres in it | Reads as |
|--------|-------------|----------|
| **Ethereal / divine** | spiritualism, glacial folk, beacons, zen core, fairy tale | weightless, holy, glowing, soft |
| **Hyperpop / Y2K-cyber** | cyberdelia, acid house, acid nora, neo aggressano, new liquid | glossy, chrome, neon, kawaii-cyber |
| **Dark / occult** | dark academia, smoke nostalgia, communist core, abstract tech | high-contrast, ominous, grain |
| **Retro / print** | retro surfers, art deco, adventure pulp, classic advertising, magazine collage, bumper stickers | flat, graphic, halftone, nostalgic |
| **Organic / textural** | microbiology core, weaving patterns, fruitage retro, cozy blanket, pacific punk wave | tactile, macro, woven, wet |
| **Systemic / data** | numbers, mazes, code web, heatmap, pixel, 8-bit | gridded, generative, schematic |

**For the current project**, the primary is **Ethereal / divine** with a **Hyperpop / Y2K-cyber**
accent — i.e. holy light and crystalline bloom, punctuated by chrome and neon. That pairing
*is* the angelcore × cloud-trance brief.

### The Mood System — angelcore × cloud-trance

Distilled directly from the strongest reference reels. This is the concrete grade.

#### Palette
- **Base:** near-black void (#05060a) and bone white (#f4f1ea). Most frames are one or the other.
- **Divine accent:** molten gold / ember orange (#ffb24d → #ff7a18) — the *one warm light* in the dark.
- **Crystalline accent:** iridescent violet→cyan→magenta bokeh (#8a6bff, #4fc3ff, #ff6ad5) — the
  hyperpop bloom, used in bright frames.
- **Danger accent (sparingly):** a single glowing red (#ff2a2a) on monochrome — for one or two
  shock cuts only.
- **Hyperpop subject:** candy pink hair / chrome / glossy white against blue sky.

Rule: **one accent per shot.** Gold lives in dark frames; iridescence lives in light frames;
never both in one shot.

#### Light & texture
- Darkness pierced by a single warm source (ember bloom, divine shaft). High contrast, deep blacks.
- Crystalline / glitter bokeh, lens flares, bloom, light leaks — *heavenly*, not dirty.
- Film grain + subtle chromatic aberration on the dark frames; clean gloss on the bright frames.
- Macro detail on negative space: a hero object centered on black (key, eye, gear, petal, water).
- Subjects: winged figures, clouds, halos, angels, crystalline structures, candy-cyber portraits.

#### Motion
- Slow, floating, weightless camera (drift, slow push, slow orbit) — *cloud* trance.
- Bursts of speed only at the drop. Otherwise everything breathes.
- Particles rising (embers, dust, glitter) — upward motion = ascension.

### The Editing Grammar (distilled)

From the reference edits, the techniques that recur and define the style:

1. **Beat-locked hard cuts.** No dissolves in the verse/drop. Cut on the kick. The eye should
   feel the BPM.
2. **Hero-on-black macro inserts.** A single sharp object centered in black negative space,
   held for 1–2 beats, then cut. Rhythmic montage of these = the cloud-trance signature.
3. **Bloom / explosion reveal.** A white or ember bloom that blows out the frame on a transient,
   then resolves into the next shot. The "divine flash" transition.
4. **Color-pop on monochrome.** Run a passage in B&W, then a single colored element (red eye,
   gold flame, pink hair) punches through on the downbeat.
5. **Speed-ramp into the drop.** Ramp footage from slow to fast across the last bar before the
   drop, hard-cut to tempo on the one.
6. **Caption keyword highlight (for talking-head / lyric sections only).** All-caps, one or two
   words highlighted in the accent color, synced to the vocal. Use for lyric video, not for the
   pure visualizer.
7. **Reaction PiP (for explainer/edit-commentary only).** Picture-in-picture talking head over
   b-roll. Out of scope for the music video itself; documented because the corpus uses it heavily.

**Do-nots:** crossfade transitions in tempo sections; more than one accent color per shot; a
shot held past its musical phrase; readable on-screen UI chrome (crop it out); mixed aspect
ratios in one timeline.

### The Pipeline — mixing the the upstream project video skills

This skill is the conductor. Each the upstream project skill is an instrument. Do not skip layers.

```
0. TASTE (this skill)        decide genre + mood + grammar BEFORE anything renders
1. STRUCTURE (video-editing) map the song: timestamps for intro/verse/drop/bridge/outro
2. GENERATE (fal-ai-media)   make b-roll per genre prompt-presets; throw away 80%
3. CUT (video-editing/FFmpeg) beat-cut + reframe to 9:16; assemble selects on the grid
4. COMPOSE (remotion-video-creation) overlays, blooms, lyric text, beat-synced sequencing
5. MOTION (motion-* skills)  easing curves, light-leak/particle motion, transition timing
6. AUDIO (fal-ai-media)      transition risers/impacts to sell the cuts (track itself is in Ableton)
7. POLISH                    grade to the palette above, final pacing pass, export
8. DISTRIBUTE (content-engine) platform-native versions + caption/cover
```

| Step | the upstream project skill to load | What it does here |
|------|-------------------|-------------------|
| Structure & cut | `video-editing` | FFmpeg cut/concat/reframe, EDL, scene/silence detection |
| Generate b-roll | `fal-ai-media` | image/video models per genre preset |
| Compose & overlay | `remotion-video-creation` | beat-synced `<Sequence>`s, text, blooms, masks |
| Motion timing | `ui:motion-and-polish`, `ui:motion-and-polish`, `ui:motion-and-polish` | easing, springs, light/particle motion |
| Server-side video | `videodb` | smart reframe, indexing if footage is large |
| Distribution | `marketing:content-marketing` | per-platform cuts, covers, captions |
| Voice/lyric VO | `video-editing` (ElevenLabs section) | only if a spoken layer is needed |

### Beat Math (lock cuts to the song)

The current track is **138 BPM, B minor**. Constants:

- `seconds_per_beat = 60 / 138 = 0.43478s`
- `frames_per_beat   = fps × 0.43478`  →  **24fps: 10.43**, **30fps: 13.04**, **60fps: 26.09**
- `1 bar (4 beats)   = 1.7391s`  →  30fps: **52.17 frames**
- `8-bar phrase      = 13.913s`  →  the loop length from the track

In Remotion, snap every `from={}` to a beat:
```ts
const FPS = 30;
const BPM = 138;
const beat = (n: number) => Math.round(n * (60 / BPM) * FPS); // beat(n) → frame
// cut on beats 0,4,8,... :  <Sequence from={beat(0)} durationInFrames={beat(4)}> ...
```

### Beat-Mapped Shot Plan (this music video)

The song arrangement (from the project's own notes) is
**Intro → Verse → Drop → Bridge → Drop → Outro (~2:05)**. Map taste to each section:

| Section | Genre/mood lean | Grammar | Shot ideas |
|---------|-----------------|---------|------------|
| **Intro** | Ethereal/divine, near-black | slow push, no cuts | ember bloom in the void; a single shaft of gold; dust rising |
| **Verse** | Dark + macro hero-on-black | hard cuts every 2 beats | key, eye, gear, water drop, petal — rhythmic macro montage |
| **Drop** | Hyperpop bloom + crystalline | speed-ramp in, cut on the one, fast | candy-pink figure, chrome, iridescent bokeh, winged ascension |
| **Bridge** | Spiritualism, weightless | one long held shot, color-pop | clouds + halo; single red accent punches once |
| **Drop 2** | as Drop, intensify | add divine-flash blooms on transients | wings open, glitter burst, light leaks maxed |
| **Outro** | Glacial folk, cold calm | slow fade to black | crystalline structure dissolving; ember dies out |

### fal.ai Prompt Presets (per mood)

Use with `fal-ai-media`. Each preset is the genre rendered to the project palette. Append
`9:16, vertical, cinematic, film grain, volumetric light, no text, no watermark` to all.

- **Divine void:** "a single molten-gold ember bloom rising in an infinite near-black void,
  deep shadow, one warm light source, weightless dust particles, holy, high contrast"
- **Macro hero:** "extreme macro of an antique brass key / a human eye / interlocking gears,
  centered on pure black negative space, razor-sharp detail, single rim light"
- **Crystalline bloom:** "iridescent violet-cyan-magenta crystalline bokeh, glittering light
  refraction, dreamy lens flares, heavenly glow, soft focus, hyperpop angelcore"
- **Candy-cyber portrait:** "candy-pink-haired figure, glossy chrome accents, bright blue sky,
  Y2K hyperpop, clean gloss, saturated, kawaii-cyber"
- **Winged ascension:** "a winged figure ascending into clouds, halo of light, bone-white and
  gold, volumetric god-rays, ethereal, religious iconography, soft"
- **Cold outro:** "pale crystalline ice structure slowly dissolving, glacial folk, cold blue
  and bone white, minimal, calm, fading to black"

Generate 6–10 per preset, keep 2–3. For motion, animate stills with an image-to-video model
or generate short clips directly; keep camera moves slow per the Motion rules.

### FFmpeg Recipes (cut + reframe)

```bash
# Reframe any landscape/raw clip to 9:16 (center crop)
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" v.mp4

# Beat-cut a clip to exactly N beats at 138 BPM (e.g. 2 beats = 0.8696s)
ffmpeg -i in.mp4 -t 0.8696 -c copy beat2.mp4

# Concatenate beat-selects into the verse montage
for f in selects/*.mp4; do echo "file '$f'"; done > concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -c copy verse.mp4

# Strip UI chrome / status bar from a screen-recorded reference (crop top+bottom)
ffmpeg -i reel.mp4 -vf "crop=iw:ih-300:0:150" clean.mp4
```

### Remotion Composition Skeleton (beat-synced)

```tsx
import { AbsoluteFill, Sequence, Video, Img, useCurrentFrame, interpolate } from "remotion";

const FPS = 30, BPM = 138;
const beat = (n: number) => Math.round(n * (60 / BPM) * FPS);

const Bloom: React.FC = () => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 3, 12], [0, 1, 0], { extrapolateRight: "clamp" }); // divine flash on a transient
  return <AbsoluteFill style={{ background: "radial-gradient(#fff,#ffb24d)", opacity: o, mixBlendMode: "screen" }} />;
};

export const AngelcoreMV: React.FC = () => (
  <AbsoluteFill style={{ background: "#05060a" }}>
    {/* Verse: macro hero-on-black, hard cut every 2 beats */}
    <Sequence from={beat(0)} durationInFrames={beat(2)}><Video src="/selects/key.mp4" /></Sequence>
    <Sequence from={beat(2)} durationInFrames={beat(2)}><Video src="/selects/eye.mp4" /></Sequence>
    <Sequence from={beat(4)} durationInFrames={beat(2)}><Video src="/selects/gear.mp4" /></Sequence>
    {/* Drop: crystalline bloom + flash on the one */}
    <Sequence from={beat(8)} durationInFrames={beat(16)}><Video src="/selects/crystalline.mp4" /></Sequence>
    <Sequence from={beat(8)} durationInFrames={beat(1)}><Bloom /></Sequence>
  </AbsoluteFill>
);
```
Render: `npx remotion render src/index.ts AngelcoreMV out.mp4`. See `remotion-video-creation`
for project setup, audio track binding, and render flags.

### Key Principles

1. **Decide the genre before the first generation.** Pick one primary family + one accent.
2. **One accent color per shot.** Gold in the dark, iridescence in the light, red once.
3. **Every hard cut lands on a beat.** Use the beat math; no transitions in tempo sections.
4. **Hero-on-black macro is the signature move.** Master it; it carries the verses.
5. **Generate 10, keep 2.** Coherence comes from rejection, not from prompting harder.
6. **Crop the chrome.** No status bars, captions, or UI in the final frame.
7. **Taste is decided first and judged last.** Set the direction, then defend it on every cut.

### Related Skills

- `video-editing` — the mechanical pipeline (FFmpeg, reframe, EDL, polish) this sits on top of
- `remotion-video-creation` — programmable beat-synced composition and rendering
- `fal-ai-media` — generate the b-roll, transition SFX, and risers
- `ui:motion-and-polish`, `ui:motion-and-polish`, `ui:motion-and-polish` — easing and motion timing
- `videodb` — server-side smart reframe and indexing for large footage
- `marketing:content-marketing` — platform-native distribution, covers, captions
- `ui:visual-design` — the same "decide a direction first" discipline, for UI

## Taste Application

<!-- source: affaan-m/ECC skills/taste-application/SKILL.md -->

The second half of the pipeline. **taste-distillation** measures references into
a style pack; this generates against that pack and cuts the result.

### Execution and Delivery Contract

The original implementation ships here in `scripts/`; no separate `ito-video`
checkout is required. Install `scripts/requirements.txt` for local processing.
Install `scripts/requirements-live.txt` only for provider execution. Live
uploads, submissions and downloads require explicit `TASTE_FORGE_ALLOW_LIVE=1`
in addition to credentials; set it only for the user's authorized run.
`--dry-run` remains credential-free and produces labelled placeholders.
An ambiguous provider timeout is not retried as a new paid job. Inspect the
provider request before deciding whether another submission is warranted.

Use existing completed takes without any provider calls:

```bash
python scripts/pipeline.py --genre example --root stylepacks \
  --takes media/take-a.mp4 media/take-b.mp4 --duration 12 --fps 30 \
  --out out/review-v1.mp4
```

`--duration` is a **best-effort cadence target**, not an exact runtime. Complete
shots may produce a shorter or longer edit; the assembler does not duplicate
clips or add padding to meet the target. The output manifest retains actual
`duration` and adds `duration_contract` with requested and actual seconds,
shortfall, overrun, and the `cadence_target` policy. Differences of at least
one output frame are warned explicitly. No exact-duration mode is provided;
when an exact runtime is required, inspect the receipt and revise or reject
the cut before delivery.

The pipeline keeps each run's graded shot files because the editable FCPXML
and EDL reference them. It refuses output collisions and reports timeline
export failures. A completed render is not a saved editor project or creative
approval. Preserve source assets and versioned project checkpoints before
and after live edits; record the saved path and digest separately from the
in-memory timeline receipt.

Clone-ready Fal graphs and their offline input compiler are documented in
`workflows/README.md`. Compile brief and style direction before submission;
do not assume a disconnected schema field affects a model prompt. Validate
current endpoint fields against the actual provider before a paid run.

For Blender, use the full textured source GLB; retopology is a separately
named derivative and never replaces that source. `blender_prop.py` supports
explicit `--width 1920 --height 1080 --fps 30 --receipt receipt.json` and
preserves pack-derived rim lighting and material textures. Saving a scene is
distinct from rendering it; inspect the receipt's state and packed images.

For Resolve overlays, use `taste.resolve.apply_placements` with injected
objects from an explicitly selected, versioned target. Set `source_end_mode`
to the convention verified on that host. Do not assume an inclusive source
end across Resolve versions. The adapter allocates overlapping effects above
preserved tracks and checks every placement immediately and again after all
appends. Composite integers must match the installed API; for the verified
Studio 21 host, Screen is 5, not the historical builder's incorrect 22.
The receipt proves in-memory placement only. Save the project, verify its
checkpoint, then inspect the exact rendered output before reporting delivery.

### When to Activate

- "make a video in this style" / "apply the pack" / "supplement this footage"
- Assembling generated clips into something with real edit rhythm
- Minting 3D props from a look and getting them back into the video
- Verifying that a finished piece actually matches its reference

### Division of Labour

**The model supplies content, motion, framing and lighting structure. The pack
supplies colour and rhythm.** This is measured, not stylistic preference — see
taste-distillation for the numbers. Practical consequences:

- The generation prompt contains **zero colour language**. Add
  *"Colour: none. Render neutral. Grading is applied afterwards."*
- Keep **two separate flags**: `--brief` (what HAPPENS: subject, action, place)
  and `--style-steer` (how it LOOKS). Merging them leaks style words into the
  scene ("teal" becomes a teal object) and subject words into the grade.
- The model responds to **local, checkable rules** far better than global ones.
  "Backgrounds pure black and unlit; subjects blowing toward white" works;
  "extreme contrast" does not.

### Generate TAKES, Not Shots

The obvious reading of "match the cadence" is one generation per shot. It is
economically absurd. A reference averaging 0.78s/shot against an endpoint with a
4-second floor turns a 10s piece into **12 calls, 48 generated seconds for 10
used (21% efficiency)**, and twelve unrelated clips stitched into what should
read as continuous.

Editors roll a longer take and cut inside it. Grouping shots into ~5s takes:
**3 calls, 13 generated seconds, 77% efficiency**, and consecutive shots that
actually belong to each other because they came from the same generation.

Tell the model what shape you want, or it renders a slow locked-off push and six
cuts inside it read as a stutter:

> "Filmed as ONE continuous take with no hard cuts inside it. It will be cut into
> 6 pieces of roughly 0.8s in the edit, so the framing, subject and light must
> keep changing throughout — any 0.8s window has to stand alone as its own shot."

### Cutting Rules

- **Re-encode, never stream-copy.** Stream copy only cuts on keyframes, which at
  0.78s mean shot length rounds every boundary to the nearest GOP — destroying
  the exact thing the pipeline exists to preserve.
- **When supplementing existing footage, use its own shot boundaries.** Slicing a
  base video into contiguous pieces and playing them in order just reassembles
  the original: every "cut" lands mid-shot and is invisible. Measured, a 20-shot
  assembly registered only 12 detected cuts. Detect real boundaries and take
  every Nth so consecutive picks are guaranteed discontinuous. That moved a cut
  measurement from 1.29s to 0.83s against a 0.78s target.
- **Sample shot lengths from the reference's distribution**, not from its mean,
  so the cut inherits rhythm variance instead of flattening to even clips.

### Grading Rules

- **Direct measurement beats a baked LUT** when you have the clip: measure it,
  match its L\* CDF, apply zone chroma. `grade_clip_direct` reached MAE 1.58 and
  contrast 34.0 against 34.7.
- **Anchor, do not CDF-match, when the clip's histogram is unlike the
  reference's.** Forcing a 68%-black generated clip onto a busy reference
  histogram lifted the entire background out of black: background preservation
  fell to 26.0% (CDF) versus 69.0% (anchor), while MAE and contrast both still
  looked excellent. Default to anchored tone.
- **Batch size matters.** Grading 48 frames at once OOM-killed the process;
  6 is safe.

### Recovered fal Platform Behavior

These observations and endpoint examples came from the recovered workflow.
Recheck current endpoint metadata; they are not guarantees about every future
provider version. The bundled graph templates record the separately verified
workflow inputs, including explicit generated-audio control.

These cost real time to discover. Check them before designing a graph.

| Limit | Detail |
|---|---|
| **No 3D renderer at all** | fal has `image-to-3d`, `text-to-3d`, `3d-to-3d` and nothing else. Every `3d-to-3d` endpoint emits another mesh. There is no `3d-to-image`/`3d-to-video` category, so a minted GLB **cannot** re-enter a fal video graph. Render locally, then use `fal-ai/ffmpeg-api/images-to-video`. |
| **compose cannot overlay** | `fal-ai/ffmpeg-api/compose` rejects a second track with *"Multiple video tracks are not supported"* — and it counts an `image` track as a video track. It sequences one video track only. **Composite locally with ffmpeg.** |
| **compose keyframes are milliseconds** | Nothing in the response says so. A run submitted in seconds is accepted and returns a video that is 1000x too short. |
| **extract-frame offers first/middle/last only** | No arbitrary timestamp. Use the three as three distinct conditioning images. |
| **No loops, no string concat in the DAG** | Per-shot fan-out has to be authored node by node, or kept local. |
| **Kling 3.0 has no reference-to-video** | The v3 line is text/image/motion-control only; reference-to-video lives on the `o3` line: `fal-ai/kling-video/o3/pro/reference-to-video`. |
| **Prefixes are not uniform** | `bytedance/*`, `tripo3d/*`, `meshy/*`, `minimax/*`, `openai/*` carry **no** `fal-ai/` prefix. `kling-video`, `veo3.1`, `flux-*`, `hunyuan-3d`, `ffmpeg-api` do. |

#### Endpoint picks

| Slot | Best | Value alternative |
|---|---|---|
| reference→video | `bytedance/seedance-2.5/reference-to-video` (~$0.473/s @720p) | `fal-ai/kling-video/o3/pro/reference-to-video` (~$0.112/s) |
| image→3D | `fal-ai/hunyuan-3d/v3.1/pro/image-to-3d` ($0.375, up to 8 views) | `tripo3d/h3.1/image-to-3d` ($0.20) |
| text→3D | `fal-ai/hunyuan-3d/v3.1/pro/text-to-3d` | `tripo3d/h3.1/text-to-3d` |
| retopology | `fal-ai/hunyuan-3d/v3.1/smart-topology` ($0.75) | `tripo3d/tripo/remesh` (~75x cheaper) |
| part split | `fal-ai/hunyuan-3d/v3.1/part` (FBX only) | `tripo3d/tripo/segment` |
| text→image | `fal-ai/nano-banana-pro` ($0.15 flat) | `fal-ai/flux-2-pro` ($0.03/MP) |

Seedance is ~4x Kling o3's price for the same 5 seconds. It earns that on
multi-reference fidelity (up to 50 mixed image/video/audio refs) and does **not**
earn it when conditioning on a single still.

Model IDs and prices drift. Verify against fal.ai/models before promising any of
them.

### The 3D Branch

```bash
python mint3d.py --genre <name> --from-stills 4 --retopo --render
python mint3d.py --genre <name> --prompt "a cracked chrome visor" --render
```

- **Generate a clean plate first; do not lift from reference stills.** The
  endpoint's stated input requirement is simple background, single object,
  object >50% of frame. Reference reels are the opposite of that — collages,
  wide shots, several subjects, burnt-in graphics — and they produce sculpted
  noise. Text → single-object plate → mesh costs ~$0.15 extra and is the
  difference between a usable mesh and a discarded one.
- **Multi-view is named per-angle fields, not a list.** `input_image_url` (front,
  required), then `back_image_url`, `left_image_url`, `right_image_url`,
  `left_front_image_url`, `right_front_image_url`, `top_image_url`,
  `bottom_image_url`. There is no `input_image_urls` and no `multi_view` flag —
  inventing them degrades every mint to single-view while appearing to work. A
  wrong angle label is worse than omitting the view, because the model trusts it.
- **Address the GLB by key, not by position.** The response carries a `thumbnail`
  PNG and a `model_urls` block alongside `model_glb`; taking the first URL works
  only until the keys reorder, and a preview PNG downloads fine — nothing fails
  until Blender refuses to open it.
- **Request PBR maps.** Without them the mesh lights like painted cardboard.
- **Retopologise** if anyone will edit or rig it. Generated meshes are dense and
  chaotic.
- **Render locally to close the loop.** Once a turntable is frames, it is
  footage, and every downstream stage already handles footage — grade it, cut it,
  screen it as an element, or upload it as a conditioning reference. Use Blender
  when a binary is on PATH; keep a dependency-light software rasteriser as the
  default, because a headless GL context is the single most common thing missing
  from a container and a renderer that only works on a workstation is not part of
  a pipeline.

### Verify, Then Believe

Every other stage claims a result. Check it, and check **distribution shape**,
not just moments:

- `background` — share of frame below L\*10 vs the **pack's** figure. Compare to
  the reference, **not** to the source clip: a generated source at 68% black is
  blacker than any reference in a 24–55% band, so "preserve the source's blacks"
  demands the wrong thing and equally excuses a lifted grade.
- `chroma_mae` — per-zone a\*/b\* error, using the **median** (matching how the
  pack's targets were measured; a mean here compares a skew-sensitive statistic
  to a robust one and reports a definition mismatch as an error).
- `contrast` / `black_point` / `white_point`
- `banding` — empty L\* histogram bins *between occupied ones*. Counting total
  empty bins does not work: a legitimately dark clip has empty highlight bins.
- `cadence` — detected mean shot length vs the reference's.

Watch the **units trap**: OpenCV changes Lab convention with dtype. On float32,
L\* is 0–100 and a\*/b\* are signed; on uint8, L\* is 0–255 and a\*/b\* are
biased +128. Mixing them reports chroma errors in the hundreds.

### Full Chain

```bash
python pipeline.py --genre <name> --refs a.mov b.mov \
  --brief "what happens" --duration 12 \
  --base-video existing.mp4 --out out/FINAL.mp4
```

mint → distill → (mint3d) → apply → forge → verify. Stages 1–3 are cached, so
iterating on briefs never re-measures anything. `--dry-run` stubs every network
call: the plan, prompts, track layout and manifest all still get exercised.

### Anti-Patterns

| Don't | Why |
|---|---|
| One generation per shot | 21% efficiency, 12 unrelated clips |
| Put colour in the prompt | Measured not to work; pushes away from the neutral base the LUT wants |
| Stream-copy the cuts | Keyframe-only boundaries destroy sub-second rhythm |
| Cut a base video contiguously | Reassembles the original; every cut invisible |
| Trust compose to overlay | It cannot; it rejects the second track |
| Send seconds to compose | Silently 1000x too short |
| Ship on MAE alone | Add the background-share check |

### Borrowed Footage Carries the Capture App's UI

The single worst defect found in a delivered cut: the finished video shipped
someone else's like button, view counter and comment bubble, because the base
footage was a screen recording and nothing cropped them out.

**`content_mask` does not solve this and its bounding box makes it worse.**
Temporal variance keeps interface chrome, because chrome *animates* - the heart
pulses, the counter ticks - so the mask marks it as moving content. Measured on
three references, the mask bbox kept 100% of the width every time while the
interface sat plainly in the right-hand margin.

The separating signal is the temporal **median**, not the variance. Footage
moves, so the median of many frames averages into mush with almost no edge
energy; chrome sits at fixed coordinates, so its edges survive intact. Sobel
energy on the median frame lights up on chrome and goes quiet on content -
measured, a right-hand column read 0.23 against an interior background of 0.03
on one reference and 0.31 against 0.15 on another.

Two implementation details that cost a cycle each:

- **Trim past the innermost outlier in each outer band, not inward from the
  edge.** Walking in while the current line is hot stops immediately, because
  the outermost lines are letterbox - flat black, zero edge energy - and the
  chrome sits *inside* that at 90-95% of width. The naive version trimmed 1%
  of frame while the like button stayed in shot.
- **Scale to cover, not pad,** when portrait source lands in a landscape cut.
  Padding 9:16 (narrower still after the UI crop) into 16:9 left ~60% of frame
  as black bars, one shot was nearly an empty rectangle, and it poisoned the
  background metric because bars are pure black. Covering loses the sides,
  which is the right trade for centre-framed material.

### Overlay Plates Are Elements, Not Washes

A glow plate is ~4% covered by construction. Composite it at frame size and you
get a small bright dot parked mid-shot - it reads as a sticker, and it was
visible in a delivered cut as an unexplained coloured blob.

- **Tighten each plate to its alpha bounding box first.** That raises coverage
  from ~4% to 15-35% and hands size control to the caller instead of inheriting
  whatever fraction of the source frame the element happened to occupy.
- **Choose wash vs element by coverage.** Diffuse plates (<10% after tightening)
  work stretched full-frame at low opacity; concentrated ones want to be scaled
  to 35-70% of frame width and placed.
- **Vary placement, scale and rotation per shot** from a seeded RNG, so the cut
  stays reproducible but no two stamped shots share a mark. One plate in one
  spot every Nth shot reads as a watermark.
- Resolve element geometry in Python, not in ffmpeg expressions: `pad()` rejects
  a negative offset and cannot pad below its input size, so an oversized or
  off-frame element kills the whole filtergraph.

### Downstream Handoff (Resolve / Blender)

**Always ship an editable timeline beside the mp4.** The flattened video is a
viewing copy and the one thing a colourist cannot work with — every cut is baked
in and the shots are no longer separable. `forge.py` writes FCPXML 1.9 and a
CMX3600 EDL referencing the individual graded shot files, so the piece lands as a
timeline that can be re-cut and re-graded.

Validate the export, do not assume it: check that asset-clip offsets equal the
running sum of prior durations (no gaps), that every `ref` resolves to a declared
asset, that every `media-rep src` exists on disk, and that the total matches the
mp4. A timeline that imports but drifts is worse than one that fails loudly.

Two things that silently destroy the work:

- **Project frame rate must be set before import.** Resolve locks timeline fps on
  first timeline creation and conforms the cadence silently. At a sub-second mean
  shot length that conform is visible.
- **The delivered shots are already graded.** `look.cube` is a *normalising* LUT
  for new material and for matching — applying it to the supplied shots
  double-grades them. Node 1, nothing before it, corrections after.

Ship a handoff doc with the measured targets in it (`scripts/HANDOFF-TEMPLATE.md`
is a filled example): the zone chroma table, the cadence distribution including
**rhythm variance** — an editor who matches the mean but not the variance
produces something that reads completely differently — and an explicit "do not"
list.

For Blender, `scripts/blender_prop.py` derives its lighting from the pack:
black world with transparent film (so renders composite with no keying), key plus
rim (a key alone lets the silhouette die against black), rim colour converted
from the pack's peak-chroma zone via Lab→linear sRGB so the prop picks up the
same cast the footage is graded to. **View transform Standard, not AgX/Filmic,
and no grading in Blender** — AgX applies its own tone curve before the LUT ever
sees the pixels, and grading twice compounds.

### Bundled Code

`scripts/` in this skill is a working implementation, not pseudocode. It has no
project-specific assumptions: point it at any reference videos and it produces a
pack.

```bash
pip install -r scripts/requirements.txt
export FAL_KEY=...            # only needed for the stages that call fal
```

Every network call is stubbed under `TASTE_FORGE_DRY_RUN=1` or `--dry-run`, so
the plan, prompts, track layout and manifest can be inspected without spending.

## Taste Distillation

<!-- source: affaan-m/ECC skills/taste-distillation/SKILL.md -->

This standalone skill ships its implementation in `scripts/`; use
`ui:motion-and-polish` for the subsequent generated or local-take edit. Keep each
named genre in its own pack. Measurements from Flash Ethereal must not be
silently reused for Fluid Sketch or 3D Cyber Glitch. A measured zero is valid
data; distinguish it from an absent field.

Local dependencies are in `scripts/requirements.txt`. Separately authorized
provider work also needs `scripts/requirements-live.txt`, credentials and
explicit `TASTE_FORGE_ALLOW_LIVE=1`. `--dry-run` does not read credentials or
submit jobs. Never infer that a workflow was saved from a local endpoint name;
use the actual provider-side workflow or request evidence.

Turn reference videos into a **style pack**: a folder of measurements and assets
that later stages consume deterministically.

### When to Activate

- "capture the look of these clips" / "distill the vibe" / "make this repeatable"
- User has reference footage and wants a LUT, a grade, or matching pacing
- Building a library of looks partitioned by genre
- Any request where the answer would otherwise be "describe the style in a prompt"

### The Core Finding

**Prompting cannot deliver a grade. Measurement can.**

Measured on real footage: three paid generations with escalating colour direction
moved midtone a\* from +1.9 → +2.8 → +0.3 against a **+24.9** target, and contrast
never left ~19 against a **34.7** target. Applying a measured pack to the same
footage hit chroma MAE **1.88** and contrast **33.7** in one deterministic pass,
for free.

So the split is: **the model supplies content, motion and lighting structure; the
pack supplies the look.** Colour words in a generation prompt are worse than
useless — they cost money and push the render away from the neutral base the LUT
wants. Say so explicitly in the prompt: *"Colour: none. Render neutral. Grading
is applied afterwards."*

### What a Pack Contains

```
stylepacks/<genre>/
  grade.json      measured colour statistics (see below)
  cadence.json    every detected shot boundary + the derived distribution
  look.cube       33^3 LUT, drag straight into Resolve as a node LUT
  spec.json       VLM description, grounded in the measurements
  grounding.txt   the measured facts fed to the VLM
  stills/         full-res frames from the longest shots (conditioning images)
  plates/         screen-blend overlay elements lifted onto black
  props/          minted GLB meshes
  pack.json       manifest
```

### Running It

```bash
python mint.py --genre <name> --refs a.mov b.mov c.mov     # offline, no API key
python distill.py --genre <name>                            # one VLM call
```

`mint.py` is pure numeric analysis — no network, no key, deterministic, so a pack
can be regenerated rather than backed up.

### The Measurements That Matter

#### Chroma by luminance zone, not globally

Colour identity usually lives in **one luminance band**. A global a\*/b\* offset
mathematically cannot represent split-toning. Measure chroma inside zones
(`L* edges [0,15,35,55,75,100]`).

A real signature: violet at L\*25 (a\* +24.9, b\* −17.5), near-neutral at both
ends. Reporting only the darkest and lightest zones calls that "uniform cast" —
**always print the whole curve.**

#### Median + MAD, never mean + std

Chroma in real reference sets is strongly right-skewed. On one measured reel the
mean midtone chroma was 36.9 against a median of 17.5, so a mean-based LUT pushed
colour ~3x harder than the material warranted.

#### Contrast is std(L\*), not white minus black

The white−black range is ~100 on almost any real footage and discriminates
nothing.

#### Background share is a first-class statistic

Record the share of pixels below L\*10. No moment of the distribution can see it:
a clip can hold the right mean, std and chroma while its blacks have been lifted
into grey. This is exactly how a grade once scored MAE 1.88 / contrast 33.7 while
the actual frame was a muddy purple mess.

#### Mask the interface before measuring

Screen-recorded references carry static furniture — letterbox bars, a status bar,
a like icon, caption text. All of it lands in the statistics as if it were the
look: black bars inflate shadow weight, a red heart skews a\* toward magenta.
**Temporal variance separates them cleanly** — the footage moves, the interface
does not — so no hand-tuned crop is needed. On real material this keeps ~65% of
pixels.

#### Cadence needs an adaptive threshold

The right content-detector threshold is material-dependent: a high-contrast
action reference cuts hard enough for 30, a moody one hides its cuts under it.
Sweep descending thresholds and take the **highest** one that still recovers ≥90%
of the shots the most sensitive setting finds — that biases toward real cuts over
noise. Reject thresholds implying an absurd cut rate (>100/min); continuous
camera moves trip the detector every frame.

Run the whole sweep in **one decode pass** with a shared `StatsManager`. The
naive version re-decodes per threshold, which on 60fps source is the difference
between seconds and minutes.

### Overlay Plates: Assets, Not Screenshots

A still is a whole frame — compositing one just puts a second picture on top.
A **plate** is the reference's graphic vocabulary (flares, streaks, glitch
fragments) lifted onto black so it screen-blends with no keying.

Two traps, both hit on real material:

1. **Absolute thresholds fail.** On a bright reference an `L>55 AND chroma>12`
   selection takes ~90% of frame, and the "plate" is the picture — including a
   recognisable face. Select by **percentile** (~top 3%) and **reject any plate
   covering more than ~22% of frame.**
2. **Rank by separation, not by brightness.** "Share of bright saturated pixels"
   ranks a washed-out frame top and a black frame with one intense flare — the
   actual signature — near the bottom. Score `p99.5(energy) / median(energy)`.

Also mask before scoring: burnt-in typography is bright, saturated and
high-contrast, so an unmasked run yields a perfect plate of someone else's title
card.

### Grounding the VLM

Feed the measurements into the system prompt before asking for a description.
Ungrounded, a VLM will report "no apparent colour grading, neutral" on footage
with a +24.9 a\* cast. Grounded, it describes the cast correctly and infers the
secondary accent independently.

Ban hedging words (`varied`, `mixed`, `dynamic`, `some`, `often`, `neutral`,
`or`) — a model cannot render "varied lighting". **Enforce the ban in code, not
just in the prompt:** it was violated in roughly one run in three. Re-ask
per-field, keep the least-hedged answer after N attempts rather than failing.

Caveat worth stating to the user: once the spec is grounded in the measurements
it is no longer an independent check on them.

### LUT Baking Gotchas

- A LUT can only encode a **per-pixel RGB function**. Anything
  distribution-dependent (histogram matching, percentile anchors) must be reduced
  to a constant *before* baking, or it silently measures the uniform LUT grid
  instead of the footage.
- `cv2.cvtColor(LAB2RGB)` **clamps internally**, so an out-of-gamut test using it
  reports 0%. Convert Lab→linear sRGB by hand; a real measurement was 83.3% OOG.
- Offset chroma transfer, not affine. Affine divides by the source σ and
  overshoots — on real footage it flipped b\* to +11.6 against a −17.5 target.
  Offset took MAE from 6.23 to 2.13.
- Gamut compression cost 3.8x runtime for identical MAE. Make it opt-in.

### Anti-Patterns

| Don't | Why |
|---|---|
| Tune against synthetic test footage | Cost four separate wrong conclusions on one project; real footage overturned every one |
| Trust MAE alone | 1.88 MAE looked like success on a visibly broken frame |
| Use mean/std for chroma | Right-skewed; pushes ~3x too hard |
| Compare only endpoint zones | Both ends are near-neutral by construction |
| Describe the look and stop | The spec is for content and structure; the pack is for colour |

### Handoff

The pack is the interface. Once it exists, use the **taste-application** skill to
generate and assemble against it, or hand `look.cube` to a colourist directly.

### Bundled Code

`scripts/` in this skill is a working implementation, not pseudocode. It has no
project-specific assumptions: point it at any reference videos and it produces a
pack.

```bash
pip install -r scripts/requirements.txt
export FAL_KEY=...            # only needed for the stages that call fal
```

Every network call is stubbed under `TASTE_FORGE_DRY_RUN=1` or `--dry-run`, so
the plan, prompts, track layout and manifest can be inspected without spending.
