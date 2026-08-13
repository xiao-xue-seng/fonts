"""
從預先下載的 google 字型 ttf 檔案中，擷取 拉丁字子集 ttf
"""

import os
from fontTools import subset

# 1. 設定字型檔案路徑與 Unicode 範圍
# 請替換成你本機解壓後的實際檔案路徑（相對路徑或絕對路徑皆可）
input_ttf = "tools/InstrumentSans-VariableFont_wdth,wght.ttf"
output_ttf = "InstrumentSans-Subset.ttf"

# 你指定的 Unicode 範圍
unicode_range_str = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"

def run_subsetter():
    # 檢查輸入檔案是否存在
    if not os.path.exists(input_ttf):
        print(f"錯誤：找不到檔案 '{input_ttf}'，請確認路徑是否正確。")
        return

    try:
        print(f"1. 讀取原始可變字型：{input_ttf}")

        # 2. 設定 fontTools 裁切選項
        options = subset.Options()
        # 【關鍵】passthrough_tables = True 確保保留 fvar, gvar 等可變字型專屬結構
        options.passthrough_tables = True

        print("2. 正在根據指定的 Unicode 範圍進行精確裁切...")

        # 3. 載入字型與執行裁切
        font_to_subset = subset.load_font(input_ttf, options)
        subsetter = subset.Subsetter(options=options)

        # 寫入指定的 Unicode 範圍
        subsetter.populate(unicodes=subset.parse_unicodes(unicode_range_str))
        subsetter.subset(font_to_subset)

        print(f"3. 正在儲存裁切後的檔案...")

        # 4. 儲存結果
        subset.save_font(font_to_subset, output_ttf, options)

        # 釋放檔案控制權，避免 Windows 鎖定
        font_to_subset.close()

        print(f"\n✅ 成功生成！檔案已存為：{output_ttf}")
        print("（已保留原始字型的 wdth 與 wght 變數軸度）")

    except Exception as e:
        print(f"\n❌ 執行失敗：{e}")

if __name__ == "__main__":
    run_subsetter()