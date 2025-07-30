import os
import pandas as pd

input_path = r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\netflix_movies.xlsx"
output_path = r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\cleaned_netflix_movies_data.xlsx"

print(f"Reading movies data from: {input_path}")
df = pd.read_excel(input_path)
print(f"Rows before cleaning: {len(df)}")

# Cleaning steps
df.drop_duplicates(inplace=True)
df.dropna(subset=['id', 'title', 'release_date', 'overview'], inplace=True)

# Strip whitespaces
df['title'] = df['title'].str.strip()
df['overview'] = df['overview'].str.strip()

# Convert data types
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')
df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')

# Clean overview text
df['overview'] = df['overview'].str.replace(r'\s+', ' ', regex=True)

# Filter valid data
df = df[df['release_date'].notnull()]
df = df[(df['vote_count'] > 0) & (df['vote_average'] > 0)]

print(f"Rows after cleaning: {len(df)}")

df.to_excel(output_path, index=False)

print(f"Saved cleaned movies data to: {output_path}")
print(f"File exists? {os.path.exists(output_path)}")
