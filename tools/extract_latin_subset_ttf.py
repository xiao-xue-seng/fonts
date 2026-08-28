"""
從預先下載的 google 字型 ttf 檔案中，擷取 拉丁字子集 ttf

輸出的 ttf 供"切片化"及"app端最佳化"作為輸入。
"""

import json
import os
import sys
from typing import Any

from fontTools.ttLib import TTFont, TTLibError

# 確保標準輸出支援 UTF-8 編碼
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 確保路徑以專案根目錄為基準
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tools.utils.subset_font import (
    SUBSET_METADATA_TAG,
    canonicalize_unicode_ranges,
    subset_font,
)

# 呼叫端可依此結構增加其他字型，進行批次處理。
FONTS_TO_PROCESS = [
    {
        "input": os.path.join(
            PROJECT_ROOT,
            "temp",
            "ttf-raw",
            "InstrumentSans-VariableFont_wdth,wght.ttf",
        ),
        "output": os.path.join(
            PROJECT_ROOT, "temp", "ttf-to-next", "InstrumentSans-Subset.ttf"
        ),
        "unicode_range_str": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
        "suffix_en": "Subset",
        "suffix_zh": "子集",
    },
]


def has_matching_subset_metadata(
    output_path: str,
    unicode_range_str: str,
    suffix_en: str,
    suffix_zh: Any,
) -> bool:
    """判斷輸出檔是否已使用相同的 Unicode range 與名稱後綴。"""
    if not os.path.isfile(output_path):
        return False

    try:
        expected = {
            "schema": "xiao-xue-seng.font-subset.v1",
            "unicode_ranges": canonicalize_unicode_ranges(unicode_range_str),
            "suffix_en": suffix_en,
            "suffix_zh": suffix_zh,
        }
        with TTFont(output_path, lazy=True) as font:
            meta_table = font.get("meta")
            if meta_table is None or SUBSET_METADATA_TAG not in meta_table.data:
                return False
            metadata = json.loads(
                meta_table.data[SUBSET_METADATA_TAG].decode("utf-8")
            )
    except (
        OSError,
        KeyError,
        TypeError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        TTLibError,
        ValueError,
    ):
        return False

    return all(metadata.get(key) == value for key, value in expected.items())


def run_subsetter():
    for font_config in FONTS_TO_PROCESS:
        input_path = font_config["input"]
        output_path = font_config["output"]
        print(f"\n來源字型：{input_path}")
        print(f"輸出字型：{output_path}")
        try:
            suffix_en = font_config.get("suffix_en", "Subset")
            suffix_zh = font_config.get("suffix_zh")
            if has_matching_subset_metadata(
                output_path=output_path,
                unicode_range_str=font_config["unicode_range_str"],
                suffix_en=suffix_en,
                suffix_zh=suffix_zh,
            ):
                print("⏩ 輸出檔案的 Unicode range 與 suffix 相同，略過處理。")
                continue

            subset_font(
                input_path=input_path,
                output_path=output_path,
                unicode_range_str=font_config["unicode_range_str"],
                suffix_en=suffix_en,
                suffix_zh=suffix_zh,
            )
            print(f"✅ 成功生成：{output_path}")
        except (FileNotFoundError, ValueError) as error:
            print(f"❌ 輸入設定錯誤：{error}")
        except Exception as error:
            print(f"❌ 處理失敗：{error}")


if __name__ == "__main__":
    run_subsetter()
