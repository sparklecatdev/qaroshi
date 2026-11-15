.PHONY: build test validate
build:
	python tools/build_lexicon_v3.py
	python tools/build_metadata.py
	python tools/build_corpus_v3.py
	python tools/build_dictionary_site.py

test:
	python -m unittest discover -s tests -v

validate:
	python tools/qaroshi.py validate
