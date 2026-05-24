#!/usr/bin/env python3
"""
Statistical analysis of Sweatman & Tsikritsis (2017) Pillar 43 archaeoastronomy claim.

Tests whether the proposed animal-constellation mappings on Pillar 43 at Göbekli Tepe
produce a statistically significant match to a notable paleoclimatic event, or whether
such matches arise readily by chance.

Thirteen analyses:
  1. Anchor test — date-coincidence probability as a strict/broad bracket.
  2. Exact rank-sum test — exact probability of Sweatman's visual-similarity scores.
  3. Joint probability — product under an independence assumption.
  4. Sensitivity analysis — how results vary with tolerance, catalog, cardinal day.
  5. Catalog robustness sweep — 500 perturbed event catalogs.
  6. Rank-sum decomposition — top-3 vs bottom-3 mappings.
  7. Leave-one-event-out — which events drive the anchor result.
  8. Multiverse / forking-paths — primary and extended path distributions.
  9. Coverage fraction — what share of the archaeological window is near an event.
  10. Circular-shift catalog test — does the absolute event placement matter?
  11. Leave-one-animal-out — which individual animals drive the similarity result.
  12. Ranking sensitivity — does the conclusion survive alternative ranking schemes?
  13. Animal-identity permutation — does it matter WHICH animals carry the signal?

Author: Simone Pomposi, Independent Researcher
Date: 2026-04
"""

import json
import os
from math import comb
from pathlib import Path

import numpy as np

# ──────────────────────────────────────────────────────────────────────
#  CONSTANTS
# ──────────────────────────────────────────────────────────────────────

PRECESSION_PERIOD_YR = 25_772
PRECESSION_RATE_DEG_PER_YR = 360.0 / PRECESSION_PERIOD_YR  # ~0.01397 °/yr
J2000_YEAR = 2000
RNG_SEED = 42
OUTPUT_DIR = Path("output")

# ──────────────────────────────────────────────────────────────────────
#  ECLIPTIC CONSTELLATION DATA (IAU boundaries along ecliptic, J2000)
# ──────────────────────────────────────────────────────────────────────

ECLIPTIC_CONSTELLATIONS = [
    {"name": "Aries",       "lam_start": 24.4,  "lam_end":  53.5},
    {"name": "Taurus",      "lam_start": 53.5,  "lam_end":  90.4},
    {"name": "Gemini",      "lam_start": 90.4,  "lam_end": 118.1},
    {"name": "Cancer",      "lam_start": 118.1, "lam_end": 138.1},
    {"name": "Leo",         "lam_start": 138.1, "lam_end": 174.1},
    {"name": "Virgo",       "lam_start": 174.1, "lam_end": 218.0},
    {"name": "Libra",       "lam_start": 218.0, "lam_end": 241.0},
    {"name": "Scorpius",    "lam_start": 241.0, "lam_end": 248.0},
    {"name": "Ophiuchus",   "lam_start": 248.0, "lam_end": 266.5},
    {"name": "Sagittarius", "lam_start": 266.5, "lam_end": 300.0},
    {"name": "Capricornus", "lam_start": 300.0, "lam_end": 327.8},
    {"name": "Aquarius",    "lam_start": 327.8, "lam_end": 352.0},
    {"name": "Pisces",      "lam_start": 352.0, "lam_end": 384.4},  # wraps past 360
]

N_VISIBLE_CONSTELLATIONS = 44  # Sweatman & Gerogiorgis (2025): 44 visible from GT

# ──────────────────────────────────────────────────────────────────────
#  SWEATMAN'S PILLAR 43 MAPPINGS
# ──────────────────────────────────────────────────────────────────────

# 6 testable animal-constellation pairs (Sweatman & Gerogiorgis 2025).
# Excludes vulture (anchor), duck/goose (obscured), squat bird (unknown).

SWEATMAN_MAPPINGS = [
    {"animal": "Scorpion",          "constellation": "Scorpius",   "rank_of_44": 1},
    {"animal": "Wolf/dog (canid)",  "constellation": "Lupus",      "rank_of_44": 1},
    {"animal": "Tall bird + snake", "constellation": "Ophiuchus",  "rank_of_44": 1},
    {"animal": "Bending bird",      "constellation": "Pisces",     "rank_of_44": 4},
    {"animal": "Ibex/quadruped",    "constellation": "Gemini",     "rank_of_44": 5},
    {"animal": "Frog/bear",         "constellation": "Virgo",      "rank_of_44": 6},
]

SWEATMAN_RANK_SUM = sum(m["rank_of_44"] for m in SWEATMAN_MAPPINGS)  # = 18
N_TESTED_ANIMALS = len(SWEATMAN_MAPPINGS)  # = 6

SWEATMAN_ANCHOR = "Sagittarius"
SWEATMAN_CARDINAL = "summer_solstice"
SWEATMAN_DATE_BC = 10_950

# ──────────────────────────────────────────────────────────────────────
#  PALEOCLIMATIC EVENT CATALOG
# ──────────────────────────────────────────────────────────────────────

EVENT_CLUSTERS = [
    {"name": "LGM peak",                        "date_bc": 19050, "half_width_yr": 1000},
    {"name": "Bonneville Flood",                 "date_bc": 15550, "half_width_yr":  500},
    {"name": "Heinrich Event 1",                 "date_bc": 14250, "half_width_yr":  500},
    {"name": "Bølling-Allerød + MWP-1A",         "date_bc": 12700, "half_width_yr":  200},
    {"name": "Older Dryas",                      "date_bc": 12075, "half_width_yr":  200},
    {"name": "YD cluster (Laacher+YD+YDIH)",     "date_bc": 10900, "half_width_yr":  250},
    {"name": "YD termination",                   "date_bc":  9750, "half_width_yr":  100},
    {"name": "PBO / Bond 8 / MWP-1B",           "date_bc":  9400, "half_width_yr":  200},
    {"name": "Bond 7",                           "date_bc":  8350, "half_width_yr":  500},
    {"name": "Mammoth mainland extinction",      "date_bc":  7700, "half_width_yr":  300},
    {"name": "Bond 6",                           "date_bc":  7450, "half_width_yr":  500},
    {"name": "8.2ka cluster (Agassiz+Storegga)",  "date_bc":  6300, "half_width_yr":  300},
    {"name": "Mazama VEI 7",                     "date_bc":  5780, "half_width_yr":  200},
    {"name": "Late cluster (BlackSea+Kikai)",    "date_bc":  5500, "half_width_yr":  400},
]


# ──────────────────────────────────────────────────────────────────────
#  PRECESSION ENGINE
# ──────────────────────────────────────────────────────────────────────

def ecliptic_longitude_of_solstice(year_bc: float, cardinal: str = "summer_solstice") -> float:
    """
    J2000 ecliptic longitude of the Sun at a cardinal day for a given epoch.
    Linear precession approximation (~1° error over 13,000 yr).
    Returns degrees in [0, 360).
    """
    offsets = {
        "spring_equinox": 0.0, "summer_solstice": 90.0,
        "autumn_equinox": 180.0, "winter_solstice": 270.0,
    }
    delta_years = J2000_YEAR + year_bc
    return (PRECESSION_RATE_DEG_PER_YR * delta_years + offsets[cardinal]) % 360.0


def date_bc_from_ecliptic_longitude(lam_j2000: float, cardinal: str = "summer_solstice") -> float:
    """Inverse of ecliptic_longitude_of_solstice. Returns year BC (positive)."""
    offsets = {
        "spring_equinox": 0.0, "summer_solstice": 90.0,
        "autumn_equinox": 180.0, "winter_solstice": 270.0,
    }
    lam_ve = (lam_j2000 - offsets[cardinal]) % 360.0
    year_bc = lam_ve / PRECESSION_RATE_DEG_PER_YR - J2000_YEAR
    while year_bc < 3_000:
        year_bc += PRECESSION_PERIOD_YR
    while year_bc > 28_000:
        year_bc -= PRECESSION_PERIOD_YR
    return year_bc


def constellation_date_range(constellation: dict, cardinal: str = "summer_solstice"):
    """
    For a given ecliptic constellation, return (date_min_bc, date_max_bc):
    the range of years BC when the Sun at the given cardinal day fell within
    the constellation's ecliptic boundaries.

    date_min_bc is the more recent boundary, date_max_bc the more ancient.
    """
    lam_s = constellation["lam_start"]
    lam_e = constellation["lam_end"]
    if lam_e > 360:
        lam_e_wrapped = lam_e - 360
        d1_s = date_bc_from_ecliptic_longitude(lam_s, cardinal)
        d1_e = date_bc_from_ecliptic_longitude(360.0, cardinal)
        d2_s = date_bc_from_ecliptic_longitude(0.0, cardinal)
        d2_e = date_bc_from_ecliptic_longitude(lam_e_wrapped, cardinal)
        all_d = [d1_s, d1_e, d2_s, d2_e]
        return (min(all_d), max(all_d))
    d_at_start = date_bc_from_ecliptic_longitude(lam_s, cardinal)
    d_at_end = date_bc_from_ecliptic_longitude(lam_e, cardinal)
    return (min(d_at_start, d_at_end), max(d_at_start, d_at_end))


def constellation_center_date(constellation: dict, cardinal: str = "summer_solstice") -> float:
    """Year BC when the Sun at cardinal day was at the constellation's ecliptic midpoint."""
    lam_mid = (constellation["lam_start"] + constellation["lam_end"]) / 2.0
    if lam_mid > 360:
        lam_mid -= 360
    return date_bc_from_ecliptic_longitude(lam_mid, cardinal)


# ──────────────────────────────────────────────────────────────────────
#  EVENT MATCHING
# ──────────────────────────────────────────────────────────────────────

def date_matches_any_event(date_bc: float, events: list, tolerance_override: float = None) -> tuple:
    """Check if a date falls within tolerance of any event. Returns (matched, name, distance)."""
    for ev in events:
        hw = tolerance_override if tolerance_override is not None else ev["half_width_yr"]
        dist = abs(date_bc - ev["date_bc"])
        if dist <= hw:
            return (True, ev["name"], dist)
    # No match — find closest
    closest = min(events, key=lambda e: abs(date_bc - e["date_bc"]))
    return (False, closest["name"], abs(date_bc - closest["date_bc"]))


def window_overlaps_any_event(date_min_bc, date_max_bc, events, tolerance_override=None):
    """Check if a constellation's full date window overlaps any event's tolerance window."""
    for ev in events:
        hw = tolerance_override if tolerance_override is not None else ev["half_width_yr"]
        ev_lo = ev["date_bc"] - hw
        ev_hi = ev["date_bc"] + hw
        if date_min_bc <= ev_hi and date_max_bc >= ev_lo:
            return (True, ev["name"])
    return (False, None)


# ──────────────────────────────────────────────────────────────────────
#  EXACT RANK-SUM PROBABILITY (inclusion-exclusion)
# ──────────────────────────────────────────────────────────────────────

def exact_rank_sum_probability(n_animals: int, n_constellations: int, target_sum: int) -> float:
    """
    Exact probability that the sum of n_animals independent uniform random variables,
    each drawn from {1, 2, ..., n_constellations}, is ≤ target_sum.

    Uses the inclusion-exclusion formula for the number of ways to write
    target_sum as an ordered sum of n_animals integers each in [1, n_constellations].

    P(S ≤ T) = (1/N^n) × Σ_{s=n}^{T} Σ_{k=0}^{n} (-1)^k × C(n,k) × C(s-k*N-1, n-1)

    where N = n_constellations, n = n_animals.
    """
    N = n_constellations
    n = n_animals
    total_outcomes = N ** n

    # Count the number of ways to get sum exactly = s, for s from n to target_sum,
    # where each variable is in [1, N].
    # Transform: let x_i = r_i - 1, so x_i in [0, N-1], sum(x_i) = s - n.
    # Number of solutions = Σ_{k=0}^{n} (-1)^k C(n,k) C(s-n - k*N + n-1, n-1)
    #                     = Σ_{k=0}^{n} (-1)^k C(n,k) C(s - 1 - k*N, n-1)

    count = 0
    for s in range(n, target_sum + 1):
        for k in range(n + 1):
            arg = s - 1 - k * N
            if arg < n - 1:
                break  # all further k give even smaller arg
            sign = (-1) ** k
            count += sign * comb(n, k) * comb(arg, n - 1)

    return count / total_outcomes


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 1: ANCHOR TEST (sensitivity bracket)
# ──────────────────────────────────────────────────────────────────────

def run_anchor_test(events, tolerance_values=(100, 250, 500)):
    """
    Two anchor models:
      - CENTER-ONLY (strict): does the constellation's midpoint date match an event?
      - WINDOW-OVERLAP (broad): does ANY date in the constellation's full window
        overlap ANY event's tolerance window?

    Results reported as a bracket: [center-only, window-overlap].
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 1: ANCHOR TEST (Look-Elsewhere Effect)")
    print("=" * 72)
    print()
    print("Two null models tested across 13 constellations × 4 cardinal days = 52 combos:")
    print("  STRICT: constellation center date falls within event tolerance")
    print("  BROAD:  any date in constellation window overlaps event tolerance")
    print()

    cardinals = ["spring_equinox", "summer_solstice", "autumn_equinox", "winter_solstice"]
    results = {}

    for tol in tolerance_values:
        center_hits = 0
        window_hits = 0
        total = 0
        center_details = []

        for const in ECLIPTIC_CONSTELLATIONS:
            for card in cardinals:
                total += 1
                d_center = constellation_center_date(const, card)
                d_min, d_max = constellation_date_range(const, card)

                # Center-only
                matched_c, ev_c, dist_c = date_matches_any_event(d_center, events,
                                                                  tolerance_override=tol)
                if matched_c:
                    center_hits += 1
                    center_details.append({
                        "constellation": const["name"], "cardinal": card,
                        "date_bc": round(d_center), "event": ev_c,
                        "distance_yr": round(dist_c),
                    })

                # Window overlap
                matched_w, _ = window_overlaps_any_event(d_min, d_max, events,
                                                         tolerance_override=tol)
                if matched_w:
                    window_hits += 1

        p_center = center_hits / total
        p_window = window_hits / total
        results[tol] = {
            "center_hits": center_hits, "window_hits": window_hits, "total": total,
            "p_center": p_center, "p_window": p_window, "center_details": center_details,
        }

        print(f"  ±{tol} yr:  center-only = {center_hits}/{total} ({p_center:.1%})"
              f"    window-overlap = {window_hits}/{total} ({p_window:.1%})")

    # Print bracket summary for ±250
    r250 = results[250]
    print(f"\n  BRACKET at ±250 yr:  {r250['p_center']:.1%}  to  {r250['p_window']:.1%}")
    print(f"  (strict to broad null model)")

    # Print center-only details at ±250
    print(f"\n  Center-only matches at ±250 yr:")
    for d in results[250]["center_details"]:
        print(f"    {d['constellation']:13s} × {d['cardinal']:17s} → "
              f"{d['date_bc']:>6,} BC  ←  {d['event']} (Δ={d['distance_yr']} yr)")

    # Validate Sweatman's specific case
    print()
    sag = next(c for c in ECLIPTIC_CONSTELLATIONS if c["name"] == "Sagittarius")
    d_min, d_max = constellation_date_range(sag, "summer_solstice")
    d_center = constellation_center_date(sag, "summer_solstice")
    lam = ecliptic_longitude_of_solstice(SWEATMAN_DATE_BC, SWEATMAN_CARDINAL)
    print(f"  Sweatman: vulture = {SWEATMAN_ANCHOR}, {SWEATMAN_CARDINAL}")
    print(f"    SS at 10,950 BC → λ = {lam:.1f}° (J2000)")
    print(f"    Sagittarius ecliptic range: {sag['lam_start']}°–{sag['lam_end']}°")
    print(f"    Sagittarius date window: {round(d_min):,}–{round(d_max):,} BC (center: {round(d_center):,} BC)")

    return results


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 2: EXACT RANK-SUM TEST
# ──────────────────────────────────────────────────────────────────────

def run_similarity_test():
    """
    Exact probability that 6 independent uniform draws from {1,...,44}
    sum to ≤ 18 (Sweatman's rank-sum).
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 2: EXACT RANK-SUM TEST (Visual Similarity)")
    print("=" * 72)
    print()
    print(f"  6 animals, each ranked against {N_VISIBLE_CONSTELLATIONS} visible constellations.")
    print(f"  Sweatman's ranks: {[m['rank_of_44'] for m in SWEATMAN_MAPPINGS]}")
    print(f"  Sweatman's rank-sum = {SWEATMAN_RANK_SUM}")
    print()

    p_exact = exact_rank_sum_probability(N_TESTED_ANIMALS, N_VISIBLE_CONSTELLATIONS,
                                          SWEATMAN_RANK_SUM)

    mean_rank = (1 + N_VISIBLE_CONSTELLATIONS) / 2
    expected_sum = N_TESTED_ANIMALS * mean_rank
    std_sum = (N_TESTED_ANIMALS * (N_VISIBLE_CONSTELLATIONS**2 - 1) / 12) ** 0.5
    z_score = (SWEATMAN_RANK_SUM - expected_sum) / std_sum

    print(f"  Expected rank-sum under null: {expected_sum:.1f} ± {std_sum:.1f}")
    print(f"  Sweatman's rank-sum: {SWEATMAN_RANK_SUM}  (z = {z_score:.2f})")
    print(f"  Exact P(sum ≤ {SWEATMAN_RANK_SUM}) = {p_exact:.6e}")
    print(f"  ≈ 1 in {1/p_exact:,.0f}")

    # Robustness: without-replacement null
    # If we require each animal to map to a DISTINCT constellation, two models arise:
    #
    # (a) Distinct constellations, independent ranks: each animal ranks all 44
    #     constellations independently. Assigning 6 distinct constellations still gives
    #     each animal a rank that is uniform on {1,...,44}, because the rankings are
    #     independent across animals. Probability is identical to with-replacement.
    #
    # (b) Distinct RANK VALUES (no two animals share the same rank): minimum possible
    #     sum = 1+2+3+4+5+6 = 21 > 18. Sweatman's observed sum of 18 (with three
    #     rank-1 ties) is impossible under this model. This confirms the with-replacement
    #     model is the appropriate null — and makes the result look more significant,
    #     not less, since the observed data could only arise under the more permissive model.

    print()
    min_distinct = sum(range(1, N_TESTED_ANIMALS + 1))  # 1+2+3+4+5+6 = 21
    print(f"  Without-replacement robustness check:")
    print(f"    Distinct constellations, independent ranks: same P (ranks are independent)")
    print(f"    Distinct rank values: min possible sum = {min_distinct} > {SWEATMAN_RANK_SUM}")
    print(f"    → Sweatman's sum of {SWEATMAN_RANK_SUM} (with three rank-1 ties) is impossible")
    print(f"      under a distinct-ranks null. The with-replacement model is the natural")
    print(f"      permissive null under independent per-animal rankings.")

    result = {
        "sweatman_rank_sum": SWEATMAN_RANK_SUM,
        "expected_sum": expected_sum,
        "std_sum": round(std_sum, 2),
        "z_score": round(z_score, 2),
        "p_exact": p_exact,
        "one_in": round(1 / p_exact),
    }
    return result


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 3: JOINT PROBABILITY (under independence assumption)
# ──────────────────────────────────────────────────────────────────────

def run_joint_test(anchor_results, similarity_results, tolerance_values=(100, 250, 500)):
    """
    Joint probability = P(anchor match) × P(similarity), under the assumption
    that the date-determining step and the visual-ranking step are independent.

    This is an assumption, not a proven fact. If the rankings were influenced by
    foreknowledge of the desired date, the two components are not independent and
    the joint probability would be higher (less significant).
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 3: JOINT PROBABILITY (independence assumption)")
    print("=" * 72)
    print()
    print("  P(joint) = P(anchor match) × P(rank-sum ≤ 18)")
    print("  NOTE: This assumes the anchor assignment and the visual rankings are")
    print("  independent. If ranking was influenced by the desired date outcome,")
    print("  the true joint probability is higher (less significant).")
    print()

    p_sim = similarity_results["p_exact"]
    results = {}

    for tol in tolerance_values:
        ar = anchor_results[tol]
        p_center = ar["p_center"]
        p_window = ar["p_window"]
        j_center = p_center * p_sim
        j_window = p_window * p_sim

        results[tol] = {
            "p_anchor_center": p_center,
            "p_anchor_window": p_window,
            "p_similarity": p_sim,
            "p_joint_center": j_center,
            "p_joint_window": j_window,
        }

        print(f"  ±{tol} yr:")
        print(f"    Strict anchor:  {p_center:.3f} × {p_sim:.2e} = {j_center:.2e}"
              f"  (≈ 1 in {1/j_center:,.0f})" if j_center > 0 else "")
        print(f"    Broad anchor:   {p_window:.3f} × {p_sim:.2e} = {j_window:.2e}"
              f"  (≈ 1 in {1/j_window:,.0f})" if j_window > 0 else "")
        print()

    return results


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 4: SENSITIVITY ANALYSIS
# ──────────────────────────────────────────────────────────────────────

def run_sensitivity_analysis(events):
    """Vary tolerance, event catalog, and cardinal-day scope."""
    print("\n" + "=" * 72)
    print("EXPERIMENT 4: SENSITIVITY ANALYSIS (center-only anchor)")
    print("=" * 72)
    print()

    major_events = [e for e in events if e["half_width_yr"] <= 250]
    tolerances = [50, 100, 150, 200, 250, 300, 400, 500]
    cardinals_ss = ["summer_solstice"]
    cardinals_all = ["spring_equinox", "summer_solstice", "autumn_equinox", "winter_solstice"]

    scenarios = [
        ("All events, all cardinals", events, cardinals_all),
        ("All events, SS only", events, cardinals_ss),
        ("Major events, all cardinals", major_events, cardinals_all),
        ("Major events, SS only", major_events, cardinals_ss),
    ]

    results = {}
    for name, ev_list, cards in scenarios:
        row = {}
        for tol in tolerances:
            hits = total = 0
            for const in ECLIPTIC_CONSTELLATIONS:
                for card in cards:
                    total += 1
                    d_center = constellation_center_date(const, card)
                    matched, _, _ = date_matches_any_event(d_center, ev_list,
                                                           tolerance_override=tol)
                    if matched:
                        hits += 1
            row[tol] = {"hits": hits, "total": total, "p": hits / total if total else 0}
        results[name] = row

    header = f"  {'Scenario':<35s} | " + " | ".join(f"±{t:>3d}" for t in tolerances)
    print(header)
    print("  " + "-" * len(header))
    for name, row in results.items():
        vals = " | ".join(f"{row[t]['p']:>4.0%}" for t in tolerances)
        print(f"  {name:<35s} | {vals}")

    return results


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 5: CATALOG ROBUSTNESS SWEEP
# ──────────────────────────────────────────────────────────────────────

def run_catalog_sweep(events, n_catalogs=500, rng_seed=RNG_SEED):
    """
    Stress-test the anchor result by generating perturbed event catalogs.

    Each trial:
      1. Randomly drop 0–3 events (simulating catalog choice uncertainty)
      2. Shift each remaining event's date by N(0, half_width/2) (simulating dating error)
      3. Run center-only anchor test at ±250 yr across all 52 combinations
      4. Record P(anchor hit)

    Produces a distribution of anchor probabilities across catalog assumptions.
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 5: CATALOG ROBUSTNESS SWEEP")
    print("=" * 72)
    print()
    print(f"  {n_catalogs} perturbed catalogs. Each trial: drop 0–3 events + shift dates.")
    print(f"  Anchor test: center-only at ±250 yr, all 13 constellations × 4 cardinals.")
    print()

    rng = np.random.default_rng(rng_seed)
    cardinals = ["spring_equinox", "summer_solstice", "autumn_equinox", "winter_solstice"]
    p_values = []

    for trial in range(n_catalogs):
        # Perturb catalog
        n_drop = rng.integers(0, 4)  # drop 0–3 events
        keep_mask = np.ones(len(events), dtype=bool)
        if n_drop > 0:
            drop_idx = rng.choice(len(events), size=min(n_drop, len(events)), replace=False)
            keep_mask[drop_idx] = False

        perturbed = []
        for i, ev in enumerate(events):
            if not keep_mask[i]:
                continue
            shifted_date = ev["date_bc"] + rng.normal(0, ev["half_width_yr"] * 0.5)
            perturbed.append({
                "name": ev["name"],
                "date_bc": shifted_date,
                "half_width_yr": ev["half_width_yr"],
            })

        # Run anchor test
        hits = total = 0
        for const in ECLIPTIC_CONSTELLATIONS:
            for card in cardinals:
                total += 1
                d_center = constellation_center_date(const, card)
                matched, _, _ = date_matches_any_event(d_center, perturbed,
                                                       tolerance_override=250)
                if matched:
                    hits += 1
        p_values.append(hits / total)

    p_arr = np.array(p_values)
    print(f"  Results across {n_catalogs} perturbed catalogs (center-only, ±250 yr):")
    print(f"    Mean P(anchor hit):   {p_arr.mean():.1%}")
    print(f"    Median:               {np.median(p_arr):.1%}")
    print(f"    5th percentile:       {np.percentile(p_arr, 5):.1%}")
    print(f"    95th percentile:      {np.percentile(p_arr, 95):.1%}")
    print(f"    Min:                  {p_arr.min():.1%}")
    print(f"    Max:                  {p_arr.max():.1%}")
    print()
    print(f"  The anchor result remains non-rare across a wide range of")
    print(f"  perturbed catalog assumptions.")

    return {
        "n_catalogs": n_catalogs,
        "mean": float(p_arr.mean()),
        "median": float(np.median(p_arr)),
        "p5": float(np.percentile(p_arr, 5)),
        "p95": float(np.percentile(p_arr, 95)),
        "min": float(p_arr.min()),
        "max": float(p_arr.max()),
        "all_p_values": p_values,
    }


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 6: RANK-SUM DECOMPOSITION (top-3 vs bottom-3)
# ──────────────────────────────────────────────────────────────────────

def run_decomposition():
    """
    Split Sweatman's 6 mappings into the 3 strongest (rank 1) and 3 weakest
    (ranks 4, 5, 6). Compute exact probabilities for each group separately.
    Shows how much of the total significance comes from which mappings.
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 6: RANK-SUM DECOMPOSITION (top-3 vs bottom-3)")
    print("=" * 72)
    print()

    ranks = sorted([m["rank_of_44"] for m in SWEATMAN_MAPPINGS])
    top3 = ranks[:3]   # [1, 1, 1]
    bot3 = ranks[3:]   # [4, 5, 6]

    print(f"  All 6 ranks: {ranks}  →  sum = {sum(ranks)}")
    print(f"  Top 3:       {top3}  →  sum = {sum(top3)}")
    print(f"  Bottom 3:    {bot3}  →  sum = {sum(bot3)}")
    print()

    N = N_VISIBLE_CONSTELLATIONS

    # Top 3: P(sum of 3 draws from {1..44} ≤ 3)
    # Only way: all three = 1. P = (1/44)^3
    p_top3 = exact_rank_sum_probability(3, N, sum(top3))
    print(f"  Top 3:    P(sum ≤ {sum(top3)}) = {p_top3:.6e}  (≈ 1 in {1/p_top3:,.0f})")
    print(f"            = 1/{N}³ = 1/{N**3:,}")

    # Bottom 3: P(sum of 3 draws from {1..44} ≤ 15)
    p_bot3 = exact_rank_sum_probability(3, N, sum(bot3))
    print(f"  Bottom 3: P(sum ≤ {sum(bot3)}) = {p_bot3:.6e}  (≈ 1 in {1/p_bot3:,.0f})")

    # Analytical cross-check for bottom 3
    # Number of ordered triples (a,b,c) from {1..44} with a+b+c ≤ 15
    # Using stars-and-bars with inclusion-exclusion
    count_bot3 = 0
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            for c in range(1, N + 1):
                if a + b + c <= sum(bot3):
                    count_bot3 += 1
    p_bot3_check = count_bot3 / N**3
    print(f"            (brute-force check: {count_bot3}/{N**3:,} = {p_bot3_check:.6e})")

    # All 6 for comparison
    p_all6 = exact_rank_sum_probability(6, N, sum(ranks))
    print(f"  All 6:    P(sum ≤ {sum(ranks)}) = {p_all6:.6e}  (≈ 1 in {1/p_all6:,.0f})")

    print(f"""
  Interpretation:
    The top 3 mappings (scorpion, canid, Ophiuchus) contribute a factor of
    1 in {N**3:,} — genuinely rare. These are visually compelling matches.

    The bottom 3 (Pisces, Gemini, Virgo) contribute only 1 in {1/p_bot3:.0f}.
    At conventional significance thresholds, the bottom 3 alone would not
    reject the null hypothesis.

    The total significance ({1/p_all6:,.0f}) is overwhelmingly driven by
    three mappings. Half the evidence base is statistically ordinary.""")

    return {
        "top3_ranks": top3, "top3_sum": sum(top3), "top3_p": p_top3,
        "bot3_ranks": bot3, "bot3_sum": sum(bot3), "bot3_p": p_bot3,
        "all6_p": p_all6,
    }


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 7: LEAVE-ONE-EVENT-OUT INFLUENCE ANALYSIS
# ──────────────────────────────────────────────────────────────────────

def run_leave_one_out(events):
    """
    Remove each event cluster one at a time and recompute the center-only
    anchor probability at ±250 yr. Identifies which events drive the result.
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 7: LEAVE-ONE-EVENT-OUT INFLUENCE ANALYSIS")
    print("=" * 72)
    print()
    print("  Remove each event cluster, recompute center-only anchor at ±250 yr.")
    print()

    cardinals = ["spring_equinox", "summer_solstice", "autumn_equinox", "winter_solstice"]
    baseline_hits = 0
    total = 0
    for const in ECLIPTIC_CONSTELLATIONS:
        for card in cardinals:
            total += 1
            d = constellation_center_date(const, card)
            matched, _, _ = date_matches_any_event(d, events, tolerance_override=250)
            if matched:
                baseline_hits += 1
    baseline_p = baseline_hits / total

    results = []
    for drop_idx, dropped in enumerate(events):
        reduced = [e for i, e in enumerate(events) if i != drop_idx]
        hits = 0
        for const in ECLIPTIC_CONSTELLATIONS:
            for card in cardinals:
                d = constellation_center_date(const, card)
                matched, _, _ = date_matches_any_event(d, reduced, tolerance_override=250)
                if matched:
                    hits += 1
        p = hits / total
        delta = p - baseline_p
        results.append({
            "dropped": dropped["name"],
            "hits": hits, "p": p,
            "delta": delta,
        })

    # Sort by impact (which removal changes the result most)
    results.sort(key=lambda r: r["delta"])

    print(f"  {'Dropped event':<45s}  Hits  P(hit)  Δ from baseline")
    print(f"  {'-'*45}  ----  ------  ---------------")
    for r in results:
        arrow = "▼" if r["delta"] < -0.001 else ("▲" if r["delta"] > 0.001 else "·")
        print(f"  {r['dropped']:<45s}  {r['hits']:>3d}   {r['p']:.1%}   {r['delta']:+.1%} {arrow}")
    print(f"  {'BASELINE (all events)':<45s}  {baseline_hits:>3d}   {baseline_p:.1%}")

    most_influential = results[0]
    print(f"\n  Most influential event to remove: {most_influential['dropped']}")
    print(f"    → P drops from {baseline_p:.1%} to {most_influential['p']:.1%}")
    print(f"    Removing it loses {baseline_hits - most_influential['hits']} anchor matches.")

    return {"baseline_p": baseline_p, "results": results}


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 8: MULTIVERSE / FORKING-PATHS ANALYSIS
# ──────────────────────────────────────────────────────────────────────

def run_multiverse(events):
    """
    Enumerate all reasonable analyst choices and compute the joint probability
    for each combination. Reports the distribution of results across the
    multiverse of defensible analytical decisions.

    Forking paths:
      - Cardinal day: SS-only (Sweatman's choice) vs all-4
      - Event catalog: all 14 clusters vs major-only (half_width ≤ 250 yr)
      - Tolerance: 100, 200, 250, 300 yr
      - Animals included: all 6 vs top 5 (drop weakest) vs top 4 vs top 3
      - Anchor model: center-only vs window-overlap
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 8: MULTIVERSE / FORKING-PATHS ANALYSIS")
    print("=" * 72)
    print()
    print("  Enumerate all defensible analyst choices. Report the distribution")
    print("  of joint probabilities across the multiverse.")
    print()

    major_events = [e for e in events if e["half_width_yr"] <= 250]
    cardinals_opts = {
        "SS only": ["summer_solstice"],
        "All 4": ["spring_equinox", "summer_solstice", "autumn_equinox", "winter_solstice"],
    }
    catalog_opts = {"All events": events, "Major only": major_events}
    tolerance_opts = [100, 200, 250, 300]

    # Animal subsets: all 6, top 5, top 4, top 3
    ranks_sorted = sorted(SWEATMAN_MAPPINGS, key=lambda m: m["rank_of_44"])
    animal_opts = {
        "All 6 (sum=18)": ranks_sorted[:6],
        "Top 5 (sum=12)": ranks_sorted[:5],
        "Top 4 (sum=7)":  ranks_sorted[:4],
        "Top 3 (sum=3)":  ranks_sorted[:3],
    }

    anchor_opts = ["center", "window"]

    N = N_VISIBLE_CONSTELLATIONS
    all_cardinals = ["spring_equinox", "summer_solstice", "autumn_equinox", "winter_solstice"]

    multiverse = []

    for card_name, cards in cardinals_opts.items():
        for cat_name, ev_list in catalog_opts.items():
            for tol in tolerance_opts:
                # Compute anchor probabilities
                total = 0
                center_hits = 0
                window_hits = 0
                for const in ECLIPTIC_CONSTELLATIONS:
                    for card in cards:
                        total += 1
                        d_center = constellation_center_date(const, card)
                        d_min, d_max = constellation_date_range(const, card)
                        mc, _, _ = date_matches_any_event(d_center, ev_list,
                                                          tolerance_override=tol)
                        if mc:
                            center_hits += 1
                        mw, _ = window_overlaps_any_event(d_min, d_max, ev_list,
                                                          tolerance_override=tol)
                        if mw:
                            window_hits += 1

                for anch_name in anchor_opts:
                    p_anchor = (center_hits if anch_name == "center" else window_hits) / total

                    for anim_name, anim_set in animal_opts.items():
                        n_a = len(anim_set)
                        s = sum(m["rank_of_44"] for m in anim_set)
                        p_sim = exact_rank_sum_probability(n_a, N, s)
                        p_joint = p_anchor * p_sim

                        multiverse.append({
                            "cardinal": card_name,
                            "catalog": cat_name,
                            "tolerance": tol,
                            "anchor": anch_name,
                            "animals": anim_name,
                            "p_anchor": p_anchor,
                            "p_similarity": p_sim,
                            "p_joint": p_joint,
                        })

    # Convert to arrays for summary stats
    joints = np.array([m["p_joint"] for m in multiverse])
    joints_nonzero = joints[joints > 0]

    print(f"  Total paths in multiverse: {len(multiverse)}")
    print(f"  Paths with p_joint > 0:    {len(joints_nonzero)}")
    print()
    if len(joints_nonzero) > 0:
        print(f"  Joint probability distribution (across all paths where p > 0):")
        print(f"    Min:    {joints_nonzero.min():.2e}  (≈ 1 in {1/joints_nonzero.min():,.0f})")
        print(f"    Median: {np.median(joints_nonzero):.2e}  (≈ 1 in {1/np.median(joints_nonzero):,.0f})")
        print(f"    Mean:   {joints_nonzero.mean():.2e}  (≈ 1 in {1/joints_nonzero.mean():,.0f})")
        print(f"    Max:    {joints_nonzero.max():.2e}  (≈ 1 in {1/joints_nonzero.max():,.0f})")

    # Split into primary (all 6 animals only) and extended (includes animal dropping)
    primary = [m for m in multiverse if m["animals"] == "All 6 (sum=18)"]
    extended = [m for m in multiverse if m["animals"] != "All 6 (sum=18)"]
    primary_joints = np.array([m["p_joint"] for m in primary if m["p_joint"] > 0])
    extended_joints = np.array([m["p_joint"] for m in extended if m["p_joint"] > 0])

    print(f"\n  PRIMARY multiverse (anchor × tolerance × catalog × cardinal, all 6 animals):")
    print(f"    {len(primary)} paths, {len(primary_joints)} with P > 0")
    if len(primary_joints) > 0:
        print(f"    Joint P range: {primary_joints.min():.2e} to {primary_joints.max():.2e}")
        print(f"    Median: {np.median(primary_joints):.2e}")

    print(f"  EXTENDED multiverse (adds animal-dropping forks):")
    print(f"    {len(extended)} additional paths, {len(extended_joints)} with P > 0")
    if len(extended_joints) > 0:
        print(f"    Joint P range: {extended_joints.min():.2e} to {extended_joints.max():.2e}")

    # Sweatman's specific path
    sw = next(m for m in multiverse
              if m["cardinal"] == "SS only" and m["catalog"] == "All events"
              and m["tolerance"] == 250 and m["anchor"] == "center"
              and m["animals"] == "All 6 (sum=18)")
    print(f"\n  Sweatman's path:")
    print(f"    SS only, all events, ±250 yr, center anchor, all 6 animals")
    print(f"    P(joint) = {sw['p_joint']:.2e}  (≈ 1 in {1/sw['p_joint']:,.0f})")

    more_sig = np.sum(joints_nonzero <= sw["p_joint"])
    print(f"    {more_sig}/{len(joints_nonzero)} paths are as or more significant")
    print(f"    ({more_sig/len(joints_nonzero):.1%} of the full multiverse)")

    # Within primary only
    if len(primary_joints) > 0:
        more_sig_primary = np.sum(primary_joints <= sw["p_joint"])
        print(f"    {more_sig_primary}/{len(primary_joints)} primary paths are as or more significant")
        print(f"    ({more_sig_primary/len(primary_joints):.1%} of primary multiverse)")

    best = min(multiverse, key=lambda m: m["p_joint"] if m["p_joint"] > 0 else float("inf"))
    worst = max(multiverse, key=lambda m: m["p_joint"])
    print(f"\n  Most significant path:")
    print(f"    {best['cardinal']}, {best['catalog']}, ±{best['tolerance']} yr, "
          f"{best['anchor']}, {best['animals']}")
    print(f"    P = {best['p_joint']:.2e}  (≈ 1 in {1/best['p_joint']:,.0f})" if best["p_joint"] > 0 else "")
    print(f"  Least significant path:")
    print(f"    {worst['cardinal']}, {worst['catalog']}, ±{worst['tolerance']} yr, "
          f"{worst['anchor']}, {worst['animals']}")
    print(f"    P = {worst['p_joint']:.2e}  (≈ 1 in {1/worst['p_joint']:,.0f})" if worst["p_joint"] > 0 else "")

    print(f"""
  Interpretation:
    The quoted significance depends heavily on analyst choices. Not all paths
    are equally defensible: dropping animals post hoc (extended multiverse) is
    a stronger degree of freedom than choosing center vs. window anchor
    (primary multiverse). Even within the primary multiverse ({len(primary)} paths),
    the range spans {primary_joints.min():.1e} to {primary_joints.max():.1e}. The reported
    p-value should be understood as conditional on one analytical path.""")

    return {
        "n_paths": len(multiverse),
        "n_primary": len(primary),
        "n_extended": len(extended),
        "n_nonzero": len(joints_nonzero),
        "primary_min": float(primary_joints.min()) if len(primary_joints) > 0 else None,
        "primary_median": float(np.median(primary_joints)) if len(primary_joints) > 0 else None,
        "primary_max": float(primary_joints.max()) if len(primary_joints) > 0 else None,
        "min_joint": float(joints_nonzero.min()) if len(joints_nonzero) > 0 else None,
        "median_joint": float(np.median(joints_nonzero)) if len(joints_nonzero) > 0 else None,
        "max_joint": float(joints_nonzero.max()) if len(joints_nonzero) > 0 else None,
        "sweatman_path_joint": sw["p_joint"],
        "frac_as_significant": float(more_sig / len(joints_nonzero)) if len(joints_nonzero) > 0 else None,
        "frac_primary_as_significant": float(more_sig_primary / len(primary_joints)) if len(primary_joints) > 0 else None,
        "all_paths": multiverse,  # full table for reproducibility
    }


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 9: COVERAGE FRACTION
# ──────────────────────────────────────────────────────────────────────

def run_coverage_fraction(events, window_start_bc=20000, window_end_bc=5000,
                          tolerance_values=(100, 250, 500)):
    """
    What fraction of the archaeological time window lies within ±tolerance
    of at least one event? Provides an intuitive baseline: if coverage is
    high, any randomly chosen date in the window is likely near something.
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 9: COVERAGE FRACTION")
    print("=" * 72)
    print()
    print(f"  Window: {window_start_bc:,}–{window_end_bc:,} BC ({window_start_bc - window_end_bc:,} years)")
    print(f"  What fraction of this window lies within ±tolerance of at least one event?")
    print()

    window_length = window_start_bc - window_end_bc
    results = {}

    for tol in tolerance_values:
        # Build the union of all event windows
        covered = np.zeros(window_length, dtype=bool)
        for ev in events:
            lo = ev["date_bc"] - tol
            hi = ev["date_bc"] + tol
            # Convert to array indices (0 = window_end_bc, window_length-1 = window_start_bc)
            idx_lo = max(0, int(lo - window_end_bc))
            idx_hi = min(window_length, int(hi - window_end_bc))
            if idx_hi > idx_lo:
                covered[idx_lo:idx_hi] = True

        frac = covered.sum() / window_length
        results[tol] = frac
        print(f"  ±{tol:>3d} yr:  {frac:.1%} of the window is covered")

    print(f"\n  At ±250 yr, {results[250]:.1%} of all years between "
          f"{window_start_bc:,} and {window_end_bc:,} BC are")
    print(f"  within 250 years of a notable event. A random date drawn from this")
    print(f"  window has a {results[250]:.1%} chance of being 'near something notable.'")

    return results


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 10: CIRCULAR-SHIFT CATALOG TEST
# ──────────────────────────────────────────────────────────────────────

def run_circular_shift_test(events, n_shifts=1000, rng_seed=RNG_SEED,
                            window_start_bc=20000, window_end_bc=5000):
    """
    Test whether the absolute placement of the event catalog matters.
    Shift the entire catalog by a random offset, wrapping events modulo the
    analysis window to preserve event count and inter-event spacing.

    If the result is similar regardless of shift, event density alone
    explains the anchor probability. If it varies, specific placement matters.
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 10: CIRCULAR-SHIFT CATALOG TEST")
    print("=" * 72)
    print()
    window_len = window_start_bc - window_end_bc
    print(f"  {n_shifts} circular shifts within {window_start_bc:,}–{window_end_bc:,} BC ({window_len:,} yr window).")
    print(f"  Events wrap modulo window length. Preserves spacing and count.")
    print()

    rng = np.random.default_rng(rng_seed)
    cardinals = ["spring_equinox", "summer_solstice", "autumn_equinox", "winter_solstice"]

    # Baseline
    baseline_hits = 0
    total = 0
    for const in ECLIPTIC_CONSTELLATIONS:
        for card in cardinals:
            total += 1
            d = constellation_center_date(const, card)
            matched, _, _ = date_matches_any_event(d, events, tolerance_override=250)
            if matched:
                baseline_hits += 1
    baseline_p = baseline_hits / total

    # Circular shifts: random offset, wrap modulo window
    p_values = []
    for _ in range(n_shifts):
        offset = rng.uniform(0, window_len)
        shifted = []
        for e in events:
            new_date = window_end_bc + (e["date_bc"] - window_end_bc + offset) % window_len
            shifted.append({"name": e["name"], "date_bc": new_date,
                            "half_width_yr": e["half_width_yr"]})

        hits = 0
        for const in ECLIPTIC_CONSTELLATIONS:
            for card in cardinals:
                d = constellation_center_date(const, card)
                matched, _, _ = date_matches_any_event(d, shifted, tolerance_override=250)
                if matched:
                    hits += 1
        p_values.append(hits / total)

    p_arr = np.array(p_values)
    print(f"  Results across {n_shifts} shifted catalogs (center-only, ±250 yr):")
    print(f"    Baseline (real):  {baseline_p:.1%}")
    print(f"    Shifted mean:     {p_arr.mean():.1%}")
    print(f"    Shifted median:   {np.median(p_arr):.1%}")
    print(f"    Shifted min:      {p_arr.min():.1%}")
    print(f"    Shifted max:      {p_arr.max():.1%}")
    print(f"    5th–95th pctile:  {np.percentile(p_arr, 5):.1%}–{np.percentile(p_arr, 95):.1%}")

    # What fraction of shifts give P ≥ baseline?
    frac_ge = np.mean(p_arr >= baseline_p)
    print(f"\n  {frac_ge:.1%} of random shifts produce P ≥ baseline ({baseline_p:.1%}).")
    print(f"  The real catalog's event placement is {'typical' if frac_ge > 0.2 else 'somewhat favorable'}"
          f" relative to random shifts.")

    return {
        "baseline_p": baseline_p,
        "mean": float(p_arr.mean()),
        "median": float(np.median(p_arr)),
        "p5": float(np.percentile(p_arr, 5)),
        "p95": float(np.percentile(p_arr, 95)),
        "frac_ge_baseline": float(frac_ge),
    }


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 11: LEAVE-ONE-ANIMAL-OUT INFLUENCE ANALYSIS
# ──────────────────────────────────────────────────────────────────────

def run_leave_one_animal_out():
    """
    Remove each animal mapping one at a time and recompute the exact
    rank-sum probability. Shows which individual animals drive the significance.
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 11: LEAVE-ONE-ANIMAL-OUT INFLUENCE ANALYSIS")
    print("=" * 72)
    print()

    N = N_VISIBLE_CONSTELLATIONS
    all_sum = sum(m["rank_of_44"] for m in SWEATMAN_MAPPINGS)
    p_all = exact_rank_sum_probability(len(SWEATMAN_MAPPINGS), N, all_sum)

    print(f"  Baseline: {len(SWEATMAN_MAPPINGS)} animals, sum = {all_sum}, "
          f"P = {p_all:.4e} (≈ 1 in {1/p_all:,.0f})")
    print()
    print(f"  {'Dropped animal':<25s}  Rank  Remaining sum  P(remaining)      1-in          Δ significance")
    print(f"  {'-'*25}  ----  -------------  ------------  ----------  ----------------")

    results = []
    for i, dropped in enumerate(SWEATMAN_MAPPINGS):
        remaining = [m for j, m in enumerate(SWEATMAN_MAPPINGS) if j != i]
        n_rem = len(remaining)
        s_rem = sum(m["rank_of_44"] for m in remaining)
        p_rem = exact_rank_sum_probability(n_rem, N, s_rem)
        ratio = p_rem / p_all  # how much less significant (>1 = weaker)

        results.append({
            "animal": dropped["animal"],
            "rank": dropped["rank_of_44"],
            "constellation": dropped["constellation"],
            "remaining_sum": s_rem,
            "p_remaining": p_rem,
            "ratio": ratio,
        })

        print(f"  {dropped['animal']:<25s}  {dropped['rank_of_44']:>3d}   "
              f"{s_rem:>12d}   {p_rem:>11.4e}  {1/p_rem:>10,.0f}  "
              f"  {ratio:>8.1f}× weaker")

    # Sort by impact
    results.sort(key=lambda r: r["ratio"], reverse=True)
    most_critical = results[0]
    least_critical = results[-1]

    print(f"\n  Most critical animal: {most_critical['animal']} (rank {most_critical['rank']})")
    print(f"    Removing it makes the result {most_critical['ratio']:.1f}× weaker.")
    print(f"  Least critical animal: {least_critical['animal']} (rank {least_critical['rank']})")
    print(f"    Removing it makes the result only {least_critical['ratio']:.1f}× weaker.")

    return {"baseline_p": p_all, "results": results}


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 12: RANKING SENSITIVITY
# ──────────────────────────────────────────────────────────────────────

# Alternative ranking schemes for the 6 animals.
# Order: Scorpion, Wolf, Ophiuchus, Pisces, Gemini, Virgo
RANKING_SCHEMES = {
    "Sweatman original":     [1, 1, 1, 4, 5, 6],
    "Conservative (+1 each)":[2, 2, 2, 5, 6, 7],
    "Skeptical (top3 at 3)": [3, 3, 3, 4, 5, 6],
    "Mixed (top3 vary)":     [1, 2, 3, 4, 5, 6],
    "Degraded (top3 at 5)":  [5, 5, 5, 4, 5, 6],
    "Generous (bot3 better)":[1, 1, 1, 2, 3, 4],
}


def run_ranking_sensitivity():
    """
    Ranking-robustness stress test: does the conclusion (top 3 dominate,
    bottom 3 are weak) survive under alternative plausible ranking schemes?
    These are hand-crafted perturbations, not independent validation.
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 12: RANKING SENSITIVITY")
    print("=" * 72)
    print()
    print("  Alternative ranking schemes for the 6 Pillar 43 animals.")
    print("  Tests whether the conclusion depends on one exact ranking vector.")
    print()

    N = N_VISIBLE_CONSTELLATIONS

    print(f"  {'Scheme':<26s}  Ranks               Sum   P(sum≤S)      1-in     Top3 P       Bot3 P")
    print(f"  {'-'*26}  ------------------  ---  ----------  ---------  -----------  -----------")

    results = []
    for name, ranks in RANKING_SCHEMES.items():
        s = sum(ranks)
        p_all = exact_rank_sum_probability(6, N, s)
        top3 = sorted(ranks)[:3]
        bot3 = sorted(ranks)[3:]
        p_top3 = exact_rank_sum_probability(3, N, sum(top3))
        p_bot3 = exact_rank_sum_probability(3, N, sum(bot3))

        results.append({
            "scheme": name, "ranks": ranks, "sum": s,
            "p_all": p_all, "p_top3": p_top3, "p_bot3": p_bot3,
            "top3_ranks": top3, "bot3_ranks": bot3,
        })

        print(f"  {name:<26s}  {str(ranks):<18s}  {s:>3d}   {p_all:>9.2e}  {1/p_all:>9,.0f}  "
              f"  {p_top3:>9.2e}   {p_bot3:>9.2e}")

    # Check stability of top-3 identity
    print(f"\n  Key question: do the same 3 animals (scorpion, canid, Ophiuchus)")
    print(f"  remain the strongest across ranking schemes?")
    print(f"  Answer: by construction, yes — these are always the lowest-ranked trio")
    print(f"  in every scheme except 'Degraded' and 'Generous'.")
    print()
    print(f"  Stability of overall significance:")
    p_values = [r["p_all"] for r in results]
    print(f"    Range: {min(p_values):.2e} to {max(p_values):.2e}")
    print(f"    ({1/max(p_values):,.0f}× to {1/min(p_values):,.0f}×)")
    print(f"    Even under 'Conservative' ranks (+1 each), significance drops")

    conservative = next(r for r in results if "Conservative" in r["scheme"])
    original = next(r for r in results if "original" in r["scheme"])
    print(f"    from 1 in {1/original['p_all']:,.0f} to 1 in {1/conservative['p_all']:,.0f}.")

    return results


# ──────────────────────────────────────────────────────────────────────
#  EXPERIMENT 13: ANIMAL-IDENTITY PERMUTATION TEST
# ──────────────────────────────────────────────────────────────────────

def run_identity_permutation():
    """
    Keep the 6 observed rank values [1,1,1,4,5,6] fixed. Randomly permute
    which animal receives which rank. How often do the three rank-1 values
    land on exactly the claimed trio (scorpion, wolf, Ophiuchus)?

    This tests whether the IDENTITY of the top-3 animals matters, beyond
    the fact that three of six ranks happen to equal 1.
    """
    print("\n" + "=" * 72)
    print("EXPERIMENT 13: ANIMAL-IDENTITY PERMUTATION TEST")
    print("=" * 72)
    print()

    ranks = sorted([m["rank_of_44"] for m in SWEATMAN_MAPPINGS])  # [1,1,1,4,5,6]
    n_animals = len(ranks)
    n_top = sum(1 for r in ranks if r == ranks[0])  # 3 animals share rank 1
    claimed_top = ["Scorpion", "Wolf/dog (canid)", "Tall bird + snake"]

    # Analytical: P = C(n_top, n_top) / C(n_animals, n_top)
    p_identity = comb(n_top, n_top) / comb(n_animals, n_top)

    print(f"  Observed ranks: {ranks}")
    print(f"  {n_top} animals share the top rank ({ranks[0]})")
    print(f"  Claimed top-{n_top}: {', '.join(claimed_top)}")
    print()
    print(f"  Under random permutation of rank assignments:")
    print(f"    P(specific trio gets all rank-1 slots) = C({n_top},{n_top})/C({n_animals},{n_top})")
    print(f"    = 1/{comb(n_animals, n_top)} = {p_identity:.1%}")
    print()

    # Monte Carlo confirmation
    rng = np.random.default_rng(RNG_SEED)
    n_sims = 100_000
    count = 0
    for _ in range(n_sims):
        perm = rng.permutation(n_animals)
        # Check if the first 3 animals (indices 0,1,2 = scorpion, wolf, Ophiuchus)
        # all get rank 1 after permutation
        assigned_ranks = [ranks[perm[i]] for i in range(n_animals)]
        if all(assigned_ranks[i] == 1 for i in range(n_top)):
            count += 1

    p_mc = count / n_sims
    print(f"  Monte Carlo ({n_sims:,} trials): {count}/{n_sims:,} = {p_mc:.1%}")
    print(f"  (matches analytical: {p_identity:.1%})")
    print()
    print(f"  Conditional on a rank pattern with three rank-1 slots, the probability")
    print(f"  that the specific claimed trio (scorpion, canid, Ophiuchus) occupies")
    print(f"  them is {p_identity:.0%}. This is mildly informative but not striking on")
    print(f"  its own. Its value is as a complement to the decomposition and")
    print(f"  leave-one-animal-out results.")

    return {
        "n_top": n_top,
        "p_identity": p_identity,
        "p_mc": p_mc,
        "claimed_top": claimed_top,
    }


# ──────────────────────────────────────────────────────────────────────
#  FIGURES
# ──────────────────────────────────────────────────────────────────────

def generate_figures(anchor_results, similarity_results, sensitivity_results, events,
                     sweep_results=None):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n  [WARN] matplotlib not installed. Skipping figures.")
        print("         pip install matplotlib --break-system-packages")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── Fig 1: Timeline ──
    fig, ax = plt.subplots(figsize=(14, 7))
    colors_c = plt.cm.Set3(np.linspace(0, 1, len(ECLIPTIC_CONSTELLATIONS)))
    for i, const in enumerate(ECLIPTIC_CONSTELLATIONS):
        d_min, d_max = constellation_date_range(const, "summer_solstice")
        ax.barh(i, d_max - d_min, left=d_min, height=0.7,
                color=colors_c[i], edgecolor="gray", linewidth=0.5)
        ax.text((d_min + d_max) / 2, i, const["name"],
                ha="center", va="center", fontsize=7, fontweight="bold")
    for ev in events:
        ax.axvline(ev["date_bc"], color="red", alpha=0.4, linewidth=0.8, linestyle="--")
        ax.text(ev["date_bc"], len(ECLIPTIC_CONSTELLATIONS) + 0.3,
                ev["name"], rotation=45, fontsize=5, ha="right", va="bottom", color="red")
    ax.axvline(SWEATMAN_DATE_BC, color="blue", linewidth=2, alpha=0.7)
    ax.text(SWEATMAN_DATE_BC, -1.2, f"Sweatman: {SWEATMAN_DATE_BC:,} BC",
            ha="center", fontsize=8, color="blue", fontweight="bold")
    ax.set_xlabel("Year BC", fontsize=11)
    ax.set_ylabel("Ecliptic Constellation (SS sun)", fontsize=11)
    ax.set_title("Summer Solstice Sun Position by Constellation\nvs. Notable Paleoclimatic Events",
                 fontsize=13)
    ax.invert_xaxis()
    ax.set_yticks(range(len(ECLIPTIC_CONSTELLATIONS)))
    ax.set_yticklabels([c["name"] for c in ECLIPTIC_CONSTELLATIONS], fontsize=8)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig1_timeline.png", dpi=200)
    plt.close(fig)
    print(f"  Saved {OUTPUT_DIR / 'fig1_timeline.png'}")

    # ── Fig 2: Sensitivity heatmap ──
    tolerances = [50, 100, 150, 200, 250, 300, 400, 500]
    scenario_names = list(sensitivity_results.keys())
    data = np.array([[sensitivity_results[s][t]["p"] for t in tolerances]
                     for s in scenario_names])
    fig, ax = plt.subplots(figsize=(10, 4))
    im = ax.imshow(data, aspect="auto", cmap="YlOrRd", vmin=0, vmax=0.6)
    ax.set_xticks(range(len(tolerances)))
    ax.set_xticklabels([f"±{t}" for t in tolerances], fontsize=9)
    ax.set_yticks(range(len(scenario_names)))
    ax.set_yticklabels(scenario_names, fontsize=8)
    ax.set_xlabel("Tolerance (years)", fontsize=11)
    ax.set_title("Anchor Test: P(random center date matches a notable event)", fontsize=12)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            color = "white" if data[i, j] > 0.35 else "black"
            ax.text(j, i, f"{data[i, j]:.0%}", ha="center", va="center",
                    fontsize=9, color=color, fontweight="bold")
    plt.colorbar(im, ax=ax, label="Probability")
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig2_sensitivity.png", dpi=200)
    plt.close(fig)
    print(f"  Saved {OUTPUT_DIR / 'fig2_sensitivity.png'}")

    # ── Fig 3: Rank-sum distribution (lightweight MC for visualization only) ──
    rng = np.random.default_rng(RNG_SEED)
    random_sums = rng.integers(1, N_VISIBLE_CONSTELLATIONS + 1,
                               size=(200_000, N_TESTED_ANIMALS)).sum(axis=1)
    fig, ax = plt.subplots(figsize=(10, 5))
    bins = np.arange(6, 265, 2)
    ax.hist(random_sums, bins=bins, density=True, color="steelblue", alpha=0.7,
            edgecolor="white", linewidth=0.3, label="Null distribution (random ranks)")
    ax.axvline(SWEATMAN_RANK_SUM, color="red", linewidth=2.5,
               label=f"Sweatman's sum = {SWEATMAN_RANK_SUM}")
    ax.axvline(random_sums.mean(), color="gray", linewidth=1, linestyle="--",
               label=f"Expected = {random_sums.mean():.0f}")
    p_exact = similarity_results["p_exact"]
    ax.text(SWEATMAN_RANK_SUM + 3, ax.get_ylim()[1] * 0.85,
            f"Exact P(sum ≤ {SWEATMAN_RANK_SUM}) = {p_exact:.4e}\n≈ 1 in {1/p_exact:,.0f}",
            fontsize=10, color="red", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.9))
    ax.set_xlabel("Rank-sum (6 animals × rank out of 44 constellations)", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)
    ax.set_title("Visual-Similarity Rank-Sum Distribution\n(Exact probability via inclusion-exclusion)",
                 fontsize=13)
    ax.legend(fontsize=9)
    ax.set_xlim(0, 270)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig3_rank_sum.png", dpi=200)
    plt.close(fig)
    print(f"  Saved {OUTPUT_DIR / 'fig3_rank_sum.png'}")

    # ── Fig 4: Anchor bracket bar chart ──
    fig, ax = plt.subplots(figsize=(9, 4))
    labels = ["Center-only\n(strict)", "Window-overlap\n(broad)"]
    r250 = anchor_results[250]
    vals = [r250["p_center"], r250["p_window"]]
    bars = ax.barh(range(2), vals, color=["#3498db", "#e74c3c"], height=0.5)
    ax.set_yticks(range(2))
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel("P(random anchor matches a notable event)", fontsize=11)
    ax.set_title("Anchor Test Bracket at ±250 yr Tolerance", fontsize=13)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:.1%}", va="center", fontsize=11, fontweight="bold")
    ax.set_xlim(0, max(vals) * 1.3)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig4_anchor_bracket.png", dpi=200)
    plt.close(fig)
    print(f"  Saved {OUTPUT_DIR / 'fig4_anchor_bracket.png'}")

    # ── Fig 5: Catalog robustness sweep ──
    if sweep_results and sweep_results.get("all_p_values"):
        p_vals = np.array(sweep_results["all_p_values"])
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(p_vals * 100, bins=30, color="darkorange", alpha=0.7,
                edgecolor="white", linewidth=0.5)
        ax.axvline(30.8, color="blue", linewidth=2, linestyle="--",
                   label="Baseline (unperturbed): 30.8%")
        ax.axvline(p_vals.mean() * 100, color="red", linewidth=2,
                   label=f"Mean: {p_vals.mean():.1%}")
        ax.set_xlabel("P(anchor hit) across perturbed catalogs (%)", fontsize=11)
        ax.set_ylabel("Count", fontsize=11)
        ax.set_title(f"Catalog Robustness: {len(p_vals)} Perturbed Event Catalogs\n"
                     f"(center-only anchor, ±250 yr)", fontsize=13)
        ax.legend(fontsize=9)
        plt.tight_layout()
        fig.savefig(OUTPUT_DIR / "fig5_catalog_sweep.png", dpi=200)
        plt.close(fig)
        print(f"  Saved {OUTPUT_DIR / 'fig5_catalog_sweep.png'}")


# ──────────────────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  GÖBEKLI TEPE PILLAR 43 — STATISTICAL ARCHAEOASTRONOMY TEST  v3   ║")
    print("║  Testing Sweatman & Tsikritsis (2017) constellation claims         ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    print(f"  Precession period:       {PRECESSION_PERIOD_YR:,} yr")
    print(f"  Ecliptic constellations: {len(ECLIPTIC_CONSTELLATIONS)}")
    print(f"  Visible constellations:  {N_VISIBLE_CONSTELLATIONS}")
    print(f"  Event clusters:          {len(EVENT_CLUSTERS)}")

    # Validate
    print("\n  Precession validation:")
    lam = ecliptic_longitude_of_solstice(10_950, "summer_solstice")
    sag = next(c for c in ECLIPTIC_CONSTELLATIONS if c["name"] == "Sagittarius")
    ok1 = sag["lam_start"] <= lam <= sag["lam_end"]
    print(f"    SS at 10,950 BC → λ = {lam:.2f}°  {'✓ in Sagittarius' if ok1 else '✗'}")
    lam2 = ecliptic_longitude_of_solstice(3_000, "spring_equinox")
    tau = next(c for c in ECLIPTIC_CONSTELLATIONS if c["name"] == "Taurus")
    ok2 = tau["lam_start"] <= lam2 <= tau["lam_end"]
    print(f"    VE at  3,000 BC → λ = {lam2:.2f}°  {'✓ in Taurus' if ok2 else '✗'}")

    # Run
    anchor_results = run_anchor_test(EVENT_CLUSTERS)
    similarity_results = run_similarity_test()
    joint_results = run_joint_test(anchor_results, similarity_results)
    sensitivity_results = run_sensitivity_analysis(EVENT_CLUSTERS)
    sweep_results = run_catalog_sweep(EVENT_CLUSTERS)
    decomp_results = run_decomposition()
    loo_results = run_leave_one_out(EVENT_CLUSTERS)
    multiverse_results = run_multiverse(EVENT_CLUSTERS)
    coverage_results = run_coverage_fraction(EVENT_CLUSTERS)
    shift_results = run_circular_shift_test(EVENT_CLUSTERS)
    animal_loo_results = run_leave_one_animal_out()
    ranking_results = run_ranking_sensitivity()
    identity_results = run_identity_permutation()

    # Summary
    r250 = anchor_results[250]
    p_sim = similarity_results["p_exact"]
    dr = decomp_results
    mv = multiverse_results
    sr = shift_results
    al = animal_loo_results
    most_critical = max(al["results"], key=lambda r: r["ratio"])
    conservative = next(r for r in ranking_results if "Conservative" in r["scheme"])
    ip = identity_results

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"""
  Sweatman claims statistical significance at ~1 in 1.4 million.
  We decompose and re-evaluate this claim across 13 experiments:

  1. DATE COINCIDENCE: Strict {r250['p_center']:.1%}, Broad {r250['p_window']:.1%}
  2. VISUAL SIMILARITY: P = {p_sim:.4e} (≈ 1 in {1/p_sim:,.0f})
  3. JOINT: Strict {r250['p_center'] * p_sim:.2e}, Broad {r250['p_window'] * p_sim:.2e}
  4. SENSITIVITY: Most conservative scenario still gives 23% at ±250 yr.
  5. CATALOG ROBUSTNESS: {sweep_results['min']:.1%}–{sweep_results['max']:.1%} across 500 catalogs.
  6. DECOMPOSITION: Top 3 = 1 in {1/dr['top3_p']:,.0f}. Bottom 3 = 1 in {1/dr['bot3_p']:,.0f}.
  7. LEAVE-ONE-EVENT-OUT: Min anchor P = {min(r['p'] for r in loo_results['results']):.1%}.
  8. MULTIVERSE: Primary {mv['primary_min']:.1e}–{mv['primary_max']:.1e}; {mv['frac_primary_as_significant']:.0%} of primary paths ≤ Sweatman's.
  9. COVERAGE: {coverage_results[250]:.1%} of 20,000–5,000 BC is near an event.
  10. CIRCULAR-SHIFT: {sr['frac_ge_baseline']:.0%} of shifts ≥ baseline.
  11. ANIMAL-LOO: Most critical = {most_critical['animal']} ({most_critical['ratio']:.1f}× impact).
  12. RANKING SENSITIVITY: Conservative (+1) drops to 1 in {1/conservative['p_all']:,.0f}.
  13. IDENTITY PERMUTATION: P(specific trio gets all rank-1 slots) = {ip['p_identity']:.0%}.

  KEY FINDINGS:
  - The date coincidence is weak: {coverage_results[250]:.0%} of the era is near something notable.
  - The visual similarity is carried by 3 of 6 mappings (1 in 85,184 vs 1 in 187).
  - Those 3 mappings are self-scored and have never been blindly validated.
  - The top-3 dominance pattern is stable across conservative ranking adjustments.
  - The identity of the top-3 trio has a {ip['p_identity']:.0%} chance under random assignment.
  - Significance varies by 2 orders of magnitude across defensible analyst choices.
  - A blind ranking experiment would be the decisive test.
""")

    # Figures
    print("Generating figures...")
    generate_figures(anchor_results, similarity_results, sensitivity_results,
                     EVENT_CLUSTERS, sweep_results)

    # JSON — save full data for reproducibility
    all_results = {
        "anchor_test": {str(k): {kk: vv for kk, vv in v.items() if kk != "center_details"}
                        for k, v in anchor_results.items()},
        "similarity_test": similarity_results,
        "joint_test": {str(k): v for k, v in joint_results.items()},
        "catalog_sweep": {k: v for k, v in sweep_results.items() if k != "all_p_values"},
        "decomposition": decomp_results,
        "leave_one_out": {
            "baseline_p": loo_results["baseline_p"],
            "per_event": [{k: v for k, v in r.items()} for r in loo_results["results"]],
        },
        "multiverse": multiverse_results,
        "coverage": coverage_results,
        "circular_shift": shift_results,
        "leave_one_animal_out": {
            "baseline_p": animal_loo_results["baseline_p"],
            "per_animal": animal_loo_results["results"],
        },
        "ranking_sensitivity": ranking_results,
        "identity_permutation": identity_results,
        "parameters": {
            "precession_period_yr": PRECESSION_PERIOD_YR,
            "n_ecliptic_constellations": len(ECLIPTIC_CONSTELLATIONS),
            "n_visible_constellations": N_VISIBLE_CONSTELLATIONS,
            "n_event_clusters": len(EVENT_CLUSTERS),
            "sweatman_rank_sum": SWEATMAN_RANK_SUM,
        },
    }
    with open(OUTPUT_DIR / "results.json", "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"  Saved {OUTPUT_DIR / 'results.json'}")
    print("\nDone.")


if __name__ == "__main__":
    main()
