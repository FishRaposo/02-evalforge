PYTHON			:= python
PIP				:= pip

.PHONY: help install test lint format clean setup eval-basic eval-citation eval-compliance eval-all

help:
	@echo "EvalForge - Available targets:"
	@echo ""
	@echo "  install          Install package with dev dependencies"
	@echo "  test             Run pytest with coverage"
	@echo "  lint             Run ruff check + mypy"
	@echo "  format           Run ruff format"
	@echo "  clean            Remove build artifacts and caches"
	@echo "  setup            First-time setup (install + verify)"
	@echo "  eval-basic       Run rag_basic example suite"
	@echo "  eval-citation    Run rag_citation example suite"
	@echo "  eval-compliance  Run compliance example suite"
	@echo "  eval-all         Run all example suites"

install:
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest --cov=evalforge --cov-report=term-missing -v

lint:
	ruff check . && mypy evalforge

format:
	ruff format .

clean:
	$(PYTHON) -c "import shutil, glob; dirs = glob.glob('**/__pycache__', recursive=True) + glob.glob('**/.pytest_cache', recursive=True) + glob.glob('**/*.egg-info', recursive=True); [shutil.rmtree(d) for d in dirs if __import__('pathlib').Path(d).exists()]"
	$(PYTHON) -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('.coverage')]"
	rm -rf reports/

setup: install test

eval-basic:
	evalforge eval example_suites/rag_basic.yaml --format markdown

eval-citation:
	evalforge eval example_suites/rag_citation.yaml --format json

eval-compliance:
	evalforge eval example_suites/compliance.yaml --format html

eval-all: eval-basic eval-citation eval-compliance
