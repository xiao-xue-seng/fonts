#!/usr/bin/env python3
"""Sync api/amec.json entries to api/fonts.json by id."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


def load_json_array(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"{path} entry at index {index} is not an object")
        if "id" not in item:
            raise ValueError(f"{path} entry at index {index} is missing 'id'")
        normalized.append(item)
    return normalized


def sync_amec_by_id(
    fonts: list[dict[str, Any]], amec: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    font_by_id = {item["id"]: deepcopy(item) for item in fonts}
    synced: list[dict[str, Any]] = []

    for item in amec:
        font_id = item["id"]
        if font_id not in font_by_id:
            continue
        synced.append(deepcopy(font_by_id[font_id]))

    return synced


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Use api/fonts.json as the canonical source and sync api/amec.json by 'id'."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root; defaults to the parent of this script.",
    )
    parser.add_argument(
        "--fonts",
        type=Path,
        default=None,
        help="Path to fonts.json (defaults to <root>/api/fonts.json).",
    )
    parser.add_argument(
        "--amec",
        type=Path,
        default=None,
        help="Path to amec.json (defaults to <root>/api/amec.json).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the synced result without writing the file.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    fonts_path = args.fonts.resolve() if args.fonts else root / "api" / "fonts.json"
    amec_path = args.amec.resolve() if args.amec else root / "api" / "amec.json"

    fonts = load_json_array(fonts_path)
    amec = load_json_array(amec_path)
    synced = sync_amec_by_id(fonts, amec)

    if args.dry_run:
        print(json.dumps(synced, ensure_ascii=False, indent=2))
        return

    amec_path.parent.mkdir(parents=True, exist_ok=True)
    amec_path.write_text(
        json.dumps(synced, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Synced {len(synced)} entries from {fonts_path} to {amec_path}")


if __name__ == "__main__":
    main()
