#!/usr/bin/env python3
"""
Collect font metadata from every immediate subdirectory containing result.css.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*(['\"])(.*?)\1", re.IGNORECASE)
METADATA_RE = re.compile(
    r"^Windows\s+(?:zh-TW|zh)\s+(?:FontFamilyName|TypographicFamilyName)\s+(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as file:
        config = json.load(file)
    if not isinstance(config, dict):
        raise ValueError(f"設定檔必須是 JSON 物件：{path}")
    return config


def first_font_family(css: str, css_path: Path) -> str:
    match = FONT_FAMILY_RE.search(css)
    if not match:
        raise ValueError(f"找不到 font-family：{css_path}")
    return match.group(2).strip()


def display_name(css: str, font_id: str, name: str, configured: dict) -> str:
    if font_id in configured:
        return configured[font_id]

    match = METADATA_RE.search(css)
    if match:
        return re.sub(r"\s+(?:Regular|常規|標準)$", "", match.group(1)).strip()
    return name


def build_font_list(root: Path, config: dict, base_url: str) -> list[dict[str, str]]:
    excluded_config = config.get("excludeFolders", [])
    names = config.get("displayNames", {})
    if not isinstance(excluded_config, list) or not isinstance(names, dict):
        raise ValueError("excludeFolders 必須是陣列，displayNames 必須是物件")
    excluded = set(excluded_config)

    fonts = []
    for folder in sorted(root.iterdir(), key=lambda item: item.name):
        if not folder.is_dir() or folder.name in excluded:
            continue

        css_path = folder / "result.css"
        if not css_path.is_file():
            continue

        css = css_path.read_text(encoding="utf-8")
        name = first_font_family(css, css_path)
        fonts.append(
            {
                "id": folder.name,
                "name": name,
                "displayName": display_name(css, folder.name, name, names),
                "cssUrl": f"{base_url.rstrip('/')}/{folder.name}/result.css",
            }
        )
    return fonts


def main() -> None:
    parser = argparse.ArgumentParser(description="從字型資料夾產生全部字型清單 JSON")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("font-list.config.json"))
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--base-url",
        default="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main",
        help="result.css 所使用的 CDN 根網址",
    )
    parser.add_argument("--exclude", action="append", default=[], help="額外排除的資料夾，可重複指定")
    args = parser.parse_args()

    config = load_config(args.config)
    config["excludeFolders"] = list(set(config.get("excludeFolders", [])) | set(args.exclude))
    output = args.output or args.root / "api" / "fonts.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    fonts = build_font_list(args.root, config, args.base_url)
    output.write_text(json.dumps(fonts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已產生 {len(fonts)} 個字型：{output}")


if __name__ == "__main__":
    main()
