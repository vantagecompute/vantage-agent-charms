SHELL:=/bin/bash
ROOT_DIR:=$(shell dirname $(shell pwd)).PHONY: help

.PHONY: lint
lint: ## Run linter
	tox -e lint

.PHONY: format
format: ## Run formatter
	tox -e format

.PHONY: static
static: ## Run static analysis
	tox -e static

.PHONY: qa
qa: lint static ## Run all quality checks

.PHONY: charm
charm: ## Pack the charm
	@git describe --tags --dirty --always > version
	@charmcraft pack

.PHONY: clean
clean: ## Remove build dirs, temp files, and charms
	@rm -rf lib/
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -type d -name "venv" -exec rm -rf {} +
	@find . -type d -name ".tox" -exec rm -rf {} +
	@find . -name "*.charm" -delete
	@find . -name "version" -delete
	@find . -name "*config*.yaml" -delete

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
