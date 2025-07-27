import pandas as pd
import numpy as np
import re

# Load the original CSV files
tv_df = pd.read_csv("C:/Users/nandh/Downloads/netflix_tv_shows_detailed_up_to_2025.csv")
movies_df = pd.read_csv("C:/Users/nandh/Downloads/netflix_movies_detailed_up_to_2025.csv")

# Fill NaNs
tv_df['cast'] = tv_df['cast'].fillna("Unknown")
tv_df['director'] = tv_df['director'].fillna("Unknown")
tv_df['genres'] = tv_df['genres'].fillna("Unknown")
tv_df['description'] = tv_df['description'].fillna("Unknown")

movies_df['cast'] = movies_df['cast'].fillna("Unknown")
movies_df['director'] = movies_df['director'].fillna("Unknown")

# Drop rows with too many missing values
tv_df.dropna(thresh=5, inplace=True)
movies_df.dropna(thresh=5, inplace=True)

# Convert dates
tv_df['date_added'] = pd.to_datetime(tv_df['date_added'], errors='coerce')
movies_df['date_added'] = pd.to_datetime(movies_df['date_added'], errors='coerce')

# Remove duplicates
tv_df.drop_duplicates(inplace=True)
movies_df.drop_duplicates(inplace=True)

# Standardize string columns
tv_df['title'] = tv_df['title'].str.strip().str.title()
movies_df['title'] = movies_df['title'].str.strip().str.title()
tv_df['language'] = tv_df['language'].str.strip().str.lower()
movies_df['language'] = movies_df['language'].str.strip().str.lower()

# Fill missing budget and revenue
movies_df['budget'] = movies_df['budget'].fillna(0)
movies_df['revenue'] = movies_df['revenue'].fillna(0)

# Create profit column
movies_df['profit'] = movies_df['revenue'] - movies_df['budget']

# ✅ Detect emojis or weird symbols
def contains_emojis_or_symbols(text):
    if isinstance(text, str):
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            u"\U00002700-\U000027BF"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        symbols_pattern = re.compile(r"[©®™ ¡¿]|[^\x00-\x7F]+")
        return bool(emoji_pattern.search(text) or symbols_pattern.search(text))
    return False

# ✅ Apply row filtering
def row_contains_emojis_or_symbols(row):
    return any(contains_emojis_or_symbols(str(cell)) for cell in row)

tv_cleaned_final = tv_df[~tv_df.apply(row_contains_emojis_or_symbols, axis=1)].reset_index(drop=True)
movies_cleaned_final = movies_df[~movies_df.apply(row_contains_emojis_or_symbols, axis=1)].reset_index(drop=True)

# ✅ Print how many rows were removed
print("Removed from TV Shows:", len(tv_df) - len(tv_cleaned_final))
print("Removed from Movies:", len(movies_df) - len(movies_cleaned_final))

# ✅ Save cleaned files
tv_cleaned_final.to_csv("C:/Users/nandh/Downloads/netflix_tv_shows_final_clean.csv", index=False)
movies_cleaned_final.to_csv("C:/Users/nandh/Downloads/netflix_movies_final_clean.csv", index=False)
