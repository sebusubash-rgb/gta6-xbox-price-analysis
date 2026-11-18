#!/usr/bin/env python3
"""Plot the public, aggregated 2026 Series S market-price snapshots.

No network requests, API keys, raw listings, or seller-level data are required.
The monthly medians come from the original filtered record-level samples; they
cannot in general be reconstructed by taking medians of daily medians.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data'
FIGURES = BASE / 'figures'


def daily_frame(filename: str, start: str, end: str) -> pd.DataFrame:
    data = pd.read_csv(DATA / filename)
    if not {'date', 'count', 'median'}.issubset(data.columns):
        raise ValueError(f'Missing required columns in {filename}')
    data['date'] = pd.to_datetime(data['date'], errors='raise')
    if data['date'].duplicated().any():
        raise ValueError(f'Duplicate daily dates in {filename}')
    if (data['count'] <= 0).any():
        raise ValueError(f'Invalid observed day count in {filename}')
    data = data.set_index('date').sort_index().reindex(pd.date_range(start, end, freq='D'))
    data.index.name = 'date'
    return data


def daily_plot(data: pd.DataFrame, output: Path, title: str, ylabel: str,
               rolling_min: int, events: bool=False) -> None:
    # Reindexing creates NaN for every date without observed data. Line graphs
    # break on those NaNs; we never fabricate values using fill/interpolation.
    rolling = data['median'].rolling(window=7, min_periods=rolling_min).median()
    rolling = rolling.where(data['median'].notna())
    fig, ax = plt.subplots(figsize=(12.8, 5.9), dpi=145)
    ax.plot(data.index, data['median'], color='#186D9E', marker='o',
            markersize=3, linewidth=1.55, label='Daily median (observed only)')
    ax.plot(data.index, rolling, color='#D47D23', linewidth=2.6,
            label=f'7-day rolling median (≥{rolling_min} observed days)')
    if events:
        ax.axvline(pd.Timestamp('2026-08-01'), color='#696969', linewidth=1.25,
                   linestyle='--', label='Xbox new-console price increase (1 Aug)')
        ax.axvline(pd.Timestamp('2026-11-19'), color='#7D4A91', linewidth=1.25,
                   linestyle=':', label='GTA VI scheduled launch (19 Nov)')
    ax.set_title(title, fontsize=14, pad=14)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('UTC date')
    ax.grid(alpha=0.21)
    ax.spines[['top','right']].set_visible(False)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1) if events
                               else mdates.WeekdayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y' if events else '%d %b'))
    fig.autofmt_xdate(rotation=25)
    ax.legend(loc='best', fontsize=9)
    fig.tight_layout()
    fig.savefig(output, bbox_inches='tight')
    plt.close(fig)


def monthly_plot(filename: str, output: Path) -> None:
    data = pd.read_csv(DATA / filename)
    dates = pd.to_datetime(data['month'] + '-01')
    fig, ax = plt.subplots(figsize=(10.6, 5.25), dpi=145)
    ax.scatter(dates, data['median'], s=75, color='#186D9E', zorder=3)
    # Draw separate contiguous monthly blocks, not a misleading May-to-Aug line.
    ordered = data.assign(dt=dates).sort_values('dt')
    blocks = (ordered['dt'].diff().dt.days.fillna(31) > 35).cumsum()
    for _, block in ordered.groupby(blocks):
        if len(block)>1: ax.plot(block['dt'],block['median'],color='#186D9E',alpha=.75)
    for date, med, n in zip(dates, data['median'], data['count']):
        ax.annotate(f'n={n}',(date,med),xytext=(0,9),textcoords='offset points',
                    ha='center',fontsize=8,color='#404040')
    ax.axvline(pd.Timestamp('2026-08-01'),color='#696969',linestyle='--',alpha=.9,
               label='New Xbox price increase')
    ax.set_title('eBay Germany: median filtered sold price by observed month',fontsize=13,pad=12)
    ax.set_ylabel('USD, listed sold price (shipping excluded)')
    ax.set_xlabel('Missing June–July: no observations, no imputation')
    ax.set_xlim(pd.Timestamp('2025-12-15'),pd.Timestamp('2026-12-02'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.grid(alpha=.2)
    ax.spines[['top','right']].set_visible(False)
    ax.legend(loc='upper left',fontsize=9)
    fig.tight_layout()
    fig.savefig(output,bbox_inches='tight')
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only',action='store_true',help='Validate data, create no charts')
    args = parser.parse_args()
    ebay = daily_frame('ebay_daily_aggregated_USD.csv','2026-01-01','2026-11-19')
    klein = daily_frame('kleinanzeigen_daily_aggregated_EUR.csv','2026-10-21','2026-11-19')
    ebay_month = pd.read_csv(DATA/'ebay_monthly_aggregated_USD.csv')
    klein_month = pd.read_csv(DATA/'kleinanzeigen_monthly_aggregated_EUR.csv')
    assert int(ebay['count'].sum()) == 2380
    assert int(klein['count'].sum()) == 285
    assert len(ebay_month)==9 and len(klein_month)==2
    assert int(ebay_month['count'].sum()) == 2380
    assert int(klein_month['count'].sum()) == 285
    assert ebay['median'].notna().sum() == 242
    assert klein['median'].notna().sum() == 20
    assert ebay.loc['2026-05-15':'2026-07-31','median'].isna().all()
    assert klein.loc[['2026-11-04','2026-11-05','2026-11-10','2026-11-11'],'median'].isna().all()
    print('Validation passed: eBay 2,380 filtered records / 242 observed days; '
          'Kleinanzeigen 285 filtered observations / 20 observed days.')
    if args.check_only:
        return
    FIGURES.mkdir(parents=True,exist_ok=True)
    daily_plot(ebay,FIGURES/'ebay_daily_gap_safe.png',
               'Xbox Series S 512 GB — filtered eBay sold-price observations',
               'USD (sold price; no shipping)',rolling_min=4,events=True)
    daily_plot(klein,FIGURES/'kleinanzeigen_daily_gap_safe.png',
               'Xbox Series S 512 GB — filtered Kleinanzeigen asking-price observations',
               'EUR (asking price; not sold price)',rolling_min=3)
    monthly_plot('ebay_monthly_aggregated_USD.csv',FIGURES/'ebay_monthly_medians.png')
    print('Saved 3 figures in:',FIGURES)

if __name__=='__main__':
    main()
