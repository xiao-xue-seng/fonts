# -*- coding: utf-8 -*-
"""字型 name table 的語系辨識與子集名稱更新工具。"""

from collections.abc import Iterable
from typing import Dict, List, Optional, Tuple

from fontTools.ttLib import TTFont


NameRecord = Tuple[int, int, int, int, str]


def _language_kind(platform_id: int, language_id: int) -> Optional[str]:
    """將 name record 的語系辨識為 English、Chinese 或其他語系。"""
    if platform_id == 1:
        if language_id == 0:
            return "en"
        if language_id in (19, 33):
            return "zh"
        return None

    if platform_id == 0 and language_id == 0:
        return "en"

    if platform_id == 3:
        if language_id == 0:
            return "en"
        primary_language_id = language_id & 0x03FF
        if primary_language_id == 0x0009:
            return "en"
        if primary_language_id == 0x0004:
            return "zh"

    return None


def _postscript_style(value: str) -> str:
    return "".join(
        character for character in value if character.isascii() and character.isalnum()
    )


def _add_suffix(value: str, suffix: str, separator: str = " ") -> str:
    if not suffix or value.endswith(f"{separator}{suffix}") or value.endswith(suffix):
        return value
    return f"{value}{separator}{suffix}"


def _postscript_with_suffix(value: str, suffix_en: str, styles: Iterable[str]) -> str:
    suffix = "".join(
        character for character in suffix_en if character.isascii() and character.isalnum()
    )
    if not suffix or value.endswith(suffix):
        return value

    style_names = {
        _postscript_style(style)
        for style in styles
        if _postscript_style(style)
    }
    for style in sorted(style_names, key=len, reverse=True):
        marker = f"-{style}"
        if value.endswith(marker):
            return f"{value[:-len(marker)]}{suffix}{marker}"

    if "-" in value:
        prefix, style = value.rsplit("-", 1)
        return f"{prefix}{suffix}-{style}"
    return f"{value}{suffix}"


def update_font_names_with_suffix(
    font: TTFont,
    suffix_en: str = "Subset",
    suffix_zh: Optional[str] = None,
) -> None:
    """只修改字型原本已有的英文／中文名稱，並將後綴放在 style 前。

    英文名稱使用 ``suffix_en``；中文名稱使用 ``suffix_zh``。需要 ASCII
    的 PostScript Name 與 Unique Identifier 一律使用英文後綴，不會建立
    原字型不存在的語系名稱。
    """
    if "name" not in font:
        return

    name_table = font["name"]
    raw_records: List[NameRecord] = [
        (
            record.nameID,
            record.platformID,
            record.platEncID,
            record.langID,
            record.toUnicode(),
        )
        for record in name_table.names
    ]

    families: Dict[Tuple[int, int, int], str] = {}
    styles: Dict[Tuple[int, int, int], List[str]] = {}
    for name_id, platform_id, encoding_id, language_id, value in raw_records:
        key = (platform_id, encoding_id, language_id)
        if name_id in (1, 16) and key not in families:
            families[key] = value
        elif name_id in (2, 17):
            styles.setdefault(key, []).append(value)

    updated_postscript: Dict[Tuple[int, int, int], str] = {}
    for name_id, platform_id, encoding_id, language_id, value in raw_records:
        kind = _language_kind(platform_id, language_id)
        suffix = suffix_en if kind == "en" else suffix_zh if kind == "zh" else None
        if not value or not suffix:
            continue

        key = (platform_id, encoding_id, language_id)
        family = families.get(key, "")
        new_value = None

        if name_id in (1, 16):
            new_value = _add_suffix(value, suffix)
        elif name_id == 4:
            if family and family in value:
                new_value = value.replace(family, _add_suffix(family, suffix), 1)
        elif name_id == 6:
            new_value = _postscript_with_suffix(value, suffix_en, styles.get(key, []))
            updated_postscript[key] = new_value
        elif name_id == 25:
            new_value = _add_suffix(value, suffix_en, separator="")
        elif name_id == 3:
            original_postscript = next(
                (
                    candidate
                    for record_id, pid, eid, lid, candidate in raw_records
                    if record_id == 6
                    and pid == platform_id
                    and eid == encoding_id
                    and lid == language_id
                ),
                "",
            )
            replacement = updated_postscript.get(key) or _postscript_with_suffix(
                original_postscript, suffix_en, styles.get(key, [])
            )
            if original_postscript and original_postscript in value:
                new_value = value.replace(original_postscript, replacement, 1)
            elif family and family in value:
                new_value = value.replace(family, _add_suffix(family, suffix), 1)

        if new_value is not None and new_value != value:
            name_table.setName(new_value, name_id, platform_id, encoding_id, language_id)
