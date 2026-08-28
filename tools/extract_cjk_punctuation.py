"""
製作標點符號子集

從 Noto Serif 擷取繁體及簡體標點符號，因為它符合現代字身垂直置中的規範，不會遇到"全字庫"那種偏低的歷史包袱。
"""

import os
import sys
import unicodedata

# 確保標準輸出支援 UTF-8 編碼
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 確保路徑以專案根目錄為基準
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
script_dir = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tools.utils.subset_font import subset_font

# 待處理字型清單設定
FONTS_TO_PROCESS = [
    {
        "name": "Noto Serif SC 標點",
        "input": os.path.join(PROJECT_ROOT, "temp", "ttf-raw", "NotoSerifCJKsc-VF.otf"),
        "output": os.path.join(
            PROJECT_ROOT, "temp", "ttf-to-next", "Noto-Serif-SC-Punct.ttf"
        ),
        "fallback_input": os.path.join(script_dir, "NotoSerifCJKsc-VF.otf"),
        "suffix_en": "Punct",
        "suffix_zh": "標點",
    },
    {
        "name": "Noto Serif TC 標點",
        "input": os.path.join(PROJECT_ROOT, "temp", "ttf-raw", "NotoSerifCJKtc-VF.otf"),
        "output": os.path.join(
            PROJECT_ROOT, "temp", "ttf-to-next", "Noto-Serif-TC-Punct.ttf"
        ),
        "fallback_input": os.path.join(script_dir, "NotoSerifCJKtc-VF.otf"),
        "suffix_en": "Punct",
        "suffix_zh": "標點",
    },
    {
        "name": "全字齊楷 標點",
        "input": os.path.join(
            PROJECT_ROOT, "temp", "ttf-to-next", "TW-Kai-Aligned.ttf"
        ),
        "output": os.path.join(
            PROJECT_ROOT, "temp", "ttf-to-next", "TW-Kai-Aligned-Punct.ttf"
        ),
        "fallback_input": os.path.join(script_dir, "TW-Kai-Aligned.ttf"),
        "suffix_en": "Punct",
        "suffix_zh": "標點",
    },
]


def get_punctuation_unicodes():
    """篩選中文標點符號與全形空白 Unicode 集合"""
    target_blocks = [
        (0x2000, 0x206F),  # 通用標點（“ ” ‘ ’ — … 等）
        (0x3000, 0x303F),  # CJK 符號和標點（、 。 《 》 「 」 【 】 等）
        (0xFE10, 0xFE1F),  # 直排形式
        (0xFE30, 0xFE4F),  # CJK 相容形式（直排引號、專名線等）
        (0xFE50, 0xFE6F),  # 小型變體形式（繁體/Big5 相容標點如 ﹐ ﹑ ﹖ 等）
        (0xFF00, 0xFFEF),  # 全形 ASCII 標點（！ ？ ， ： ； 等）
    ]

    unicodes = set()
    for start, end in target_blocks:
        for codepoint in range(start, end + 1):
            char = chr(codepoint)
            category = unicodedata.category(char)
            if category.startswith("P") or codepoint == 0x3000:
                unicodes.add(codepoint)
    return unicodes


def process_font(font_cfg, punct_unicode_range_str):
    font_name = font_cfg["name"]
    input_path = font_cfg["input"]
    output_path = font_cfg["output"]
    print(f"\n==================================================")
    print(f"開始處理：{font_name}")

    # 檢查輸入檔案路徑 (若主要路徑不存在則嘗試 fallback 路徑)
    if not os.path.exists(input_path):
        fallback = font_cfg.get("fallback_input")
        if fallback and os.path.exists(fallback):
            input_path = fallback
        else:
            print(f"⚠️ 找不到輸入字型檔：{input_path}，略過。")
            return

    # 判斷若輸出檔案已存在，並且比輸入檔案更新，則略過不處理
    if os.path.exists(output_path):
        input_mtime = os.path.getmtime(input_path)
        output_mtime = os.path.getmtime(output_path)
        if output_mtime >= input_mtime:
            print(f"⏩ 輸出檔案 '{output_path}' 已存在且較輸入檔案新，略過不處理。")
            return

    print(f"來源檔案：{input_path}")
    print(f"輸出目標：{output_path}")

    # 確保輸出目錄存在
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        print("1. 正在載入字型並擷取標點符號...")
        subset_font(
            input_path=input_path,
            output_path=output_path,
            unicode_range_str=punct_unicode_range_str,
            suffix_en=font_cfg.get("suffix_en", "Punct"),
            suffix_zh=font_cfg.get("suffix_zh"),
        )
        print(f"✅ 成功生成標點符號字型：{output_path}")

    except Exception as e:
        print(f"❌ 處理 {font_name} 失敗：{e}")


def main():
    print("1. 正在分析 Unicode 區塊並篩選中文標點字碼...")
    punct_unicodes = sorted(get_punctuation_unicodes())
    punct_unicode_range_str = ",".join(
        f"U+{codepoint:04X}" for codepoint in punct_unicodes
    )
    print(f"   -> 共鎖定 {len(punct_unicodes)} 個標點/全形空白字碼。")

    for font_cfg in FONTS_TO_PROCESS:
        process_font(font_cfg, punct_unicode_range_str)

    print("\n✨ 全部處理程序結束。")


if __name__ == "__main__":
    main()
