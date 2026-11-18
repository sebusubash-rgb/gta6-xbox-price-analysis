#!/usr/bin/env python3
"""Reproduce public EUR-comparison figures, offline. No API keys or network calls."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BASE=Path(__file__).resolve().parent
D=BASE/"data"
F=BASE/"figures"
F.mkdir(exist_ok=True)
BLUE="#1775a7"
ORANGE="#d16a1e"
FXURL="https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/eurofxref-graph-usd.en.html"

fx=pd.read_csv(D/"ECB_USD_per_EUR_reference_rates.csv",parse_dates=["rate_date"])
eb=pd.read_csv(D/"ebay_daily_aggregated_USD.csv",parse_dates=["date"])
kl=pd.read_csv(D/"kleinanzeigen_daily_aggregated_EUR.csv",parse_dates=["date"])
assert len(fx)==79 and len(eb)==242 and len(kl)==20
assert eb["count"].sum()==2380 and kl["count"].sum()==285
cal=pd.DataFrame({"date":pd.date_range("2026-08-01","2026-11-18")})
daily=pd.merge_asof(cal,fx.rename(columns={"rate_date":"applied_rate_date"}),
                    left_on="date",right_on="applied_rate_date",direction="backward")
daily=daily.merge(eb[["date","count","median"]],on="date",how="left",validate="one_to_one")
assert daily["median"].notna().all() and daily["usd_per_eur"].notna().all()
daily["estimated_median_eur"]=daily["median"]/daily["usd_per_eur"]
daily = daily.rename(columns={"count":"ebay_n","median":"ebay_median_usd"})
daily.to_csv(
    D/"ebay_daily_estimated_EUR.csv",index=False,float_format="%.6f")
shared=pd.DataFrame({"date":pd.date_range("2026-10-21","2026-11-18")})
shared=shared.merge(daily[["date","ebay_n","estimated_median_eur"]],on="date",how="left")
shared=shared.merge(kl[["date","count","median"]],on="date",how="left")
shared.rename(columns={"count":"klein_n","median":"klein_asking_median_eur"}).to_csv(
    D/"shared_dates_EUR_comparison.csv",index=False,float_format="%.6f")
assert shared.klein_asking_median_eur.notna().sum()==20

plt.rcParams.update({"figure.dpi":155,"font.size":10,
                    "axes.spines.top":False,"axes.spines.right":False})
def setup(ax):
    ax.grid(axis="y",alpha=.2)
    ax.set_ylabel("EUR")

fig,(a,b)=plt.subplots(2,1,figsize=(11,7.5),sharex=True,sharey=True)
a.plot(shared.date,shared.estimated_median_eur,color=BLUE,marker="o",lw=2.2,ms=3)
b.plot(shared.date,shared.klein_asking_median_eur,color=ORANGE,marker="o",lw=2.2,ms=4)
for ax,label,color in [(a,"eBay — reported SOLD prices, estimated EUR",BLUE),
                        (b,"Kleinanzeigen — advertised ASKING prices, EUR",ORANGE)]:
    setup(ax);ax.set_ylim(115,390)
    ax.text(.01,.92,label,transform=ax.transAxes,color=color,weight="bold",va="top")
b.xaxis.set_major_locator(mdates.DayLocator(interval=3))
b.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
fig.suptitle("Used Xbox Series S 512 GB | same currency, different price measures",weight="bold")
fig.text(.05,.014,"Missing Kleinanzeigen dates left blank. Different item samples; NOT matched sales.",
         fontsize=8,color="#6c747f")
fig.savefig(F/"comparison_both_EUR_OctNov.png",bbox_inches="tight");plt.close(fig)

fig,ax=plt.subplots(figsize=(11.5,6))
roll=daily.estimated_median_eur.rolling(7,min_periods=4).median()
ax.scatter(daily.date,daily.estimated_median_eur,s=17,alpha=.45,color=BLUE,label="Daily eBay median (EUR est.)")
ax.plot(daily.date,roll,color=BLUE,lw=2.7,label="7-day median of daily medians")
ax.axvline(pd.Timestamp("2026-11-19"),color="#ad493c",ls="--",label="GTA VI scheduled release, 19 Nov")
ax.set_xlim(pd.Timestamp("2026-07-31"),pd.Timestamp("2026-11-23"))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.set_title("eBay Germany used Series S sold-price trend | estimated EUR, August–November",weight="bold")
ax.set_ylabel("Estimated sold price (EUR), shipping excluded")
ax.grid(axis="y",alpha=.2)
ax.legend(frameon=False,loc="upper left")
fig.text(.05,.018,"ECB historical reference FX by sale date; third-party USD may not equal original euro checkout price.",
         color="#6c747f",fontsize=8)
fig.savefig(F/"ebay_AugNov_estimated_EUR.png",bbox_inches="tight");plt.close(fig)

months=pd.read_csv(D/"ebay_monthly_EUR_record_level_aggregates.csv")
assert months.n.sum()==1347
fig,ax=plt.subplots(figsize=(9.5,5))
bars=ax.bar(range(4),months.median_eur_est,color=BLUE,width=.65)
ax.set_xticks(range(4),["Aug","Sep","Oct","Nov 1–18"])
ax.set_ylim(0,355)
for bar,row in zip(bars,months.itertuples()):
    ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+8,
            f"€{row.median_eur_est:.0f}\nn={row.n}",ha="center",weight="bold")
ax.set_title("Monthly eBay sold-price medians | historical-FX estimated EUR",weight="bold")
ax.set_ylabel("Estimated median EUR (shipping excluded)")
ax.grid(axis="y",alpha=.2)
fig.text(.04,.02,"Monthly EUR medians computed upstream from individual filtered records; raw listings not redistributed.",
         fontsize=8,color="#6c747f")
fig.savefig(F/"ebay_monthly_estimated_EUR.png",bbox_inches="tight");plt.close(fig)
print("EUR comparison published: 110 eBay days, 20 common observed dates, 3 figures.")
