import time
import os

refresh_interval = 60  # seconds

while True:
    print("Refreshing data from TMDB API...")
    os.system("python netflix_tmdb_data_excel.py")
    print("Data fetched and saved.")

    print("Running movies cleaning script...")
    os.system("python clean_netflix_movies_data.py")
    print("Movies cleaning done.")

    print("Running TV shows cleaning script...")
    os.system("python clean_netflix_tv_shows_data.py")
    print("TV shows cleaning done.")

    print("Running SQL import script to update database...")
    os.system("python insert_netflix_data_to_sql.py")
    print("SQL database updated with cleaned data.")

    print(f"Waiting {refresh_interval // 60} minute...\n")
    time.sleep(refresh_interval)
