# SENG8081-S25-Team2

## Project Contributors

1. Veera Rani  
2. Nandhakumar Balaji  
3. Isha Patel  
4. Yesha Panchal

---

## Project Title

**Netflix Movies and TV shows till 2025**

---

## Project Objective

This dataset contains information on Netflix movies and TV shows, sourced from TMDb (The Movie Database). It includes titles, genres, release dates, ratings, descriptions, and other relevant metadata. The dataset has been curated to provide a comprehensive overview of Netflix's content library, making it useful for data analysis, recommendation systems, and trend exploration.

---

## Abstract

Managing and analyzing content data is essential for understanding viewer preferences and content trends in the fast-growing world of online streaming. This project presents a Python-based approach to organizing and analyzing Netflix’s movie and TV show catalog using data sourced from TMDb (The Movie Database) and Kaggle.

The system collects detailed information, including titles, genres, release dates, ratings, and content descriptions. The data is cleaned, formatted, and stored in a structured database for smooth querying and trend analysis. The backend uses Python to connect to TMDb's API and retrieve the latest content details, ensuring the dataset remains current and relevant.

Key features of the system include genre-based categorization, rating distribution tracking, and content release timeline analysis. This dataset and system can be used to build recommendation engines, explore content trends over time, and support content-based marketing strategies.

By combining historical and live content data, this project delivers a strong base for deep insights into Netflix’s evolving media library and enhances the potential for personalized recommendations and media analytics.

---

## Introduction

This project aims to conduct a detailed analysis of Netflix's content library, focusing on historical and current data related to movies and TV shows. It explores patterns in content genres, release trends, viewer ratings, and other metadata to understand how Netflix's catalog has evolved. The main objective is to uncover insights about content popularity, genre distribution, and viewer engagement that can support data-driven decisions and recommendations. The project uses a cleaned and processed dataset from Kaggle, integrates real-time updates from the TMDb API, and builds visualizations and models to highlight key trends.

---

## System Components for Netflix Movies & TV Shows Project

- **Python Backend**: Used for collecting data from files and APIs, cleaning data, and preparing it for storage.  
- **Real-Time API**: Fetches the latest movie and TV show details to keep the dataset updated.  
- **Historical Dataset**: Contains movie and TV show data collected earlier from Kaggle and other sources.  
- **Database**: Microsoft SQL Server stores all cleaned and detailed Netflix movies and TV shows data.  
- **Dashboard/Visualization**: Tools like Tableau can be used to show reports and charts from the stored data.

---

## Data Research and Integration

### Sources

- Kaggle Netflix Dataset: https://www.kaggle.com/datasets/bhargavchirumamilla/netflix-movies-and-tv-shows-till-2025  
- TMDb API – Real-Time Content Data: https://api.themoviedb.org/3

---

## Data Collection & Processing

### Source

TMDb API – Real-Time Content Data  
Kaggle Netflix Dataset

### Transformations

The data has been cleaned, formatted, and filtered to ensure consistency and usability. Duplicate or irrelevant entries were removed, and missing values were handled appropriately.

### Potential Uses

Content analysis, trend discovery, machine learning models for recommendation systems, and more.

---

### Historical Data

- Download CSV or JSON datasets from sources.  
- Clean the data using Python’s pandas library.  
- Load the cleaned data into Microsoft SQL Server using pyodbc.

---

### Real-Time Data

- Fetch new data using APIs with an API key and Python’s requests library.  
- Parse JSON responses and convert them into tables.  
- Combine real-time data with historical data using pandas or SQL queries.


---

## Data Storage and Maintenance

### Data Storage

Use Microsoft SQL Server to store all Netflix movies and TV shows data.

### Data Maintenance

- Archive API data monthly to keep the database updated and clean.  
- Set up automated backups to prevent data loss.


---

### Data Quality


Several problems with the data were identified and resolved, such as missing data (director, cast), duplication (duplicate records), inconsistent naming standards (e.g., "USA" vs. "United States"), invalid formats (dates stored as strings), and garbage or emoji characters in some fields.

To handle them, Python libraries such as pandas and regular expressions were utilized to:

- Drop or suitably fill missing values
- Normalise country and language names
- Convert data to the correct type (e.g., dates, numbers)
- Remove non-English characters


---

### Data Documentation & Metadata

A data dictionary was used to define each column, including its type and accepted values. Metadata offers data sources, cleaning rules, and transformation steps. This increases dataset transparency and allows consistent use by users and systems.


---

### Sample Data Dictionary

- Column	Description	Example
- show_id	Unique ID for the title	s1
- type	Movie or TV Show	Movie
- title	Title of the content	Stranger Things
- director	Name of the director	Shawn Levy
- cast	Lead actors	Millie Bobby Brown
- country	Production country	United States
- release_year	Year in which the content was created	2019
- duration	Length or number of seasons	2 Seasons
- rating	Age rating	TV-14
- description	Short description of the content	Sci-fi drama series


---

### Data Analysis and Visualizations

Python libraries seaborn and matplotlib were used to create charts and analyze patterns of data. Visualizations included:

- Bar charts of genre frequency
- Line graphs of trends in the release of content over the years
- Histograms of ratings distributions
- Treemaps showing original languages

These visualizations helped in presenting the most popular genres, countries of active content, and viewer preferences.


---

### Unit Testing

To guarantee functionality, a series of unit tests was designed using the pytest framework for the whole data pipeline. API integration, data cleaning, Excel export, SQL connection, and refresh automation were all covered.

All 17 test cases were executed, with all passing, confirming the data pipeline is in working order and reliable.

Code coverage was recorded and an HTML report generated using the pytest-cov plugin.


---

### Project Extensions

The future directions are:

Construction of a machine learning recommendation system

Analysis of public opinion based on social media postings

Automatic updating of API data implementation

Investigating content equality by genre, country, and language coverage


---

### Future Work

Other possible improvements would be:

Inclusion of data from IMDb and other sources

Using user interaction data (views, likes) as predictors

Forecasting trends through time series models

Constructing the pipeline into a complete dashboard or web application


---

### Conclusion

This project combined historical information from Kaggle with live information from the TMDb API to create a cleaned, enriched dataset for Netflix content. The use of SQL Server and Python enabled effective analysis of content trends, genre, and user ratings. The system provides a solid foundation for future recommendation systems and analytics.


---

### References

Kaggle Netflix Dataset: https://www.kaggle.com/datasets/bhargavchirumamilla/netflix-movies-and-tv-shows-till-2025

TMDb API: https://developer.themoviedb.org/docs
