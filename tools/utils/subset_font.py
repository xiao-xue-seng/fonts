# -*- coding: utf-8 -*-
"""單一字型 Unicode 子集擷取工具。"""

import os
from typing import Optional

from fontTools import subset

from .font_names import update_font_names_with_suffix


def _default_options() -> subset.Options:
    """建立以保留原字型資訊為優先的 subset 選項。"""
    options = subset.Options()
    options.passthrough_tables = True
    options.drop_tables = []
    options.name_IDs = ["*"]
    options.name_languages = ["*"]
    options.name_legacy = True
    options.glyph_names = True
    options.legacy_cmap = True
    options.symbol_cmap = True
    options.layout_features = ["*"]
    return options


def subset_font(
    input_path: str,
    output_path: str,
    unicode_range_str: str,
    suffix_en: str = "Subset",
    suffix_zh: Optional[str] = None,
    options: Optional[subset.Options] = None,
) -> None:
    """擷取單一字型的 Unicode 子集並輸出。

    ``unicode_range_str`` 採用 fontTools 格式，例如
    ``"U+0000-00FF,U+2000-206F"``。輸出檔存在時會直接覆寫；缺少輸入檔
    或 Unicode 格式錯誤時會以例外通知呼叫者。
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"找不到輸入字型檔：{input_path}")
    if not unicode_range_str or not unicode_range_str.strip():
        raise ValueError("Unicode range 不可為空。")

    try:
        unicodes = subset.parse_unicodes(unicode_range_str)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Unicode range 格式錯誤：{unicode_range_str}") from error
    if not unicodes:
        raise ValueError("Unicode range 未包含任何 Unicode 碼點。")

    output_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_dir, exist_ok=True)
    subset_options = options or _default_options()
    font = None
    try:
        font = subset.load_font(input_path, subset_options)
        subsetter = subset.Subsetter(options=subset_options)
        subsetter.populate(unicodes=unicodes)
        subsetter.subset(font)
        update_font_names_with_suffix(font, suffix_en=suffix_en, suffix_zh=suffix_zh)
        subset.save_font(font, output_path, subset_options)
    finally:
        if font is not None:
            font.close()


__all__ = ["subset_font"]
