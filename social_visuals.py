#!/usr/bin/env python3
"""Reproduce three fast-reading portfolio figures using public aggregate files."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT=Path(__file__).resolve().parent
D=ROOT/"data"
OUT=ROOT/"figures"
OUT.mkdir(exist_ok=True)
NAVY="#193249"; TEAL="#007f80"; PALE="#a4b9c7"; GOLD="#d28a27"; MUTED="#536575"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.spines.top":False,
                     "axes.spines.right":False,"axes.spines.left":False,"axes.titleweight":"bold"})
def save(fig,path):
    fig.savefig(OUT/path,dpi=180,bbox_inches="tight",facecolor="white")
    plt.close(fig)
m=pd.read_csv(D/"ebay_monthly_IQR_from_private_aggregates.csv")
allm=pd.read_csv(D/"ebay_monthly_aggregated_USD.csv")
assert list(m.month)==["2026-08","2026-09","2026-10","2026-11"]
assert m.n.sum()==1347 and allm["count"].sum()==2380
delta=100*(m.iloc[-1].median_usd/m.iloc[0].median_usd-1)
assert round(delta,1)==43.5

# HERO: four bars, from a zero baseline. No GTA causation claim.
fig=plt.figure(figsize=(13.3,7.5))
fig.text(.074,.922,"USED XBOX SERIES S · GERMANY",fontsize=12,color=TEAL,weight="bold")
fig.text(.073,.865,"Prices in the filtered eBay sample",fontsize=25,color=NAVY,weight="bold")
fig.text(.073,.815,"Typical reported SOLD price (median) · 512 GB · USD, excluding shipping",
         fontsize=12,color=MUTED)
fig.text(.895,.874,f"+{delta:.1f}%",ha="right",fontsize=40,color=TEAL,weight="bold")
fig.text(.895,.822,"August → Nov 1–18",ha="right",fontsize=11,color=MUTED)
ax=fig.add_axes([.078,.24,.86,.505])
x=np.arange(4)
ax.bar(x,m.median_usd,width=.64,color=[PALE,PALE,PALE,TEAL])
for i,r in enumerate(m.itertuples()):
    ax.text(i,r.median_usd+9,f"\u0024{r.median_usd:,.0f}",ha="center",
            fontsize=20,weight="bold",color=TEAL if i==3 else NAVY)
ax.set_xlim(-.65,3.65);ax.set_ylim(0,385)
ax.set_xticks(x,[f"{label}\nn={r.n}" for label,r in zip(
    ["AUG","SEP","OCT","NOV 1–18"],m.itertuples())],fontweight="bold",color=NAVY,fontsize=12)
ax.set_yticks([0,100,200,300],["$0","$100","$200","$300"])
ax.tick_params(axis="both",length=0,pad=8,labelcolor=MUTED)
ax.grid(axis="y",alpha=.12,color=NAVY);ax.set_axisbelow(True)
fig.text(.074,.14,"CONTEXT",fontweight="bold",color=GOLD,fontsize=10)
fig.text(.153,.14,"Retail rose 1 Aug (€349.99 → €499.99). August is already post-increase; Jan–Apr used median: $193.",
         color=NAVY,fontsize=10)
fig.text(.074,.095,"Observed sample change, not proof of a GTA VI effect. Nov is partial; classification not fully validated.",
         fontsize=10,color=MUTED)
save(fig,"hero_LinkedIn_USD.png")

# FULL YEAR: Jan–May, explicit June/July missing, Aug–Nov. Partial months flagged.
series=allm.set_index("month")
months=pd.period_range("2026-01","2026-11",freq="M")
fig,ax=plt.subplots(figsize=(13.3,7.15))
fig.text(.075,.937,"THE LONGER BASELINE",fontsize=12,weight="bold",color=TEAL)
fig.text(.075,.876,"Observed monthly sold prices throughout 2026",fontsize=20,weight="bold",color=NAVY)
fig.text(.075,.824,"Monthly medians from selected eBay sale records (USD)",fontsize=11,color=MUTED)
for i,p in enumerate(months):
    key=str(p)
    if key not in series.index:
        ax.bar(i,370,width=.7,color="none",edgecolor="#abb5bd",hatch="//",alpha=.6,linewidth=.8)
        ax.text(i,173,"NO\nDATA",ha="center",va="center",fontsize=10,color=MUTED,weight="bold")
    else:
        val=float(series.loc[key,"median"])
        ax.bar(i,val,width=.7,color=TEAL if i>=7 else PALE,alpha=1 if i>=7 else .78)
        ax.text(i,val+9,f"\u0024{val:,.0f}",ha="center",fontsize=11,color=NAVY,weight="bold")
labels=[p.strftime("%b").upper()+("*" if str(p) in ("2026-05","2026-11") else "")+
        ("\nn="+str(int(series.loc[str(p),"count"])) if str(p) in series.index else "")
        for p in months]
ax.set_xlim(-.65,len(months)-.35);ax.set_ylim(0,405)
ax.set_xticks(range(len(months)),labels,fontsize=10,fontweight="bold",color=NAVY)
ax.set_yticks([0,100,200,300],["$0","$100","$200","$300"])
ax.grid(axis="y",alpha=.12);ax.set_axisbelow(True)
ax.tick_params(length=0,pad=8,labelcolor=MUTED)
fig.subplots_adjust(left=.08,right=.975,top=.76,bottom=.20)
fig.text(.08,.11,"January–April pooled median $193.47 (947 records); summer coverage missing, not zero sales. *Partial month.",
         fontsize=10,color=NAVY)
fig.text(.08,.074,"Retail price change took effect 1 August. August sample is already post-change.",
         fontsize=10,color=MUTED)
save(fig,"full_year_context_USD.png")

# EUR SUPPLEMENT: distinct sold vs asking measures, holes on missing dates.
fx=pd.read_csv(D/"ebay_daily_estimated_EUR.csv",parse_dates=["date"])
kl=pd.read_csv(D/"kleinanzeigen_daily_aggregated_EUR.csv",parse_dates=["date"])
assert fx.ebay_n.sum()==1347 and kl["count"].sum()==285
col="estimated_median_eur" if "estimated_median_eur" in fx else "ebay_median_eur_est"
cal=pd.DataFrame({"date":pd.date_range("2026-10-26","2026-11-18")})
cal=cal.merge(fx[["date",col]].rename(columns={col:"ebay_eur"}),how="left",on="date")
cal=cal.merge(kl[["date","median","count"]].rename(
    columns={"median":"klein_eur","count":"klein_n"}),how="left",on="date")
assert cal.klein_eur.notna().sum()==20
fig,axes=plt.subplots(2,1,figsize=(12.5,7.8),sharex=True,sharey=True)
fig.text(.082,.949,"SUPPLEMENTARY · EUR COMPARISON",fontsize=11,color=TEAL,weight="bold")
fig.text(.082,.905,"Same currency. Different price measures.",fontsize=22,color=NAVY,weight="bold")
fig.text(.082,.862,"These are not matched consoles or equivalent transactions.",fontsize=10.5,color=MUTED)
for ax,c,color,label in [
 (axes[0],"ebay_eur",TEAL,"eBay · SOLD prices · estimated EUR"),
 (axes[1],"klein_eur",GOLD,"Kleinanzeigen · ASKING prices · original EUR")]:
    ax.plot(cal.date,cal[c],marker="o",ms=4,lw=2.3,color=color)
    ax.set_title(label,loc="left",fontsize=11,pad=11,color=color,fontweight="bold")
    ax.grid(axis="y",alpha=.14);ax.set_axisbelow(True);ax.set_ylabel("EUR")
for d in cal.loc[cal.klein_eur.isna(),"date"]:
    axes[1].axvspan(d-pd.Timedelta(hours=12),d+pd.Timedelta(hours=12),
                    color="#dce1e5",alpha=.7,lw=0)
low=cal.loc[cal.date==pd.Timestamp("2026-10-26")].iloc[0]
axes[1].annotate("n=5 (small sample)",xy=(low.date,low.klein_eur),xytext=(15,25),
                 textcoords="offset points",fontsize=8.5,color=MUTED,
                 arrowprops={"arrowstyle":"-","color":MUTED})
values=pd.concat([cal.ebay_eur,cal.klein_eur]).dropna()
axes[1].set_ylim(max(0,np.floor(values.min()/20)*20-20),np.ceil(values.max()/20)*20+20)
axes[1].set_xlim(pd.Timestamp("2026-10-25"),pd.Timestamp("2026-11-19"))
axes[1].xaxis.set_major_locator(mdates.DayLocator(interval=4))
axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
fig.subplots_adjust(left=.085,right=.97,top=.78,bottom=.17,hspace=.36)
fig.text(.085,.096,"Grey stripes = missing Kleinanzeigen collection days (not zero listings). Small daily samples are noisy.",
         fontsize=9.5,color=MUTED)
fig.text(.085,.065,"eBay USD prices converted by date using ECB reference rates; original EUR sale prices unverified.",
         fontsize=9.5,color=MUTED)
save(fig,"final_ebay_vs_klein_EUR_comparison.png")
print("Generated public hero, full-year context, and corrected EUR supplement.")
