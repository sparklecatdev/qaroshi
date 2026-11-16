.PHONY: build test standard8
standard8:
	python tools/standard_8/build_standard.py
build: standard8
	python tools/build_wiki.py
	python tools/build_academy.py
	python tools/v17/build_practical.py
test:
	python -m unittest discover -s tests -v
