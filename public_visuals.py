#!/usr/bin/env python3
"""Public-facing figures from aggregate CSVs only (no private sales, no network)."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BASE=Path(__file__).resolve().parent
DATA=BASE/'data'
OUT=BASE/'figures'
OUT.mkdir(exist_ok=True)
BLUE='#17648b'; ORANGE='#d16a1e'; GREY='#56687a'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
                     'axes.spines.top':False,'axes.spines.right':False,
                     'axes.titleweight':'bold'})
def save(fig,name):
    fig.savefig(OUT/name,dpi=175,bbox_inches='tight',facecolor='white')
    plt.close(fig)

monthly=pd.read_csv(DATA/'ebay_monthly_IQR_from_private_aggregates.csv')
assert monthly.n.sum()==1347
fig,ax=plt.subplots(figsize=(11,6))
x=range(4)
ax.vlines(x,monthly.p25_usd,monthly.p75_usd,linewidth=22,alpha=.22,
          color=BLUE,label='Middle half of prices')
ax.plot(x,monthly.median_usd,'o-',lw=3,ms=10,color=BLUE,label='Typical price (median)')
for i,r in monthly.iterrows():
    ax.annotate(f'USD {r.median_usd:,.0f}',(i,r.median_usd),xytext=(0,12),
                textcoords='offset points',ha='center',weight='bold',fontsize=15)
    ax.annotate(f'{int(r.n)} records',(i,r.p25_usd),xytext=(0,-14),
                textcoords='offset points',ha='center',color=GREY,fontsize=9)
ax.set_xticks(list(x),['AUG','SEP','OCT','NOV 1–18'])
ax.set_xlim(-.4,3.4);ax.set_ylim(120,405)
ax.set_ylabel('eBay sold-price sample · USD (shipping excluded)')
ax.set_title('Used Xbox Series S 512 GB: prices in the months before GTA VI',loc='left',pad=20)
ax.text(0,1.01,'August to 1–18 November: +43.5% in reported median sold price',
        transform=ax.transAxes,color=GREY)
ax.legend(loc='upper left',frameon=False);ax.grid(axis='y',alpha=.2)
fig.text(.11,.012,'Sample classification not fully validated. GTA VI scheduled release: 19 Nov 2026. Association is not causation.',
         fontsize=9,color=GREY)
fig.subplots_adjust(left=.11,right=.98,top=.82,bottom=.18)
save(fig,'final_main_USD_monthly_IQR.png')

usd=pd.read_csv(DATA/'ebay_daily_aggregated_USD.csv',parse_dates=['date'])
assert usd['count'].sum()==2380
daily=pd.DataFrame({'date':pd.date_range('2026-08-01','2026-11-18')})
daily=daily.merge(usd[['date','median','count']],how='left',on='date',validate='one_to_one')
assert daily['median'].notna().sum()==110
daily['rolling']=daily['median'].rolling(7,min_periods=4).median()
fig,ax=plt.subplots(figsize=(12,6.4))
ax.scatter(daily.date,daily['median'],s=14,color=BLUE,alpha=.38,label='Observed daily middle price')
ax.plot(daily.date,daily['rolling'],lw=3,color=BLUE,label='7-day median of daily medians')
launch=pd.Timestamp('2026-11-19')
ax.axvline(launch,linestyle='--',color=ORANGE,lw=2)
ax.annotate('Scheduled GTA VI release\n19 Nov 2026',xy=(launch,200),
            xytext=(-10,0),textcoords='offset points',ha='right',color=ORANGE)
ax.set_xlim(pd.Timestamp('2026-07-30'),pd.Timestamp('2026-11-23'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.set_title('eBay Germany: observed sold-price trend, August–November 2026',loc='left',pad=20)
ax.set_ylabel('Reported sold prices · USD')
ax.grid(axis='y',alpha=.2);ax.legend(loc='upper left',frameon=False)
fig.text(.11,.02,'Data through 18 Nov only. The release date is contextual, not a tested cause. Filter is exploratory.',
         color=GREY,fontsize=9)
fig.subplots_adjust(left=.11,right=.98,top=.90,bottom=.16)
save(fig,'final_eBay_USD_prelaunch_trend.png')

fx=pd.read_csv(DATA/'ebay_daily_estimated_EUR.csv',parse_dates=['date'])
klein=pd.read_csv(DATA/'kleinanzeigen_daily_aggregated_EUR.csv',parse_dates=['date'])
assert fx['ebay_n'].sum()==1347 and klein['count'].sum()==285
col='estimated_median_eur' if 'estimated_median_eur' in fx.columns else 'ebay_median_eur_est'
shared=pd.DataFrame({'date':pd.date_range('2026-10-21','2026-11-18')})
shared=shared.merge(fx[['date',col]].rename(columns={col:'eBay_EUR'}),how='left',on='date')
shared=shared.merge(klein[['date','median']].rename(columns={'median':'Klein_EUR'}),how='left',on='date')
assert shared['Klein_EUR'].notna().sum()==20
fig,axes=plt.subplots(2,1,figsize=(12,7.5),sharex=True,sharey=True)
for ax,column,color,title in [
    (axes[0],'eBay_EUR',BLUE,'eBay — reported SOLD prices, estimated EUR'),
    (axes[1],'Klein_EUR',ORANGE,'Kleinanzeigen — advertised ASKING prices, EUR')]:
    ax.plot(shared.date,shared[column],marker='o',ms=3,lw=1.8,color=color)
    ax.set_title(title,loc='left',fontsize=12,pad=12,color=color)
    ax.grid(axis='y',alpha=.2);ax.set_ylabel('EUR')
axes[0].set_ylim(110,390)
axes[1].xaxis.set_major_locator(mdates.DayLocator(interval=4))
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
fig.suptitle('Two marketplaces, one currency — but different price measures',
             fontsize=16,weight='bold')
fig.text(.1,.012,'No missing-day filling. Separate samples; not matched transactions. eBay EUR amounts are exchange-rate estimates.',
         fontsize=9,color=GREY)
fig.subplots_adjust(left=.1,right=.98,top=.88,bottom=.1,hspace=.35)
save(fig,'final_ebay_vs_klein_EUR_comparison.png')
print('Checks passed: eBay 2,380 (USD), 1,347 (Aug–Nov EUR), Kleinanzeigen 285.')
