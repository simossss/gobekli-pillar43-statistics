# How Significant Is the Pillar 43 Sky Map?

**A Statistical Decomposition of the Göbekli Tepe Archaeoastronomy Claim**

Simone Pomposi, Independent Researcher

| Version | Date | Where | PDF in this repository |
|---------|------|-------|------------------------|
| 3 (current) | 2026-11-10 | not yet on Zenodo | [`gobekli-pillar43-statistics_paper_v3.pdf`](gobekli-pillar43-statistics_paper_v3.pdf) |
| 2 | 2026-10-23 | [10.5281/zenodo.23593750](https://doi.org/10.5281/zenodo.23593750) | [`gobekli-pillar43-statistics_paper_v2.pdf`](gobekli-pillar43-statistics_paper_v2.pdf) |
| 1 | 2026-05-24 | [10.5281/zenodo.20364947](https://doi.org/10.5281/zenodo.20364947) | [`gobekli-pillar43-statistics_paper.pdf`](gobekli-pillar43-statistics_paper.pdf) |

All versions on Zenodo: [10.5281/zenodo.20364946](https://doi.org/10.5281/zenodo.20364946). That DOI always resolves to the latest one.

Manuscript source: [`paper/gobekli-pillar43-statistics.md`](paper/gobekli-pillar43-statistics.md)

---

## Summary

Sweatman & Tsikritsis (2017) proposed that animal carvings on Pillar 43 at Göbekli Tepe encode star constellations and a summer-solstice date near 10,950 BC. Sweatman & Gerogiorgis (2025) state a probability of about 1 in 1.4 million. That figure is the rank-sum probability times 2/7. It does not contain a date term.

This repository is an independent decomposition of that claim. The numbers below are from `gobekli_statistical_test.py` (`output/results.json`).

- **The published headline has no date term.** Exact rank-sum × 2/7 = \(7.31\times10^{-7}\) (1 in 1,368,083). With the Greek stick-figure sum of 26 the same formula gives 1 in 110,312, which is Sweatman’s second figure.
- **A date match is not rare.** The published date is 50 years from the Younger Dryas cluster. But 41.8% of 20,000–5,000 BC lies within ±250 years of a listed event. Strict anchor rate 14/52 (26.9%); broad rate 30/52 (57.7%). Counting only events that predate the monument, coverage is still 33.3%.
- **The visual signal is concentrated, and the top three were chosen after the ranks were seen.** Pre-specified top three: 1 in 85,184. Sort-then-pick: 1 in 4,484. The other three: 1 in 187.
- **The date × visual product depends on analyst choices.** Across 32 primary paths it spans a factor of about 11 (1 in 6.8 million to 1 in 635 thousand), and about 49 once animals are dropped after the ranks are seen.
- **The ranks are self-scored.** A blind ranking is the decisive next test.

## What changed in version 3

Version 2 tested the middle of Sagittarius (11,835 BC) in place of the date Sweatman publishes (10,950 BC). It therefore said the date hit the Older Dryas and not the Younger Dryas. That was wrong and is withdrawn. The published date is 50 years from the Younger Dryas cluster.

| Quantity | Version 2 | Version 3 |
|----------|-----------|-----------|
| Observed reading | Sagittarius midpoint, 11,835 BC | published date, 10,950 BC |
| Event matched by the observed reading | Older Dryas | Younger Dryas cluster |
| Valid primary paths | 24 of 32 | 32 of 32 |
| Primary paths as significant as the reference | 5/24 = 20.8% | 13/32 = 40.6% |
| Span of primary joints | factor 3.6 | factor 10.7 |
| Events that predate the monument only | not run | coverage 33.3%, strict 7/52, broad 21/52 |
| Mammoth cluster removed or recalibrated | not run | strict 14/52 or 15/52 |
| Strict rate among in-window anchors | not reported | 14/30 = 46.7% |
| Position null (random date in a window) | not reported | 23.9% |

Unchanged: the rank-sum, the 2/7 product, the decomposition, both leave-one-out tables, the anchor rates, coverage, the circular shift, and the catalog sweep. The version 1 to version 2 changes are in Appendix A of the manuscript.

Still open: a Stellarium residual table, and a sourced calendar age for the mammoth cluster (robustness check B shows it does not affect the result).

## Repository contents

```
paper/gobekli-pillar43-statistics.md        Manuscript source (version 3)
gobekli_statistical_test.py                 Analysis script (13 experiments, 2 robustness checks)
gobekli-pillar43-statistics_paper_v3.pdf    PDF built from the manuscript
gobekli-pillar43-statistics_paper_v2.pdf    Zenodo v2 PDF (unchanged deposit)
gobekli-pillar43-statistics_paper.pdf       Zenodo v1 PDF (unchanged deposit)
scripts/build_pdf.sh                        Rebuild the PDF (pandoc + XeLaTeX)
scripts/pdf_header.tex                      Page style, captions, and table spacing
scripts/pdf_table_widths.lua                Wrapping column widths for the manuscript tables
requirements.txt                            Python packages
CITATION.cff                                How to cite
output/
  run_log.txt                  Console log of the run
  results.json                 Numerical results, including the multiverse table
  fig1_timeline.png            Constellation windows vs paleoclimatic events
  fig2_sensitivity.png         Sensitivity heatmap (tolerance × scenario)
  fig3_rank_sum.png            Rank-sum null distribution
  fig4_anchor_bracket.png      Anchor test bracket
  fig5_catalog_sweep.png       Catalog robustness histogram
```

## Running the script

Requirements: Python 3.9+, numpy, matplotlib

```bash
pip install -r requirements.txt
python gobekli_statistical_test.py
```

The script writes `output/run_log.txt`, `output/results.json`, and the five figures. Constellation boundaries, the event catalog, and Sweatman’s ranks are in the script. Seed 42.

## Building the PDF

`scripts/build_pdf.sh` reads `paper/gobekli-pillar43-statistics.md` and writes `gobekli-pillar43-statistics_paper_v3.pdf`. It does not edit the manuscript. Where the manuscript cites Figure 1–5, the build inserts the matching file from `output/`.

Requirements: [pandoc](https://pandoc.org/), XeLaTeX, and the TeX Gyre Pagella text and math fonts (Debian/Ubuntu: `pandoc`, `texlive-xetex`, `texlive-latex-recommended`, `texlive-latex-extra`, `texlive-fonts-recommended`, `texlive-science`, `fonts-texgyre-math`). Run it in a UTF-8 locale.

```bash
scripts/build_pdf.sh
```

## The 13 experiments

| # | Experiment | Tests |
|---|-----------|-------|
| 1 | Anchor test | Date-coincidence probability (strict, broad, in-window, position null) |
| 2 | Exact rank-sum | Visual similarity, plus the published ×2/7 factor |
| 3 | Joint probability | Exploratory product under independence. Not the 1.4M headline |
| 4 | Sensitivity analysis | Tolerance × catalog × cardinal day |
| 5 | Catalog robustness | 500 perturbed event catalogs |
| 6 | Rank-sum decomposition | Pre-specified top 3 and sort-then-pick top 3 |
| 7 | Leave-one-event-out | Which events drive the anchor result |
| 8 | Multiverse | 128 paths; the published date must be a hit |
| 9 | Coverage fraction | Share of 20,000–5,000 BC near an event |
| 10 | Circular-shift test | Whether absolute event placement matters |
| 11 | Leave-one-animal-out | Which animals drive the similarity result |
| 12 | Ranking sensitivity | Alternative ranking schemes (stress test) |
| 13 | Identity permutation | Whether the specific top-3 trio matters |
| A | Pre-monument events | Date test with only the events older than the monument |
| B | Mammoth cluster | Date test with the placeholder removed or recalibrated |

## Key references

- Sweatman, M.B. & Tsikritsis, D. (2017). Decoding Göbekli Tepe with archaeoastronomy. *Mediterranean Archaeology and Archaeometry*, 17(1), 233–250.
- Sweatman, M.B. & Gerogiorgis, D. (2025). Origin of some of the ancient Greek constellations via analysis of Pillar 43 at Göbekli Tepe. Submitted manuscript, not peer-reviewed. https://martinsweatman.blogspot.com/2025/05/new-paper-submitted-origin-of-some-of.html
- Notroff, J., Dietrich, O., & Schmidt, K. (2017). More than a vulture: A response to Sweatman and Tsikritsis. *Mediterranean Archaeology and Archaeometry*, 17(2), 57–63.

## AI disclosure

This research was conducted using Claude (Anthropic) as a technical reasoning partner for statistical design, code development, and manuscript drafting. ChatGPT (OpenAI) served as an independent reviewer across multiple review cycles. Accuracy reviews for versions 2 and 3 were performed with Grok, Codex, and Claude. The analysis was executed on an NVIDIA DGX Spark. The author takes full responsibility for the scientific content and conclusions.

## License

CC BY 4.0
