"""Run the full Student Performance Analysis pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path
import json

from data_cleaning import load_data, validate_data, clean_data, save_data
from analysis import (
    add_average_score,
    subject_summary,
    class_summary,
    add_performance_band,
    band_summary,
    attendance_vs_marks,
    top_students,
)
from visualisation import generate_all_charts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run student performance analysis pipeline.")
    parser.add_argument("--input", default="data/raw/student_performance.csv")
    parser.add_argument("--processed", default="data/processed/cleaned_student_performance.csv")
    parser.add_argument("--charts", default="outputs/charts")
    parser.add_argument("--summary", default="outputs/summary.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = load_data(args.input)
    issues = validate_data(df)
    cleaned, report = clean_data(df)
    cleaned = add_average_score(cleaned)
    cleaned = add_performance_band(cleaned)

    save_data(cleaned, args.processed)
    subj = subject_summary(cleaned)
    cls = class_summary(cleaned)
    bands = band_summary(cleaned)
    att = attendance_vs_marks(cleaned, threshold=75.0)
    top = top_students(cleaned, n=10)
    charts = generate_all_charts(cleaned, bands, cls, args.charts)

    summary = {
        "validation_issues": issues,
        "cleaning_report": report,
        "subject_summary": subj.reset_index().rename(columns={"index": "subject"}).to_dict(orient="records"),
        "class_summary": cls.to_dict(orient="records"),
        "performance_bands": bands.to_dict(orient="records"),
        "attendance_vs_marks": att,
        "top_students": top.to_dict(orient="records"),
        "charts": [str(Path(p)) for p in charts],
    }
    Path(args.summary).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary).write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Rows:", len(cleaned))
    print("Charts:", len(charts))
    print("Summary:", args.summary)


if __name__ == "__main__":
    main()
