# Qaroshi Wiki · Release 17

The Qaroshi website includes a 30,000-entry dictionary, 4,383 examples, 90 grammar chapters, an Academy, and an everyday communicator with phrases, dialogues, and practice tools. The practical examples are editorial material, not speaker-attested. See the [release notes](RELEASE_17_NOTES.md).

The AI assistant requires an OpenRouter API key, saved in the browser.

To rebuild the GitHub Pages site, install Pillow and Mistune, then run:

```sh
python3 tools/build_wiki.py
python3 tools/build_academy.py
python3 tools/v17/build_practical.py
```
