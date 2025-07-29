# Makefile for Helm Repository Management

.PHONY: fetch index clean

setup:
	@uv sync

fetch:
	@uv run scripts/fetch.py

index:
	@uv run scripts/build-index.py

clean:
	@rm -rf index