import pandas as pd

# Use raw string for file path
df = pd.read_excel(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\netflix_movies.xlsx")

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

# Clean text in 'overview' with raw string for regex
df['overview'] = df['overview'].str.replace(r'\s+', ' ', regex=True)

# Filter valid data
df = df[df['release_date'].notnull()]
df = df[(df['vote_count'] > 0) & (df['vote_average'] > 0)]

# Save to new Excel file
df.to_excel('cleaned_netflix_movies_data.xlsx', index=False)
print("Data cleaning complete. File saved as 'cleaned_netflix_movies_data.xlsx'")
