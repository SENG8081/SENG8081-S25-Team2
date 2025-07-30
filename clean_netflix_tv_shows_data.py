import os
import pandas as pd

input_path = r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\netflix_tv_shows.xlsx"
output_path = r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\cleaned_netflix_tv_shows.xlsx"

print(f"Reading TV shows data from: {input_path}")
df = pd.read_excel(input_path)
print(f"Rows before cleaning: {len(df)}")

# Drop duplicates
df.drop_duplicates(inplace=True)

# Drop rows with missing important data
df.dropna(subset=['id', 'name', 'original_language', 'first_air_date', 'overview'], inplace=True)

# Strip whitespace from text columns
df['name'] = df['name'].str.strip()
df['original_language'] = df['original_language'].str.strip()

# Convert dates to datetime format
df['first_air_date'] = pd.to_datetime(df['first_air_date'], errors='coerce')

# Convert numeric columns to numbers
df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')
df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')

# Clean overview text
df['overview'] = df['overview'].str.replace(r'\s+', ' ', regex=True).str.strip()

# Filter valid data
df = df[df['first_air_date'].notnull()]
df = df[(df['vote_count'] > 0) & (df['vote_average'] > 0)]

print(f"Rows after cleaning: {len(df)}")

df.to_excel(output_path, index=False)

print(f"Saved cleaned TV shows data to: {output_path}")
print(f"File exists? {os.path.exists(output_path)}")
