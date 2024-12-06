import os
import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from datetime import datetime

import pandas as pd


def extract_git_logs(repo_path):
    """
    Extract Git logs with author, email, date, and timezone information from the specified repository.
    """
    # Extract logs with %ad containing date, time, and timezone
    cmd = ["git", "-C", repo_path, "log", "--pretty=format:%an|%ae|%ad", "--date=iso"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    logs = result.stdout.splitlines()

    # Process logs to extract time zone
    processed_logs = []
    for log in logs:
        try:
            author, email, date_time = log.split("|")
            date_parts = date_time.strip().rsplit(
                " ", 1
            )  # Split date_time by the last space
            date = date_parts[0]  # Extract the date and time
            timezone = (
                date_parts[1] if len(date_parts) > 1 else "UNKNOWN"
            )  # Extract the timezone
            processed_logs.append(f"{author}|{email}|{date}|{timezone}")
        except ValueError:
            continue  # Skip malformed logs
    return processed_logs


def parse_logs(logs, include_email=True):
    """
    Parse Git logs to extract relevant information.
    """
    data = []
    for log in logs:
        try:
            author, email, date, timezone = log.split("|")
            commit_date = datetime.fromisoformat(date.strip())
            entry = {
                "author": author.strip(),
                "date": commit_date,
                "timezone": timezone.strip(),
            }
            if include_email:
                entry["email"] = email.strip()
            data.append(entry)
        except ValueError:
            continue  # Skip malformed logs
    return pd.DataFrame(data)


def analyze_timezones(df, threshold):
    """
    Analyze timezones and detect frequent changes.
    """
    group_cols = ["author"]
    if "email" in df.columns:
        group_cols.append("email")

    grouped = df.groupby(group_cols)
    analysis = []

    for group_key, group in grouped:
        group = group.sort_values("date")
        timezones = group["timezone"].tolist()
        unique_timezones = set(timezones)
        timezone_changes = sum(
            1 for i in range(1, len(timezones)) if timezones[i] != timezones[i - 1]
        )

        analysis_entry = {
            "author": group_key[0],
            "total_commits": len(group),
            "unique_timezones": len(unique_timezones),
            "timezone_changes": timezone_changes,
            "suspicious": timezone_changes > threshold,
        }
        if "email" in df.columns:
            analysis_entry["email"] = group_key[1]
        analysis.append(analysis_entry)

    return pd.DataFrame(analysis)


def is_git_repository(path):
    """
    Check if the given path is a Git repository.
    """
    try:
        subprocess.run(
            ["git", "-C", path, "rev-parse"], check=True, capture_output=True, text=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def clone_repo(remote_url):
    """
    Clone the remote Git repository into a temporary directory.
    """
    temp_dir = tempfile.mkdtemp()
    subprocess.run(["git", "clone", remote_url, temp_dir], check=True)
    return temp_dir


def calculate_suspicious_changes(df, time_threshold, distance_threshold):
    """
    Analyze timezone changes and mark suspicious patterns.

    Args:
        df (pd.DataFrame): DataFrame containing timezone change data.
        time_threshold (int): Maximum allowed hours between timezone changes.
        distance_threshold (int): Maximum allowed timezone offset difference.

    Returns:
        pd.DataFrame: DataFrame with an additional 'suspicious' column.
    """
    # Ensure datetime columns are properly converted
    df["previous_date"] = pd.to_datetime(df["previous_date"])
    df["current_date"] = pd.to_datetime(df["current_date"])

    # Calculate time difference between changes (in hours)
    df["time_difference"] = (
        df["current_date"] - df["previous_date"]
    ).dt.total_seconds() / 3600

    # Calculate timezone offset differences
    df["timezone_difference"] = df.apply(
        lambda row: abs(int(row["current_timezone"]) - int(row["previous_timezone"]))
        / 100,
        axis=1,
    )

    # Mark changes as suspicious based on thresholds
    df["suspicious"] = (
        df["time_difference"] <= time_threshold
    ) & (  # Time between changes is too short
        df["timezone_difference"] >= distance_threshold
    )  # Distance between timezones is too large

    return df
