import argparse
import logging
import os
import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from datetime import datetime

import pandas as pd

import defected.api as dapi

logger = logging.getLogger(__name__)

command_description = """
Inspect commits from a specific user.
"""
long_description = """
Inspect commits from a specific user and provide detailed timezone information.
"""


def add_arguments(parser):
    """
    Adds the argument options to the extract command parser.
    """
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.description = long_description

    parser.add_argument(
        "--repo", type=str, help="Remote Git repository URL to clone and analyze."
    )
    parser.add_argument(
        "--user", type=str, default="", help="Specify the user by name."
    )
    parser.add_argument(
        "--email", type=str, default="", help="Specify the user by email."
    )
    parser.add_argument(
        "--threshold", type=int, default=2, help="Threshold for timezone changes."
    )
    parser.add_argument(
        "--max-threshold",
        type=int,
        default=24,
        help="Maximum allowed hours between timezone changes to be seen as suspicious.",
    )
    parser.add_argument(
        "--max-distance",
        type=int,
        default=5,
        help="Maximum allowed timezone offset difference.",
    )
    parser.add_argument(
        "--output", type=str, default="inspect_results.csv", help="Output file."
    )
    parser.add_argument(
        "--only-suspicious",
        action="store_true",
        help="Show and save only suspicious results (default: show all results).",
    )


def main(args):
    repo_path = None
    temp_dir = None
    try:
        if args.repo:
            print(f"Cloning remote repository: {args.repo}...")
            repo_path = dapi.clone_repo(args.repo)
        else:
            repo_path = os.getcwd()
            if not dapi.is_git_repository(repo_path):
                raise ValueError(
                    f"The current directory '{repo_path}' is not a Git repository."
                )

        print("Extracting Git logs...")
        logs = dapi.extract_git_logs(repo_path)
        print(f"{len(logs)} commits extracted.")
        df = dapi.parse_logs(logs)

        # Filter by user or email
        user = None
        email = None
        if args.user:
            df = df[df["author"] == args.user]
            user = args.user
        elif args.email:
            df = df[df["email"] == args.email]
            email = args.email

        if df.empty:
            print(f"No commits found for the specified user: {user or email}")
            return

        print(f"\nCommits found for {user or email}: {len(df)}")

        # Analyze the filtered data
        result = dapi.analyze_timezones(df, args.threshold)

        # Generate timezone usage report
        timezone_usage = df["timezone"].value_counts().reset_index()
        timezone_usage.columns = ["timezone", "commit_count"]

        # Generate timezone change log
        df = df.sort_values("date")
        timezone_changes = []
        previous_row = None
        for index, row in df.iterrows():
            if previous_row is not None and row["timezone"] != previous_row["timezone"]:
                timezone_changes.append(
                    {
                        "previous_date": previous_row["date"],
                        "previous_timezone": previous_row["timezone"],
                        "current_date": row["date"],
                        "current_timezone": row["timezone"],
                    }
                )
            previous_row = row

        timezone_changes_df = pd.DataFrame(timezone_changes)

        # Calculate suspicious changes
        if not timezone_changes_df.empty:
            timezone_changes_df = dapi.calculate_suspicious_changes(
                timezone_changes_df, args.max_threshold, args.max_distance
            )

        # Display results
        print("\nTimezone usage:")
        print(timezone_usage)

        print("\nTimezone change log:")
        for _, change in timezone_changes_df.iterrows():
            suspicious_flag = " (SUSPICIOUS)" if change["suspicious"] else ""
            if args.only_suspicious and not change["suspicious"]:
                continue

            print(
                f"From {change['previous_timezone']} at {change['previous_date']} "
                f"to {change['current_timezone']} at {change['current_date']}{suspicious_flag}"
            )

        # Save results to CSV
        timezone_usage.to_csv(args.output.replace(".csv", "_usage.csv"), index=False)
        timezone_changes_df.to_csv(
            args.output.replace(".csv", "_changes.csv"), index=False
        )
        print(
            f"\nDetailed results saved to '{args.output.replace('.csv', '_usage.csv')}' and '{args.output.replace('.csv', '_changes.csv')}'."
        )

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if temp_dir:
            print("Cleaning up temporary files...")
            shutil.rmtree(temp_dir)
