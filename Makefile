.PHONY: all verify lean docs docs-setup docs-serve static manifest package verify-package release clean

all: verify

verify: lean docs static

lean:
	lake update
	lake build MarkedRootedClosure
	lake env lean MarkedRootedClosure/Oracle.lean

docs:
	bash scripts/build_docs.sh

docs-setup:
	python3 -m venv .venv-docs
	.venv-docs/bin/python -m pip install --disable-pip-version-check -r requirements-docs.txt

docs-serve:
	@if [ -x .venv-docs/bin/python ]; then \
		.venv-docs/bin/python -m mkdocs serve; \
	else \
		python3 -m mkdocs serve; \
	fi

static:
	bash scripts/check_no_placeholders.sh
	python3 scripts/check_artifact.py
	python3 scripts/check_internal_links.py
	@if [ -x .venv-docs/bin/python ]; then \
		.venv-docs/bin/python scripts/check_metadata.py; \
	else \
		python3 scripts/check_metadata.py; \
	fi

manifest:
	python3 scripts/generate_manifest.py

package: static docs manifest
	python3 scripts/make_release.py
	python3 scripts/verify_release.py

verify-package: package

release: lean package

clean:
	lake clean || true
	rm -rf site release .venv .venv-docs __pycache__
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
