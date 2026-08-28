"""
這隻腳本會自動掃描同目錄下的 ukai.ttc 與 uming.ttc 兩個檔案，自動辨識內部的子字型名稱，並一口氣幫你匯出以下 4 個獨立的 .ttf 檔案：
- AR-PL-UKai-TW.ttf（文鼎楷體 - 台灣教育部標準）
- AR-PL-UKai-CN.ttf（文鼎楷體 - 大陸 GB 標準）
- AR-PL-UMing-TW.ttf（文鼎明體 - 台灣教育部標準）
- AR-PL-UMing-CN.ttf（文鼎明體 - 大陸 GB 標準）

🟡註：cn版與tw版在字形方面並沒有差別，標點符號也沒有差別(都是置中)，所以只需要拿字碼較多的tw版去切片即可。
"""

import os
from fontTools.ttLib import TTFont
from fontTools.ttLib.sfnt import readTTCHeader

script_dir = os.path.dirname(os.path.abspath(__file__))

# 定義要處理的 TTC 檔案資訊
TARGET_TTCS = [
    {"filename": "ukai.ttc", "prefix": "AR-PL-UKai", "label": "文鼎 PL 中楷 (UKai)"},
    {"filename": "uming.ttc", "prefix": "AR-PL-UMing", "label": "文鼎 PL 細上海宋 (UMing)"},
]

print("🚀 開始自動處理 ukai.ttc 與 uming.ttc 字型檔...\n")

total_extracted = 0

for target in TARGET_TTCS:
    filename = target["filename"]
    prefix = target["prefix"]
    label = target["label"]
    ttc_path = os.path.join(script_dir, filename)

    print(f"📦 正在分析 [{label}] ({filename})...")

    # 檢查檔案是否存在
    if not os.path.exists(ttc_path):
        print(f"   ⚠️ 在同目錄下找不到 {filename}，已跳過該檔案。\n")
        print("-" * 50 + "\n")
        continue

    # 讀取 TTC 標頭
    with open(ttc_path, "rb") as f:
        header = readTTCHeader(f)
        num_fonts = header.numFonts

    tw_index = None
    cn_index = None

    print(f"   共包含 {num_fonts} 個子字型：")

    # 掃描並印出內部子字型名稱
    for i in range(num_fonts):
        font = TTFont(ttc_path, fontNumber=i)
        name_table = font["name"]
        font_name = name_table.getDebugName(4) or name_table.getDebugName(1)
        print(f"   - Index [{i}]: {font_name}")

        # 精準判斷 TW 版 (排除 MBE 筆順版)
        if "TW" in font_name and "MBE" not in font_name:
            tw_index = i

        # 精準判斷 CN 版
        if "CN" in font_name:
            cn_index = i

    print()

    # 匯出 TW 版本
    if tw_index is not None:
        output_tw = os.path.join(script_dir, f"{prefix}-TW.ttf")
        print(
            f"   ✨ 正在匯出 TW 台灣標準版 ➔ [{prefix}-TW.ttf] (Index [{tw_index}])..."
        )
        tw_font = TTFont(ttc_path, fontNumber=tw_index)
        tw_font.save(output_tw)
        total_extracted += 1
    else:
        print(f"   ❌ 在 {filename} 中未找到 TW 版本。")

    # 匯出 CN 版本
    # if cn_index is not None:
    #     output_cn = os.path.join(script_dir, f"{prefix}-CN.ttf")
    #     print(
    #         f"   ✨ 正在匯出 CN 大陸標準版 ➔ [{prefix}-CN.ttf] (Index [{cn_index}])..."
    #     )
    #     cn_font = TTFont(ttc_path, fontNumber=cn_index)
    #     cn_font.save(output_cn)
    #     total_extracted += 1
    # else:
    #     print(f"   ❌ 在 {filename} 中未找到 CN 版本。")

    print("-" * 50 + "\n")

print(f"🎉 全部處理完成！共成功匯出 {total_extracted} 個 .ttf 檔案。")
