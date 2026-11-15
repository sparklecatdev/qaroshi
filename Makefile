.PHONY: build test
build:
	python tools/build_wiki.py
test:
	python -m unittest discover -s tests -v
