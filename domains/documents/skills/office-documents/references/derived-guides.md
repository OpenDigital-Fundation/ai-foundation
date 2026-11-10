# Office documents — derived guides

Part of `documents:office-documents`.

## PDF Processing Guide

<!-- source: davila7/claude-code-templates cli-tool/components/skills/document-processing/pdf-processing/SKILL.md#python-libraries -->

### Python Libraries

#### pypdf - Basic Operations

##### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

##### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

##### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

##### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

#### pdfplumber - Text and Table Extraction

##### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

##### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

##### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

#### reportlab - Create PDFs

##### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

##### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

##### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Local file conversion

<!-- source: wshobson/agents plugins/file-conversion/skills/file-conversion/SKILL.md#inspect-and-choose,verify-and-deliver -->

### Inspect and choose

1. Confirm the input path, requested output format, and any requirements for quality,
   layout, transparency, streams, or data types. Inspect the actual format and size;
   a filename extension alone is not evidence. Use `file` or the format's local reader.
2. Find installed tools with `command -v` on POSIX shells or `Get-Command` in PowerShell.
   Check the installed version and its readers, writers, codecs, or delegates. Use a
   tool only for a route it supports. Follow the session's existing permission policy
   for installation if a required tool is missing; otherwise report the missing tool.
3. Check local assets and fonts. If inspection cannot rule out external links or
   macros, convert only with network access blocked and macros disabled; otherwise
   stop. Request local assets instead of fetching linked URLs.
4. Choose the smallest suitable route:

| Input and goal | Local tool | Check before converting |
|---|---|---|
| Audio/video container or codec change | FFmpeg + FFprobe | Inspect streams; check encoders/muxers. Stream copying works only when the target container supports the existing codecs. |
| Image format change | ImageMagick (`magick`) | Check `magick -list format`, frame count, color profile, orientation, and alpha. PDF/HEIC support depends on the build and policy. |
| Markdown, HTML, DOCX, or other structured text | Pandoc | Check `--list-input-formats` and `--list-output-formats`. Its JSON format is the Pandoc document tree, not arbitrary JSON data. |
| Office document to PDF | LibreOffice (`soffice`) | Check the installed import/export filters and fonts. Inspect the rendered pages afterward. |
| CSV/JSON data conversion | Python 3 standard library | Inspect encoding, delimiter, headers, nesting, and desired types. Define the schema; do not silently flatten or coerce data. |

PDF to editable Word is not a general lossless conversion. Scanned PDFs need local
OCR tooling before text extraction; layout reconstruction still needs review. Do not
promise a route for an unsupported, encrypted, or damaged input. Explain the limit and
stop rather than renaming the extension or falling back to a hosted service.

### Verify and deliver

- Check the exit status and diagnostics, then require a nonempty output created in
  this attempt's fresh directory. A zero exit status alone is insufficient. Reopen it
  with a reader for the target format; a new suffix does not prove conversion.
- For images, check dimensions, frame count, orientation, and intended alpha/color
  changes. Preview the result. For audio/video, compare stream selection and duration
  with the source and inspect or play a sample; allow for documented encoder padding.
- For documents, inspect text, tables, fonts, and page order. Compare page counts when
  pagination should be preserved; use a PDF reader or `pdfinfo` if available. A text
  extraction check alone cannot establish visual fidelity.
- For data, parse the output and compare row counts, field names, and representative
  values, including Unicode, quoting, empty cells, and leading zeros.

On failure, retain the original, identify the missing capability or reported error,
and do not present a partial file as a completed conversion. Return the absolute output
path, source and target formats, validation results, and any quality loss or unchecked
properties. Keep files local throughout the conversion and delivery workflow.

Command references: [FFmpeg](https://ffmpeg.org/ffmpeg.html),
[Pandoc](https://pandoc.org/MANUAL.html), and
[LibreOffice parameters](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html).

## Markdown to Word with Mermaid

<!-- source: github/awesome-copilot skills/markdown-to-word-mermaid/SKILL.md#conversion-behavior,verification -->

### Conversion behavior

- Headings, paragraphs, emphasis, lists (preserving ordered list start numbers and separate list boundaries), blockquotes, tables, and code blocks become Word content.
- Each Mermaid fence renders to SVG and a 3x PNG with a per-command timeout (default: 120 seconds). Office SVG extensions reference the SVG; the normal image reference retains the PNG fallback, and drawing metadata (`title` and `descr`) includes the section heading or Mermaid `accTitle`/`accDescr` plus the diagram type.
- Output DOCX files are staged and SVG-injected inside a temporary directory before moving to the destination path so failed runs never leave partial files behind.
- The selected font is applied to Word paragraph styles and Mermaid's font configuration. Code runs use Consolas. Fonts are not embedded; unavailable fonts may be substituted.
- `htmlLabels: false` is set globally and for flowcharts to avoid HTML `foreignObject` labels that Office may not display. Check actual SVG output for unsupported constructs.
- Diagrams are centered, keep their aspect ratio, and use a non-splitting paragraph. Diagrams occupying at least 70% of the page body height start on a new page. Oversized diagrams are scaled to the page body height. Large diagrams generate a readability warning.
- A simple single-line frontmatter `title` becomes the document title; other frontmatter fields are removed from the body. This is not a full YAML metadata parser.
- Ordinary Markdown image links remain alt text and a source path or URL; they are not embedded. Raw HTML is reduced to text, not executed.

### Verification

Run the test suite from the skill directory:

```sh
python -m unittest discover -s tests -v
```

The ordinary suite mocks Mermaid rendering. To run the real-renderer test as well, set `MERMAID_CLI` to the CLI executable's absolute path, then run the command again. On Windows PowerShell:

```powershell
$env:MERMAID_CLI = (Join-Path $env:APPDATA "npm\mmdc.cmd")
python -m unittest discover -s tests -v
```

That test renders the bundled sample and checks the resulting DOCX's SVG references, PNG fallbacks, labels, and drawing dimensions. It does not automate Word visual inspection.

Before reporting completion:

- Count Mermaid fences and verify the same number of SVG parts and SVG image references in the DOCX.
- Confirm PNG fallback references exist and no label `foreignObject` remains in the sample's SVGs.
- In Word, inspect node names, branch labels, font, diagram placement, and page boundaries; check zoomed or printed output when sharpness matters.
- If Word or the actual renderer was unavailable, state which checks were not performed.

For contribution scope, evaluation cases, and a draft submission description, see references/publication.md. That file is maintainer guidance, not permission to publish.
