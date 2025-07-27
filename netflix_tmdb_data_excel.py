# data collection From API

import requests 
import json
import time
import pandas as pd

# Replace with your actual TMDb API key
API_KEY = 'f79e762d950a97125c34ee3dfb1113eb'  
BASE_URL = 'https://api.themoviedb.org/3'

# Function to get Netflix content using TMDb "watch providers" filter
def get_netflix_content(content_type='movie', pages=50):
    all_data = []

    for page in range(1, pages + 1):
        url = f"{BASE_URL}/discover/{content_type}"
        params = {
            'api_key': API_KEY,
            'with_watch_providers': '8',  # 8 = Netflix
            'watch_region': 'US',
            'language': 'en-US',
            'sort_by': 'release_date.desc',
            'page': page,
            'include_adult': 'false'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data['results'])
            time.sleep(0.2)  # Avoid hitting rate limit
        else:
            print(f"Error: {response.status_code}")
            break

    return all_data

# Extract and filter useful columns
def filter_fields(data, content_type='movie'):
    df = pd.DataFrame(data)
    if content_type == 'movie':
        columns = ['id', 'title', 'original_language', 'release_date', 'popularity', 'vote_average', 'vote_count', 'overview']
    else:
        columns = ['id', 'name', 'original_language', 'first_air_date', 'popularity', 'vote_average', 'vote_count', 'overview']
    return df[columns]

# Get data
movies_data = get_netflix_content('movie', pages=50)
tv_data = get_netflix_content('tv', pages=50)

# Filter and convert to DataFrames
movies_df = filter_fields(movies_data, 'movie')
tv_df = filter_fields(tv_data, 'tv')

# Save to Excel
movies_df.to_excel('netflix_movies.xlsx', index=False)
tv_df.to_excel('netflix_tv_shows.xlsx', index=False)

print("✅ Excel files created: 'netflix_movies.xlsx' and 'netflix_tv_shows.xlsx'")
