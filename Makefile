POETRY_VERSION=2.0.0
POETRY ?= $(shell if [ -x /opt/homebrew/bin/poetry ]; then echo /opt/homebrew/bin/poetry; elif [ -x /usr/local/bin/poetry ]; then echo /usr/local/bin/poetry; else command -v poetry; fi)

.PHONY: all
.DEFAULT_GOAL=help

.PHONY: clean
clean:
	rm -rf __pycache__ 
	rm -rf .pytest_cache 
	rm -rf .coverage 
	rm -rf reports
	rm -rf dist 
	rm -rf requirements.txt
	rm -rf build 

.PHONY: distclean
distclean: clean
	- rm -rf .venv

.PHONY: build
build:
	$(POETRY) install

.PHONY: update
update:
	$(POETRY) update

.PHONY: precommit
precommit:
	pre-commit install
	pre-commit run --all-files


.PHONY: test
test:
	$(POETRY) run pytest

.PHONY: cover
cover:
	mkdir -p reports
	$(POETRY) run pytest --junitxml reports/xunit.xml

.PHONY: coverage-check
coverage-check:
	mkdir -p reports
	$(POETRY) run pytest --cov-fail-under=90

.PHONY: package
package: ## Create deployable whl package for python3 project
	@if grep -q 'package-mode = false' pyproject.toml; then \
		echo "Skipping package build: package-mode is false in pyproject.toml"; \
	else \
		$(POETRY) build --format=wheel; \
	fi

.PHONY: ci
ci: clean build test coverage-check cover package ## Runs clean, build, test, coverage checks and package

.PHONY: format
format: ## Formats the python3 files
	ruff format

.PHONY: lint
lint: ## Lints the python3 files
	ruff check .

.PHONY: help
help: ## Show this help
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF\
	}' $(MAKEFILE_LIST)
