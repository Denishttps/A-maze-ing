SRC_DIR = src
MAIN    = $(SRC_DIR)/a_maze_ing.py
CONFIG  = config.txt

.PHONY: all install run debug lint lint-strict clean

all: install

install:
	uv sync

run:
	uv run python $(MAIN) $(CONFIG)

debug:
	uv run python -m pdb $(MAIN) $(CONFIG)

lint:
	uv run flake8 $(SRC_DIR)
	uv run mypy $(SRC_DIR) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--explicit-package-bases

lint-strict:
	uv run flake8 $(SRC_DIR)
	uv run mypy $(SRC_DIR) --strict --explicit-package-bases

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc"       -delete
	find . -type f -name "*.pyo"       -delete