"""Analysis functions for Student Performance Analysis."""

from __future__ import annotations

import pandas as pd

SUBJECT_COLUMNS = [
    "mathematics_marks",
    "science_marks",
    "english_marks",
    "social_science_marks",
    "computer_marks",
]


def add_average_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["average_score"] = df[SUBJECT_COLUMNS].mean(axis=1).round(2)
    return df


def subject_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = df[SUBJECT_COLUMNS].agg(["mean", "median", "min", "max"]).T
    summary = summary.rename(columns={"mean": "mean", "median": "median", "min": "min", "max": "max"})
    return summary.round(2)


def class_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "class_name" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby("class_name", dropna=False)
        .agg(
            student_count=("student_id", "count"),
            avg_attendance=("attendance_percentage", "mean"),
            avg_score=("average_score", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("avg_score", ascending=False)
    )


def performance_band(score: float) -> str:
    if score >= 80:
        return "80-100: Excellent"
    if score >= 60:
        return "60-79.99: Good"
    if score >= 40:
        return "40-59.99: Needs improvement"
    return "Below 40: At risk"


def add_performance_band(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["performance_band"] = df["average_score"].apply(performance_band)
    return df


def band_summary(df: pd.DataFrame) -> pd.DataFrame:
    order = [
        "80-100: Excellent",
        "60-79.99: Good",
        "40-59.99: Needs improvement",
        "Below 40: At risk",
    ]
    counts = df["performance_band"].value_counts().reindex(order, fill_value=0)
    out = counts.rename_axis("performance_band").reset_index(name="student_count")
    out["percentage"] = (out["student_count"] / len(df) * 100).round(2)
    return out


def attendance_vs_marks(df: pd.DataFrame, threshold: float = 75.0) -> dict:
    below = df[df["attendance_percentage"] < threshold]
    corr = df[["attendance_percentage", "average_score"]].corr().loc[
        "attendance_percentage", "average_score"
    ]
    return {
        "threshold": threshold,
        "students_below_threshold": int(len(below)),
        "percent_below_threshold": round(len(below) / len(df) * 100, 2) if len(df) else 0.0,
        "correlation_attendance_average": round(float(corr), 4) if pd.notna(corr) else None,
    }


def top_students(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    cols = ["student_id", "student_name", "class_name", "attendance_percentage", "average_score"]
    existing = [c for c in cols if c in df.columns]
    return df.sort_values("average_score", ascending=False)[existing].head(n).reset_index(drop=True)
