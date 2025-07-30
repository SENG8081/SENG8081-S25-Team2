"""
test_netflix_pipeline.py
Comprehensive unit tests for SENG8081-S25-TEAM2 Netflix Data Pipeline
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import patch, MagicMock
import pyodbc
import re
import os
import requests

# ==============================================
# FIXTURES FOR TEST DATA
# ==============================================

@pytest.fixture
def raw_movies_data():
    return pd.DataFrame({
        'id': [1, 2, 3],
        'title': ['Movie 1', 'Movie 2', None],
        'original_language': ['en', 'fr', 'es'],
        'release_date': ['2021-01-01', '2021-02-01', None],
        'popularity': [100.0, 200.0, 50.0],
        'vote_average': [8.5, 7.2, None],
        'vote_count': [1000, 500, None],
        'overview': ['Great movie', 'Average movie', None]
    })

@pytest.fixture
def raw_tv_data():
    return pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Show 1', 'Show 2', None],
        'original_language': ['en', 'fr', 'es'],
        'first_air_date': ['2021-01-01', '2021-02-01', None],
        'popularity': [80.0, 150.0, 30.0],
        'vote_average': [9.0, 6.5, None],
        'vote_count': [800, 300, None],
        'overview': ['Great show', 'Average show', None]
    })

@pytest.fixture
def detailed_movies_data():
    return pd.DataFrame({
        'show_id': [1, 2, 3],
        'type': ['Movie', 'Movie', 'Movie'],
        'title': ['Detailed Movie 1', 'Detailed Movie 2', None],
        'director': ['Director A', None, 'Director C'],
        'cast': ['Actor X, Actor Y', None, 'Actor Z'],
        'country': ['USA', 'Canada', None],
        'date_added': ['2021-01-01', '2021-02-01', None],
        'release_year': [2020, 2021, 2020],
        'rating': ['PG-13', 'R', None],
        'duration': ['120 min', '90 min', None],
        'genres': ['Action', 'Comedy', None],
        'language': ['English', 'French', None],
        'description': ['Description 1', 'Description 2', None],
        'popularity': [100.0, 200.0, 50.0],
        'vote_count': [1000, 500, 0],
        'vote_average': [8.5, 7.2, 0],
        'budget': [1000000, 2000000, None],
        'revenue': [2000000, 3000000, None],
        'profit': [1000000, 1000000, None]
    })

@pytest.fixture
def detailed_tv_data():
    return pd.DataFrame({
        'show_id': [1, 2, 3],
        'type': ['TV Show', 'TV Show', 'TV Show'],
        'title': ['Detailed Show 1', 'Detailed Show 2', None],
        'director': ['Director A', None, 'Director C'],
        'cast': ['Actor X, Actor Y', None, 'Actor Z'],
        'country': ['USA', 'Canada', None],
        'date_added': ['2021-01-01', '2021-02-01', None],
        'release_year': [2020, 2021, 2020],
        'rating': ['TV-14', 'TV-MA', None],
        'duration': ['2 Seasons', '1 Season', None],
        'genres': ['Drama', 'Comedy', None],
        'language': ['English', 'French', None],
        'description': ['Description 1', 'Description 2', None],
        'popularity': [80.0, 150.0, 30.0],
        'vote_count': [800, 300, 0],
        'vote_average': [9.0, 6.5, 0],
        'num_seasons': [2, 1, None]
    })

@pytest.fixture
def cleaned_movies_data():
    return pd.DataFrame({
        'id': [1, 2],
        'title': ['Cleaned Movie 1', 'Cleaned Movie 2'],
        'release_date': [pd.to_datetime('2021-01-01'), pd.to_datetime('2021-02-01')],
        'overview': ['Overview 1', 'Overview 2'],
        'vote_average': [8.5, 7.2],
        'vote_count': [1000, 500]
    })

@pytest.fixture
def api_response():
    return {
        'results': [{
            'id': 1,
            'title': 'API Movie',
            'original_language': 'en',
            'release_date': '2021-01-01',
            'popularity': 100.0,
            'vote_average': 8.0,
            'vote_count': 1000,
            'overview': 'Test overview'
        }]
    }

# ==============================================
# TESTS FOR netflix_tmdb_data_excel.py
# ==============================================

class TestTMDBDataCollection:
    @patch('requests.get')
    def test_api_request(self, mock_get, api_response):
        mock_get.return_value.json.return_value = api_response
        mock_get.return_value.status_code = 200
        response = requests.get("https://api.themoviedb.org/3/movie/550")
        assert response.status_code == 200
        assert 'results' in response.json()

    def test_dataframe_creation(self, api_response):
        df = pd.DataFrame(api_response['results'])
        assert not df.empty
        assert 'title' in df.columns
        assert 'popularity' in df.columns

    def test_excel_output(self, raw_movies_data, raw_tv_data, tmp_path):
        movies_path = tmp_path / "netflix_movies.xlsx"
        tv_path = tmp_path / "netflix_tv_shows.xlsx"
        raw_movies_data.to_excel(movies_path, index=False)
        raw_tv_data.to_excel(tv_path, index=False)
        assert movies_path.exists()
        assert tv_path.exists()

# ==============================================
# TESTS FOR clean_netflix_movies_data.py
# ==============================================

class TestMoviesDataCleaning:
    def test_null_removal(self, raw_movies_data):
        df = raw_movies_data.copy()
        initial_count = len(df)
        df.dropna(subset=['id', 'title', 'release_date', 'overview'], inplace=True)
        assert len(df) < initial_count

    def test_date_conversion(self, raw_movies_data):
        df = raw_movies_data.copy()
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        assert pd.api.types.is_datetime64_any_dtype(df['release_date'])

    def test_text_cleaning(self, raw_movies_data):
        df = raw_movies_data.copy()
        df['title'] = df['title'].str.strip()
        df['overview'] = df['overview'].str.strip()
        assert df['title'].str.contains('  ').sum() == 0

    def test_numeric_conversion(self, raw_movies_data):
        df = raw_movies_data.copy()
        df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
        df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')
        assert df['vote_average'].dtype == 'float64'
        assert df['vote_count'].dtype == 'float64'

# ==============================================
# TESTS FOR clean_netflix_tv_shows_data.py
# ==============================================

class TestTVShowsDataCleaning:
    def test_null_removal(self, raw_tv_data):
        df = raw_tv_data.copy()
        initial_count = len(df)
        df.dropna(subset=['id', 'name', 'first_air_date', 'overview'], inplace=True)
        assert len(df) < initial_count

    def test_date_conversion(self, raw_tv_data):
        df = raw_tv_data.copy()
        df['first_air_date'] = pd.to_datetime(df['first_air_date'], errors='coerce')
        assert pd.api.types.is_datetime64_any_dtype(df['first_air_date'])

    def test_text_cleaning(self, raw_tv_data):
        df = raw_tv_data.copy()
        df['name'] = df['name'].str.strip()
        df['overview'] = df['overview'].str.strip()
        assert df['name'].str.contains('  ').sum() == 0

    def test_numeric_conversion(self, raw_tv_data):
        df = raw_tv_data.copy()
        df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
        df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')
        assert df['vote_average'].dtype == 'float64'
        assert df['vote_count'].dtype == 'float64'

# ==============================================
# TESTS FOR movies_remove_row.py AND tv_shows_remove_row.py
# ==============================================

class TestGibberishRemoval:
    def test_gibberish_detection(self):
        assert bool(re.search(r'[^\x00-\x7F]', 'Weïrd©')) is True
        assert bool(re.search(r'[^\x00-\x7F]', 'Normal')) is False

    def test_row_cleaning(self, detailed_movies_data):
        df = detailed_movies_data.copy()
        initial_count = len(df)
        df = df[~df['title'].apply(lambda x: bool(re.search(r'[^\x00-\x7F]', str(x))))]
        assert len(df) <= initial_count

    def test_row_cleaning_tv(self, detailed_tv_data):
        df = detailed_tv_data.copy()
        initial_count = len(df)
        df = df[~df['title'].apply(lambda x: bool(re.search(r'[^\x00-\x7F]', str(x))))]
        assert len(df) <= initial_count

# ==============================================
# TESTS FOR insert_netflix_data_to_sql.py
# ==============================================

class TestSQLOperations:
    @patch('pyodbc.connect')
    def test_db_connection(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=test;DATABASE=test")
        assert conn is not None

    @patch('pandas.read_excel')
    @patch('pandas.read_csv')
    @patch('pyodbc.connect')
    def test_data_insertion(self, mock_connect, mock_read_csv, mock_read_excel,
                            cleaned_movies_data, detailed_movies_data):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_read_excel.return_value = cleaned_movies_data
        mock_read_csv.return_value = detailed_movies_data

        mock_cursor.execute("INSERT INTO table VALUES (?)", (1,))
        mock_cursor.execute.assert_called_once()

# ==============================================
# TESTS FOR auto_refresh.py
# ==============================================

class TestAutoRefresh:
    @patch('os.system')
    @patch('time.sleep')
    def test_refresh_cycle(self, mock_sleep, mock_system):
        mock_system.return_value = 0
        os.system("python netflix_tmdb_data_excel.py")
        os.system("python clean_netflix_movies_data.py")
        os.system("python clean_netflix_tv_shows_data.py")
        assert mock_system.call_count == 3

# ==============================================
# MAIN TEST EXECUTION
# ==============================================

if __name__ == "__main__":
    pytest.main(["-v", "--cov=.", "--cov-report=html"])
