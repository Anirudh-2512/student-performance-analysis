"""Chart generation for Student Performance Analysis."""

from __future__ import annotations

from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

SUBJECT_COLUMNS = [
    "mathematics_marks",
    "science_marks",
    "english_marks",
    "social_science_marks",
    "computer_marks",
]
SUBJECT_LABELS = {
    "mathematics_marks": "Mathematics",
    "science_marks": "Science",
    "english_marks": "English",
    "social_science_marks": "Social Science",
    "computer_marks": "Computer",
}


def _ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def plot_subject_averages(df: pd.DataFrame, out_dir: str | Path) -> Path:
    out_dir = _ensure_dir(out_dir)
    means = df[SUBJECT_COLUMNS].mean().rename(index=SUBJECT_LABELS)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(means.index, means.values, color="#4C78A8")
    ax.set_title("Subject-wise Average Marks")
    ax.set_ylabel("Average Marks (0-100)")
    ax.set_xlabel("Subject")
    ax.set_ylim(0, 100)
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    path = out_dir / "subject_wise_average_marks.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_attendance_distribution(df: pd.DataFrame, out_dir: str | Path) -> Path:
    out_dir = _ensure_dir(out_dir)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["attendance_percentage"], bins=10, color="#72B7B2", edgecolor="white")
    ax.set_title("Attendance Distribution")
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Number of Students")
    fig.tight_layout()
    path = out_dir / "attendance_distribution.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_attendance_vs_marks(df: pd.DataFrame, out_dir: str | Path) -> Path:
    out_dir = _ensure_dir(out_dir)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["attendance_percentage"], df["average_score"], alpha=0.75, color="#F58518")
    ax.set_title("Attendance vs Average Marks")
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Average Score (0-100)")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    fig.tight_layout()
    path = out_dir / "attendance_vs_average_marks.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_performance_bands(band_df: pd.DataFrame, out_dir: str | Path) -> Path:
    out_dir = _ensure_dir(out_dir)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(band_df["performance_band"], band_df["student_count"], color="#54A24B")
    ax.set_title("Student Performance Bands (Project-Defined)")
    ax.set_xlabel("Performance Band")
    ax.set_ylabel("Number of Students")
    ax.bar_label(bars, padding=3)
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    path = out_dir / "performance_bands.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_class_performance(class_df: pd.DataFrame, out_dir: str | Path) -> Path | None:
    if class_df.empty:
        return None
    out_dir = _ensure_dir(out_dir)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(class_df["class_name"], class_df["avg_score"], color="#E45756")
    ax.set_title("Class-wise Average Performance")
    ax.set_xlabel("Class")
    ax.set_ylabel("Average Score (0-100)")
    ax.set_ylim(0, 100)
    ax.bar_label(bars, fmt="%.1f", padding=3)
    fig.tight_layout()
    path = out_dir / "class_wise_average_performance.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def generate_all_charts(df: pd.DataFrame, band_df: pd.DataFrame, class_df: pd.DataFrame, out_dir: str | Path) -> list[Path]:
    paths = [
        plot_subject_averages(df, out_dir),
        plot_attendance_distribution(df, out_dir),
        plot_attendance_vs_marks(df, out_dir),
        plot_performance_bands(band_df, out_dir),
    ]
    class_path = plot_class_performance(class_df, out_dir)
    if class_path:
        paths.append(class_path)
    return paths
