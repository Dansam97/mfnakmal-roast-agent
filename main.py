#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun bounty entry.

Writes one single-line roast of my own AI agent to entry.txt in the
output directory (env MAKEFUN_OUTPUT_DIR, default /output).
Standard library only, no network, fully deterministic.
"""

import os

TEXT = (
    "My agent asks my permission to delete one empty file, then rebuilds "
    "the entire production database on its own at 3 a.m. and titles the "
    "pull request 'minor cleanup'."
)


def validated_text() -> str:
    """Return TEXT after checking it against the bounty gate.

    The gate takes UTF-8 text of 1 to 200 characters, not only white
    space, as a single line. Fail loudly here rather than write an
    entry the sealed scorer would mark invalid.
    """
    encoded = TEXT.encode("utf-8")
    if encoded.decode("utf-8") != TEXT:
        raise ValueError("entry text does not round-trip as UTF-8")
    if not 1 <= len(TEXT) <= 200:
        raise ValueError("entry text must be 1 to 200 characters")
    if not TEXT.strip():
        raise ValueError("entry text must not be only white space")
    if "\n" in TEXT or "\r" in TEXT:
        raise ValueError("entry text must be exactly one line")
    return TEXT


def main() -> None:
    text = validated_text()
    payload = (text + "\n").encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(payload)
    with open(path, "rb") as fh:
        if fh.read() != payload:
            raise ValueError("written entry does not match the payload")


if __name__ == "__main__":
    main()
