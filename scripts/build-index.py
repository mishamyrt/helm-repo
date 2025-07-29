#!/usr/bin/env python3
"""
This script packages charts found in the 'charts' directory that are also defined in
the chart-sources.yaml manifest, and then generates a Helm repository index.
"""

import os
import subprocess

from config import load_config, Configuration


def _collect_charts(config: Configuration) -> list[str]:
    """
    Collects all charts from the sources defined in the configuration.
    """
    charts = []
    for source in config.sources:
        for chart in source["charts"]:
            path = os.path.join(config.target, chart["name"])
            if os.path.isdir(path):
                charts.append(path)
            else:
                print(f"Warning: Chart '{chart['name']}' not found at '{path}'")
    return charts


def main():
    """
    Packages charts found in the 'charts' directory that are also defined in
    the chart-sources.yaml manifest, and then generates a Helm repository index.
    """
    config = load_config()

    charts_to_package = _collect_charts(config)
    if not charts_to_package:
        print("No charts found to package.")
        return

    print("Packaging the following charts:")
    for chart_path in charts_to_package:
        print(f"- {chart_path}")
        print(f"  Building dependencies for {chart_path}...")
        subprocess.run(["helm", "dependency", "build", chart_path], check=True)

        print(f"  Packaging {chart_path}...")
        subprocess.run(
            ["helm", "package", chart_path, "--destination", config.build], check=True
        )

    print("Generating repository index...")
    subprocess.run(["helm", "repo", "index", config.build, "--url", config.url], check=True)

    print("Index updated successfully.")


if __name__ == "__main__":
    main()
