#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
模組名稱：字型 Metadata / Name Table 工具函式庫
功能：提供為 TTFont 更新多語系 (Windows / Mac, 英文與繁中) 名稱資訊之共用函式
===============================================================================
"""

from fontTools.ttLib import TTFont


def update_font_metadata(
    font: TTFont, en_name: str, en_style: str, zh_name: str, zh_style: str
) -> None:
    """
    同時為字型寫入 Windows 與 Mac 的多語系名稱 (英文 + 繁體中文)

    :param font: fontTools TTFont 物件
    :param en_name: 英文字型家族名稱 (例如: "TW-Kai-Aligned")
    :param en_style: 英文樣式名稱 (例如: "Regular")
    :param zh_name: 中文字型家族名稱 (例如: "全字齊楷")
    :param zh_style: 中文樣式名稱 (例如: "標準")
    """
    if "name" not in font:
        return

    name_table = font["name"]
    ps_name = en_name.replace(" ", "")
    unique_id = f"1.000;{ps_name};{ps_name}-{en_style}"

    # 1. 寫入 Windows Unicode 平台 (PlatformID=3, PlatEncID=1)
    # 英文 (LanguageID: 0x0409 / 1033)
    name_table.setName(en_name, 1, 3, 1, 0x0409)  # Family
    name_table.setName(en_style, 2, 3, 1, 0x0409)  # Subfamily
    name_table.setName(unique_id, 3, 3, 1, 0x0409)  # Unique ID
    name_table.setName(en_name, 4, 3, 1, 0x0409)  # Full Name
    name_table.setName(ps_name, 6, 3, 1, 0x0409)  # PostScript Name (必為英文)
    name_table.setName(en_name, 16, 3, 1, 0x0409)  # Typographic Family

    # 繁體中文 (LanguageID: 0x0404 / 1028, zh-TW)
    name_table.setName(zh_name, 1, 3, 1, 0x0404)  # 中文 Family
    name_table.setName(zh_style, 2, 3, 1, 0x0404)  # 中文 Subfamily
    name_table.setName(zh_name, 4, 3, 1, 0x0404)  # 中文 Full Name
    name_table.setName(zh_name, 16, 3, 1, 0x0404)  # 中文 Typographic Family

    # 2. 寫入 Macintosh 平台 (PlatformID=1, PlatEncID=0/2)
    # 英文 (LanguageID: 0)
    name_table.setName(en_name, 1, 1, 0, 0)
    name_table.setName(en_style, 2, 1, 0, 0)
    name_table.setName(en_name, 4, 1, 0, 0)
    name_table.setName(ps_name, 6, 1, 0, 0)

    # 繁體中文 (PlatformID=1, PlatEncID=2, LanguageID=19, Mac Traditional Chinese)
    name_table.setName(zh_name, 1, 1, 2, 19)
    name_table.setName(zh_style, 2, 1, 2, 19)
    name_table.setName(zh_name, 4, 1, 2, 19)


__all__ = ["update_font_metadata"]
