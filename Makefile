SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

PYTHON ?= python3
ORACLE_LOG ?= .oracle.log
LEAN_BUILD_TIMEOUT ?= 3600
LEAN_ORACLE_TIMEOUT ?= 600
LAKE_UPDATE_TIMEOUT ?= 1800
LAKE_CLEAN_TIMEOUT ?= 300

.PHONY: all verify verify-nonlean preflight prepare test syntax lean lean-build \
        lean-oracle docs docs-setup docs-serve static lock-refresh manifest \
        evidence package package-determinism smoke-release verify-package \
        release clean

all: verify

# Recursive invocations keep the gates ordered even when a caller supplies -j.
verify:
	$(MAKE) verify-nonlean
	$(MAKE) lean

verify-nonlean:
	$(MAKE) test
	$(MAKE) syntax
	$(MAKE) docs
	$(MAKE) static

preflight: verify-nonlean

prepare:
	$(PYTHON) scripts/assemble_paper.py

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

syntax:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m compileall -q scripts tests
	bash -n scripts/*.sh

lean:
	$(MAKE) lean-build
	$(MAKE) lean-oracle

lean-build:
	LEAN_BUILD_TIMEOUT="$(LEAN_BUILD_TIMEOUT)" \
		$(PYTHON) scripts/run_lean_gate.py build

lean-oracle:
	LEAN_ORACLE_TIMEOUT="$(LEAN_ORACLE_TIMEOUT)" \
		$(PYTHON) scripts/run_lean_gate.py oracle --oracle-log "$(ORACLE_LOG)"

lock-refresh:
	$(PYTHON) scripts/process_runner.py --timeout "$(LAKE_UPDATE_TIMEOUT)" -- lake update
	$(PYTHON) scripts/check_lake_lock.py
	@printf '%s\n' 'Review the full lake-manifest.json diff before committing.'

docs: prepare
	bash scripts/build_docs.sh

docs-setup:
	$(PYTHON) -m venv .venv-docs
	.venv-docs/bin/python -m pip install --disable-pip-version-check -r requirements-docs.lock
	.venv-docs/bin/python -m pip check

docs-serve: prepare
	@if [ -x .venv-docs/bin/python ]; then \
		.venv-docs/bin/python -m mkdocs serve; \
	else \
		$(PYTHON) -m mkdocs serve; \
	fi

static: prepare
	bash scripts/check_no_placeholders.sh
	$(PYTHON) scripts/check_project_identity.py
	$(PYTHON) scripts/check_version_consistency.py
	$(PYTHON) scripts/check_python_lock.py
	$(PYTHON) scripts/check_lake_lock.py
	$(PYTHON) scripts/check_source_manifest.py
	$(PYTHON) scripts/check_paper_manifest.py
	$(PYTHON) scripts/check_theorem_manifest.py
	$(PYTHON) scripts/check_proof_dag.py
	$(PYTHON) scripts/check_references.py
	$(PYTHON) scripts/check_agent_index.py
	$(PYTHON) scripts/check_workflows.py
	$(PYTHON) scripts/check_artifact.py
	$(PYTHON) scripts/check_internal_links.py
	$(PYTHON) scripts/check_accessibility.py
	@if [ -x .venv-docs/bin/python ]; then \
		.venv-docs/bin/python scripts/check_metadata.py; \
	else \
		$(PYTHON) scripts/check_metadata.py; \
	fi

manifest:
	$(PYTHON) scripts/generate_manifest.py

evidence:
	$(PYTHON) scripts/generate_sbom.py
	$(PYTHON) scripts/generate_cyclonedx.py
	$(PYTHON) scripts/generate_buildinfo.py
	$(PYTHON) scripts/generate_provenance.py
	$(PYTHON) scripts/generate_release_index.py

package:
	$(MAKE) verify-nonlean
	$(MAKE) manifest
	$(PYTHON) scripts/make_release.py
	$(MAKE) evidence
	$(PYTHON) scripts/verify_release.py
	$(PYTHON) scripts/smoke_test_release.py

package-determinism:
	$(MAKE) verify-nonlean
	$(MAKE) manifest
	$(PYTHON) scripts/check_release_determinism.py
	$(MAKE) evidence
	$(PYTHON) scripts/verify_release.py
	$(PYTHON) scripts/smoke_test_release.py

smoke-release:
	$(PYTHON) scripts/smoke_test_release.py

verify-package: package-determinism

release:
	$(MAKE) lean
	$(MAKE) package-determinism

clean:
	-$(PYTHON) scripts/process_runner.py --timeout "$(LAKE_CLEAN_TIMEOUT)" -- lake clean
	rm -rf site release .venv .venv-docs docs/generated $(ORACLE_LOG) __pycache__
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
