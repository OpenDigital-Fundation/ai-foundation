---
name: office-documents
description: "Use when a task reads or produces Word, Excel, PowerPoint or PDF files (.docx, .xlsx, .pptx, .pdf): creating, editing, converting, extracting tables or text, filling forms or merging. Routes to the official document skills and gives a fallback workflow when they are not installed."
license: MIT
metadata:
  domain: documents
  status: experimental
---
# Office documents

The best skills for Office and PDF files are Anthropic's `docx`, `xlsx`, `pptx` and `pdf` skills. Their licence does not allow redistribution, so this catalog does not copy them: install them from <https://github.com/anthropics/skills> (they are also built into claude.ai), and prefer them whenever they are available.

## Without the official skills

1. **Identify the job:** read, create, edit in place, convert, or extract. Ask for the exact input files and the expected output format.
2. **Pick a library already in the environment** and do not install new ones without asking: `python-docx`, `openpyxl`, `python-pptx`, `pypdf`/`pdfplumber`, or LibreOffice headless for conversion.
3. **Preserve what you did not change:** edit existing files in place (styles, formulas, layouts, comments); never regenerate a document from scratch when the user asked for an edit.
4. **Spreadsheets:** keep formulas as formulas, never paste computed values over them; recalculate and check for errors before delivering.
5. **Verify the output** by reopening it and, for visual formats, rendering it to an image or PDF and looking at it.
6. **Report** the output path and anything that could not be preserved.

For a professional document generated from data or a template, see the reference below.

## References

Load only what the task needs:

- [`references/document-generation.md`](references/document-generation.md) — covers Document Generator
