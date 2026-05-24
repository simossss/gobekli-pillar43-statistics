# How Significant Is the Pillar 43 Sky Map?

**A Statistical Decomposition of the Göbekli Tepe Archaeoastronomy Claim**

Simone Pomposi — Independent Researcher

Paper: [Zenodo DOI forthcoming]

---

## Summary

Sweatman & Tsikritsis (2017) proposed that animal carvings on Pillar 43 at Göbekli Tepe encode star constellations, dating the monument to ~10,950 BC via precession of the equinoxes. The revised statistical significance claim (Sweatman & Gerogiorgis, 2025) stands at approximately 1 in 1.4 million.

This repository contains an independent statistical decomposition of that claim across 13 experiments. Key findings:

- **The date coincidence is not rare.** 43% of the 20,000–5,000 BC window lies within ±250 years of a notable paleoclimatic event. 31% of random constellation-cardinal assignments produce a date match.
- **The visual similarity is genuine but concentrated.** The overall P ≈ 1 in 391,000 is overwhelmingly driven by three of six mappings (1 in 85,184). The remaining three contribute 1 in 187 — still significant, but far less weight.
- **Significance is path-dependent.** Across 128 analyst-choice paths, the joint probability spans two orders of magnitude (1 in 10M to 1 in 111K).
- **Rankings are self-scored.** The entire statistical case depends on three visual similarity judgments made by the hypothesis proponent and never independently validated.

## Repository contents

```
gobekli_statistical_test.py    Main analysis script (13 experiments, ~1,500 lines)
paper.pdf                      Full paper
output/
  run_log.txt                  Complete console output from the official run
  results.json                 Full numerical results (including multiverse path table)
  fig1_timeline.png            Constellation windows vs paleoclimatic events
  fig2_sensitivity.png         Sensitivity heatmap (tolerance × scenario)
  fig3_rank_sum.png            Rank-sum null distribution
  fig4_anchor_bracket.png      Anchor test bracket chart
  fig5_catalog_sweep.png       Catalog robustness histogram
```

## Running the script

Requirements: Python 3.8+, numpy, matplotlib

```bash
pip install numpy matplotlib
python gobekli_statistical_test.py
```

The script is fully self-contained. All data — constellation boundaries, event catalog, Sweatman's rankings — are embedded. No external files or APIs needed. Output goes to `output/`.

## The 13 experiments

| # | Experiment | Tests |
|---|-----------|-------|
| 1 | Anchor test | Date-coincidence probability (strict and broad null) |
| 2 | Exact rank-sum | Visual similarity probability (inclusion-exclusion) |
| 3 | Joint probability | Combined under independence assumption |
| 4 | Sensitivity analysis | Tolerance × scenario × cardinal day |
| 5 | Catalog robustness | 500 perturbed event catalogs |
| 6 | Rank-sum decomposition | Top-3 vs bottom-3 mappings |
| 7 | Leave-one-event-out | Which events drive the anchor result |
| 8 | Multiverse | 128 analyst-choice paths (primary vs extended) |
| 9 | Coverage fraction | What share of the era is near an event |
| 10 | Circular-shift test | Does absolute event placement matter |
| 11 | Leave-one-animal-out | Which animals drive the similarity result |
| 12 | Ranking sensitivity | Alternative ranking schemes (stress test) |
| 13 | Identity permutation | Does the specific top-3 trio matter |

## Key references

- Sweatman, M.B. & Tsikritsis, D. (2017). "Decoding Göbekli Tepe with Archaeoastronomy." *MAA*, 17(1), 233–250.
- Sweatman, M.B. & Gerogiorgis, D. (2025). "Origin of some ancient Greek constellations via Pillar 43." [Preprint]
- Notroff, J. et al. (2017). "More than a vulture: A response to Sweatman and Tsikritsis." *MAA*, 17(2), 57–63.

## AI disclosure

This research was conducted using Claude (Anthropic) as a technical reasoning partner for statistical design, code development, and manuscript drafting. ChatGPT (OpenAI) served as an independent reviewer across multiple review cycles. The analysis was executed on an NVIDIA DGX Spark. The author takes full responsibility for the scientific content and conclusions.

## License

CC BY 4.0
