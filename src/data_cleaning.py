"""Data loading, validation, and cleaning for Student Performance Analysis."""

from __future__ import annotations

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "student_id",
    "student_name",
    "class_name",
    "attendance_percentage",
    "mathematics_marks",
    "science_marks",
    "english_marks",
    "social_science_marks",
    "computer_marks",
]

OPTIONAL_COLUMNS = ["gender"]

SUBJECT_COLUMNS = [
    "mathematics_marks",
    "science_marks",
    "english_marks",
    "social_science_marks",
    "computer_marks",
]


def load_data(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    df = pd.read_csv(path)
    return df


def validate_data(df: pd.DataFrame) -> dict:
    issues: dict[str, object] = {}
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    issues["missing_columns"] = missing_cols
    if missing_cols:
        return issues

    issues["duplicate_rows"] = int(df.duplicated().sum())
    issues["duplicate_student_ids"] = int(df["student_id"].duplicated().sum())
    issues["missing_values_by_column"] = df.isnull().sum().to_dict()

    numeric_cols = ["attendance_percentage", *SUBJECT_COLUMNS]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    issues["non_numeric_coerced_to_nan"] = df[numeric_cols].isnull().sum().to_dict()

    issues["invalid_attendance_rows"] = int(
        df.loc[~df["attendance_percentage"].between(0, 100, inclusive="both")].shape[0]
    )
    out_of_range = {}
    for col in SUBJECT_COLUMNS:
        out_of_range[col] = int(df.loc[~df[col].between(0, 100, inclusive="both")].shape[0])
    issues["out_of_range_marks_rows"] = out_of_range
    issues["row_count"] = int(len(df))
    return issues


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    report: dict[str, object] = {}
    df = df.copy()
    before = len(df)

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Normalize text
    for col in ["student_name", "class_name", "gender"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    numeric_cols = ["student_id", "attendance_percentage", *SUBJECT_COLUMNS]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    report["rows_before"] = before
    report["duplicate_rows_removed"] = int(df.duplicated().sum())
    df = df.drop_duplicates()

    report["duplicate_student_ids_before"] = int(df["student_id"].duplicated().sum())
    # Keep first occurrence but report; in real projects investigate duplicates.
    df = df.drop_duplicates(subset=["student_id"], keep="first")

    # Missing critical IDs/names cannot be reliably imputed.
    critical_missing = df["student_id"].isnull() | df["student_name"].isnull() | df["class_name"].isnull()
    report["rows_removed_missing_critical"] = int(critical_missing.sum())
    df = df.loc[~critical_missing].copy()

    # Do not silently replace missing marks with zero; drop rows with missing/out-of-range values.
    numeric_check_cols = ["attendance_percentage", *SUBJECT_COLUMNS]
    missing_numeric = df[numeric_check_cols].isnull().any(axis=1)
    report["rows_removed_missing_numeric"] = int(missing_numeric.sum())
    df = df.loc[~missing_numeric].copy()

    invalid_attendance = ~df["attendance_percentage"].between(0, 100, inclusive="both")
    report["rows_removed_invalid_attendance"] = int(invalid_attendance.sum())
    df = df.loc[~invalid_attendance].copy()

    invalid_marks = ~df[SUBJECT_COLUMNS].apply(lambda s: s.between(0, 100, inclusive="both")).all(axis=1)
    report["rows_removed_invalid_marks"] = int(invalid_marks.sum())
    df = df.loc[~invalid_marks].copy()

    df["student_id"] = df["student_id"].astype(int)
    df = df.sort_values("student_id").reset_index(drop=True)
    report["rows_after"] = int(len(df))
    report["rows_removed_total"] = before - len(df)
    return df, report


def save_data(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
