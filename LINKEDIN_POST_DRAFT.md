# LinkedIn-ready post (not yet posted to LinkedIn)

Can a video game release period change what people pay for a secondhand console? 🎮📈

I analyzed historical prices for used Xbox Series S 512 GB consoles in Germany using Python and two marketplace datasets.

**One finding:** In my filtered third-party eBay sample, the middle reported sold price rose from **$230.54 in August (301 records)** to **$330.81 during 1–18 November 2026 (372 records)** — an **observed increase of 43.5%**.

I also looked at Kleinanzeigen asking prices and estimated eBay euro equivalents using historical exchange rates. Importantly, **asking prices are not completed sales** and the two samples are not directly interchangeable.

The real challenge wasn't just making a chart: it was checking duplicate values, testing alternative product filters, handling missing historical days without fabricating prices, and measuring uncertainty.

This is **exploratory research, not proof that GTA VI caused the change**. Microsoft's new-console pricing, seasonality and item mix may also matter.

My Python code, readable charts, aggregates and full limitations are here:
https://github.com/sebusubash-rgb/gta6-xbox-price-analysis

What other factor would you test to explain the rise?

#Python #DataAnalytics #MarketResearch #DataVisualization #PersonalProject

**Suggested image to attach:** figures/final_main_USD_monthly_IQR.png or figures/final_eBay_USD_prelaunch_trend.png
