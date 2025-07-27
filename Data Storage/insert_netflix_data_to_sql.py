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
# STEP 2: Load Excel and CSV Files
# --------------------------
movies_cleaned = pd.read_excel(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\cleaned_netflix_movies_data.xlsx")
movies_detailed = pd.read_csv(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\netflix_movies_detailed_up_to_2025_clean[1].csv")
tv_cleaned = pd.read_excel(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\cleaned_netflix_tv_shows.xlsx")
tv_detailed = pd.read_csv(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\netflix_tv_shows_detailed_up_to_2025_clean[1].csv")

# --------------------------
# STEP 3: Clean Numeric Columns & Dates
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
            print(f"Inserted cleaned movie ID: {row['id']}")
        except Exception as e:
            print(f"Error inserting cleaned movie id {row['id']}: {e}")

    # Insert Detailed Movies
    print("🔍 Inserting detailed movies...")
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
            print(f"Inserted movie show_id: {row['show_id']}")
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
            print(f"Inserted cleaned TV show ID: {row['id']}")
        except Exception as e:
            print(f"Error inserting cleaned TV show id {row['id']}: {e}")

    # FIXED: Insert Detailed TV Shows with correct float and string types
    print("Inserting detailed TV shows...")
    for _, row in tv_detailed.iterrows():
        try:
            show_id = int(row['show_id']) if pd.notna(row['show_id']) else None
            type_ = str(row['type']) if pd.notna(row['type']) else None
            title = str(row['title']) if pd.notna(row['title']) else None
            director = str(row['director']) if pd.notna(row['director']) else None
            cast = str(row['cast']) if pd.notna(row['cast']) else None
            country = str(row['country']) if pd.notna(row['country']) else None
            date_added = row['date_added'].date() if pd.notna(row['date_added']) else None
            release_year = int(row['release_year']) if pd.notna(row['release_year']) else None
            rating = str(row['rating']) if pd.notna(row['rating']) else None
            duration = str(row['duration']) if pd.notna(row['duration']) else None
            genres = str(row['genres']) if pd.notna(row['genres']) else None
            language = str(row['language']) if pd.notna(row['language']) else None
            description = str(row['description']) if pd.notna(row['description']) else None
            popularity = round(float(row['popularity']), 4) if pd.notna(row['popularity']) else 0.0
            vote_count = int(row['vote_count']) if pd.notna(row['vote_count']) else 0
            vote_average = round(float(row['vote_average']), 4) if pd.notna(row['vote_average']) else 0.0
            num_seasons = int(row['num_seasons']) if pd.notna(row['num_seasons']) else 0

            cursor.execute("""
                INSERT INTO Netflix_TV_Shows_Detailed
                (show_id, type, title, director, cast, country, date_added, release_year, rating,
                 duration, genres, language, description, popularity, vote_count, vote_average,
                 num_seasons)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, show_id, type_, title, director, cast, country, date_added, release_year,
                rating, duration, genres, language, description,
                popularity, vote_count, vote_average, num_seasons)
            print(f"Inserted detailed TV show show_id: {show_id}")
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
