# How Significant Is the Pillar 43 Sky Map?

**A Statistical Decomposition of the Göbekli Tepe Archaeoastronomy Claim**

Simone Pomposi — Independent Researcher

Zenodo v1 (deposited PDF): [10.5281/zenodo.20364947](https://doi.org/10.5281/zenodo.20364947)

Corrected manuscript (not yet a Zenodo version): [`paper/gobekli-pillar43-statistics.md`](paper/gobekli-pillar43-statistics.md)

The PDF in this repository is the v1 deposit. It has not been rebuilt. Nothing in this revision was uploaded to Zenodo.

---

## Summary

Sweatman & Tsikritsis (2017) proposed that animal carvings on Pillar 43 at Göbekli Tepe encode star constellations and a summer-solstice date near 10,950 BC. Sweatman & Gerogiorgis (2025) state a probability of about 1 in 1.4 million. That figure is the rank-sum probability times 2/7. It does not contain a date term.

This repository is an independent decomposition of that claim. The numbers below are from `gobekli_statistical_test.py` in this revision (`output/results.json`).

- **The published headline has no date term.** Exact rank-sum × 2/7 = \(7.31\times10^{-7}\) (1 in 1,368,083). Sweatman’s “about 1 in 1.4 million,” and the sensitivity down to about 1 in 110,000, are his statements of that product.
- **A date match is not rare on this catalog.** 41.8% of 20,000–5,000 BC lies within ±250 years of a listed event. Strict anchor rate 14/52 (26.9%); broad rate 30/52 (57.7%).
- **The visual signal is concentrated, and the top three were chosen after the ranks were seen.** Pre-specified top three: 1 in 85,184. Sort-then-pick: 1 in 4,484. The other three: 1 in 187. Those subgroup probabilities do not multiply to the six-animal probability (1 in 390,881).
- **Paths that miss the observed reading are not counted as support.** Of 24 valid primary paths, 5 (20.8%) are at least as significant as the exploratory reference path. Eight further primary paths miss (Sagittarius × summer solstice at ±100 or ±200 years).
- **The ranks are self-scored.** The canid → Lupus identification is tentative. A blind ranking is the decisive next test.

## Changelog of figures intended for a Zenodo v2

v1 is the deposited PDF and the previous `output/results.json`. “This run” is the committed recompute. Do not treat the v1 PDF as carrying these figures.

| Quantity | Zenodo v1 | This run |
|----------|-----------|----------|
| Sweatman 1.4M described as | date × visual, weakened because he omitted date look-elsewhere | rank-sum × 2/7; no date term. Exact product 1 in 1,368,083 |
| Strict anchor, ±250 yr | 16/52 = 30.8% | 14/52 = 26.9% |
| Broad anchor, ±250 yr | 35/52 = 67.3% (branch-cut bug) | 30/52 = 57.7% |
| Unwrap only, v1 catalog (diagnostic) | — | 31/52 = 59.6% |
| Coverage, ±250 yr | 42.5% (abstract said 43%) | 41.8% |
| Coverage, ±500 yr | 71.2% | 69.2% |
| Exploratory strict joint, ±250 yr | \(7.87\times10^{-7}\) (1 in 1.27M) | \(6.89\times10^{-7}\) (1 in 1.45M) |
| Exploratory broad joint, ±250 yr | \(1.72\times10^{-6}\) (1 in 581k) | \(1.48\times10^{-6}\) (1 in 678k) |
| Top 3 | 1 in 85,184, as if pre-specified | 1 in 85,184 pre-specified; **1 in 4,484** sort-then-pick |
| Primary paths as significant as the reference | 42% (zero-*P* paths dropped; misses counted) | **5/24 = 20.8%** of valid paths. 0 zero-*P* paths. 8/32 primary misses excluded |
| Reference-path joint | \(7.87\times10^{-7}\) (1 in 1,270,363) | \(5.90\times10^{-7}\) (1 in 1,693,817), hit = Older Dryas, not the YD cluster |
| Valid primary range | about \(9.84\times10^{-8}\) to \(1.97\times10^{-6}\) (unfiltered) | \(4.43\times10^{-7}\) to \(1.57\times10^{-6}\) |
| Extended multiverse | about 1 in 10M to 1 in 111k | 1 in 6,775,270 to 1 in 138,424 (factor ≈ 49) |
| Leave-one-event-out minimum | 25.0% | 21.2% (drop Older Dryas) |
| Circular shifts ≥ baseline | 23.9% | 37.6% |
| Catalog-sweep mean (min–max) | 25.9% (9.6–38.5%) | 25.7% (9.6–38.5%) |
| Heinrich 1 | 14,250 BCE | **14,850 BCE** (Hemming 2004) |
| Mazama | 5,780 ± 200 | **5,677 ± 150 BCE** (Zdanowicz et al. 1999) |
| Mammoth | 7,700 BCE, read as calendar | 7,700 BCE **kept, labeled uncalibrated \(^{14}\)C placeholder** |
| “Major-only” | half-width ≤ 250, described as major events | **precision filter** (dating precision, not magnitude). Matches use the tolerance, not the half-width |
| Pisces/Aries junction | 24.4° | **28.687°** |
| Rank-sum, bottom 3, animal leave-one-out, Table 6 | — | unchanged |

Still open before any Zenodo upload: a Stellarium residual table, an IntCal age for the mammoth cluster, a rebuilt PDF, and record metadata (related identifiers, keywords). Details are in the manuscript changelog and the pull request.

## Repository contents

```
paper/gobekli-pillar43-statistics.md   Corrected manuscript source
gobekli_statistical_test.py            Analysis script (13 experiments)
gobekli-pillar43-statistics_paper.pdf  Zenodo v1 PDF (not regenerated)
output/
  run_log.txt                  Console log of the corrected run
  results.json                 Numerical results, including the multiverse table
  fig1_timeline.png            Constellation windows vs paleoclimatic events
  fig2_sensitivity.png         Sensitivity heatmap (tolerance × scenario)
  fig3_rank_sum.png            Rank-sum null distribution
  fig4_anchor_bracket.png      Anchor test bracket
  fig5_catalog_sweep.png       Catalog robustness histogram
```

## Running the script

Requirements: Python 3.8+, numpy, matplotlib

```bash
pip install numpy matplotlib
python gobekli_statistical_test.py
```

The script writes `output/run_log.txt`, `output/results.json`, and the five figures. Constellation boundaries, the event catalog, and Sweatman’s ranks are in the script. Seed 42.

## The 13 experiments

| # | Experiment | Tests |
|---|-----------|-------|
| 1 | Anchor test | Date-coincidence probability (strict and broad), with unwrapped windows |
| 2 | Exact rank-sum | Visual similarity, plus the published ×2/7 factor |
| 3 | Joint probability | Exploratory product under independence. Not the 1.4M headline |
| 4 | Sensitivity analysis | Tolerance × catalog × cardinal day. Precision filter, not “major” |
| 5 | Catalog robustness | 500 perturbed event catalogs |
| 6 | Rank-sum decomposition | Pre-specified top 3 and sort-then-pick top 3 |
| 7 | Leave-one-event-out | Which events drive the anchor result |
| 8 | Multiverse | 128 paths; validity filter requires the observed reading to be a hit |
| 9 | Coverage fraction | Share of 20,000–5,000 BC near an event |
| 10 | Circular-shift test | Whether absolute event placement matters |
| 11 | Leave-one-animal-out | Which animals drive the similarity result |
| 12 | Ranking sensitivity | Alternative ranking schemes (stress test) |
| 13 | Identity permutation | Whether the specific top-3 trio matters |

## Key references

- Sweatman, M.B. & Tsikritsis, D. (2017). Decoding Göbekli Tepe with archaeoastronomy. *Mediterranean Archaeology and Archaeometry*, 17(1), 233–250.
- Sweatman, M.B. & Gerogiorgis, D. (2025). Origin of some of the ancient Greek constellations via analysis of Pillar 43 at Göbekli Tepe. Submitted manuscript, not peer-reviewed. https://martinsweatman.blogspot.com/2025/05/new-paper-submitted-origin-of-some-of.html
- Notroff, J., Dietrich, O., & Schmidt, K. (2017). More than a vulture: A response to Sweatman and Tsikritsis. *Mediterranean Archaeology and Archaeometry*, 17(2), 57–63.

## AI disclosure

This research was conducted using Claude (Anthropic) as a technical reasoning partner for statistical design, code development, and manuscript drafting. ChatGPT (OpenAI) served as an independent reviewer across multiple review cycles. The analysis was executed on an NVIDIA DGX Spark. The author takes full responsibility for the scientific content and conclusions.

## License

CC BY 4.0
