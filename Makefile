.PHONY: help build check test validate secret-scan install-hooks

UV ?= uv

help:
	@echo "  make build          render the public WKD files"
	@echo "  make validate       check the served tree and run tests"
	@echo "  make secret-scan    scan tracked files for secrets"
	@echo "  make install-hooks  activate local Git and JJ checks (optional)"

build:
	$(UV) run --locked python -B scripts/build-wkd.py

check:
	$(UV) run --locked python -B scripts/build-wkd.py --check

test:
	$(UV) run --locked python -B -m unittest discover -s tests

validate: check test

secret-scan:
	@bash .githooks/pre-commit --scan-only

install-hooks:
	git config core.hooksPath .githooks
	@if [ -d .jj ] && command -v jj >/dev/null 2>&1; then \
	    jj config set --repo aliases.push '["util","exec","--","bash","-c","exec bash \"$$(jj workspace root)/.githooks/jj-push\" \"$$@\"","jj-push"]'; \
	    echo "Use jj push to run checks before publication."; \
	elif [ -d .jj ]; then \
	    echo "JJ is unavailable. The optional push alias was not installed." >&2; \
	fi
