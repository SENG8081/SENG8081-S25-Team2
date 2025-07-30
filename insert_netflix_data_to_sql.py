import pandas as pd
import pyodbc

# --------------------------
# STEP 1: Connect to SQL Server
# --------------------------
def connect_to_db():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-3T50FGA\\MSQL;'
            'DATABASE=Netflix_Movies_TV_Shows_2025;'
            'Trusted_Connection=yes;'
        )
        conn.autocommit = True
        print("Connected to SQL Server successfully.")
        return conn
    except pyodbc.Error as e:
        print("Database connection failed:", e)
        return None

# --------------------------
# STEP 2: Load cleaned Excel/CSV Files
# --------------------------
movies_cleaned = pd.read_excel(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\cleaned_netflix_movies_data.xlsx")
movies_detailed = pd.read_csv(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\netflix_movies_detailed_up_to_2025_clean[1].csv")
tv_cleaned = pd.read_excel(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\cleaned_netflix_tv_shows.xlsx")
tv_detailed = pd.read_csv(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\netflix_tv_shows_detailed_up_to_2025_clean[1].csv")

# --------------------------
# STEP 3: Clean Numeric Columns & Dates (optional, if needed)
# --------------------------
def clean_numeric(df, cols):
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

def clean_dates(df, cols):
    for col in cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

movies_detailed = clean_numeric(movies_detailed, ['popularity', 'vote_count', 'vote_average', 'budget', 'revenue', 'profit'])
movies_detailed = clean_dates(movies_detailed, ['date_added'])

tv_detailed = clean_numeric(tv_detailed, ['popularity', 'vote_count', 'vote_average', 'num_seasons'])
tv_detailed = clean_dates(tv_detailed, ['date_added'])

movies_cleaned = clean_dates(movies_cleaned, ['release_date'])
tv_cleaned = clean_dates(tv_cleaned, ['first_air_date'])

# --------------------------
# STEP 4: Insert Data into SQL Server
# --------------------------
def insert_all_data():
    conn = connect_to_db()
    if conn is None:
        print("No connection. Exiting.")
        return
    cursor = conn.cursor()

    # DELETE old data from all tables before inserting new
    cursor.execute("DELETE FROM Cleaned_Netflix_Movies_Data")
    cursor.execute("DELETE FROM Netflix_Movies_Detailed")
    cursor.execute("DELETE FROM Cleaned_Netflix_TV_Shows")
    cursor.execute("DELETE FROM Netflix_TV_Shows_Detailed")
    conn.commit()
    print("Old data deleted from all tables.")

    # Insert Cleaned Movies
    print("Inserting cleaned movies...")
    for _, row in movies_cleaned.iterrows():
        try:
            cursor.execute("""
                INSERT INTO Cleaned_Netflix_Movies_Data
                (id, title, original_language, release_date, popularity, vote_average, vote_count, overview)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            int(row['id']) if not pd.isna(row['id']) else None,
            row['title'],
            row['original_language'],
            row['release_date'].date() if pd.notna(row['release_date']) else None,
            float(row['popularity']),
            float(row['vote_average']),
            int(row['vote_count']),
            row['overview'])
        except Exception as e:
            print(f"Error inserting cleaned movie id {row['id']}: {e}")

    # Insert Detailed Movies
    print("Inserting detailed movies...")
    for _, row in movies_detailed.iterrows():
        try:
            cursor.execute("""
                INSERT INTO Netflix_Movies_Detailed
                (show_id, type, title, director, cast, country, date_added, release_year, rating,
                duration, genres, language, description, popularity, vote_count, vote_average,
                budget, revenue, profit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            int(row['show_id']) if pd.notna(row['show_id']) else None,
            str(row['type']),
            str(row['title']),
            str(row['director']),
            str(row['cast']),
            str(row['country']),
            row['date_added'].date() if pd.notna(row['date_added']) else None,
            int(row['release_year']) if pd.notna(row['release_year']) else None,
            str(row['rating']),
            str(row['duration']),
            str(row['genres']),
            str(row['language']),
            str(row['description']),
            round(float(row['popularity']), 4),
            int(row['vote_count']),
            round(float(row['vote_average']), 4),
            int(float(row['budget'])),
            int(float(row['revenue'])),
            int(float(row['profit'])))
        except Exception as e:
            print(f"Failed to insert movie show_id {row['show_id']}: {e}")

    # Insert Cleaned TV Shows
    print("Inserting cleaned TV shows...")
    for _, row in tv_cleaned.iterrows():
        try:
            cursor.execute("""
                INSERT INTO Cleaned_Netflix_TV_Shows
                (id, name, original_language, first_air_date, popularity, vote_average, vote_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            int(row['id']) if not pd.isna(row['id']) else None,
            row['name'],
            row['original_language'],
            row['first_air_date'].date() if pd.notna(row['first_air_date']) else None,
            float(row['popularity']),
            float(row['vote_average']),
            int(row['vote_count']))
        except Exception as e:
            print(f"Error inserting cleaned TV show id {row['id']}: {e}")

    # Insert Detailed TV Shows
    print("Inserting detailed TV shows...")
    for _, row in tv_detailed.iterrows():
        try:
            cursor.execute("""
                INSERT INTO Netflix_TV_Shows_Detailed
                (show_id, type, title, director, cast, country, date_added, release_year, rating,
                 duration, genres, language, description, popularity, vote_count, vote_average,
                 num_seasons)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            int(row['show_id']) if pd.notna(row['show_id']) else None,
            str(row['type']),
            str(row['title']),
            str(row['director']),
            str(row['cast']),
            str(row['country']),
            row['date_added'].date() if pd.notna(row['date_added']) else None,
            int(row['release_year']) if pd.notna(row['release_year']) else None,
            str(row['rating']),
            str(row['duration']),
            str(row['genres']),
            str(row['language']),
            str(row['description']),
            round(float(row['popularity']), 4),
            int(row['vote_count']),
            round(float(row['vote_average']), 4),
            int(row['num_seasons']) if pd.notna(row['num_seasons']) else None)
        except Exception as e:
            print(f"Error inserting detailed TV show show_id {row['show_id']}: {e}")

    cursor.close()
    conn.close()
    print("All Netflix data inserted into SQL Server successfully.")

# --------------------------
# Main Execution
# --------------------------
if __name__ == "__main__":
    insert_all_data()
