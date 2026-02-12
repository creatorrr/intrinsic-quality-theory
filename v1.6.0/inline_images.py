#!/usr/bin/env python3
"""inline_images.py — Extract images from iqt_v1_6_0.docx and inline them
as base64 data-URLs into iqt_v1_7_0.md at the correct figure locations.

Image-to-figure mapping (determined by visual inspection):

  image1.jpg  → Figure 1 (line 354): IQT Three-Level Hierarchy
  image6.jpg  → Figure 1 (line 481): Nested Causal Diamonds
  image3.png  → Figure 2 (line 504): Three Layers of Temporal Directionality
  image9.jpg  → Figure 3 (line 513): The Effective-Theory Bridge
  image5.jpg  → Figure 4 (line 544): Shape-Phenomenology Mapping
  image10.jpg → Figure 5 (line 799): Toy Pipeline
  image2.jpg  → Figure 6a (line 973): Overlapping Parcellations
  image7.jpg  → Figure 6b (line 973): Tripartite O-Information Structure
  image8.jpg  → Figure 7 (line 1113): Predicted P(w) Persistence Profiles
  image4.png  → Figure 8 (line 1283): Thought-Experiment Universes
"""

import base64
import os
import re
import zipfile

DOCX = os.path.join(os.path.dirname(__file__), "iqt_v1_6_0.docx")
MD = os.path.join(os.path.dirname(os.path.dirname(__file__)), "iqt_v1_7_0.md")


def extract_images(docx_path):
    """Extract all images from docx and return {filename: base64_data_url}."""
    images = {}
    with zipfile.ZipFile(docx_path) as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                data = z.read(name)
                fname = os.path.basename(name)
                ext = fname.rsplit(".", 1)[-1].lower()
                mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                        "png": "image/png", "gif": "image/gif"}.get(ext, f"image/{ext}")
                b64 = base64.b64encode(data).decode("ascii")
                images[fname] = f"data:{mime};base64,{b64}"
    return images


def img_tag(data_url, alt):
    """Return a markdown image tag with a base64 data URL."""
    return f"![{alt}]({data_url})"


def inline_images():
    images = extract_images(DOCX)
    with open(MD) as f:
        lines = f.readlines()

    # We'll work with line content (keeping newlines).
    # Strategy: find each figure caption line and insert an image tag above it.

    # Build insertion map: {line_number (0-indexed): [image_markdown_lines_to_insert_before]}
    insertions = {}

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Figure 1 (Three-Level Hierarchy) — inline text paragraph
        # Line starts with "IQT: Three Levels of Phenomenal Structure Figure 1:"
        if stripped.startswith("IQT: Three Levels of Phenomenal Structure Figure 1:"):
            tag = img_tag(images["image1.jpg"],
                          "Figure 1: IQT Three-Level Hierarchy – Quality > Experience > Report")
            # Replace the entire line with image + caption
            lines[i] = (
                tag + "\n"
            )
            # Insert a proper caption line after (we'll add it next line)
            insertions[i + 1] = [
                "\n",
                "> **Figure 1: IQT Three-Level Hierarchy** – Quality > Experience > Report. "
                "*\"So rocks are conscious?\"* conflates Level 0 with Level 2.\n",
                "\n",
            ]

        # Figure 1 (Nested Causal Diamonds) — heading
        elif stripped.startswith("#### Figure 1: Nested Causal Diamonds"):
            tag = img_tag(images["image6.jpg"],
                          "Figure 1: Nested Causal Diamonds with Perspectival Relativity")
            insertions[i] = [tag + "\n", "\n"]

        # Figure 2: Three Layers of Temporal Directionality
        elif stripped.startswith("#### Figure 2: Three Layers of Temporal Directionality"):
            tag = img_tag(images["image3.png"],
                          "Figure 2: Three Layers of Temporal Directionality")
            insertions[i] = [tag + "\n", "\n"]

        # Figure 3: The Effective-Theory Bridge
        elif stripped.startswith("#### Figure 3: The Effective-Theory Bridge"):
            tag = img_tag(images["image9.jpg"],
                          "Figure 3: The Effective-Theory Bridge")
            insertions[i] = [tag + "\n", "\n"]

        # Figure 4: Shape-Phenomenology Mapping
        elif stripped.startswith("#### Figure 4: Shape-Phenomenology Mapping"):
            tag = img_tag(images["image5.jpg"],
                          "Figure 4: Shape-Phenomenology Mapping")
            insertions[i] = [tag + "\n", "\n"]

        # Figure 5: Toy Pipeline
        elif stripped.startswith("#### Figure 5: Toy Pipeline"):
            tag = img_tag(images["image10.jpg"],
                          "Figure 5: Toy Pipeline")
            insertions[i] = [tag + "\n", "\n"]

        # Figure 6: Protocol 2 — two images (parcellations + O-information)
        elif stripped.startswith("#### Figure 6: Protocol 2"):
            tag1 = img_tag(images["image2.jpg"],
                           "Figure 6a: Overlapping Parcellations")
            tag2 = img_tag(images["image7.jpg"],
                           "Figure 6b: Tripartite O-Information Structure")
            insertions[i] = [tag1 + "\n", "\n", tag2 + "\n", "\n"]

        # Figure 7: Protocol 3 — persistence profiles
        elif "Figure 7:" in stripped and "Protocol 3" in stripped:
            tag = img_tag(images["image8.jpg"],
                          "Figure 7: Predicted P(w) Persistence Profiles Under Psychedelic Compounds")
            insertions[i] = [tag + "\n", "\n"]

        # Figure 8: Thought-Experiment Universes
        elif stripped.startswith("#### Figure 8: Thought-Experiment Universes"):
            tag = img_tag(images["image4.png"],
                          "Figure 8: Thought-Experiment Universes")
            insertions[i] = [tag + "\n", "\n"]

    # Apply insertions in reverse order (so line numbers don't shift)
    for line_num in sorted(insertions.keys(), reverse=True):
        for insert_line in reversed(insertions[line_num]):
            lines.insert(line_num, insert_line)

    with open(MD, "w") as f:
        f.writelines(lines)

    # Summary
    print(f"Inlined images into {MD}")
    print(f"Total images inlined: {sum(len(v) // 2 for v in insertions.values())}")
    print(f"Output lines: {len(lines)}")


if __name__ == "__main__":
    inline_images()
