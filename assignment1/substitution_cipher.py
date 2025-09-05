"""
Simple Substitution Cipher implementation

Features:
- Generate a random 26-letter key (permutation of A-Z)
- Encrypt and decrypt preserving case and non-letter characters
- Validate keys
- Command-line interface for quick use

Usage examples:
python substitution_cipher.py --gen          # prints a generated key
python substitution_cipher.py --key KEY --encrypt "Hello, World!"
python substitution_cipher.py --key KEY --decrypt "...ciphertext..."
"""

from __future__ import annotations

import argparse
import random
import string
import sys
from typing import Dict, Optional

ALPHABET = string.ascii_uppercase


class SubstitutionCipher:
    """Substitution cipher using a key which is a 26-character permutation of A-Z.

    The key maps ALPHABET -> key. For example, if key[0] == 'Q', then 'A' -> 'Q'.
    Encryption preserves case; non-letters are left unchanged.
    """

    def __init__(self, key: Optional[str] = None):
        if key is None:
            key = self.generate_key()
        key = key.upper()
        if not self._is_valid_key(key):
            raise ValueError("Key must be a 26-character permutation of A-Z")
        self.key = key
        self._enc_map = self._build_enc_map()
        self._dec_map = {v: k for k, v in self._enc_map.items()}

    @staticmethod
    def generate_key() -> str:
        """Return a random 26-letter key (permutation of A-Z)."""
        letters = list(ALPHABET)
        random.shuffle(letters)
        return "".join(letters)

    @staticmethod
    def _is_valid_key(key: str) -> bool:
        return len(key) == 26 and set(key) == set(ALPHABET)

    def _build_enc_map(self) -> Dict[str, str]:
        return {ALPHABET[i]: self.key[i] for i in range(26)}

    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext using the substitution key."""
        out_chars = []
        for ch in plaintext:
            if ch.isalpha():
                if ch.isupper():
                    out_chars.append(self._enc_map.get(ch, ch))
                else:
                    # lowercase
                    mapped = self._enc_map.get(ch.upper(), ch.upper())
                    out_chars.append(mapped.lower())
            else:
                out_chars.append(ch)
        return "".join(out_chars)

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt ciphertext using the inverse key."""
        out_chars = []
        for ch in ciphertext:
            if ch.isalpha():
                if ch.isupper():
                    out_chars.append(self._dec_map.get(ch, ch))
                else:
                    mapped = self._dec_map.get(ch.upper(), ch.upper())
                    out_chars.append(mapped.lower())
            else:
                out_chars.append(ch)
        return "".join(out_chars)

    def key_string(self) -> str:
        return self.key


def _parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Substitution cipher CLI")
    group = p.add_mutually_exclusive_group(required=False)
    group.add_argument("--gen", action="store_true", help="Generate and print a random key")
    p.add_argument("--key", type=str, help="26-letter key (permutation of A-Z)")
    # mode flags: choose one
    p.add_argument("--encrypt", action="store_true", help="Encrypt the provided input")
    p.add_argument("--decrypt", action="store_true", help="Decrypt the provided input")
    # input source: mutually exclusive
    input_group = p.add_mutually_exclusive_group(required=False)
    input_group.add_argument("--text", type=str, help="Text to encrypt/decrypt")
    input_group.add_argument("--file", type=str, help="Path to a file to read input from")
    input_group.add_argument("--stdin", action="store_true", help="Read input from stdin")
    return p.parse_args(argv)


def main(argv: Optional[list] = None) -> int:
    args = _parse_args(argv)

    if args.gen:
        print(SubstitutionCipher.generate_key())
        return 0

    if not args.key:
        print("Error: --key is required unless --gen is used", file=sys.stderr)
        return 2

    try:
        cipher = SubstitutionCipher(args.key)
    except ValueError as e:
        print(f"Invalid key: {e}", file=sys.stderr)
        return 2

    # Require exactly one of encrypt/decrypt
    if bool(args.encrypt) == bool(args.decrypt):
        print("Error: either --encrypt or --decrypt must be specified (but not both)", file=sys.stderr)
        return 2

    # Read input from the chosen source
    if args.text is not None:
        data = args.text
    elif args.file is not None:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                data = fh.read()
        except Exception as e:
            print(f"Failed to read file: {e}", file=sys.stderr)
            return 2
    elif args.stdin:
        data = sys.stdin.read()
    else:
        print("Error: no input provided. Use --text, --file or --stdin", file=sys.stderr)
        return 2

    if args.encrypt:
        print(cipher.encrypt(data))
    else:
        print(cipher.decrypt(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
