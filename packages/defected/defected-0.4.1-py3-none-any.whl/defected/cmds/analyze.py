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
Analyze Git logs for timezone changes and suspicious activities.
"""
long_description = """
Analyze Git logs for timezone changes and suspicious activities.
"""


def add_arguments(parser):
    """
    Adds the argument options to the extract command parser.
    """
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.description = long_description

    parser.add_argument(
        "--repo",
        type=str,
        help="Remote Git repository URL to clone and analyze. If not provided, the current directory will be analyzed.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=2,
        help="Number of timezone changes considered suspicious (default: 2).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="timezone_analysis.csv",
        help="Output file for the analysis (default: timezone_analysis.csv).",
    )
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="Disable inclusion of contributor email addresses in the analysis.",
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

        print("Parsing logs...")
        df = dapi.parse_logs(logs, include_email=not args.no_email)
        if df.empty:
            print("No valid logs found.")
            return

        print(
            f"Analyzing timezones with a threshold of {args.threshold} timezone changes..."
        )
        analysis = dapi.analyze_timezones(df, args.threshold)

        if args.only_suspicious:
            analysis = analysis[analysis["suspicious"]]
            print("\nShowing only suspicious results:")

        print(analysis.sort_values("timezone_changes", ascending=False))

        print(f"\nSaving analysis to '{args.output}'...")
        analysis.to_csv(args.output, index=False)
        print("Analysis saved.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if temp_dir:
            print("Cleaning up temporary files...")
            shutil.rmtree(temp_dir)
