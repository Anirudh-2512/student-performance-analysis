"""Quick sanity checks for the analysis pipeline."""

from pathlib import Path
import pandas as pd
from data_cleaning import load_data, validate_data, clean_data
from analysis import add_average_score, add_performance_band


def test_validate_and_clean_synthetic_data():
    df = load_data('data/raw/student_performance.csv')
    issues = validate_data(df)
    assert issues['missing_columns'] == []
    cleaned, report = clean_data(df)
    assert len(cleaned) == 60
    assert report['rows_removed_total'] == 0


def test_invalid_values_are_removed():
    df = load_data('data/raw/student_performance.csv')
    df.loc[0, 'attendance_percentage'] = 120
    df.loc[1, 'mathematics_marks'] = -5
    df.loc[2, 'science_marks'] = None
    cleaned, report = clean_data(df)
    assert report['rows_removed_invalid_attendance'] == 1
    assert report['rows_removed_missing_numeric'] == 1
    assert report['rows_removed_invalid_marks'] == 1
    assert len(cleaned) == 57


def test_average_and_band():
    df = load_data('data/raw/student_performance.csv')
    cleaned, _ = clean_data(df)
    cleaned = add_average_score(cleaned)
    cleaned = add_performance_band(cleaned)
    assert cleaned['average_score'].between(0, 100).all()
    assert set(cleaned['performance_band']).issubset({
        '80-100: Excellent','60-79.99: Good','40-59.99: Needs improvement','Below 40: At risk'
    })
