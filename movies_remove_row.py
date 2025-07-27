import pandas as pd
import re

# Load the Movies CSV file
movies_df = pd.read_csv("netflix_movies_detailed_up_to_2025_clean (1).csv")

# Function to detect gibberish (non-ASCII characters)
def contains_gibberish(text):
    if isinstance(text, str):
        return bool(re.search(r'[^\x00-\x7F]', text))  # Matches any non-ASCII char
    return False

# Function to check if a row is clean (no gibberish in any cell)
def is_row_clean(row):
    return not any(contains_gibberish(str(cell)) for cell in row)

# Keep only clean rows
movies_cleaned = movies_df[movies_df.apply(is_row_clean, axis=1)].reset_index(drop=True)

# Save the cleaned data
movies_cleaned.to_csv("netflix_movies_detailed_up_to_2025_clean (1).csv", index=False)

# Print number of rows removed
print("Movies – Gibberish rows removed:", len(movies_df) - len(movies_cleaned))
