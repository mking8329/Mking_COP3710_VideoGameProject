# 1) Must be in the same file as the CSVs
# 2) Replace the address in BASE with the folder path
# 3) Run 'py "[ADDRESS OF PROGRAM]"' in terminal.
# 4) Should see "Cleaned CSV files written to [location]". Generates a file containing the cleaned CSVs

import pandas as pd
import re
from pathlib import Path

BASE = Path(r'C:\Users\mtkg8\OneDrive\Desktop\Database Project\PartDSubby\data') #Change to folder path
OUT = BASE / 'oracle_etl_v2' / 'cleaned'
OUT.mkdir(parents=True, exist_ok=True)


def parse_month_year(value: str):
    if pd.isna(value):
        return None
    s = str(value).strip()
    if not s:
        return None
    # Examples: Aug-12, Dec-17
    try:
        dt = pd.to_datetime('01-' + s, format='%d-%b-%y', errors='raise')
        return dt.strftime('%Y-%m-%d')
    except Exception:
        pass
    # Examples: 2007-10, 2013-09
    m = re.fullmatch(r'(\d{4})-(\d{2})', s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-01"
    # Fallbacks
    dt = pd.to_datetime(s, errors='coerce')
    if pd.isna(dt):
        return None
    return dt.strftime('%Y-%m-%d')


def parse_date(value: str):
    if pd.isna(value):
        return None
    s = str(value).strip()
    if not s:
        return None
    for fmt in ('%d-%b-%y', '%m/%d/%Y', '%Y-%m-%d'):
        try:
            return pd.to_datetime(s, format=fmt).strftime('%Y-%m-%d')
        except Exception:
            pass
    dt = pd.to_datetime(s, errors='coerce')
    if pd.isna(dt):
        return None
    return dt.strftime('%Y-%m-%d')


def parse_bool_01(value):
    s = str(value).strip().lower()
    return 1 if s in {'1', 'y', 'yes', 'true'} else 0


def parse_int(value):
    if pd.isna(value):
        return None
    s = re.sub(r'[^0-9-]', '', str(value))
    return int(s) if s not in {'', '-'} else None


def parse_money_floor(value):
    """Converts strings like $13B+ to a numeric lower bound.
    Examples: $500M+ -> 500000000, $1B?2B -> 1000000000.
    """
    if pd.isna(value):
        return None
    s = str(value).strip().upper().replace(',', '')
    m = re.search(r'(\d+(?:\.\d+)?)\s*([BM])', s)
    if not m:
        return None
    num = float(m.group(1))
    unit = m.group(2)
    mult = 1_000_000_000 if unit == 'B' else 1_000_000
    return round(num * mult, 2)


# Franchise
fr = pd.read_csv(BASE / 'franchise.csv')
fr = fr[['FranchiseID', 'FranchiseName', 'Publisher', 'StartYear', 'WebsiteURL']].copy()
fr['FranchiseID'] = fr['FranchiseID'].astype(int)
fr['StartYear'] = fr['StartYear'].astype(int)
fr.to_csv(OUT / 'franchise_clean.csv', index=False)

# Platform
pl = pd.read_csv(BASE / 'platform.csv')
pl = pl.rename(columns={'PlatformID.1': 'PlatformName'})
pl = pl[['PlatformID', 'PlatformName', 'Manufacturer', 'ReleaseYear']].copy()
pl = pl.dropna(subset=['PlatformID', 'PlatformName'])
pl['PlatformID'] = pl['PlatformID'].astype(int)
pl['PlatformName'] = pl['PlatformName'].astype(str).str.strip()
pl['Manufacturer'] = pl['Manufacturer'].fillna('Unknown').astype(str).str.strip()
pl['ReleaseYear'] = pl['ReleaseYear'].apply(parse_int)
# Schema requires NOT NULL and check >= 1970. Use minimum allowed placeholder for unknown years.
pl['ReleaseYear'] = pl['ReleaseYear'].fillna(1970).astype(int)
pl.loc[pl['ReleaseYear'] < 1970, 'ReleaseYear'] = 1970
pl.to_csv(OUT / 'platform_clean.csv', index=False)

# Region
rg = pd.read_csv(BASE / 'region.csv')
rg = rg[['RegionID', 'RegionName', 'Currency']].copy()
rg['RegionID'] = rg['RegionID'].astype(int)
rg.to_csv(OUT / 'region_clean.csv', index=False)

# Game
gm = pd.read_csv(BASE / 'games.csv')
gm = gm[['GameID', 'Title', 'ReleaseDate', 'Genre', 'ESRBRating', 'FranchiseID']].copy()
gm['GameID'] = gm['GameID'].astype(int)
gm['FranchiseID'] = gm['FranchiseID'].astype(int)
gm['ReleaseDate'] = gm['ReleaseDate'].apply(parse_month_year)
gm = gm.dropna(subset=['ReleaseDate'])
gm.to_csv(OUT / 'game_clean.csv', index=False)

# GamePlatform
gp = pd.read_csv(BASE / 'gameplatform.csv')
gp = gp[[c for c in gp.columns if not c.startswith('Unnamed')]].copy()
gp = gp[['GameID', 'PlatformID', 'ReleaseDateOnPlatform', 'PlatformExclusive']]
gp['GameID'] = gp['GameID'].astype(int)
gp['PlatformID'] = gp['PlatformID'].astype(int)
gp['ReleaseDateOnPlatform'] = gp['ReleaseDateOnPlatform'].apply(parse_date)
gp['PlatformExclusive'] = gp['PlatformExclusive'].apply(parse_bool_01)
gp = gp.dropna(subset=['ReleaseDateOnPlatform'])
gp.to_csv(OUT / 'gameplatform_clean.csv', index=False)

# QuarterlySales
qs = pd.read_csv(BASE / 'quarterlysales.csv')
qs = qs[['GameID', 'RegionID', 'Year', 'Quarter', 'UnitsSold', 'Revenue']].copy()
qs = qs.rename(columns={'Year': 'SalesYear'})
qs['GameID'] = qs['GameID'].astype(int)
qs['RegionID'] = qs['RegionID'].astype(int)
qs['SalesYear'] = qs['SalesYear'].astype(int)
qs['QuarterNum'] = qs['Quarter'].astype(str).str.extract(r'(\d)').astype(int)
qs['UnitsSold'] = qs['UnitsSold'].apply(parse_int).astype(int)
qs['Revenue'] = qs['Revenue'].astype(str).str.replace(r'[$,]', '', regex=True).astype(float)
qs = qs[['GameID', 'RegionID', 'SalesYear', 'QuarterNum', 'UnitsSold', 'Revenue']]
qs.to_csv(OUT / 'quarterlysales_clean.csv', index=False)

# FranchisePerformanceRank
fpr = pd.read_csv(BASE / 'franchiseperformancerank.csv')
fpr = fpr[['FranchiseID', 'GlobalRank', 'TotalRevenue', 'LastUpdatedDate']].copy()
fpr['FranchiseID'] = fpr['FranchiseID'].astype(int)
fpr['GlobalRank'] = fpr['GlobalRank'].astype(str).str.extract(r'(\d+)').astype(int)
fpr['TotalRevenue'] = fpr['TotalRevenue'].apply(parse_money_floor)
fpr['LastUpdatedDate'] = fpr['LastUpdatedDate'].apply(parse_date)
fpr = fpr.dropna(subset=['TotalRevenue', 'LastUpdatedDate'])
fpr.to_csv(OUT / 'franchiseperformancerank_clean.csv', index=False)

print(f'Cleaned CSV files written to {OUT}')
