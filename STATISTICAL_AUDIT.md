# Statistical review (based on private, filtered row-level samples)

This document reports independently checked summary outputs; item-level data are not redistributed. The product-selection rules are *not* completely validated against original listings.

| Sample | Earlier median | Later median | Change | Bootstrap approximate 95% interval | Earlier n | Later n |
|---|---:|---:|---:|---|---:|---:|
| eBay reported USD sold prices, Aug vs Nov 1–18 | $230.54 | $330.81 | +43.5% | +41.0% to +48.7% | 301 | 372 |
| eBay estimated EUR sold prices, Aug vs Nov 1–18 | €199.00 | €298.58 | +50.0% | +46.4% to +55.6% | 301 | 372 |
| Kleinanzeigen EUR asking prices, Oct 26–31 vs Nov 1–18 | €240.00 | €290.00 | +20.8% | +10.2% to +60.0% | 48 | 237 |

**Bootstrap:** 6,000 repetitions, resampling all sales/observations from sampled calendar days as whole groups, separately within each period, seed 20261119. These are not population-level confidence bounds; bootstrap assumptions do not correct non-random collection, autocorrelation across adjacent days, reobserved listings or mislabeled consoles.

**Exact-value duplicate sensitivity:** eBay 301→276 baseline and 372→335 later under removal of identical exported fields, +43.2% vs +43.5% originally. For Kleinanzeigen 48→41 and 237→180, +30.2% vs +20.8% originally. Equal field values are insufficient to prove actual transaction duplication.

**Alternative secondary classifier:** eBay n=143 in August vs n=146 in November, medians $230.52 and $330.69, +43.5%. Kleinanzeigen n=29 vs n=136, €240 vs €282.50, +17.7%. These tests demonstrate sensitivity to filtering, not ground-truth console identities.

**Interquartile ranges:** eBay August $208.26–$242.74; November $297.09–$351.85. The eBay EUR estimates are €179.90–€209.89 and €266.64–€316.27 for the same periods.

**Critical limits:** eBay source reported USD, and historical conversion applied to each observation date for August–November only. The record sample and price measurement differ from Kleinanzeigen asking-price observations, and incomplete date coverage must not be backfilled. GTA VI's scheduled 19 November release is a contextual marker, not a causal finding.
