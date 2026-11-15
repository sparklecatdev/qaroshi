.PHONY: build test
build:
	python tools/build_wiki.py
	python tools/build_academy.py
	python tools/v17/build_practical.py
test:
	python -m unittest discover -s tests -v
