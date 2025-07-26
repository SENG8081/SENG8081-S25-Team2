import pandas as pd
import re

# Load the TV shows CSV file
tv_df = pd.read_csv("netflix_tv_shows_detailed_up_to_2025_clean (1).csv")

# Function to detect gibberish (non-ASCII characters)
def contains_gibberish(text):
    if isinstance(text, str):
        return bool(re.search(r'[^\x00-\x7F]', text))  # Match any non-ASCII character
    return False

# Function to check if the row is clean (no gibberish in any cell)
def is_row_clean(row):
    return not any(contains_gibberish(str(cell)) for cell in row)

# Filter rows to keep only clean ones
tv_cleaned = tv_df[tv_df.apply(is_row_clean, axis=1)].reset_index(drop=True)

# Save cleaned TV shows data
tv_cleaned.to_csv("netflix_tv_shows_detailed_up_to_2025_clean (1).csv", index=False)

# Print number of rows removed
print("TV Shows – Gibberish rows removed:", len(tv_df) - len(tv_cleaned))
