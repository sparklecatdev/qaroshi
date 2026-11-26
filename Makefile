.PHONY: build test standard8 stress82 stress83 stress84 stress89 stress88 stress90 stress91 stress92 stress93 stress94
standard8:
	python tools/standard_8/build_standard.py
stress82: standard8
	python tools/stress82/build_review.py
stress83: stress82
	python tools/stress83/complete.py
stress84: stress83
	python tools/stress84/build_readiness.py
stress89: stress84
	python tools/stress89/compose.py
	python tools/stress89/audit.py
stress90: stress89
	python tools/stress90/compose.py
	python tools/stress90/audit.py
stress91: stress90
	python tools/stress91/compose.py
	python tools/stress91/audit.py
stress92: stress91
	python tools/stress92/build_grammar.py --check
	python tools/stress92/heldout.py
	python tools/stress92/semantic_audit.py
stress93: stress92
	python tools/grammar93/benchmark.py
stress94: stress93
	python tools/semantic94/complete.py
stress88: stress84
	python tools/stress88/compose.py
build: standard8
	python tools/build_wiki.py
	python tools/build_academy.py
	python tools/v17/build_practical.py
test: build
	node tools/standard10/gap_report.cjs --out data/standard10/generated
	python -m unittest discover -s tests -v
