# Methodology and data quality

## Research design and cutoff

An observational historical price study of selected second-hand Xbox Series S 512 GB listings, with the data cutoff at **18 November 2026**, before the scheduled **19 November 2026** GTA VI launch. Research question: whether resale prices rise in the pre-launch period, acknowledging alternative drivers and missing data. **Association is not causation**.

## Data sources and measurement

1. **eBay Germany:** Third-party CompsAPI historical sold-listing data, reported **in USD**. `sold_date` comes from the provider's sold timestamps. The analyzed dependent variable is reported item price; shipping is **not** included. The original data contained **18,502** unique reported sales records; a previous project's inherited “used Xbox Series S 512 GB” selection has **2,380** rows. The exact accuracy of third-party sold-price confirmations is not independently verified.
2. **Kleinanzeigen Germany:** Historical scraped/API listings. Asking prices are **in EUR**, not sold prices. There were **4,858** deduplicated source observations; the project's inherited used-512 GB subset has **285 listing-day observations**. The same listing can be reobserved, and a listing-day isn't necessarily a unique sale or a unique machine.

For this publication, only **aggregate** derived CSVs are included. No seller details, URLs, original listings or complete API responses are redistributed. Original scraping scripts are intentionally not included because they may expose implementation details or disallowed scraping flows; `analyze.py` uses only the safe aggregates.

## Filtering integrity: open issue

The inherited strict sample was generated with earlier code. A **separate classifier contradicts some strict classifications**:

| Dataset | Strict subset records | Secondary classifier false | Status |
|---|---:|---:|---|
| eBay | 2,380 | 1,272 `is_series_s_console=False` | Disagreement unresolved |
| Kleinanzeigen | 285 | 120 `is_console=False` | Disagreement unresolved |

These are **not proven invalid listings**. For example, mentions of "controller" may trigger an overly aggressive accessory detector even in genuine console-bundle ads. However, the disagreement prevents claiming the subset has been fully audited. Additional Kleinanzeigen storage titles may say "500 GB" while mapped to 512 GB. Robustness checks should reclassify manually reviewed records or use a clear documented title/condition rule and recalculate everything. Do **not** treat the strict label as externally certified.

## Aggregation: what is actually in the public CSVs

- **Daily tables:** Dates with any included records, record count, sample median and sample mean, min and max, by marketplace. They are the observed values, **not an exhaustive market census**.
- **Monthly tables:** Each monthly sample median is calculated from *individual selected record prices* for that month, not from an unweighted median of daily medians. Monthly counts are sample counts, not population transactions.
- **Coverage:** The Kleinanzeigen coverage table distinguishes any imported data from a verified complete-day crawl. `complete_day_verified` is false even when `has_any_data` is true.
- **Deduplication:** Imported CSVs were deduplicated upstream. Two sources that reuse the same listing may still have limitations due to changes in identifiers or snapshots; the aggregate publication does not re-audit that process.

## Missingness: no made-up observations

- **eBay:** 8–9 May; 15 May–31 July (78 days). June and July monthly medians are deliberately absent. The May median is from **only 86 sample observations**.
- **Kleinanzeigen:** 21–25 October; 4–5 November; 10–11 November. Full-day completeness has not been verified for any day.
- Rolling medians show a smoothed view of observed days only. They do **not** fill empty dates or imply prices were observed when they were not. A long unobserved time gap is a data-collection limitation—not evidence of no listings.
- **Do not** fill a 78-day gap with the nearest median, last observation, or a straight line and present it as observed data. Model-based imputations, if added later, should use dashed lines, explicit assumptions, uncertainty, and an observed-only main specification.

## Calculations

- eBay August 2026: `n=301`, median **USD 230.54**.
- eBay 1–18 November 2026: `n=372`, median **USD 330.81**. Relative change **(330.81/230.54 - 1) × 100 ≈ 43.5%**.
- Kleinanzeigen 26–31 October 2026: `n=48`, median **EUR 240**.
- Kleinanzeigen 1–18 November 2026: `n=237`, median **EUR 290**. Relative change **(290/240 - 1) × 100 ≈ 20.8%**.

These are across-month or across-period medians of sampled records. They are **not** matched repeated-sale prices, constant-quality price indices or inflation-adjusted/currency-normalized metrics. Both pricing and item mix may vary over time.

## Competing explanations and threats to inference

- **Microsoft's retail price increase:** Official worldwide adjustment effective 1 Aug 2026. Reported German Series S 512 GB MSRP **€349.99 → €499.99**. This is a significant time-varying factor affecting substitution into used consoles.
- **GTA VI anticipation:** Release announced for 19 Nov 2026. The project only observes pre-release data, so cannot compare prices before and after launch.
- **Seasonality:** Demand and selling behavior around autumn, holidays and Black Friday may be changing.
- **Product mix and condition:** Bundled accessories, wear, storage labeling and seller behavior can affect prices.
- **Sampling limitations:** The provider's historical API caps and pagination caused incomplete date coverage, potentially nonrandom missingness. There is no proof of representativeness.
- **Cross-market differences:** eBay reports sold prices in USD via a third party, while Kleinanzeigen contains asks in EUR. Their trends cannot be pooled as a single treatment-control analysis.

## External factual context

- [Microsoft Xbox Wire, 25 June 2026](https://news.xbox.com/en-us/2026/06/25/xbox-console-price-update/)
- [ComputerBase: German Xbox prices after the August increase](https://www.computerbase.de/news/gaming/spielkonsole-xbox-series-x-s-kostet-jetzt-bis-zu-weitere-200-euro-mehr.98679/)
- [Rockstar Games: GTA VI release-date announcement](https://www.rockstargames.com/newswire/article/ak3ak31a49a221/grand-theft-auto-vi-is-now-set-to-launch-november-19-2026)

## Redistribution and privacy

The publication includes aggregated statistics only. Sharing item-level third-party marketplace data may implicate rights or restrictions; permissions have not been established. The user's API secrets and any raw listing data remain private and are not included.
