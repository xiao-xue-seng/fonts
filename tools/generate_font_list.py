#!/usr/bin/env python3
"""從 .dist 中已建置的 npm 字型套件產生 api/fonts.json。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_BASE_URL = "https://cdn.jsdelivr.net/npm/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = PROJECT_ROOT / ".dist"
DEFAULT_OUTPUT = PROJECT_ROOT / "api" / "fonts.json"
FONT_FAMILY_RE = re.compile(
    r"font-family\s*:\s*(?:\"([^\"]+)\"|'([^']+)'|([^;]+))",
    re.IGNORECASE,
)


def load_package_json(package_dir: Path) -> dict[str, Any]:
    package_path = package_dir / "package.json"
    if not package_path.is_file():
        raise ValueError(f"找不到 package.json：{package_path}")
    try:
        data = json.loads(package_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"package.json 格式錯誤：{package_path}") from error
    if not isinstance(data, dict):
        raise ValueError(f"package.json 必須是 JSON 物件：{package_path}")
    return data


def require_package_identity(package_json: dict[str, Any], package_dir: Path) -> tuple[str, str]:
    name = package_json.get("name")
    version = package_json.get("version")
    if not isinstance(name, str) or not name:
        raise ValueError(f"package.json 缺少有效的 name：{package_dir}")
    if not isinstance(version, str) or not version:
        raise ValueError(f"package.json 缺少有效的 version：{package_dir}")
    return name, version


def first_font_family(css_path: Path) -> str:
    match = FONT_FAMILY_RE.search(css_path.read_text(encoding="utf-8"))
    if match:
        return next(value for value in match.groups() if value is not None).strip()
    raise ValueError(f"找不到 font-family：{css_path}")


def font_metadata(package_json: dict[str, Any], package_dir: Path) -> dict[str, Any]:
    metadata = package_json.get("fontMetadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"package.json 缺少有效的 fontMetadata：{package_dir}")
    title = metadata.get("title")
    if not isinstance(title, str) or not title:
        raise ValueError(f"fontMetadata.title 必須是非空字串：{package_dir}")
    return metadata


def css_url(base_url: str, package_name: str, version: str, css_path: str) -> str:
    return f"{base_url.rstrip('/')}/{package_name}@{version}/{css_path.lstrip('/')}"


def build_font_item(
    *,
    item_id: str,
    css_path: Path,
    css_url_path: str,
    metadata_package_dir: Path,
    identity_package_json: dict[str, Any],
    base_url: str,
) -> dict[str, str]:
    metadata = font_metadata(load_package_json(metadata_package_dir), metadata_package_dir)
    package_name, version = require_package_identity(
        identity_package_json, metadata_package_dir
    )
    item: dict[str, str] = {
        "id": item_id,
        "name": first_font_family(css_path),
        "displayName": metadata["title"],
        "cssUrl": css_url(base_url, package_name, version, css_url_path),
    }
    ttf_url = metadata.get("ttfUrl")
    if isinstance(ttf_url, str) and ttf_url:
        item["ttfUrl"] = ttf_url
    return item


def build_font_list(root: Path, base_url: str) -> list[dict[str, str]]:
    fonts: list[dict[str, str]] = []
    for package_dir in sorted(root.iterdir(), key=lambda item: item.name):
        if not package_dir.is_dir():
            continue
        package_json = load_package_json(package_dir)
        child_dirs = [
            child
            for child in sorted(package_dir.iterdir(), key=lambda item: item.name)
            if child.is_dir() and (child / "result.css").is_file()
        ]

        if child_dirs:
            index_css = package_dir / "index.css"
            if not index_css.is_file():
                raise ValueError(f"群組套件缺少 index.css：{package_dir}")
            require_package_identity(package_json, package_dir)
            fonts.append(
                build_font_item(
                    item_id=package_dir.name,
                    css_path=index_css,
                    css_url_path="index.css",
                    metadata_package_dir=package_dir,
                    identity_package_json=package_json,
                    base_url=base_url,
                )
            )
            for child_dir in child_dirs:
                fonts.append(
                    build_font_item(
                        item_id=f"{package_dir.name}/{child_dir.name}",
                        css_path=child_dir / "result.css",
                        css_url_path=f"{child_dir.name}/result.css",
                        metadata_package_dir=child_dir,
                        identity_package_json=package_json,
                        base_url=base_url,
                    )
                )
            continue

        result_css = package_dir / "result.css"
        if result_css.is_file():
            fonts.append(
                build_font_item(
                    item_id=package_dir.name,
                    css_path=result_css,
                    css_url_path="result.css",
                    metadata_package_dir=package_dir,
                    identity_package_json=package_json,
                    base_url=base_url,
                )
            )
    return fonts


def main() -> None:
    parser = argparse.ArgumentParser(description="從 .dist 產生字型清單 JSON")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    if not root.is_dir():
        raise SystemExit(f"找不到字型輸出資料夾：{root}")
    fonts = build_font_list(root, args.base_url)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(fonts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"已產生 {len(fonts)} 個字型：{output}")


if __name__ == "__main__":
    main()
