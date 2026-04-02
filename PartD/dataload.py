import pandas as pd
import oracledb
from pathlib import Path

oracledb.init_oracle_client(lib_dir=r"C:\Users\mtkg8\OneDrive\Desktop\instantclient_23_0")

# Address of the cleaned CSV folder
BASE = Path(r'C:\Users\mtkg8\OneDrive\Desktop\Database Project\oracle_etl_v2\cleaned')

DB_USER = 'system'
DB_PASSWORD = '123abc'
DB_DSN = oracledb.makedsn("localhost", 1521, sid="xe")


def load_csv(name):
    return pd.read_csv(BASE / name)


def insert_dataframe(cursor, sql, df):
    data = [tuple(row) for row in df.itertuples(index=False, name=None)]
    cursor.executemany(sql, data)


def main():
    conn = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )
    cursor = conn.cursor()

    print("Connected successfully")

    cursor.execute("SELECT USER FROM dual")
    print("USER:", cursor.fetchone()[0])

    cursor.execute("""
        SELECT table_name
        FROM user_tables
        WHERE table_name IN (
            'FRANCHISE',
            'PLATFORM',
            'REGION',
            'GAME',
            'GAMEPLATFORM',
            'QUARTERLYSALES',
            'FRANCHISEPERFORMANCERANK'
        )
        ORDER BY table_name
    """)
    print("TABLES:", cursor.fetchall())

    try:
        franchise = load_csv('franchise_clean.csv')
        platform = load_csv('platform_clean.csv')
        region = load_csv('region_clean.csv')
        game = load_csv('game_clean.csv')
        gameplatform = load_csv('gameplatform_clean.csv')
        quarterlysales = load_csv('quarterlysales_clean.csv')
        fpr = load_csv('franchiseperformancerank_clean.csv')

        print("Loading FRANCHISE...")
        insert_dataframe(cursor, """
            INSERT INTO Franchise
            (FranchiseID, FranchiseName, Publisher, StartYear, WebsiteURL)
            VALUES (:1, :2, :3, :4, :5)
        """, franchise)

        print("Loading PLATFORM...")
        insert_dataframe(cursor, """
            INSERT INTO Platform
            (PlatformID, PlatformName, Manufacturer, ReleaseYear)
            VALUES (:1, :2, :3, :4)
        """, platform)

        print("Loading REGION...")
        insert_dataframe(cursor, """
            INSERT INTO Region
            (RegionID, RegionName, Currency)
            VALUES (:1, :2, :3)
        """, region)

        print("Loading GAME...")
        game_rows = []
        for row in game.itertuples(index=False):
            game_rows.append((
                row.GameID,
                row.Title,
                row.ReleaseDate,
                row.Genre,
                row.ESRBRating,
                row.FranchiseID
            ))
        cursor.executemany("""
            INSERT INTO Game
            (GameID, Title, ReleaseDate, Genre, ESRBRating, FranchiseID)
            VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5, :6)
        """, game_rows)

        print("Loading GAMEPLATFORM...")
        gp_rows = []
        for row in gameplatform.itertuples(index=False):
            gp_rows.append((
                row.GameID,
                row.PlatformID,
                row.ReleaseDateOnPlatform,
                row.PlatformExclusive
            ))
        cursor.executemany("""
            INSERT INTO GamePlatform
            (GameID, PlatformID, ReleaseDateOnPlatform, PlatformExclusive)
            VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4)
        """, gp_rows)

        print("Loading QUARTERLYSALES...")
        insert_dataframe(cursor, """
            INSERT INTO QuarterlySales
            (GameID, RegionID, SalesYear, QuarterNum, UnitsSold, Revenue)
            VALUES (:1, :2, :3, :4, :5, :6)
        """, quarterlysales)

        print("Loading FRANCHISEPERFORMANCERANK...")
        fpr_rows = []
        for row in fpr.itertuples(index=False):
            fpr_rows.append((
                row.FranchiseID,
                row.GlobalRank,
                row.TotalRevenue,
                row.LastUpdatedDate
            ))
        cursor.executemany("""
            INSERT INTO FranchisePerformanceRank
            (FranchiseID, GlobalRank, TotalRevenue, LastUpdatedDate)
            VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))
        """, fpr_rows)

        conn.commit()
        print("Database populated successfully.")

    except Exception as e:
        conn.rollback()
        print("Error loading data:")
        print(type(e).__name__)
        print(e)
        raise

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()
