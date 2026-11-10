# Technical writing — derived guides

Part of `documents:technical-writing`.

## Markdown to HTML Conversion

<!-- source: github/awesome-copilot skills/markdown-to-html/SKILL.md#converting-markdown-to-html -->

### Converting Markdown to HTML

#### Essential Basic Conversions

For more see basic-markdown-to-html.md

```text
    ```markdown
    # Level 1
    ## Level 2

    One sentence with a [link](https://example.com), and a HTML snippet like `<p>paragraph tag</p>`.

    - `ul` list item 1
    - `ul` list item 2

    1. `ol` list item 1
    2. `ol` list item 1

    | Table Item | Description |
    | One | One is the spelling of the number `1`. |
    | Two | Two is the spelling of the number `2`. |

    ```js
    var one = 1;
    var two = 2;

    function simpleMath(x, y) {
     return x + y;
    }
    console.log(simpleMath(one, two));
    ```
    ```

    ```html
    <h1>Level 1</h1>
    <h2>Level 2</h2>

    <p>One sentence with a <a href="https://example.com">link</a>, and a HTML snippet like <code>&lt;p&gt;paragraph tag&lt;/p&gt;</code>.</p>

    <ul>
     <li>`ul` list item 1</li>
     <li>`ul` list item 2</li>
    </ul>

    <ol>
     <li>`ol` list item 1</li>
     <li>`ol` list item 2</li>
    </ol>

    <table>
     <thead>
      <tr>
       <th>Table Item</th>
       <th>Description</th>
      </tr>
     </thead>
     <tbody>
      <tr>
       <td>One</td>
       <td>One is the spelling of the number `1`.</td>
      </tr>
      <tr>
       <td>Two</td>
       <td>Two is the spelling of the number `2`.</td>
      </tr>
     </tbody>
    </table>

    <pre>
     <code>var one = 1;
     var two = 2;

     function simpleMath(x, y) {
      return x + y;
     }
     console.log(simpleMath(one, two));</code>
    </pre>
    ```
```

#### Code Block Conversions

For more see code-blocks-to-html.md

```text

    ```markdown
    your code here
    ```

    ```html
    <pre><code class="language-md">
    your code here
    </code></pre>
    ```

    ```js
    console.log("Hello world");
    ```

    ```html
    <pre><code class="language-js">
    console.log("Hello world");
    </code></pre>
    ```

    ```markdown
      ```

      ```
      visible backticks
      ```

      ```
    ```

    ```html
      <pre><code>
      ```

      visible backticks

      ```
      </code></pre>
    ```
```

#### Collapsed Section Conversions

For more see collapsed-sections-to-html.md

```text
    ```markdown
    <details>
    <summary>More info</summary>

    ### Header inside

    - Lists
    - **Formatting**
    - Code blocks

        ```js
        console.log("Hello");
        ```

    </details>
    ```

    ```html
    <details>
    <summary>More info</summary>

    <h3>Header inside</h3>

    <ul>
     <li>Lists</li>
     <li><strong>Formatting</strong></li>
     <li>Code blocks</li>
    </ul>

    <pre>
     <code class="language-js">console.log("Hello");</code>
    </pre>

    </details>
    ```
```

#### Mathematical Expression Conversions

For more see writing-mathematical-expressions-to-html.md

```text
    ```markdown
    This sentence uses `$` delimiters to show math inline: $\sqrt{3x-1}+(1+x)^2$
    ```

    ```html
    <p>This sentence uses <code>$</code> delimiters to show math inline:
     <math-renderer><math xmlns="http://www.w3.org/1998/Math/MathML">
      <msqrt><mn>3</mn><mi>x</mi><mo>−</mo><mn>1</mn></msqrt>
      <mo>+</mo><mo>(</mo><mn>1</mn><mo>+</mo><mi>x</mi>
      <msup><mo>)</mo><mn>2</mn></msup>
     </math>
    </math-renderer>
    </p>
    ```

    ```markdown
    **The Cauchy-Schwarz Inequality**\
    $$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$
    ```

    ```html
    <p><strong>The Cauchy-Schwarz Inequality</strong><br>
     <math-renderer>
      <math xmlns="http://www.w3.org/1998/Math/MathML">
       <msup>
        <mrow><mo>(</mo>
         <munderover><mo data-mjx-texclass="OP">∑</mo>
          <mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow><mi>n</mi>
         </munderover>
         <msub><mi>a</mi><mi>k</mi></msub>
         <msub><mi>b</mi><mi>k</mi></msub>
         <mo>)</mo>
        </mrow>
        <mn>2</mn>
       </msup>
       <mo>≤</mo>
       <mrow><mo>(</mo>
        <munderover><mo>∑</mo>
         <mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow>
         <mi>n</mi>
        </munderover>
        <msubsup><mi>a</mi><mi>k</mi><mn>2</mn></msubsup>
        <mo>)</mo>
       </mrow>
       <mrow><mo>(</mo>
         <munderover><mo>∑</mo>
          <mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow>
          <mi>n</mi>
         </munderover>
         <msubsup><mi>b</mi><mi>k</mi><mn>2</mn></msubsup>
         <mo>)</mo>
       </mrow>
      </math>
     </math-renderer></p>
    ```
```

#### Table Conversions

For more see tables-to-html.md

```text
    ```markdown
    | First Header  | Second Header |
    | ------------- | ------------- |
    | Content Cell  | Content Cell  |
    | Content Cell  | Content Cell  |
    ```

    ```html
    <table>
     <thead><tr><th>First Header</th><th>Second Header</th></tr></thead>
     <tbody>
      <tr><td>Content Cell</td><td>Content Cell</td></tr>
      <tr><td>Content Cell</td><td>Content Cell</td></tr>
     </tbody>
    </table>
    ```

    ```markdown
    | Left-aligned | Center-aligned | Right-aligned |
    | :---         |     :---:      |          ---: |
    | git status   | git status     | git status    |
    | git diff     | git diff       | git diff      |
    ```

    ```html
    <table>
      <thead>
       <tr>
        <th align="left">Left-aligned</th>
        <th align="center">Center-aligned</th>
        <th align="right">Right-aligned</th>
       </tr>
      </thead>
      <tbody>
       <tr>
        <td align="left">git status</td>
        <td align="center">git status</td>
        <td align="right">git status</td>
       </tr>
       <tr>
        <td align="left">git diff</td>
        <td align="center">git diff</td>
        <td align="right">git diff</td>
       </tr>
      </tbody>
    </table>
    ```
```

## Copy Editing

<!-- source: davila7/claude-code-templates cli-tool/components/skills/business-marketing/copy-editing/SKILL.md#the-seven-sweeps-framework -->

### The Seven Sweeps Framework

Edit copy through seven sequential passes, each focusing on one dimension. After each sweep, loop back to check previous sweeps aren't compromised.

#### Sweep 1: Clarity

**Focus:** Can the reader understand what you're saying?

**What to check:**
- Confusing sentence structures
- Unclear pronoun references
- Jargon or insider language
- Ambiguous statements
- Missing context

**Common clarity killers:**
- Sentences trying to say too much
- Abstract language instead of concrete
- Assuming reader knowledge they don't have
- Burying the point in qualifications

**Process:**
1. Read through quickly, highlighting unclear parts
2. Don't correct yet—just note problem areas
3. After marking issues, recommend specific edits
4. Verify edits maintain the original intent

**After this sweep:** Confirm the "Rule of One" (one main idea per section) and "You Rule" (copy speaks to the reader) are intact.

---

#### Sweep 2: Voice and Tone

**Focus:** Is the copy consistent in how it sounds?

**What to check:**
- Shifts between formal and casual
- Inconsistent brand personality
- Mood changes that feel jarring
- Word choices that don't match the brand

**Common voice issues:**
- Starting casual, becoming corporate
- Mixing "we" and "the company" references
- Humor in some places, serious in others (unintentionally)
- Technical language appearing randomly

**Process:**
1. Read aloud to hear inconsistencies
2. Mark where tone shifts unexpectedly
3. Recommend edits that smooth transitions
4. Ensure personality remains throughout

**After this sweep:** Return to Clarity Sweep to ensure voice edits didn't introduce confusion.

---

#### Sweep 3: So What

**Focus:** Does every claim answer "why should I care?"

**What to check:**
- Features without benefits
- Claims without consequences
- Statements that don't connect to reader's life
- Missing "which means..." bridges

**The So What test:**
For every statement, ask "Okay, so what?" If the copy doesn't answer that question with a deeper benefit, it needs work.

❌ "Our platform uses AI-powered analytics"
*So what?*
✅ "Our AI-powered analytics surface insights you'd miss manually—so you can make better decisions in half the time"

**Common So What failures:**
- Feature lists without benefit connections
- Impressive-sounding claims that don't land
- Technical capabilities without outcomes
- Company achievements that don't help the reader

**Process:**
1. Read each claim and literally ask "so what?"
2. Highlight claims missing the answer
3. Add the benefit bridge or deeper meaning
4. Ensure benefits connect to real reader desires

**After this sweep:** Return to Voice and Tone, then Clarity.

---

#### Sweep 4: Prove It

**Focus:** Is every claim supported with evidence?

**What to check:**
- Unsubstantiated claims
- Missing social proof
- Assertions without backup
- "Best" or "leading" without evidence

**Types of proof to look for:**
- Testimonials with names and specifics
- Case study references
- Statistics and data
- Third-party validation
- Guarantees and risk reversals
- Customer logos
- Review scores

**Common proof gaps:**
- "Trusted by thousands" (which thousands?)
- "Industry-leading" (according to whom?)
- "Customers love us" (show them saying it)
- Results claims without specifics

**Process:**
1. Identify every claim that needs proof
2. Check if proof exists nearby
3. Flag unsupported assertions
4. Recommend adding proof or softening claims

**After this sweep:** Return to So What, Voice and Tone, then Clarity.

---

#### Sweep 5: Specificity

**Focus:** Is the copy concrete enough to be compelling?

**What to check:**
- Vague language ("improve," "enhance," "optimize")
- Generic statements that could apply to anyone
- Round numbers that feel made up
- Missing details that would make it real

**Specificity upgrades:**

| Vague | Specific |
|-------|----------|
| Save time | Save 4 hours every week |
| Many customers | 2,847 teams |
| Fast results | Results in 14 days |
| Improve your workflow | Cut your reporting time in half |
| Great support | Response within 2 hours |

**Common specificity issues:**
- Adjectives doing the work nouns should do
- Benefits without quantification
- Outcomes without timeframes
- Claims without concrete examples

**Process:**
1. Highlight vague words and phrases
2. Ask "Can this be more specific?"
3. Add numbers, timeframes, or examples
4. Remove content that can't be made specific (it's probably filler)

**After this sweep:** Return to Prove It, So What, Voice and Tone, then Clarity.

---

#### Sweep 6: Heightened Emotion

**Focus:** Does the copy make the reader feel something?

**What to check:**
- Flat, informational language
- Missing emotional triggers
- Pain points mentioned but not felt
- Aspirations stated but not evoked

**Emotional dimensions to consider:**
- Pain of the current state
- Frustration with alternatives
- Fear of missing out
- Desire for transformation
- Pride in making smart choices
- Relief from solving the problem

**Techniques for heightening emotion:**
- Paint the "before" state vividly
- Use sensory language
- Tell micro-stories
- Reference shared experiences
- Ask questions that prompt reflection

**Process:**
1. Read for emotional impact—does it move you?
2. Identify flat sections that should resonate
3. Add emotional texture while staying authentic
4. Ensure emotion serves the message (not manipulation)

**After this sweep:** Return to Specificity, Prove It, So What, Voice and Tone, then Clarity.

---

#### Sweep 7: Zero Risk

**Focus:** Have we removed every barrier to action?

**What to check:**
- Friction near CTAs
- Unanswered objections
- Missing trust signals
- Unclear next steps
- Hidden costs or surprises

**Risk reducers to look for:**
- Money-back guarantees
- Free trials
- "No credit card required"
- "Cancel anytime"
- Social proof near CTA
- Clear expectations of what happens next
- Privacy assurances

**Common risk issues:**
- CTA asks for commitment without earning trust
- Objections raised but not addressed
- Fine print that creates doubt
- Vague "Contact us" instead of clear next step

**Process:**
1. Focus on sections near CTAs
2. List every reason someone might hesitate
3. Check if the copy addresses each concern
4. Add risk reversals or trust signals as needed

**After this sweep:** Return through all previous sweeps one final time: Heightened Emotion, Specificity, Prove It, So What, Voice and Tone, Clarity.

---

## Docs Sync Audit

<!-- source: github/awesome-copilot skills/docs-sync-audit/SKILL.md#evidence-standards -->

### Evidence Standards

- Verify every citation before you write it, and apply one test: **the line you cite must literally contain the thing you name.** Citing a symbol means citing the line the symbol's name appears on -- not the blank line above it, not the decorator above it, not a line inside the body, and not a line inside a multi-line literal or dict that merely sits nearby. If you cite a range, its first line must contain the name. Prefer a single anchor line holding a distinctive token over a hand-counted range.
- When you quote text, cite the line the quoted characters are on. A comment, a docstring, or a sentence of prose has its own line number, and it is usually not the line of the code or heading next to it. Re-read the line before writing its number.
- When you attribute a finding to a tool's output, quote the path and line the tool itself reported. Never infer which lines a linter or type checker fired on by reading the code. If the tool's output does not name the line, report the pattern without claiming the tool flagged it.
- Any number you state -- matches, files, occurrences, endpoints -- must appear under **Checks Run** next to the command that produced it. Show the command and its result. If you are unwilling to show the command, do not state the number: describe the pattern instead. A count with no visible command behind it is the single easiest claim to get wrong, and forbidding it is not enough, so the rule is to evidence it or drop it.
- Before reporting that something is absent -- undocumented config, an unused dependency, a missing control, a variable nothing reads -- check every plausible location, not the first one. For a config variable that means the README, env sample files, deploy manifests, comments, and the transitive callers of whatever helper reads it. For a dependency it means whether it is a documented transitive requirement of something you do use. A negative claim from a single grep is not evidence.
- Cite the source of truth and the stale/missing documentation.
- For missing docs, cite the code/config/change that should be documented and the doc area where users would expect it.
- Include exact paths and line references whenever possible.
- State whether the docs are confirmed stale, likely stale, or missing based on inference.
- Do not claim docs are safe to delete unless references, links, generated sources, and navigation were checked.
