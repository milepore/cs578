"""
Letter frequency counter for English letters A-Z.

Usage examples:
python letter_frequency.py --text "Hello, World!"
python letter_frequency.py --file path/to/file.txt
cat file.txt | python letter_frequency.py --stdin

The script prints counts and percentages for each letter A-Z, case-insensitive.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from typing import Dict, Tuple

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_letter_frequency(text: str) -> Dict[str, Tuple[int, float]]:
    """Return a dictionary mapping each uppercase letter A-Z to (count, percent).

    Percent is the percentage of all letters (0-100). If there are no letters,
    percent will be 0.0 for all letters.
    """
    text = text.upper()
    counts = Counter(ch for ch in text if ch.isalpha())
    total_letters = sum(counts.get(ch, 0) for ch in ALPHABET)

    freq: Dict[str, Tuple[int, float]] = {}
    for ch in ALPHABET:
        cnt = counts.get(ch, 0)
        pct = (cnt / total_letters * 100.0) if total_letters > 0 else 0.0
        freq[ch] = (cnt, pct)
    return freq


def _parse_args(argv: list | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Compute letter frequency for A-Z")
    group = p.add_mutually_exclusive_group(required=False)
    group.add_argument("--text", type=str, help="Text to analyze (prefer quoting) ")
    group.add_argument("--file", type=str, help="Path to a file to analyze")
    group.add_argument("--stdin", action="store_true", help="Read text from stdin")
    p.add_argument("--top", type=int, default=0, help="Show only top N letters by count (0 = show all)")
    return p.parse_args(argv)


def print_frequency(freq: Dict[str, Tuple[int, float]], top: int = 0) -> None:
    items = list(freq.items())
    # Sort by count desc, then letter asc
    items.sort(key=lambda kv: (-kv[1][0], kv[0]))
    if top > 0:
        items = items[:top]

    # Print header
    print(f"Total distinct letters shown: {len(items)}")
    print("Letter  Count  Percent")
    print("------  -----  -------")
    for ch, (cnt, pct) in items:
        print(f"{ch:>6}  {cnt:5d}  {pct:7.2f}%")


def main(argv: list | None = None) -> int:
    args = _parse_args(argv)

    text = ""
    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                text = fh.read()
        except Exception as e:
            print(f"Failed to read file: {e}", file=sys.stderr)
            return 2
    elif args.text is not None:
        text = args.text
    else:
        print("No input specified. Use --text, --file, or --stdin", file=sys.stderr)
        return 2

    freq = get_letter_frequency(text)
    print(f"Total letters: {sum(cnt for cnt, _ in freq.values())}")
    print_frequency(freq, top=args.top)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
