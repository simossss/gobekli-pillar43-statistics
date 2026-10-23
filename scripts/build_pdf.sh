#!/usr/bin/env bash
# Build gobekli-pillar43-statistics_paper_v2.pdf from the corrected manuscript.
# The manuscript file is not modified. Figures are inserted only in the
# temporary build copy, at the paragraphs that already cite them.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANUSCRIPT="$ROOT/paper/gobekli-pillar43-statistics.md"
OUT="$ROOT/gobekli-pillar43-statistics_paper_v2.pdf"
HEADER="$ROOT/scripts/pdf_header.tex"
FILTER="$ROOT/scripts/pdf_table_widths.lua"

for cmd in pandoc xelatex python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    echo "Install pandoc and a XeLaTeX distribution (texlive-xetex, texlive-latex-extra, texlive-fonts-recommended, texlive-science)." >&2
    exit 1
  fi
done

for f in "$MANUSCRIPT" "$HEADER" "$FILTER"; do
  if [[ ! -f "$f" ]]; then
    echo "Missing file: $f" >&2
    exit 1
  fi
done

for fig in \
  output/fig1_timeline.png \
  output/fig2_sensitivity.png \
  output/fig3_rank_sum.png \
  output/fig4_anchor_bracket.png \
  output/fig5_catalog_sweep.png
do
  if [[ ! -f "$ROOT/$fig" ]]; then
    echo "Missing figure: $ROOT/$fig" >&2
    exit 1
  fi
done

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
BUILD_MD="$TMP/manuscript.md"

python3 - "$MANUSCRIPT" "$BUILD_MD" << 'PY'
import sys
from pathlib import Path

source = Path(sys.argv[1]).read_text(encoding="utf-8")
dest = Path(sys.argv[2])

# Title, subtitle, author, and version are carried by the pandoc title block.
# Drop only those lines so the body is not printed twice. Every other
# sentence stays as written in the manuscript.
preamble = [
    "# How Significant Is the Pillar 43 Sky Map?\n",
    "## A Statistical Decomposition of the Göbekli Tepe Archaeoastronomy Claim\n",
    "\n",
    "**Authors:** Simone Pomposi, Independent Researcher\n",
    "\n",
    "**Version:** 2 draft (2026-10-23, Europe/Paris). Not uploaded to Zenodo.  \n",
]
for line in preamble:
    if not source.startswith(line):
        raise SystemExit(
            "Manuscript preamble does not match the expected opening line:\n"
            + repr(line)
            + "\nFound:\n"
            + repr(source[:120])
        )
    source = source[len(line):]

def figure(path, caption, width="100%"):
    # Alt text is the caption. LaTeX figure labels are suppressed in the header
    # so the manuscript's own "Figure N" is the only number.
    return f"\n\n![{caption}]({path}){{width={width}}}\n\n```{{=latex}}\n\\FloatBarrier\n```\n"

insertions = [
    (
        "center **11,835 BC**.",
        figure(
            "output/fig4_anchor_bracket.png",
            "Figure 4. Anchor test at ±250 years: center-date matches and window matches.",
            "88%",
        )
        + figure(
            "output/fig1_timeline.png",
            "Figure 1. Summer-solstice windows against the catalog.",
        ),
    ),
    (
        "The lower end remains near 10%.",
        figure(
            "output/fig5_catalog_sweep.png",
            "Figure 5. Center-date hit rate across 500 perturbed event catalogs (±250 years).",
        ),
    ),
    (
        "These rank-sum figures do not depend on the catalog or the boundary update.",
        figure(
            "output/fig3_rank_sum.png",
            "Figure 3. Rank-sum null distribution. The observed sum is 18.",
        ),
    ),
    (
        "Half-widths do not set the match window in this grid.",
        figure(
            "output/fig2_sensitivity.png",
            "Figure 2. Center-date anchor rate by tolerance and scenario. Rows use the precision-filtered labels.",
        ),
    ),
]

for anchor, block in insertions:
    count = source.count(anchor)
    if count != 1:
        raise SystemExit(f"Expected exactly one occurrence of anchor, found {count}: {anchor}")
    source = source.replace(anchor, anchor + block, 1)

dest.write_text(source, encoding="utf-8")
print(f"Wrote build manuscript: {dest}")
PY

cd "$ROOT"
pandoc "$BUILD_MD" \
  --from=markdown+tex_math_dollars+tex_math_single_backslash+raw_attribute+implicit_figures \
  --pdf-engine=xelatex \
  --shift-heading-level-by=-1 \
  --resource-path="$ROOT" \
  --lua-filter="$FILTER" \
  --include-in-header="$HEADER" \
  --metadata=title:"How Significant Is the Pillar 43 Sky Map?" \
  --metadata=subtitle:"A Statistical Decomposition of the Göbekli Tepe Archaeoastronomy Claim" \
  --metadata=author:"Simone Pomposi, Independent Researcher" \
  --metadata=date:"Version 2 draft (2026-10-23, Europe/Paris). Not uploaded to Zenodo." \
  --variable=lang:en \
  --variable=papersize:a4 \
  --variable=fontsize:11pt \
  --variable=documentclass:article \
  --variable=geometry:margin=2.35cm \
  --variable=mainfont:"TeX Gyre Pagella" \
  --variable=mathfont:"TeX Gyre Pagella Math" \
  --variable=colorlinks:true \
  --variable=linkcolor:NavyBlue \
  --variable=urlcolor:NavyBlue \
  --output="$OUT"

echo "Wrote $OUT"
