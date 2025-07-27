CREATE DATABASE Netflix_Movies_TV_Shows_2025;
GO

USE Netflix_Movies_TV_Shows_2025;
GO

-- Drop tables if they exist (from bottom to top based on dependency)
IF OBJECT_ID('Netflix_TV_Shows_Detailed', 'U') IS NOT NULL DROP TABLE Netflix_TV_Shows_Detailed;
IF OBJECT_ID('Cleaned_Netflix_TV_Shows', 'U') IS NOT NULL DROP TABLE Cleaned_Netflix_TV_Shows;
IF OBJECT_ID('Netflix_Movies_Detailed', 'U') IS NOT NULL DROP TABLE Netflix_Movies_Detailed;
IF OBJECT_ID('Cleaned_Netflix_Movies_Data', 'U') IS NOT NULL DROP TABLE Cleaned_Netflix_Movies_Data;


-- Table 1: Cleaned Netflix Movies
CREATE TABLE Cleaned_Netflix_Movies_Data (
    id INT,
    title NVARCHAR(500),
    original_language VARCHAR(10),
    release_date DATE,
    popularity FLOAT,
    vote_average FLOAT,
    vote_count INT,
    overview NVARCHAR(MAX)
);

-- Table 2: Detailed Movies
CREATE TABLE Netflix_Movies_Detailed (
    show_id INT,
    type VARCHAR(50),
    title NVARCHAR(500),
    director NVARCHAR(500),
    cast NVARCHAR(MAX),
    country NVARCHAR(255),
    date_added DATE,
    release_year INT,
    rating VARCHAR(50),
    duration VARCHAR(50),
    genres NVARCHAR(500),
    language VARCHAR(50),
    description NVARCHAR(MAX),
    popularity FLOAT,
    vote_count INT,
    vote_average FLOAT,
    budget BIGINT,
    revenue BIGINT,
    profit BIGINT
);

-- Table 3: Cleaned TV Shows
CREATE TABLE Cleaned_Netflix_TV_Shows (
    id INT,
    name NVARCHAR(500),
    original_language VARCHAR(10),
    first_air_date DATE,
    popularity FLOAT,
    vote_average FLOAT,
    vote_count INT
);

-- Table 4: Detailed TV Shows
CREATE TABLE Netflix_TV_Shows_Detailed (
    show_id INT,
    type VARCHAR(50),
    title NVARCHAR(500),
    director NVARCHAR(500),
    cast NVARCHAR(MAX),
    country NVARCHAR(255),
    date_added DATE,
    release_year INT,
    rating VARCHAR(50),
    duration VARCHAR(50),
    genres NVARCHAR(500),
    language VARCHAR(50),
    description NVARCHAR(MAX),
    popularity FLOAT,
    vote_count INT,
    vote_average FLOAT,
    num_seasons INT
);


select * from Cleaned_Netflix_Movies_Data;
select * from Netflix_Movies_Detailed;
select * from Cleaned_Netflix_TV_Shows;
select * from Netflix_TV_Shows_Detailed;

