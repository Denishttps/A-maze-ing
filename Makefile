PY  := python3
URU  := uv run
CFG ?= config.txt
OUT ?= maze.txt
MAZE := src/a_maze_ing.py

install:
	uv sync

run:
	$(URU) $(PY) $(MAZE) $(CFG)

test:
	$(URU) pytest -v tests/

debug:
	$(URU) $(PY) -m pdb $(MAZE) $(CFG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache

output:
	$(URU) $(PY) $(MAZE) $(CFG)
	@echo
	@echo "----- $(OUT) -----"
	@cat $(OUT)

lint:
# 	$(URU) flake8 src/
	$(URU) mypy src/ --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(URU) flake8 .
	$(URU) mypy . --strict

.PHONY: install run test debug clean lint lint-strict output
