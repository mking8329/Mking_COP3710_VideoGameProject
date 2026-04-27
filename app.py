import oracledb

# --- DATABASE SETUP ---
oracledb.init_oracle_client(
    lib_dir=r"C:\Users\mtkg8\OneDrive\Desktop\instantclient_23_0"
)

DB_USER = "system"
DB_PASSWORD = "123abc"
DB_DSN = "localhost:1521/xe"


def get_connection():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )


def run_query(sql, params=None):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(sql, params or [])
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")


def main():
    while True:
        print("\nVideo Game Sales & Market Analytics Database")
        print("1. Game titles with an ESRB rating")
        print("2. Franchise names with a global ranking")
        print("3. Game titles and franchise start years before a certain year")
        print("4. Franchise names with a certain number of game titles")
        print("5. Franchise website URLs with games of a certain ESRB rating")
        print("0. Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            rating = input("Enter ESRB rating (M, T, E, E10+, NonRated, Not Rated): ")

            sql = """
                SELECT g.Title
                FROM Game g
                WHERE g.ESRBRating = :1
            """

            run_query(sql, [rating])

        elif choice == "2":
            rank = int(input("Enter global ranking: "))

            sql = """
                SELECT f.FranchiseName
                FROM Franchise f
                JOIN FranchisePerformanceRank p
                    ON f.FranchiseId = p.FranchiseId
                WHERE p.GlobalRank = :1
            """

            run_query(sql, [rank])

        elif choice == "3":
            year = int(input("Enter year: "))

            sql = """
                SELECT g.Title, f.StartYear
                FROM Franchise f
                JOIN Game g
                    ON f.FranchiseId = g.FranchiseId
                WHERE f.StartYear < :1
                ORDER BY f.StartYear
            """

            run_query(sql, [year])

        elif choice == "4":
            num_games = int(input("Enter number of games: "))

            sql = """
                SELECT f.FranchiseName
                FROM Franchise f
                JOIN Game g
                    ON f.FranchiseId = g.FranchiseId
                GROUP BY f.FranchiseName
                HAVING COUNT(*) = :1
            """

            run_query(sql, [num_games])

        elif choice == "5":
            rating = input("Enter ESRB rating (M, T, E, E10+, NonRated, Not Rated): ")

            sql = """
                SELECT DISTINCT f.WebsiteURL
                FROM Franchise f
                JOIN Game g
                    ON f.FranchiseId = g.FranchiseId
                WHERE g.ESRBRating = :1
            """

            run_query(sql, [rating])

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()