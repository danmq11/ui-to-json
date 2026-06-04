#!/usr/bin/env python
"""
Validate every worked-example JSON block in the reference files against
references/schema.json. Run after editing the skill to catch regressions.

Usage:
    python scripts/validate.py

Exit code 0 = all examples valid; 1 = at least one failure or schema error.
Requires the `jsonschema` package for deep validation; without it, falls back
to plain JSON.parse checks and warns.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REFS = os.path.join(ROOT, "references")
SCHEMA_PATH = os.path.join(REFS, "schema.json")

PLACEHOLDER = re.compile(r"\.\.\.|…")


def json_blocks(text):
    """Yield fenced ```json blocks that look like complete objects (no placeholders)."""
    for block in re.findall(r"```json\n(.*?)```", text, re.S):
        s = block.strip()
        if s.startswith("{") and not PLACEHOLDER.search(s):
            yield s


def main():
    failures = 0
    checked = 0

    try:
        schema = json.load(open(SCHEMA_PATH, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"[FATAL] schema.json is not valid JSON: {e}")
        return 1

    try:
        import jsonschema
        validator = jsonschema.Draft7Validator(schema)
        deep = True
    except ImportError:
        print("[warn] jsonschema not installed — doing JSON.parse checks only "
              "(`pip install jsonschema` for full schema validation)")
        deep = False

    md_files = sorted(f for f in os.listdir(REFS) if f.endswith(".md"))
    for fname in md_files:
        text = open(os.path.join(REFS, fname), encoding="utf-8").read()
        for s in json_blocks(text):
            checked += 1
            try:
                obj = json.loads(s)
            except json.JSONDecodeError as e:
                failures += 1
                print(f"[FAIL] {fname}: invalid JSON — {e}")
                continue
            if deep:
                errs = sorted(validator.iter_errors(obj), key=lambda e: e.path)
                if errs:
                    failures += 1
                    loc = obj.get("mode", obj.get("batch", "?"))
                    print(f"[FAIL] {fname} ({loc}): {errs[0].message}")
                    continue
            print(f"[ok]   {fname}: {obj.get('mode', 'batch')} example valid")

    print(f"\n{checked} example(s) checked, {failures} failure(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
