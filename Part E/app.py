
import streamlit as st
import oracledb


# --- DATABASE SETUP ---
LIB_DIR = r"C:\Users\j5r24\Downloads\instantclient-basic-windows.x64-11.2.0.4.0\instantclient_11_2"
DB_USER = "RWATERMAN0451_SCHEMA_N0KUW"
DB_PASS = "2CSA8#YK62NSRgZHS6SDRFBN5TMLYI"
DB_DSN = "db.freesql.com:1521/23ai_34ui2"


# Initialize Oracle Client for Thick Mode
@st.cache_resource
def init_db():
    if LIB_DIR:
        try:
            oracledb.init_oracle_client(lib_dir=LIB_DIR)
        except Exception as e:
            st.error(f"Error initializing Oracle Client: {e}")


init_db()


def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)


# --- STREAMLIT UI ---
st.title("Video Game Sales & Market Analytics Database")

menu = ["Game titles with an ESRB rating", "Franchise names with a global ranking", "Game titles and the start year of each franchise before a certain year", "Franchise names with a certain number of game titles", "Franchise website URLs with any games with a certain ESRB rating"]
choice = st.sidebar.selectbox("Select Feature", menu)


# if choice == "Game titles with an ESRB rating":
#     st.write("### Enter a certain ESRB rating to see all the game titles with that rating.\n\nOPTIONS: 'M', 'T', 'E', 'E10+', 'NonRated', 'Not Rated'")
#     ESRBRating = st.text_input("ESRB Rating")

# 1
if choice == "Game titles with an ESRB rating":
    st.write("### Enter a certain ESRB rating to see all the game titles with that rating.")
    menu1 = ["M", "T", "E", "E10+", "NonRated", "Not Rated"]
    ESRBRating = st.selectbox("Select ESRB Rating", menu1)

    if st.button("Get Game Titles"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT g.Title FROM Game g WHERE g.ESRBRating = (:1)", [ESRBRating])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()
            if data:
                st.table(data)
            else:
                st.info("No records found.")
        except Exception as e:
            st.error(f"Error: {e}")

        #     st.success(f"Successfully showed {ESRBRating}!")
        # except Exception as e:
        #     st.error(f"Error: {e}")



# 2
if choice == "Franchise names with a global ranking":
    st.write("### Enter a certain global ranking to see all the franchise names with that ranking.")
    menu2 = ["5", "10", "15", "20", "25", "30", "50", "100"]
    GlobalRank = st.selectbox("Select Global Ranking", menu2)

    if st.button("Get Franchise Names"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT f.FranchiseName FROM Franchise f JOIN FranchisePerformanceRank p ON f.FranchiseId = p.FranchiseId WHERE p.GlobalRank = (:1)", [GlobalRank])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()
            if data:
                st.table(data)
            else:
                st.info("No records found.")
        except Exception as e:
            st.error(f"Error: {e}")



# 3
if choice == "Game titles and the start year of each franchise before a certain year":
    st.write("### Enter a certain year to see the game titles and start year of each franchise that began before that year. They are sorted from oldest to newest.")
    menu3 = ["1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    StartYear = st.selectbox("Select Year", menu3)

    if st.button("Get Game Titles & Start Year"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT g.Title as Title, f.StartYear as StartYear FROM Franchise f JOIN Game g ON f.FranchiseId = g.FranchiseId WHERE f.StartYear < (:1) ORDER BY f.StartYear", [StartYear])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()
            if data:
                st.table(data)
            else:
                st.info("No records found.")
        except Exception as e:
            st.error(f"Error: {e}")



# 4
if choice == "Franchise names with a certain number of game titles":
    st.write("### Enter a certain number to see the franchise names with that number of games.")
    menu4 = ["1", "2", "3"]
    NumberOfGamesInAFranchise = st.selectbox("Select Number", menu4)

    if st.button("Get Franchise Names"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT f.FranchiseName FROM Franchise f JOIN Game g ON f.FranchiseId = g.FranchiseId GROUP BY f.FranchiseName HAVING COUNT(*) = (:1)", [NumberOfGamesInAFranchise])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()
            if data:
                st.table(data)
            else:
                st.info("No records found.")
        except Exception as e:
            st.error(f"Error: {e}")



# 5
if choice == "Franchise website URLs with any games with a certain ESRB rating":
    st.write("### Enter a certain ESRB rating to see the website URLs of the franchises with any games with that rating.")
    menu5 = ["M", "T", "E", "E10+", "NonRated", "Not Rated"]
    ESRBRating = st.selectbox("Select ESRB Rating", menu5)

    if st.button("Get Website URLs"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT f.WebsiteURL FROM Franchise f JOIN Game g ON f.FranchiseId = g.FranchiseId WHERE g.ESRBRating = (:1)", [ESRBRating])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()
            if data:
                st.table(data)
            else:
                st.info("No records found.")
        except Exception as e:
            st.error(f"Error: {e}")
