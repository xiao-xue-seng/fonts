"""
從預先下載的 google 字型 ttf 檔案中，擷取 拉丁字子集 ttf
"""

import os
import sys

# 確保標準輸出支援 UTF-8 編碼
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 確保路徑以專案根目錄為基準
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tools.utils.subset_font import subset_font

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


def run_subsetter():
    for font_config in FONTS_TO_PROCESS:
        input_path = font_config["input"]
        output_path = font_config["output"]
        print(f"\n來源字型：{input_path}")
        print(f"輸出字型：{output_path}")
        try:
            subset_font(
                input_path=input_path,
                output_path=output_path,
                unicode_range_str=font_config["unicode_range_str"],
                suffix_en=font_config.get("suffix_en", "Subset"),
                suffix_zh=font_config.get("suffix_zh"),
            )
            print(f"✅ 成功生成：{output_path}")
        except (FileNotFoundError, ValueError) as error:
            print(f"❌ 輸入設定錯誤：{error}")
        except Exception as error:
            print(f"❌ 處理失敗：{error}")


if __name__ == "__main__":
    run_subsetter()
