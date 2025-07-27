import time
import os

# Refresh interval in seconds (1 minute)
refresh_interval = 60

while True:
    print("Refreshing data from TMDB API...")

    # Step 1: Refresh the data
    os.system("python netflix_tmdb_data_excel.py") 
    print("Data refreshed and files overwritten.")

   
    print(f" Waiting {refresh_interval // 60} minute...\n")

    # Step 3: Wait before next refresh
    time.sleep(refresh_interval)
