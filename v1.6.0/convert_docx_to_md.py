#!/usr/bin/env python3
"""convert_docx_to_md.py — One-shot conversion of iqt_v1_6_0.docx to Markdown.

Preserves heading hierarchy, bold/italic formatting, and marks figure captions.
"""

from docx import Document

DOCX = "iqt_v1_6_0.docx"
OUT = "iqt_v2.md"

HEADING_MAP = {
    "Heading 1": "#",
    "Heading 2": "##",
    "Heading 3": "###",
    "Heading 4": "####",
    "Title": "#",
}


def runs_to_md(paragraph):
    """Convert a paragraph's runs to Markdown inline formatting."""
    parts = []
    for run in paragraph.runs:
        text = run.text
        if not text:
            continue
        if run.bold and run.italic:
            text = f"***{text}***"
        elif run.bold:
            text = f"**{text}**"
        elif run.italic:
            text = f"*{text}*"
        parts.append(text)
    # Fallback: if no runs, use paragraph text
    if not parts and paragraph.text.strip():
        return paragraph.text
    return "".join(parts)


def is_figure_caption(text):
    """Check if a paragraph is a figure caption."""
    stripped = text.strip()
    return (
        stripped.startswith("Figure ")
        or stripped.startswith("Protocol ")
        and ":" in stripped[:30]
    )


def convert():
    doc = Document(DOCX)
    lines = []
    prev_was_empty = False

    for para in doc.paragraphs:
        style = para.style.name
        text = para.text.strip()

        # Skip empty paragraphs (but allow one blank line)
        if not text:
            if not prev_was_empty:
                lines.append("")
                prev_was_empty = True
            continue

        prev_was_empty = False

        # Headings
        if style in HEADING_MAP:
            prefix = HEADING_MAP[style]
            lines.append("")
            lines.append(f"{prefix} {text}")
            lines.append("")
            continue

        # Figure captions
        if is_figure_caption(text):
            lines.append(f"> **{text}**")
            lines.append("")
            continue

        # Normal paragraphs with inline formatting
        md_text = runs_to_md(para)
        lines.append(md_text)
        lines.append("")

    # Write output
    content = "\n".join(lines)
    # Clean up excessive blank lines
    while "\n\n\n\n" in content:
        content = content.replace("\n\n\n\n", "\n\n\n")

    with open(OUT, "w") as f:
        f.write(content)

    print(f"Converted {DOCX} -> {OUT}")
    print(f"Lines: {len(content.splitlines())}")


if __name__ == "__main__":
    convert()
