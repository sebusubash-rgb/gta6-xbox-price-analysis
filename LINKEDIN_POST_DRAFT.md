# LinkedIn post draft — REVIEW BEFORE POSTING

**What happened to used Xbox Series S prices in Germany during 2026?** 🎮📊

I analyzed historical marketplace data in Python, including **2,380 filtered eBay sold-price records**.

My clearest finding: the **median reported sold price** in this sample rose from **$230.54 in August (n=301)** to **$330.81 during 1–18 November (n=372)** — **+43.5%**.

But there's a major complication: **Microsoft increased the NEW Xbox Series S 512 GB retail price in Germany from €349.99 to €499.99 on 1 August 2026**. And June–July historical sales coverage is missing. So the data cannot tell us whether GTA VI anticipation caused the resale-price rise.

I checked the finding against alternative product filters, identical-value records, price ranges and day-resampling uncertainty estimates. The eBay trend held up; the shorter Kleinanzeigen asking-price sample was less stable.

The lesson for me wasn't only making a chart. It was learning how to **question the data behind the chart**.

📈 Chart: simple eBay sold-price summary, with sample counts and retail-price context.

Full code, visualizations, public aggregates and limitations:
https://github.com/sebusubash-rgb/gta6-xbox-price-analysis

What other factors would you test — retail pricing, seasonality, or something else?

#Python #DataAnalytics #MarketResearch #DataVisualization

---

**Images to attach in this order:** (1) `figures/hero_LinkedIn_USD.png` for the five-second headline; (2) `figures/full_year_context_USD.png` to show the pre-August baseline, missing June–July data and August's post-Microsoft-increase timing.

**Important:** USD here is the third-party provider's reported eBay sold-price currency, not confirmed original EUR checkout values. GTA VI release date: 19 Nov 2026; collection ends 18 Nov. This is an exploratory sample, not a causal study.
