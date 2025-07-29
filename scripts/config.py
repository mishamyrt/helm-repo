"""
Configuration for the Helm repository.
"""

from typing import TypedDict

import yaml

DEFAULT_CONFIG_PATH = "configuration.yaml"


class SourceType:
    """Chart source type"""

    GIT = "git"


class Chart(TypedDict):
    """Chart configuration"""

    name: str
    path: str


class Source(TypedDict):
    """Chart configuration"""

    kind: SourceType
    url: str
    version: str
    charts: list[Chart]


def _assert_source(source_like: Source):
    assert "kind" in source_like
    assert "url" in source_like
    assert "version" in source_like
    assert "charts" in source_like

    assert isinstance(source_like["kind"], str)
    assert isinstance(source_like["url"], str)
    assert source_like["url"] != ""

    assert isinstance(source_like["version"], str)
    assert source_like["version"] != ""

    assert isinstance(source_like["charts"], list)
    assert len(source_like["charts"]) > 0

    for chart in source_like["charts"]:
        assert isinstance(chart, dict)
        assert chart["name"] != ""
        assert chart["path"] != ""


def _parse_kind(kind: str) -> SourceType:
    if kind == SourceType.GIT:
        return SourceType.GIT
    else:
        raise ValueError(f"Invalid source kind: {kind}")


class Configuration:
    """Configuration for the Myrt Helm repository."""

    sources: list[Source]
    url: str
    target: str
    build: str

    def __init__(
        self,
        sources: list[Source],
        url: str,
        target: str,
        build: str,
    ):
        for source in sources:
            _assert_source(source)
            source["kind"] = _parse_kind(source["kind"])

        self.sources = sources
        self.url = url
        self.target = target
        self.build = build


def load_config(path: str = DEFAULT_CONFIG_PATH) -> Configuration:
    """Load the configuration from the file."""
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        return Configuration(
            sources=config["sources"],
            url=config["url"],
            target=config["target"],
            build=config["build"],
        )
