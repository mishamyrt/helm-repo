#!/usr/bin/env python3
"""
This script fetches charts from git repositories and moves them to the charts directory.
"""

import os
from shutil import move, rmtree
import subprocess
import tempfile

from config import Source, SourceType, load_config


def clone_git_repo(repo_url: str, version: str, target_dir: str) -> None:
    """
    Clones a git repository and checks out the specified version.
    """
    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", version, repo_url, target_dir],
        check=True,
    )


def fetch_git_source(source: Source, target_dir: str) -> None:
    """
    Fetches a chart from a git repository and moves it to the charts directory.
    """
    url = source["url"]
    charts = source["charts"]
    version = source["version"]

    print(f"Fetching charts from '{url}' with version '{version}'")

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_git_repo(url, version, temp_dir)

        for chart in charts:
            source_chart_path = os.path.join(temp_dir, chart["path"])
            target_chart_path = os.path.join(target_dir, chart["name"])
            rmtree(target_chart_path, ignore_errors=True)
            move(source_chart_path, target_chart_path)


def main():
    """
    Main function.
    """
    config = load_config()

    for source in config.sources:
        source_kind = source.get("kind", SourceType.GIT)
        if source_kind == SourceType.GIT:
            fetch_git_source(source, config.target)
        else:
            print(f"Skipping unsupported source kind: {source_kind}")


if __name__ == "__main__":
    main()
