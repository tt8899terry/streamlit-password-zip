# GIT_COMMIT_HASH := $(shell git rev-list -1 HEAD)
# GIT_STATUS := $(shell git status -s | grep -q "^[ M]" && echo "DIRTY" || echo "CLEAN")
# NOTE: makefile must be defined using tabs not spaces otherwise `missing separator` errors may be emitted
# in VSCode check bottom right status bar next to the line and col number should be `Tab Size` if it says space tap it and change to tabs

.PHONY: run
run: ## run steamlit
	streamlit run main.py

	
# .PHONY: run-rerun
# run-rerun: ## run steamlit rerun when code change
# 	streamlit run main.py

.PHONY: run-viewer
run-viewer: ## run streamlit as viewer mode
	streamlit run --client.toolbarMode viewer main.py

.PHONY: run-local-env
run-local-env: ## run streamlitwith local virtual env
	mkdir .venv -p
	streamlit run main.py 

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help