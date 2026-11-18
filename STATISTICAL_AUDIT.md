# Statistical audit and interpretation

Independent checks against private filtered row-level extracts confirmed the public median, IQR, date-count and estimated EUR aggregates. **Original listing/product classification is not fully hand-validated**, and third-party source reliability is not independently certified.

## Historical context must come before causal speculation

The most important competing event is **Microsoft's increase in the NEW German Xbox Series S 512 GB recommended retail price from €349.99 to €499.99**, effective **1 August 2026**. See [Microsoft Xbox Wire](https://news.xbox.com/en-us/2026/06/25/xbox-console-price-update/) and [ComputerBase's German comparison](https://www.computerbase.de/news/gaming/spielkonsole-xbox-series-x-s-kostet-jetzt-bis-zu-weitere-200-euro-mehr.98679/).

The observed eBay August–November sold-price median increase of +43.5% is numerically similar to the **+42.9% retail MSRP increase**, but is **not a like-for-like percentage comparison**: one is *used marketplace prices reported in USD over August–November* and the other *new-console German MSRP in EUR changed on 1 August*. Crucially, **August is already after the MSRP increase**; the data cannot isolate its contribution to the subsequent rise.

Pooled January–April median reported eBay price = **$193.47 (n=947)**, while November 1–18 = **$330.81 (n=372)**, an approximate **+71.0%** difference. June–July records are unavailable and May is partial; do not assign the timing of the unobserved increase.

## Recalculated period outcomes

| Measure | Earlier period | Later period | Observed change | Approximate day-bootstrap 95% interval | Baseline n | Later n |
|---|---:|---:|---:|---|---:|---:|
| eBay reported USD SOLD price, Aug vs Nov 1–18 | $230.54 | $330.81 | +43.5% | +41.0% to +48.7% | 301 | 372 |
| eBay estimated EUR SOLD price, Aug vs Nov 1–18 | €199.00 | €298.58 | +50.0% | +46.4% to +55.6% | 301 | 372 |
| Kleinanzeigen EUR ASKING price, Oct 26–31 vs Nov 1–18 | €240.00 | €290.00 | +20.8% | **unstable; not suitable as a precise headline** | 48 | 237 |

**Method:** 6,000 repetitions with seed 20261119, resampling complete observed days independently within each comparison period. Separate 20,000-draw checks using a different seed reproduced the eBay intervals and found Kleinanzeigen much more volatile. This day-resampling approach does **not** account for adjacent-day serial dependence, sample-selection error, provider errors, repeated listings, or misclassification. The eBay intervals are conditional on the sample and bootstrap assumptions and are **not population confidence bounds**.

**IQRs:** eBay August $208.26–$242.74 and Nov 1–18 $297.09–$351.85 (the middle 50% of sampled sales, **not uncertainty intervals**). In estimated EUR, August €179.90–€209.89 and Nov €266.64–€316.27.

## Suspected repeated records: material for Kleinanzeigen

Within the deliberately stripped-down audit extract (date, price and limited flags), **163 eBay and 64 Kleinanzeigen rows have identical field combinations**. There are also many same-day, same-price occurrences. These patterns merit a source-ID audit because identical values alone cannot identify a transaction.

We **provisionally retain** all records in the main report; removing identical-value rows yields:

| Sensitivity scenario | eBay Aug to Nov increase | Kleinanzeigen Oct 26–31 to Nov increase |
|---|---:|---:|
| Original filtered sample | +43.5% | +20.8% |
| After removing identical-value rows | +43.2% | +30.2% |
| Secondary-classifier-approved subset | +43.5% (Aug n=143; Nov n=146) | +17.7% (Oct n=29; Nov n=136) |

Removing rows sharing only date and price can delete genuine independent transactions; retaining them can preserve repeat collection artifacts. Without original transaction IDs, neither treatment is verified ground truth. **The eBay result is robust to the tested choices; Kleinanzeigen's change is roughly +18% to +30% depending on the rules.** With only six observed baseline dates, the Kleinanzeigen result must remain *suggestive*.

## Currencies and comparability

- eBay's third-party sold-price records are in **provider-reported USD**. For 1 Aug–18 Nov only, each price was converted into estimated EUR using the ECB reference rate on that date (latest preceding published rate on weekends/nonpublication days).
- The estimated USD→EUR growth difference primarily reflects the historical exchange-rate change. The computed EUR numbers are not verified original EUR checkout values and do **not** exist for Jan–May in this project.
- Kleinanzeigen observations are **asking prices**, not verified completed sales. Its October baseline is different from the eBay August baseline. The two marketplaces are not controlled matches and cannot be pooled.

## Scope and next questions

The study includes **no GTA VI post-launch resale observations**: the latest observation is **18 November 2026**, one day before the release date. Other possible drivers include retail replacement cost, seasonal electronics demand, changed condition/bundle mixes, sampling method shifts and collection caps.

This repository only redistributes non-identifying aggregates; it does not certify third-party transaction sources or provide a full manual review of product titles.
