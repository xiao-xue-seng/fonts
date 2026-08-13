#!/usr/bin/env python3
"""
Collect font metadata from every immediate subdirectory containing result.css
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*(['\"])(.*?)\1", re.IGNORECASE)
METADATA_RE = re.compile(
    r"^Windows\s+(?:zh-TW|zh)\s+(?:FontFamilyName|TypographicFamilyName)\s+(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
# 用於匹配語意化版本號（SemVer）並提取 Major 主版本號
TAG_MAJOR_RE = re.compile(r"^v?(\d+)(?:\.\d+)*", re.IGNORECASE)


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as file:
        config = json.load(file)
    if not isinstance(config, dict):
        raise ValueError(f"設定檔必須是 JSON 物件：{path}")
    return config


def get_latest_git_tag(repo_root: Path) -> str | None:
    raw_tag = None

    # 1. 優先判斷：如果在 GitHub Actions 環境中且是由 Tag 觸發
    if os.environ.get("GITHUB_REF_TYPE") == "tag":
        raw_tag = os.environ.get("GITHUB_REF_NAME")

    # 2. 次要判斷：直接列出所有標籤並取最高版本號
    if not raw_tag:
        try:
            result = subprocess.run(
                ["git", "tag", "--sort=-v:refname"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True,
            )
            tags = [t.strip() for t in result.stdout.splitlines() if t.strip()]
            if tags:
                raw_tag = tags[0]  # 取最大的版本號 (例如 v1.1.0)
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    if not raw_tag:
        return None

    # 3. 將完整版本號 (如 v1.1.0, 1.0.0) 轉為主版本號格式 (如 v1)
    match = TAG_MAJOR_RE.match(raw_tag)
    if match:
        return f"v{match.group(1)}"

    return raw_tag


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
    ttf_base_url = config.get("ttfBaseUrl", base_url)
    ttf_filenames = config.get("ttfFilenames", {})
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
        font_item = {
            "id": folder.name,
            "name": name,
            "displayName": display_name(css, folder.name, name, names),
            "cssUrl": f"{base_url.rstrip('/')}/{folder.name}/result.css",
        }

        # 只有在 ttfFilenames 中有該子資料夾的檔名時，才新增 ttfUrl
        if folder.name in ttf_filenames:
            ttf_filename = ttf_filenames[folder.name]
            font_item["ttfUrl"] = f"{ttf_base_url.rstrip('/')}/{ttf_filename}"

        fonts.append(font_item)
    return fonts


def main() -> None:
    parser = argparse.ArgumentParser(description="從字型資料夾產生全部字型清單 JSON")
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parent.parent
    )
    parser.add_argument(
        "--config", type=Path, default=Path(__file__).with_name("font-list.config.json")
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--tag",
        type=str,
        default=None,
        help="指定 Git tag（預設自動取得最新的 tag 主版本號，若無則使用 main）",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="result.css 所使用的 CDN 根網址（若未指定，則自動使用 https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@{TAG_OR_MAIN}）",
    )
    parser.add_argument(
        "--exclude", action="append", default=[], help="額外排除的資料夾，可重複指定"
    )
    args = parser.parse_args()

    tag = args.tag or get_latest_git_tag(args.root) or "main"
    base_url = args.base_url or f"https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@{tag}"

    config = load_config(args.config)
    config["excludeFolders"] = list(
        set(config.get("excludeFolders", [])) | set(args.exclude)
    )
    output = args.output or args.root / "api" / "fonts.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    fonts = build_font_list(args.root, config, base_url)
    output.write_text(
        json.dumps(fonts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"已產生 {len(fonts)} 個字型：{output} (使用 base_url: {base_url})")


if __name__ == "__main__":
    main()
