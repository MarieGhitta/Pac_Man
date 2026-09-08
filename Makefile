MAIN := pac-man.py
CONFIG := config.json

.PHONY: install uninstall run debug clean lint lint-strict

install:
	uv sync

uninstall:
	rm -rf .venv

run:
	uv run $(MAIN) $(CONFIG)

debug:
	uv run -m pdb $(MAIN) $(CONFIG)

lint:
	uv run flake8 .
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	find . -type f -name '*.py[co]' -delete
