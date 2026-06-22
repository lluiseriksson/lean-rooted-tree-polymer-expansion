SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

PYTHON ?= python3
ORACLE_LOG ?= .oracle.log

.PHONY: all verify prepare lean docs docs-setup docs-serve static lock-refresh \
        manifest package package-determinism verify-package release clean

all: verify

verify: lean docs static

prepare:
	$(PYTHON) scripts/assemble_paper.py

lean:
	lake build MarkedRootedClosure
	@set -o pipefail; lake env lean MarkedRootedClosure/Oracle.lean | tee $(ORACLE_LOG)
	$(PYTHON) scripts/check_oracle_output.py $(ORACLE_LOG)
	@rm -f $(ORACLE_LOG)
	@if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then \
		git diff --exit-code -- lake-manifest.json; \
	fi

lock-refresh:
	lake update
	$(PYTHON) scripts/check_lake_lock.py
	@printf '%s\n' 'Review the full lake-manifest.json diff before committing.'

docs: prepare
	bash scripts/build_docs.sh

docs-setup:
	$(PYTHON) -m venv .venv-docs
	.venv-docs/bin/python -m pip install --disable-pip-version-check -r requirements-docs.txt

docs-serve: prepare
	@if [ -x .venv-docs/bin/python ]; then \
		.venv-docs/bin/python -m mkdocs serve; \
	else \
		$(PYTHON) -m mkdocs serve; \
	fi

static: prepare
	bash scripts/check_no_placeholders.sh
	$(PYTHON) scripts/check_project_identity.py
	$(PYTHON) scripts/check_lake_lock.py
	$(PYTHON) scripts/check_paper_manifest.py
	$(PYTHON) scripts/check_artifact.py
	$(PYTHON) scripts/check_internal_links.py
	@if [ -x .venv-docs/bin/python ]; then \
		.venv-docs/bin/python scripts/check_metadata.py; \
	else \
		$(PYTHON) scripts/check_metadata.py; \
	fi

manifest:
	$(PYTHON) scripts/generate_manifest.py

package: static docs manifest
	$(PYTHON) scripts/make_release.py
	$(PYTHON) scripts/generate_sbom.py
	$(PYTHON) scripts/verify_release.py

package-determinism: static docs manifest
	$(PYTHON) scripts/check_release_determinism.py
	$(PYTHON) scripts/generate_sbom.py
	$(PYTHON) scripts/verify_release.py

verify-package: package-determinism

release: lean package-determinism

clean:
	lake clean || true
	rm -rf site release .venv .venv-docs docs/generated $(ORACLE_LOG) __pycache__
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
