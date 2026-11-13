#!/usr/bin/env python3
"""Checks that the prompt inside README.md / README.de.md matches PROMPT.md / PROMPT.de.md.

    python3 tools/check-readme.py          # exit 1 if they differ
    python3 tools/check-readme.py --fix    # copy the PROMPT files into the READMEs
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAIRS = (("PROMPT.md", "README.md"), ("PROMPT.de.md", "README.de.md"))
BLOCK = re.compile(r"(<!-- prompt:start -->\n```text\n)(.*?)(\n```\n<!-- prompt:end -->)", re.S)

bad = 0
for prompt_file, readme_file in PAIRS:
    prompt = open(os.path.join(ROOT, prompt_file), encoding="utf-8").read().rstrip()
    path = os.path.join(ROOT, readme_file)
    readme = open(path, encoding="utf-8").read()
    m = BLOCK.search(readme)
    if not m:
        print(f"{readme_file}: no <!-- prompt:start --> block"); bad += 1; continue
    if m.group(2) != prompt:
        if "--fix" in sys.argv:
            readme = readme[:m.start(2)] + prompt + readme[m.end(2):]
            open(path, "w", encoding="utf-8").write(readme)
            print(f"{readme_file}: updated from {prompt_file}")
        else:
            print(f"{readme_file}: prompt differs from {prompt_file}. Run: python3 tools/check-readme.py --fix"); bad += 1
sys.exit(1 if bad else 0)
