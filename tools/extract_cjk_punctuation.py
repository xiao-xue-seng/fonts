"""
製作全字庫繁體楷書 / 宋體 標點符號字型

🟢限制：
寒蟬正楷體 源自於 全字庫楷體。由於 全字庫正楷體 使用的是 1024 × 1024 的"畫布"，而 寒蟬正楷體 的作者在修改時，將畫布縮放改成了 1000 × 1000 的標準。所以無法透過 fontTools 合併出一個新的「具有繁體標點的寒蟬楷體」。

🟢新的策略：
用 Python 從《全字庫》中單獨切出一個只有 169 個標點符號的迷你字型（TW-Kai-Punct.ttf / TW-Sung-Punct.ttf）。
將這個迷你字型跑 cn-font-split。
在 CSS 的 font-family 中，把標點符號字型排在第一順位，寒蟬正楷體排在第二順位。利用 CSS 字型備援 (Fallback)來處理標點問題。瀏覽器非常聰明，它會自動處理 1024 與 1000 的縮放問題，讓標點符號完美對齊！

這個做法的三大好處：
完全避開 UPM 錯誤：不用冒險修改字型的底層畫布，瀏覽器渲染引擎會自動幫你無縫縮放對齊。
模組化：未來如果你又找到了另一款大陸的好字型，你完全可以直接套用這個 tw-kai-punct 標點包，把它排在第一順位，瞬間就能把任何字型的標點「繁中化」！
極度輕量：因為只有標點，檔案極小，完全不影響載入速度。

🟢後續處理：
將輸出的 "TW-Kai-Punct.ttf" 進行切片。
以同樣的方式也製作 TW-Sung-Punct 供宋體使用。
"""

import os
import sys
import unicodedata
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

# 確保標準輸出支援 UTF-8 編碼
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 確保路徑以專案根目錄為基準
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
script_dir = os.path.dirname(os.path.abspath(__file__))

# 待處理字型清單設定
FONTS_TO_PROCESS = [
    {
        "name": "全字齊楷 (TW-Kai-Aligned)",
        "input": os.path.join(PROJECT_ROOT, "temp", "ttf-to-next", "TW-Kai-Aligned.ttf"),
        "output": os.path.join(PROJECT_ROOT, "temp", "ttf-to-next", "TW-Kai-Aligned-Punct.ttf"),
        "fallback_input": os.path.join(script_dir, "TW-Kai-Aligned.ttf"),
        "suffix": "Punct",
    },
    {
        "name": "全字齊宋 (TW-Sung-Aligned)",
        "input": os.path.join(PROJECT_ROOT, "temp", "ttf-to-next", "TW-Sung-Aligned.ttf"),
        "output": os.path.join(PROJECT_ROOT, "temp", "ttf-to-next", "TW-Sung-Aligned-Punct.ttf"),
        "fallback_input": os.path.join(script_dir, "TW-Sung-Aligned.ttf"),
        "suffix": "Punct",
    },
    {
        "name": "全字庫正楷體 (TW-Kai)",
        "input": os.path.join(PROJECT_ROOT, "temp", "ttf-raw", "TW-Kai-98_1.ttf"),
        "output": os.path.join(PROJECT_ROOT, "temp", "ttf-to-next", "TW-Kai-Punct.ttf"),
        "fallback_input": os.path.join(script_dir, "TW-Kai-98_1.ttf"),
        "suffix": "Punct",
    },
    {
        "name": "全字庫正宋體 (TW-Sung)",
        "input": os.path.join(PROJECT_ROOT, "temp", "ttf-raw", "TW-Sung-98_1.ttf"),
        "output": os.path.join(PROJECT_ROOT, "temp", "ttf-to-next", "TW-Sung-Punct.ttf"),
        "fallback_input": os.path.join(script_dir, "TW-Sung-98_1.ttf"),
        "suffix": "Punct",
    },
]


def update_font_names_with_suffix(font: TTFont, suffix: str = "Punct") -> None:
    """
    在字型英文名稱後加上後綴（如 'Punct'），以避免與原始字型混淆。
    """
    if "name" not in font:
        return

    name_table = font["name"]
    suffix_clean = suffix.strip().lstrip("-")
    suffix_ps = suffix_clean.replace(" ", "")

    # 先取得修改前的名稱快照
    raw_records = [
        (r.nameID, r.platformID, r.platEncID, r.langID, r.toUnicode())
        for r in name_table.names
    ]

    for name_id, plat_id, enc_id, lang_id, val in raw_records:
        if not val:
            continue
        # 只處理英文/通用名稱 (避免修改既有的繁中名稱欄位)
        if lang_id in [0x0404, 0x0804, 19]:
            continue

        # 找出同一語系的原始 Family Name
        orig_fam = next(
            (v for nid, pid, eid, lid, v in raw_records if nid == 1 and pid == plat_id and eid == enc_id and lid == lang_id),
            ""
        )
        sep = " " if (" " in (orig_fam or val)) else "-"

        new_val = None
        if name_id == 1:  # Font Family Name: "TW-Kai" -> "TW-Kai-Punct"
            new_val = f"{val}{sep}{suffix_clean}"
        elif name_id == 16:  # Typographic Family Name
            new_val = f"{val}{sep}{suffix_clean}"
        elif name_id == 4:  # Full Font Name: "TW-Kai" -> "TW-Kai-Punct"
            if orig_fam and orig_fam in val:
                new_fam = f"{orig_fam}{sep}{suffix_clean}"
                new_val = val.replace(orig_fam, new_fam, 1)
            else:
                new_val = f"{val}{sep}{suffix_clean}"
        elif name_id == 6:  # PostScript Name: "TW-Kai-98_1" -> "TW-Kai-98_1-Punct"
            new_val = f"{val}-{suffix_ps}"
        elif name_id == 25:  # Variations PostScript Name Prefix
            new_val = f"{val}{suffix_ps}"
        elif name_id == 3:  # Unique identifier: "TW-Kai : 22-7-2013" -> "TW-Kai-Punct : 22-7-2013"
            if orig_fam and orig_fam in val:
                new_fam = f"{orig_fam}{sep}{suffix_clean}"
                new_val = val.replace(orig_fam, new_fam, 1)
            else:
                new_val = f"{val}-{suffix_ps}"

        if new_val is not None:
            name_table.setName(new_val, name_id, plat_id, enc_id, lang_id)


def get_punctuation_unicodes():
    """篩選中文標點符號與全形空白 Unicode 集合"""
    target_blocks = [
        (0x2000, 0x206F),
        (0x3000, 0x303F),
        (0xFE10, 0xFE1F),
        (0xFE30, 0xFE4F),
        (0xFF00, 0xFFEF),
    ]

    unicodes = set()
    for start, end in target_blocks:
        for codepoint in range(start, end + 1):
            char = chr(codepoint)
            category = unicodedata.category(char)
            if category.startswith("P") or codepoint == 0x3000:
                unicodes.add(codepoint)
    return unicodes


def process_font(font_cfg, punct_unicodes):
    font_name = font_cfg["name"]
    input_path = font_cfg["input"]
    output_path = font_cfg["output"]
    suffix = font_cfg.get("suffix", "Punct")

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
        print("1. 正在載入字型並擷取居中標點符號...")
        tw_font = TTFont(input_path)

        options = Options()
        # 為了網頁載入最佳化，不保留多餘的排版表格
        options.layout_features = []
        subsetter = Subsetter(options=options)
        subsetter.populate(unicodes=punct_unicodes)
        subsetter.subset(tw_font)

        print(f"2. 正在更新字型內部英文名稱（加入 '-{suffix}' 後綴）...")
        update_font_names_with_suffix(tw_font, suffix=suffix)

        print("3. 正在儲存純標點字型...")
        tw_font.save(output_path)
        tw_font.close()

        print(f"✅ 成功生成標點符號字型：{output_path}")

    except Exception as e:
        print(f"❌ 處理 {font_name} 失敗：{e}")


def main():
    print("1. 正在分析 Unicode 區塊並篩選中文標點字碼...")
    punct_unicodes = get_punctuation_unicodes()
    print(f"   -> 共鎖定 {len(punct_unicodes)} 個標點/全形空白字碼。")

    for font_cfg in FONTS_TO_PROCESS:
        process_font(font_cfg, punct_unicodes)

    print("\n✨ 全部處理程序結束。")


if __name__ == "__main__":
    main()

