import pandas as pd

# Load the TV shows Excel file (change path and filename if needed)
df = pd.read_excel(r"C:\Users\veera\OneDrive - Conestoga College\Desktop\datttaaa\netflix_tv_shows.xlsx")

# Drop duplicates
df.drop_duplicates(inplace=True)

# Drop rows with missing important data
df.dropna(subset=['id', 'name', 'original_language', 'first_air_date', 'overview'], inplace=True)

# Strip whitespace from text columns
df['name'] = df['name'].str.strip()
df['original_language'] = df['original_language'].str.strip()

# Convert dates to datetime format
df['first_air_date'] = pd.to_datetime(df['first_air_date'], errors='coerce')

# Convert numeric columns to numbers, forcing errors to NaN
df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')
df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')

# Clean overview text: replace multiple spaces with a single space (using raw string for regex)
df['overview'] = df['overview'].str.replace(r'\s+', ' ', regex=True).str.strip()

# Filter valid data (remove rows with bad dates or zero votes)
df = df[df['first_air_date'].notnull()]
df = df[(df['vote_count'] > 0) & (df['vote_average'] > 0)]

# Save cleaned data to new Excel file
df.to_excel('cleaned_netflix_tv_shows.xlsx', index=False)

print("TV shows data cleaning complete. Saved as 'cleaned_netflix_tv_shows.xlsx'")
