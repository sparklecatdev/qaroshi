.PHONY: build test standard8 stress82 stress83
standard8:
	python tools/standard_8/build_standard.py
stress82: standard8
	python tools/stress82/build_review.py
stress83: stress82
	python tools/stress83/complete.py
build: standard8
	python tools/build_wiki.py
	python tools/build_academy.py
	python tools/v17/build_practical.py
test:
	python -m unittest discover -s tests -v
