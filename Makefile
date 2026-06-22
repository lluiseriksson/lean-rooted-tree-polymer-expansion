.PHONY: all lean paper audit clean release

all: lean paper audit

lean:
	lake update
	lake build MarkedRootedClosure
	lake env lean MarkedRootedClosure/Oracle.lean

paper:
	$(MAKE) -C paper

audit:
	bash scripts/check_no_placeholders.sh
	python3 scripts/check_artifact.py
	bash scripts/check_pdf.sh

release: all
	bash scripts/make_release.sh

clean:
	lake clean || true
	$(MAKE) -C paper clean
	rm -rf release
