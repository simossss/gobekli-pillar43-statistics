# How Significant Is the Pillar 43 Sky Map?
## A Statistical Decomposition of the Göbekli Tepe Archaeoastronomy Claim

**Authors:** Simone Pomposi, Independent Researcher

**Version:** 2 draft (2026-10-23, Europe/Paris). Not uploaded to Zenodo.  
**Zenodo v1:** [10.5281/zenodo.20364947](https://doi.org/10.5281/zenodo.20364947)  
**Manuscript source:** `paper/gobekli-pillar43-statistics.md`  
**Numbers:** recomputed by `gobekli_statistical_test.py` in this revision. Authoritative machine output is `output/results.json` and `output/run_log.txt`. The repository PDF is the v1 deposit and has not been regenerated.

No Stellarium residual table was produced. Where a calendar age is not in the cited primary source, the text says so instead of substituting a calibration.

---

## Changelog vs Zenodo v1

| # | Severity | Change |
|---|----------|--------|
| 1 | **Critical** | Sweatman & Gerogiorgis (2025) **1 in 1.4 million** is rank-sum probability × **2/7** (top-row reversal × spatial correlation). It has **no date term**. Date coincidence is a separate exploratory test. Their own sensitivity range, switching stick-figure sets, is about **1.4 million to 110 thousand**. Our exact product is \(7.31\times10^{-7}\) (**1 in 1,368,083**). |
| 2 | **High** | Multiverse **validity filter**: the observed Sagittarius × summer-solstice reading must be a hit. This run: **5/24 = 20.8%** of valid primary paths are as or more significant than the exploratory reference path. **0** paths have joint probability 0. **8/32** primary paths are observed misses and are excluded from that percentage. v1 reported **42%** after dropping zero-*P* paths and counting misses. |
| 3 | **High** | Top-3 **1 in 85,184** is only the pre-specified trio (\(1/44^3\)). Sort-then-pick gives \(P(\ge 3\text{ of }6\text{ ranks}=1)=2.230\times10^{-4}\) (**1 in 4,484**). \(P(\text{top})\times P(\text{bottom})\neq P(\text{all six})\). |
| 4 | **High** | `constellation_date_range()` no longer folds endpoints across the precession branch cut. On the **unchanged v1 catalog** that fix moves the broad match from **35/52 (67.3%)** to **31/52 (59.6%)**. After the catalog and Pisces/Aries updates below, this run’s broad match is **30/52 (57.7%)** and the strict match is **14/52 (26.9%)**. |
| 5 | **High** | Heinrich 1 set to **14,850 BCE** (Hemming 2004: 16,800 calendar years, 1950 BP convention). Mazama set to **5,677 ± 150 BCE** (Zdanowicz et al. 1999). Mammoth **7,700 BCE kept as an uncalibrated placeholder** — Kuzmin & Orlova (2004) publish \(^{14}\)C ages, not a calendar date. “Major-only” renamed **precision-filtered** (half-width ≤ 250 yr). Matching uses the stated tolerance, not half-width. |
| 6 | **High** | §2.3: 2017 ≈ 100 million → 2019 ≈ **140 million** is a **stronger** claim, not a reduction. The 2017 statistic was not summed ranks. The 2019 appendix includes a **×13** factor that treats scorpion = Scorpius as given. |
| 7 | **Medium+** | Equinox prose: **Virgo = spring**, **Pisces = autumn**. The pool of 44 is Ptolemy’s 48 minus Canis Major, Lepus, Eridanus, and Argo Navis, not every constellation visible from the site. Notroff’s objection is paraphrased, not quoted as “incredibly arbitrary.” Canid → Lupus marked tentative. Dietrich et al. (2013) cited as calibrated ranges for Enclosure D, not a site-wide Gaussian. Coverage is **41.8%** in this run (v1 results were 42.5%; the v1 abstract’s 43% rounded that figure). |
| 8 | **Code** | Pisces/Aries ecliptic junction set to **28.687°** (IAU boundary ∩ J2000 ecliptic; the review’s ~28.8°). Other junctions stay at the v1 one-decimal table. |
| 9 | **Citations** | Sweatman 2025 URL and not-peer-reviewed status; Sweatman 2024 full cite and DOI; Ruggles as editor; Ryan et al.; Holliday et al. 2023 as optional YDIH context. |
| 10 | **Not in this commit** | Stellarium residual table. IntCal calendar age for the mammoth cluster. Rebuilt PDF. Zenodo `newversion`, related identifiers, or keywords. |

---

## Abstract

Sweatman & Tsikritsis (2017) proposed that animal carvings on Pillar 43 at Göbekli Tepe encode star constellations, dating the monument to ∼10,950 BC via precession of the equinoxes—coinciding with the proposed Younger Dryas impact event. Sweatman & Gerogiorgis (2025) later stated a combinatorial visual-similarity probability of approximately **1 in 1.4 million**. That figure is the probability of a rank-sum ≤ 18 multiplied by **2/7** (top-row reversal symmetry and a spatial-correlation allowance). It does **not** include a paleoclimatic date term. An exact evaluation of the same product is \(7.31\times10^{-7}\) (1 in 1,368,083). We separate that published calculation from an exploratory date test.

Across 13 analyses on the corrected catalog we find: (1) the date coincidence is not rare—**14/52 (26.9%)** of constellation × cardinal-day center dates fall within ±250 years of a catalogued event, and **30/52 (57.7%)** of the full constellation windows overlap such an event; **41.8%** of the years from 20,000 to 5,000 BC lie within ±250 years of at least one catalogued event; (2) within Sweatman’s self-scored ranks the visual similarity is unusual (\(P = 2.558\times10^{-6}\), about 1 in 390,881), but the signal is concentrated in three of six mappings (**1 in 85,184** if those three animals are pre-specified; **1 in 4,484** if the three best ranks are chosen after seeing all six), while the other three remain conventionally significant and much weaker (1 in 187); (3) after requiring that the observed Sagittarius × summer-solstice reading actually hit, **5 of 24** valid primary paths (20.8%) are as or more significant than the exploratory reference path. The statistical case depends on three self-scored visual rankings that have not been blindly replicated. A blind ranking experiment would be the decisive test. Code and data are in this repository.

**Keywords:** archaeoastronomy, Göbekli Tepe, statistical significance, look-elsewhere effect, precession, multiverse analysis

---

## 1. Introduction

Göbekli Tepe, a monumental Neolithic site in southeastern Turkey, has produced some of the most debated archaeological interpretations of the last decade. Among them, the proposal by Sweatman and Tsikritsis (2017) stands out for its specificity: the animal carvings on Pillar 43 in Enclosure D represent star constellations, and the scene encodes the date of the summer solstice at approximately 10,950 BC via precession of the equinoxes. This date coincides with the proposed Younger Dryas impact event (Kennett et al., 2015; see also Holliday et al., 2023, for a critical review of the Younger Dryas Impact Hypothesis), leading the authors to interpret the pillar as a memorial to a cosmic catastrophe. The claim was published in *Mediterranean Archaeology and Archaeometry* and has since been extended to European Palaeolithic cave art (Sweatman & Coombs, 2019), a lunisolar calendar embedded in the same pillar’s geometric symbols (Sweatman, 2024), and a further probabilistic analysis (Sweatman & Gerogiorgis, 2025).

The excavation team responded with a qualitative rebuttal (Notroff et al., 2017), raising objections about pillar repositioning during multi-phase rebuilding, a 700–1,000 year gap between the proposed date and the site’s radiocarbon chronology, and the assumption that Neolithic hunters recognized Greek-derived constellations—an assumption the rebuttal treats as highly arbitrary. These are serious concerns. Neither the rebuttal nor later work published the quantitative decomposition attempted here: whether the stated statistical evidence is as strong as claimed, or whether it arises from a dense event record, subjective visual matching, and researcher degrees of freedom.

This paper evaluates Sweatman’s **visual-similarity** calculation (the rank-sum and the published **2/7** multiplier) and, separately, a **date-coincidence** component under paleoclimatic look-elsewhere models. Joint products of those components are reported as exploratory and are not identified with the 1.4-million headline.

The date component is readily obtained under the null used here. The visual component is concentrated in three of six mappings, and that concentration is weaker once the three mappings are recognized as the best of six rather than as a pre-specified trio. The paper proceeds as follows. Section 2 is background. Section 3 is methods. Section 4 is the 13 analyses. Section 5 is implications, limitations, and the blind-test proposal.

---

## 2. Background

### 2.1 Göbekli Tepe and Pillar 43

Göbekli Tepe is located near Şanlıurfa in southeastern Turkey, approximately 15 km northeast of the city centre. Excavations led by Klaus Schmidt (DAI) from 1995 until his death in 2014, and continued by the Şanlıurfa Museum and DAI, have uncovered a sequence of roughly circular enclosures formed by T-shaped megalithic pillars and rough stone walls (Schmidt, 2003; Dietrich et al., 2012). Enclosure D plaster and associated contexts yield calibrated radiocarbon ranges in the mid-to-late 10th millennium cal BC (Dietrich et al., 2013; e.g. sample KIA-44149: 9745–9314 cal BC). Treating these as a single Gaussian such as “9,530 ± 215 BCE” would overstate precision and would present a site-wide estimate the excavation report does not make. The chronological gap relative to ~10,950 BC is left as qualitative context from the excavation team.

Pillar 43 is embedded in the northwestern portion of Enclosure D’s perimeter wall. Its western broadside carries an elaborate relief: a large vulture or eagle with a circular disc on its wing, a scorpion below, a canid to the left, a tall bird grasping a fish or snake to the right, a partially obscured swimming bird at the bottom, and several smaller figures. The narrow faces carry further carvings, including snakes and a spider. A headless human figure appears at the base.

The excavation team reads the scene in the context of Pre-Pottery Neolithic mortuary ritual and excarnation (Peters & Schmidt, 2004; Notroff et al., 2016). The vulture and headless man are referred to a documented tradition of defleshing by raptors. The disc is sometimes read as a severed head.

### 2.2 Sweatman’s astronomical interpretation

Sweatman and Tsikritsis (2017) identified animal symbols on Pillar 43 with star constellations, using the modern Western set as drawn in Stellarium. The mappings used here are in Table 1.

**Table 1.** Animal–constellation mappings for Pillar 43. Ranks are those published by Sweatman & Gerogiorgis (2025) against a pool of **44** constellations: Ptolemy’s 48 minus four southern figures they treat as not visible from the site at the relevant epoch (Canis Major, Lepus, Eridanus, and Argo Navis). That pool is not a census of every modern constellation above the horizon at ~37.2°N. The vulture is the date anchor and is excluded from the rank-sum. The duck/goose is excluded as partly obscured. The canid → Lupus identification is **tentative** (Section 5.2): the carving is a canid, and the wolf/dog species call is not independently settled.

| Animal | Constellation | Rank (of 44) | Role |
|--------|---------------|--------------|------|
| Vulture/eagle | Sagittarius | — | Anchor (excluded) |
| Scorpion | Scorpius | 1 | Tested |
| Wolf/dog | Lupus | 1 | Tested (tentative) |
| Tall bird + snake | Ophiuchus | 1 | Tested |
| Bending bird | Pisces | 4 | Tested |
| Ibex/quadruped | Gemini | 5 | Tested |
| Frog/bear | Virgo | 6 | Tested |
| Duck/goose | Libra | — | Excluded (obscured) |

The date is derived in five steps. The disc on the vulture’s wing is identified as the Sun, by analogy with a disc beside a crescent on Pillar 18. The vulture is Sagittarius, specifically the “teapot” asterism. The Sun in Sagittarius is read as the summer solstice, because a winter solstice in Sagittarius falls near 2000 AD. With a precession period of about 25,772 years, the summer-solstice Sun lay in Sagittarius near 10,950 ± 250 BC. Three “handbag” symbols are then read as the other cardinal stations: **Virgo for the spring equinox, Gemini for the winter solstice, and Pisces for the autumn equinox**. The v1 prose swapped Pisces and Virgo between spring and autumn. The analysis code used the assignment in this paragraph.

### 2.3 The probability calculation and its revisions

The published figure has moved more than once in eight years. The path is **not** a sequence of revisions each reducing the claimed significance.

- Sweatman & Tsikritsis (2017) reported approximately **1 in 100 million**. That calculation ranked Göbekli Tepe animal symbols against a small constellation pool and counted favorable combinations. It was **not** the later summed-ranks statistic.
- Sweatman & Coombs (2019) reported approximately **1 in 140 million** for the Vulture Stone match. Moving from 100 million to 140 million **increases** the claimed rarity. Appendix A of that paper multiplies by **13** after treating the scorpion = Scorpius identification as given, and then applies a separate positional factor. The 2019 statistic is still a symbol-combination count, not the 2025 rank-sum.
- Sweatman & Gerogiorgis (2025) — a submitted manuscript posted by the authors, not a peer-reviewed journal article — exclude the vulture from the test, compare six animals with 44 constellations, and state a headline of about **1 in 1.4 million**. In their own words the probability is \(p \times 2/7\), where \(p\) is the probability of rolling a score of 18 or less on six 44-sided dice, the factor 2 is the symmetry of the top row (the order can be reversed and still read as the same date), and division by 7 is the spatial correlation carried forward from 2019. There is no paleoclimatic date in that product. Using a more detailed Greek stick-figure set, they report that the same headline moves to about **1 in 110,000**.

Our exact rank-sum is \(p = 2.558\times10^{-6}\) (1 in 390,881). Multiplied by 2/7 it is \(7.31\times10^{-7}\) (1 in 1,368,083), the same order as the stated 1.4 million. Sweatman’s round number comes from an online calculator applied to the same product, not from a date term.

The v1 paper’s exploratory joint, about 1 in 1.27 million, was \(2.56\times10^{-6}\times 0.308\). That 0.308 was the strict anchor rate before the corrections in this draft. It sits near \(2/7 \approx 0.286\), so the two products looked alike. The likeness was a shared rank-sum times an \(O(0.3)\) factor. It was not evidence that the 1.4 million calculation contains a date. On this run the strict joint is \(2.558\times10^{-6}\times 14/52 = 6.89\times10^{-7}\) (1 in 1,451,844). The comparison with \(p\times 2/7\) is unchanged in kind.

### 2.4 The Notroff et al. rebuttal

Notroff et al. (2017) object that Enclosure D’s pillars are not all in their original positions, that 10,950 BC is 700–1,000 years older than the oldest radiocarbon dates associated with Enclosure D, that recognizing the Greek constellations in Neolithic art is highly arbitrary, and that the argument selects a few pillars from a site with many animal reliefs.

Sweatman and Tsikritsis (2017b) answered that a probability should outrank an opinion, and that the radiocarbon date dates wall mortar rather than the carving. Neither side published the null models in Section 3.

---

## 3. Methods

### 3.1 Precession engine

The ecliptic longitude of the vernal equinox is shifted linearly at \(360^\circ/25{,}772 \approx 0.01397^\circ\) per year. For a year BC and a cardinal day, the Sun’s J2000 ecliptic longitude is compared with the constellation intervals in the script. Two internal checks, which are **not** a Stellarium validation, still pass: at 10,950 BC the summer-solstice Sun is at \(270.89^\circ\), inside Sagittarius (\(266.5^\circ\)–\(300.0^\circ\)); at 3,000 BC the vernal equinox is at \(69.84^\circ\), inside Taurus (\(53.5^\circ\)–\(90.4^\circ\)).

The Pisces/Aries junction in this run is **28.687°**, the intersection of the IAU (B1875) boundary with the J2000 ecliptic (Asher’s reduction; the review rounded this to ~28.8°). v1 used 24.4°. The other twelve junctions are still the v1 one-decimal table. A residual table against Stellarium or a full boundary refresh was **not run**. The linear engine is treated as adequate for windows of a few centuries, with about \(1^\circ\) of error over 13,000 years (~70 years).

`constellation_date_range()` returns one short interval centered on the constellation midpoint, with length \(\Delta\lambda\) divided by the precession rate. v1 folded each endpoint into a single 25,772-year branch and took the minimum and maximum. Four pairs straddle that branch cut — Taurus × spring equinox, Leo × summer solstice, Libra × autumn equinox, and Aquarius × winter solstice — and their windows jumped by almost a full precession cycle. On the v1 catalog those four spurious windows raised the ±250 yr broad hit count from 31/52 to 35/52. The script now refuses to continue if any of the 52 windows disagrees with its angular width by more than a year.

### 3.2 Paleoclimatic event catalog

The catalog is 14 analyst-defined clusters between 20,000 and 5,000 BC (Table 2). Sources are ice-core chronologies (GICC05), speleothems, radiocarbon-dated geological events, and marine cores. The construction note in v1 said that events with different physical causes less than 500 years apart were grouped. That rule was not applied consistently. This run still has three pairs of centers less than 500 years apart, kept as separate clusters:

- YD termination and PBO / Bond 8 / MWP-1B, 350 years
- the mammoth placeholder and Bond 6, 250 years
- Mazama and the late cluster, 177 years

The 14 clusters are scenarios, not a unique partition of the deglacial record. Each cluster carries a half-width as a dating-uncertainty label. **Primary matches do not use that half-width.** They use a uniform tolerance (±100, 200, 250, or 300 years in the multiverse; the anchor grid also reports ±500). The half-width is used to build the precision-filtered subset and to scale the catalog-sweep perturbations.

**Table 2.** Event clusters used in this run. Dates in bold differ from v1.

| Cluster | Date (BC) | Half-width (yr) | Basis |
|---------|-----------|-----------------|-------|
| LGM peak | 19,050 | 1,000 | Clark et al. (2009); v1 date retained |
| Bonneville Flood | 15,550 | 500 | O’Connor (1993); v1 date retained |
| Heinrich Event 1 | **14,850** | 500 | Hemming (2004), Table 4: 16,800 calendar years (14,200 \(^{14}\)C yr + 2,600). Placed at 14,850 BCE with the 1950 BP convention. v1 used 14,250 BCE |
| Bølling-Allerød + MWP-1A | 12,700 | 200 | Deschamps et al. (2012); v1 date retained |
| Older Dryas | 12,075 | 200 | Rasmussen et al. (2014); v1 date retained |
| YD cluster | 10,900 | 250 | Reinig et al. (2021); Kennett et al. (2015); v1 date retained |
| YD termination | 9,750 | 100 | Cheng et al. (2020); v1 date retained |
| PBO / Bond 8 / MWP-1B | 9,400 | 200 | Rasmussen et al. (2007); v1 date retained |
| Bond 7 | 8,350 | 500 | Bond et al. (1997); v1 date retained |
| Mammoth extinction (N. Asia) | 7,700 | 300 | **Not a calibrated age.** Kuzmin & Orlova (2004): mainland extinction ca. 9700 \(^{14}\)C BP; Wrangel survival ca. 7700–3700 \(^{14}\)C BP. v1’s 7700 BCE is retained only as that placeholder |
| Bond 6 | 7,450 | 500 | Bond et al. (1997); v1 date retained |
| 8.2 ka cluster | 6,300 | 300 | Barber et al. (1999); v1 date retained |
| Mazama VEI 7 | **5,677** | **150** | Zdanowicz et al. (1999): 7627 ± 150 cal yr BP = 5677 ± 150 BCE. v1 used 5780 ± 200 |
| Late cluster | 5,500 | 400 | Ryan et al. (1997); v1 date retained |

The subset formerly called “major-only” is **precision-filtered**: half-width ≤ 250 years. In this catalog that keeps six clusters (Bølling-Allerød + MWP-1A, Older Dryas, the YD cluster, YD termination, PBO / Bond 8 / MWP-1B, and Mazama). Heinrich 1, with half-width 500 years, is excluded. The cut is dating precision, not event size. A precision-filtered event is still matched at the scenario tolerance, which can be wider than its half-width.

### 3.3 Visual similarity model

Each of the six tested animals is ranked independently against the 44-constellation pool. The published ranks are [1, 1, 1, 4, 5, 6], sum 18. \(P(S \le 18)\) for six independent uniform draws from \(\{1,\ldots,44\}\) is computed by inclusion-exclusion. Three-animal subgroups are checked by enumeration.

The published multiplier is evaluated directly: \(P_{\text{2025}} = P(S \le 18)\times(2/7)\). That quantity is compared with the exploratory date × visual products. It is not replaced by them.

### 3.4 Null models

**Anchor null (date, exploratory).** A random assignment picks one of 13 ecliptic constellations and one of four cardinal days (52 combinations), computes the precession date, and asks whether it meets the catalog. The strict variant uses the constellation center. The broad variant asks whether the constellation’s date interval overlaps any event window at the stated tolerance. Only **30 of the 52** center dates fall inside 20,000–5,000 BC. Coverage (uniform over years) and the anchor rate (uniform over 52 anchors) are different sampling domains. Both are reported, and statements are conditioned on the domain.

**Similarity null.** Each animal draws a rank uniformly from \(\{1,\ldots,44\}\). \(P(S \le 18)\) is the visual *p*-value under that null.

**Joint exploratory product.** \(P(\text{joint}) = P(\text{anchor match})\times P(S \le 18)\), assuming independence. This is not the 2025 headline. If the ranks were influenced by the target date, the joint probability is higher (less rare).

**Multiverse.** Paths cross anchor model (center vs window), tolerance (100, 200, 250, 300 yr), catalog (all 14 vs precision-filtered), cardinal scope (summer solstice only vs all four), and animal inclusion (all 6, or the best 5, 4, or 3). There are 128 paths, of which 32 keep all six animals (the primary set).

**Validity filter.** A path is valid only when Sagittarius × summer solstice is a hit under that path’s catalog, tolerance, and anchor model. Center-model hits use the Sagittarius midpoint. Window-model hits use the Sagittarius date interval. Paths on which that observed reading misses — including summer-solstice center tests at ±100 and ±200 years, where the midpoint (11,835 BC) is 240 years from the Older Dryas and does not land on the Younger Dryas cluster — are excluded from the “as significant as the reference” count and are listed. Zero-probability paths are counted rather than dropped. This run has **zero** such paths, so the v1 habit of reporting a fraction out of 31 rather than 32 does not arise. The reference path is summer solstice, all events, ±250 years, center anchor, all six animals. Its joint is an exploratory product, not \(p\times 2/7\).

### 3.5 Software and reproducibility

One Python script, `gobekli_statistical_test.py`, uses only numpy and matplotlib. Constellation boundaries, the event catalog, and the ranks are in the script. The committed outputs are `output/run_log.txt`, `output/results.json`, and `output/fig1_timeline.png` through `output/fig5_catalog_sweep.png`. Seed 42 fixes the catalog sweep, the circular shift, the rank-sum histogram, and the identity permutation.

---

## 4. Results

### 4.1 The date coincidence is not rare

**Anchor test (Experiment 1).** Of 52 constellation × cardinal-day combinations at ±250 years, **14 (26.9%)** match on the center date and **30 (57.7%)** match on the window (Figure 4). At ±100 years the strict rate is **7/52 (13.5%)**. The 14 strict matches at ±250 years cover **10** of the 13 ecliptic constellations and all four cardinal days, from the Bonneville Flood to the late cluster. Figure 1 shows summer-solstice windows against the catalog. Sagittarius at the summer solstice still runs from **10,635 to 13,034 BC**, center **11,835 BC**.

The broad rate of 30/52 is not the unwrap-only diagnostic. With the date-range fix and the **v1** dates and boundaries, the broad count is 31/52 (59.6%). Heinrich, Mazama, and the Pisces/Aries junction then move it to 30/52.

**Coverage (Experiment 9).** **41.8%** of the 15,000 years from 20,000 to 5,000 BC lies within ±250 years of at least one catalogued event. At ±100 years coverage is 18.5%; at ±500 years it is 69.2%. v1’s results file had 42.5% at ±250 years. The v1 abstract’s “43%” was a rounding of that 42.5%, not a separate estimate. This draft uses 41.8% wherever it states the recomputed coverage.

**Leave-one-event-out (Experiment 7).** The ±250 year center rate is 26.9% (14/52). Removing the Older Dryas drops it to **21.2%** (11/52), a **5.8** percentage-point fall, the largest single-cluster effect. Removing the Younger Dryas cluster does not change the 14 hits. The Sagittarius summer-solstice center (11,835 BC) is 240 years from the Older Dryas (12,075 BC) and about 935 years from the YD cluster (10,900 BC), so the strict anchor “hit” for the observed constellation is an Older Dryas hit, not a Younger Dryas hit. v1’s statement that no removal pushes the rate below 25% does not survive the updated catalog.

**Circular shift (Experiment 10).** Shifting the whole catalog inside 20,000–5,000 BC, wrapping modulo 15,000 years, preserves the number of events and their spacing. Across 1,000 shifts, **37.6%** produce a ±250 year center rate at least as high as the 26.9% baseline (shifted mean 24.1%). v1 reported 23.9% against its 30.8% baseline. Event density still does most of the work; the real placement is not an unusually favorable alignment under this shift model.

**Catalog sweep (Experiment 5).** Five hundred catalogs drop 0–3 events and shift the remaining dates by a normal draw with standard deviation half the cluster half-width. The ±250 year center rate runs from **9.6% to 38.5%** (mean **25.7%**, median 25.0%; Figure 5). The lower end remains near 10%.

### 4.2 The visual similarity is unusual and concentrated

**Exact rank-sum (Experiment 2).** \(P(S \le 18) = 2.558\times10^{-6}\), 1 in 390,881. The null expectation is \(135 \pm 31\). The observed sum 18 is 3.76 standard deviations below that mean (Figure 3). These rank-sum figures do not depend on the catalog or the boundary update.

**The 2/7 factor.** \(2.558\times10^{-6}\times 2/7 = 7.309\times10^{-7}\), 1 in 1,368,083. That is the published headline’s order of magnitude, with no date term. A date look-elsewhere correction does not “explain” the 1.4 million figure from inside the 2025 formula. It answers a different question.

**Decomposition (Experiment 6).** Sorting the six ranks and splitting them into [1, 1, 1] and [4, 5, 6] is what the code does. For three **pre-specified** animals, \(P(\text{all three rank 1}) = 1/44^3 = 1/85{,}184\). For the operation actually performed — keep the best three of six — the null probability of three or more rank-1 outcomes is

\[
\sum_{k=3}^{6}\binom{6}{k}\left(\frac{1}{44}\right)^{k}\left(\frac{43}{44}\right)^{6-k} = 2.230\times10^{-4},
\]

which is **1 in 4,484**. The bottom three have \(P(S \le 15) = 5.34\times10^{-3}\) (1 in 187). The product of the pre-specified top-three probability and the bottom-three probability is \(6.27\times10^{-8}\), which is **not** \(P(S \le 18)\). Table 3 is a diagnostic split, not a factorization.

**Table 3.** Rank-sum decomposition. Inclusion-exclusion, checked by enumeration for the groups of three.

| Group | Ranks | Sum | *P* | ≈ 1 in |
|-------|-------|-----|-----|--------|
| Top 3, pre-specified (scorpion, canid, Ophiuchus) | [1, 1, 1] | 3 | \(1.17\times10^{-5}\) | 85,184 |
| Top 3, sort-then-pick | at least three 1s among six | — | \(2.23\times10^{-4}\) | 4,484 |
| Bottom 3 (Pisces, Gemini, Virgo) | [4, 5, 6] | 15 | \(5.34\times10^{-3}\) | 187 |
| All 6 | [1, 1, 1, 4, 5, 6] | 18 | \(2.56\times10^{-6}\) | 390,881 |

**Leave-one-animal-out (Experiment 11).** Dropping any one rank-1 animal multiplies the rank-sum probability by 14.7 (Table 4). The three rank-1 animals tie. Dropping the bending bird (rank 4) weakens the result by 4.7×, the ibex (rank 5) by 3.1×, and the frog/bear (rank 6) by 1.9×.

**Table 4.** Leave-one-animal-out. Unchanged from v1; the ranks did not change.

| Dropped animal | Rank | Remaining *P* | ≈ 1 in | Weakening |
|----------------|------|---------------|--------|-----------|
| Scorpion | 1 | \(3.75\times10^{-5}\) | 26,651 | 14.7× |
| Wolf/dog | 1 | \(3.75\times10^{-5}\) | 26,651 | 14.7× |
| Tall bird + snake | 1 | \(3.75\times10^{-5}\) | 26,651 | 14.7× |
| Bending bird | 4 | \(1.21\times10^{-5}\) | 82,376 | 4.7× |
| Ibex/quadruped | 5 | \(7.80\times10^{-6}\) | 128,140 | 3.1× |
| Frog/bear | 6 | \(4.80\times10^{-6}\) | 208,228 | 1.9× |

**Identity permutation (Experiment 13).** Conditional on a rank pattern with three rank-1 slots, the probability that one specific trio occupies all three is \(1/\binom{6}{3} = 1/20 = 5\%\). That is a complement to the decomposition, not a separate discovery.

### 4.3 The exploratory joint depends on the path

**Joint product (Experiment 3).** At ±250 years the strict joint is \(6.89\times10^{-7}\) (1 in 1,451,844) and the broad joint is \(1.48\times10^{-6}\) (1 in 677,527). v1 reported \(7.87\times10^{-7}\) (1 in 1.27 million) and \(1.72\times10^{-6}\) (1 in 581,000) from the wrapped broad rate and the old catalog. Neither number corrects the 2025 headline. The v1 sentence that the joints are weaker than 1.4 million *because Sweatman omitted a date look-elsewhere term* is withdrawn.

**Sensitivity (Experiment 4).** On the center-only grid the anchor rate runs from **0%** (summer solstice only, ±50 years, whether or not the catalog is precision-filtered) to **46%** (all events, summer solstice only, ±400 and ±500 years). v1’s upper figure of 54% is not reproduced. Precision-filtered events with summer solstice only still give **23%** at ±250 years (3 of 13). Figure 2 uses the precision-filtered labels. Half-widths do not set the match window in this grid.

**Multiverse (Experiment 8).** All 128 paths have positive joint probability, so there is nothing to drop for a zero-*P* exclusion. Of the 32 primary paths, **8** have an observed miss (center anchor at ±100 or ±200 years, on both catalogs and both cardinal scopes). The Sagittarius midpoint is 240 years from the Older Dryas, so those tolerances miss, and it is not a Younger Dryas match at any of the tolerances in the grid. The other **24** primary paths are valid. The reference path is valid and matches the **Older Dryas**, not the YD cluster. Its joint is \(5.90\times10^{-7}\) (1 in 1,693,817).

Among the 24 valid primary paths, **5 (20.8%)** have a joint at least as small as that reference. An unfiltered tally that still counts the eight misses, which is the v1 comparison with the zero-*P* drop removed, is 13/32 = 40.6% on this catalog. v1’s 42% was that style of tally on the old catalog. Table 5 reports the filtered numbers. The full path table, with an `observed_hit` flag on every row, is in `output/results.json`.

The extended multiverse, which also drops animals after seeing the ranks, runs from \(1.48\times10^{-7}\) (1 in 6,775,270) to \(7.22\times10^{-6}\) (1 in 138,424), a factor of about **49**. The valid primary set is narrower: \(4.43\times10^{-7}\) to \(1.57\times10^{-6}\), a factor of about **3.6**. v1 described a primary range of about 20× and a full range of about two orders of magnitude. Those spans were computed with the branch-cut windows, the old dates, and no validity filter. Dropping animals remains a stronger degree of freedom than choosing center versus window, and those extended paths are not on the same footing as the primary set.

**Table 5.** Primary multiverse. v1 numbers are the deposited run (unfiltered, zero-*P* paths removed from the share). This run’s column is the validity-filtered primary set (*n* = 24). The reference row is the exploratory product, not \(p\times 2/7\).

| Statistic | v1 joint *P* | v1 ≈ 1 in | This run | This run ≈ 1 in |
|-----------|--------------|-----------|----------|-----------------|
| Minimum (most significant) | \(9.84\times10^{-8}\) | 10,162,905 | \(4.43\times10^{-7}\) | 2,258,423 |
| Median | \(9.35\times10^{-7}\) | 1,069,519 | \(7.87\times10^{-7}\) | 1,270,363 |
| Exploratory reference path | \(7.87\times10^{-7}\) | 1,270,363 | \(5.90\times10^{-7}\) | 1,693,817 |
| Maximum (least significant) | \(1.97\times10^{-6}\) | 507,614 | \(1.57\times10^{-6}\) | 635,182 |
| Share at least as significant as the reference | 42% of nonzero primary paths | — | **5/24 = 20.8%** of valid paths | — |

**Ranking sensitivity (Experiment 12).** Adding 1 to every published rank moves the six-animal probability from 1 in 390,881 to 1 in 53,912 (Table 6). Setting the top three ranks to 3 instead of 1 leaves that same six-animal probability and changes the pre-specified top-three piece from 1 in 85,184 to 1 in 1,015. These are hand-built stress tests. They show that the published probability moves when the rank vector moves. They are not a blind replication.

**Table 6.** Ranking sensitivity. Unchanged from v1.

| Scheme | Ranks | Sum | *P*(sum ≤ *S*) | ≈ 1 in |
|--------|-------|-----|----------------|--------|
| Sweatman original | [1, 1, 1, 4, 5, 6] | 18 | \(2.56\times10^{-6}\) | 390,881 |
| Conservative (+1 each) | [2, 2, 2, 5, 6, 7] | 24 | \(1.85\times10^{-5}\) | 53,912 |
| Skeptical (top 3 at rank 3) | [3, 3, 3, 4, 5, 6] | 24 | \(1.85\times10^{-5}\) | 53,912 |
| Mixed (top 3 vary) | [1, 2, 3, 4, 5, 6] | 21 | \(7.48\times10^{-6}\) | 133,722 |
| Degraded (top 3 at rank 5) | [5, 5, 5, 4, 5, 6] | 30 | \(8.18\times10^{-5}\) | 12,221 |
| Generous (bottom 3 improved) | [1, 1, 1, 2, 3, 4] | 12 | \(1.27\times10^{-7}\) | 7,853,154 |

---

## 5. Discussion

### 5.1 What the evidence actually supports

Inside the published scoring, three animals are ranked first of 44. If scorpion → Scorpius, canid → Lupus, and bird-with-snake → Ophiuchus were named in advance, three independent rank-1 draws have probability 1 in 85,184. The code, and the prose that follows it, sorts six ranks and keeps the best three. The null for that procedure is 1 in 4,484. Either figure is the core of the visual claim, and they answer different questions. The canid identification is the weakest of the three on archaeological grounds even though its published rank is 1 (Section 5.2).

The date component is a different claim, and under this catalog it is common: 41.8% of the analysis window is already within ±250 years of some listed event, and 26.9% of random anchors match on the center date. It is not part of \(p\times 2/7\). The bottom three mappings are significant at a conventional 0.05 threshold and carry much less weight than the top three. Exploratory joints move with the path. On the valid primary set the move is a factor of about 3.6; once post-hoc animal dropping is included it is a factor of about 50.

### 5.2 The self-scoring problem

Sweatman and colleagues ranked all \(6\times 44 = 264\) animal–constellation pairs themselves, knowing the hypothesis. The papers give verbal reasons for each chosen match. This is a structural limit, not an accusation about intent. Subjective alignment judgments in archaeoastronomy are a known vulnerability (Ruggles, 2015; Silva, 2020). The people who stated the hypothesis also produced the ranks the test consumes.

The ranks also stack three questions: whether ancient observers named constellations at all, whether they grouped the same stars the later Greek tradition grouped, and whether they used the same animals. This analysis only scores the last question inside the modern Western figures Sweatman adopted. Some matches are helped by the shared animal name (scorpion → Scorpius, canid → Lupus) rather than by a star pattern that would force that reading on its own. Sweatman & Gerogiorgis (2025) treat the canid pose as an objective rank-1 match to Lupus. The carving’s species is still only a canid, and that identification should stay marked tentative until someone who does not know the hypothesis repeats it. A blind ranking would test whether the published similarity judgments replicate. It would not show that Pre-Pottery Neolithic observers partitioned the sky as later Mediterranean traditions did.

### 5.3 Implications for archaeoastronomy methodology

**Date coincidences in the deglacial period are inexpensive.** A study that aligns an archaeoastronomical date with a “notable” event should report the coverage of its own window. Without that baseline, a crowded catalog manufactures alignments.

**Visual scores should be produced by raters who do not know the hypothesis.** The rank-sum machinery is usable. The open problem is the input. Silva (2020) treats structural orientations, not the iconographic comparison that carries Pillar 43.

**Analyst choices should be shown as a multiverse, with a validity filter.** A path that makes the observed reading a miss is not an alternative evaluation of that reading. Zero-probability paths belong in the denominator disclosure even when, as here, there are none.

**A pre-specified trio and the best three of six are different tests.** Reporting \(1/44^3\) for animals chosen after the ranks are known overstates how rare the pattern is.

**Leave-one-out on both the events and the animals** shows which pieces carry the result. Here the strict date hit attributed to the pillar’s anchor is an Older Dryas coincidence of the Sagittarius midpoint, and it disappears as a Younger Dryas result as soon as one asks which event was matched.

### 5.4 Limitations

The core rank tests accept the published ranks. Experiment 12 only perturbs them. The event catalog is ours. The sweep and the circular shift keep the qualitative conclusion — a date match is not rare — but the percentages in Section 4 are catalog-dependent. In particular:

- The mammoth row is still 7700 BCE with half-width 300 years. That is **not** an IntCal age for Kuzmin & Orlova’s ca. 9700 \(^{14}\)C BP mainland extinction, and it is not a calendar reading of the Wrangel 7700 \(^{14}\)C BP survival. A calibrated replacement has to wait on an explicit calibration. Until then the cluster can affect matches near the 8th millennium BCE, including the Capricornus × autumn-equinox center hit in this run.
- Heinrich 1 is placed at Hemming’s 16,800 calendar years under the 1950 convention. Later work splits Heinrich layer 1 into more than one peak. The ±500 year half-width does not turn 14,850 BCE into that later chronology.
- Mazama uses Zdanowicz et al. (1999), not a newer Bayesian tephra age.
- Only the Pisces/Aries junction was moved to the IAU-boundary intersection. The other boundaries are the v1 rounded table.
- No Stellarium ephemeris was compared with the linear engine beyond the two internal longitude checks in Section 3.1.
- Thirty of 52 center dates lie in the 20,000–5,000 BC window. The anchor probability is not a probability for a year drawn uniformly from that window. Coverage is that second probability, at 41.8% for ±250 years.
- Three cluster pairs closer than 500 years were left unmerged. Independence of the 14 clusters is an analyst choice.

The linear precession approximation is about \(1^\circ\) over 13,000 years, small next to a typical ecliptic constellation and worth about 70 years. Dates in this paper are not good to a decade.

The 2024 lunisolar-calendar reading (Sweatman, 2024) is not tested. If it holds, it is a separate line of evidence.

Archaeological objections — whether the constellations could have been known, whether the pillars are in place, whether the radiocarbon ranges fit 10,950 BC — are those of Notroff et al. (2017) and the excavation reports. They are not answered by the *p*-values above.

### 5.5 The blind ranking experiment

The open question is whether the three strong visual matches are forced by the figures or supplied by the hypothesis. A usable protocol is: standardized images of the six carvings and of the 44 constellation figures; raters with no knowledge of Göbekli Tepe, archaeoastronomy, or the Sweatman hypothesis; a preregistered score. The outcome that matters is whether scorpion, canid, and bird-with-snake are still rank 1 for Scorpius, Lupus, and Ophiuchus when that context is absent.

If those three ranks replicate, the visual signal is at least reproducible inside the modern figure set, and the pre-specified calculation becomes the relevant one only if the trio was locked before the ranks were seen. If they do not replicate, the reported rank-sum rests on judgments that were not separated from the desired outcome. The experiment would not decide whether Pre-Pottery Neolithic observers used those groupings.

---

## 6. Conclusion

The 2025 headline of about 1 in 1.4 million is the rank-sum probability times **2/7**. Our evaluation of that product is 1 in 1,368,083. It does not contain a date. Three further points follow from the recomputed tests.

First, a date match is not rare on this catalog. **41.8%** of 20,000–5,000 BC lies within ±250 years of a listed event. **26.9%** of random anchors match at the center date, and **57.7%** match somewhere in the constellation window. The Sagittarius summer-solstice center hits the Older Dryas, not the Younger Dryas cluster.

Second, the visual weight sits in three of the six mappings. As a pre-specified trio that is 1 in 85,184. As the best three of six it is 1 in 4,484. The other three are 1 in 187. Those probabilities do not multiply to the six-animal result.

Third, the exploratory joint is a distribution. On the 24 primary paths where the observed reading is a hit, 20.8% are at least as significant as the reference path, and the joints span a factor of about 3.6 (\(4.43\times10^{-7}\) to \(1.57\times10^{-6}\)). Including post-hoc animal dropping widens the span to a factor of about 50.

Until a blind ranking is done, the Pillar 43 claim is an unvalidated hypothesis. Its published 1-in-1.4-million figure should not be read as a rare date coincidence multiplied by a rare visual match.

---

## AI Disclosure

This research was conducted using Claude (Anthropic) as a technical reasoning partner for statistical design, code development, and manuscript drafting. ChatGPT (OpenAI) served as an independent reviewer of the statistical methodology and code across multiple review cycles. Accuracy reviews informing this v2 draft were performed with Grok, Codex, and Claude Opus. The v2 numerical revision reported here was recomputed from `gobekli_statistical_test.py`. The analysis was executed on an NVIDIA DGX Spark. The author takes full responsibility for the scientific content and conclusions.

---

## Data Availability

Script, run log, results JSON, and figures:

`gobekli_statistical_test.py`  
`output/run_log.txt`  
`output/results.json`  
`output/fig1_timeline.png` … `output/fig5_catalog_sweep.png`

Repository: https://github.com/simossss/gobekli-pillar43-statistics

The file `gobekli-pillar43-statistics_paper.pdf` is the Zenodo v1 PDF. It has not been rebuilt from this manuscript. Zenodo record 10.5281/zenodo.20364947 has not been versioned.

---

## References

Barber, D. C. et al. (1999). Forcing of the cold event of 8,200 years ago by catastrophic drainage of Laurentide lakes. *Nature*, 400, 344–348.

Bond, G. et al. (1997). A pervasive millennial-scale cycle in North Atlantic Holocene and glacial climates. *Science*, 278, 1257–1266.

Cheng, H. et al. (2020). Timing and structure of the Younger Dryas event and its underlying climate dynamics. *PNAS*, 117(38), 23408–23417.

Clark, P. U. et al. (2009). The Last Glacial Maximum. *Science*, 325, 710–714.

Deschamps, P. et al. (2012). Ice-sheet collapse and sea-level rise at the Bølling warming 14,600 years ago. *Nature*, 483, 559–564.

Dietrich, O. et al. (2012). The role of cult and feasting in the emergence of Neolithic communities. *Antiquity*, 86, 674–695.

Dietrich, O. et al. (2013). Establishing a Radiocarbon Sequence for Göbekli Tepe. *Neo-Lithics*, 1/13, 36–41.

Hemming, S. R. (2004). Heinrich events: Massive late Pleistocene detritus layers of the North Atlantic and their global climate imprint. *Reviews of Geophysics*, 42, RG1005. https://doi.org/10.1029/2003RG000128

Holliday, V. T. et al. (2023). Comprehensive refutation of the Younger Dryas Impact Hypothesis (YDIH). *Earth-Science Reviews*, 247, 104502.

Kennett, J. P. et al. (2015). Bayesian chronological analyses consistent with synchronous age of 12,835–12,735 Cal B.P. for Younger Dryas boundary on four continents. *PNAS*, 112(32), E4344–E4353.

Kuzmin, Y. V. & Orlova, L. A. (2004). Radiocarbon chronology and environment of woolly mammoth (*Mammuthus primigenius* Blum.) in northern Asia: results and perspectives. *Earth-Science Reviews*, 68, 133–169. https://doi.org/10.1016/j.earscirev.2004.04.002

Notroff, J. et al. (2016). Gathering of the Dead? The Early Neolithic sanctuaries of Göbekli Tepe. In Renfrew, C., Boyd, M. J., & Morley, I. (eds.), *Death Rituals, Social Order and the Archaeology of Immortality in the Ancient World*, 65–81. Cambridge University Press.

Notroff, J., Dietrich, O., & Schmidt, K. (2017). More than a vulture: A response to Sweatman and Tsikritsis. *Mediterranean Archaeology and Archaeometry*, 17(2), 57–63.

O’Connor, J. E. (1993). Hydrology, hydraulics, and geomorphology of the Bonneville Flood. *Geological Society of America Special Paper*, 274.

Peters, J. & Schmidt, K. (2004). Animals in the symbolic world of Pre-Pottery Neolithic Göbekli Tepe. *Anthropozoologica*, 39(1), 179–218.

Rasmussen, S. O. et al. (2007). Early Holocene climate oscillations recorded in three Greenland ice cores. *Quaternary Science Reviews*, 26, 1907–1914.

Rasmussen, S. O. et al. (2014). A stratigraphic framework for abrupt climatic changes during the Last Glacial period. *Quaternary Science Reviews*, 106, 14–28.

Reinig, F. et al. (2021). Precise date for the Laacher See eruption synchronizes the Younger Dryas. *Nature*, 595, 66–69.

Ruggles, C. L. N. (Ed.). (2015). *Handbook of Archaeoastronomy and Ethnoastronomy*. Springer.

Ryan, W. B. F., Pitman, W. C., et al. (1997). An abrupt drowning of the Black Sea shelf. *Marine Geology*, 138, 119–126.

Schmidt, K. (2003). The 2003 campaign at Göbekli Tepe. *Neo-Lithics*, 2/03, 3–8.

Silva, F. (2020). A probabilistic framework and significance test for the analysis of structural orientations in skyscape archaeology. *Journal of Archaeological Science*, 118, 105138.

Sweatman, M. B. (2024). Representations of calendars and time at Göbekli Tepe and Karahan Tepe support an astronomical interpretation of their symbolism. *Time and Mind*, 17(3–4), 191–247. https://doi.org/10.1080/1751696X.2024.2373876

Sweatman, M. B. & Coombs, A. (2019). Decoding European Palaeolithic art: Extremely ancient knowledge of precession of the equinoxes. *Athens Journal of History*, 5(1), 1–30. https://doi.org/10.30958/ajhis.5-1-1

Sweatman, M. B. & Gerogiorgis, D. (2025). Origin of some of the ancient Greek constellations via analysis of Pillar 43 at Göbekli Tepe. Submitted manuscript, posted by the authors; **not peer-reviewed**. https://martinsweatman.blogspot.com/2025/05/new-paper-submitted-origin-of-some-of.html

Sweatman, M. B. & Tsikritsis, D. (2017). Decoding Göbekli Tepe with archaeoastronomy: What does the fox say? *Mediterranean Archaeology and Archaeometry*, 17(1), 233–250.

Sweatman, M. B. & Tsikritsis, D. (2017b). Comment on “More than a vulture: A response to Sweatman and Tsikritsis.” *Mediterranean Archaeology and Archaeometry*, 17(2), 63.

Zdanowicz, C. M., Zielinski, G. A., & Germani, M. S. (1999). Mount Mazama eruption: Calendrical age verified and atmospheric impact assessed. *Geology*, 27(7), 621–624. https://doi.org/10.1130/0091-7613(1999)027<0621:MMECAV>2.3.CO;2

---

## Supplementary materials

- S1. `output/run_log.txt` — console log of this run.
- S2. `output/results.json` — numerical output, including every multiverse path and its `observed_hit` flag.
- S3. Primary multiverse paths — the 32 rows in S2 with `animals` = “All 6 (sum=18)”.
- S4. Leave-one-event-out — `results.json` → `leave_one_out`.
- S5. Leave-one-animal-out — `results.json` → `leave_one_animal_out`.
- S6. Ranking sensitivity — `results.json` → `ranking_sensitivity`.
- S7. Selection-adjusted top-3 — `decomposition.top3_selection_adjusted_p` in S2, derived in Section 4.2.
- S8. Stellarium residual table — **not run**. Do not treat Section 3.1’s two longitude checks as that table.

---

*Draft for the author’s review. No Zenodo upload.*
