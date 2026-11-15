# Using the Qaroshi offline wiki

Open `Qaroshi_Wiki.html` directly in a current browser. Nothing needs an account or network connection.

The left sidebar browses topics and 70 grammar chapters. The top search looks through dictionary definitions, grammar and sentence examples. Press `/` to focus search. Press Escape to close the mobile sidebar. Browse the Dictionary page for detailed filters; it searches English meanings and Qaroshi spelling, including unaccented search approximations such as `gero` → `gëro`.

Open a word to see its definition, prominent English-style sound-out, broad IPA, native script, grammatical metadata, example sentences, related terms, and clickable components (when it is a compound). Extended letter-by-letter pronunciation can be opened from a details control.

The Native script page converts **Romanized Qaroshi into handwritten glyphs**, not English into Qaroshi; it can export PNG. The Latin A–Z guide describes English letter-name pronunciations separately from native Qaroshi phonemes. The moon/sun button switches appearance without connecting to a service.

The CSV, JSON, and Markdown files in the package are suitable for editing or further linguistic analysis. Build the standalone HTML with `python tools/build_wiki.py` after changing reference files.
