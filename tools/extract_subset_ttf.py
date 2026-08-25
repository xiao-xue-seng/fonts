"""
從預先下載的 google 字型 ttf 檔案中，擷取 拉丁字子集 ttf
"""

import os
import sys
from fontTools import subset
from fontTools.ttLib import TTFont

# 確保標準輸出支援 UTF-8 編碼
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 確保路徑以專案根目錄為基準
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 1. 設定字型檔案路徑與 Unicode 範圍
# 請替換成你本機解壓後的實際檔案路徑（相對路徑或絕對路徑皆可）
input_ttf = os.path.join(PROJECT_ROOT, "temp", "ttf-raw", "InstrumentSans-VariableFont_wdth,wght.ttf")
output_ttf = os.path.join(PROJECT_ROOT, "temp", "ttf-to-next", "InstrumentSans-Subset.ttf")

# 你指定的 Unicode 範圍
unicode_range_str = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"


def update_font_names_with_suffix(font: TTFont, suffix: str = "Subset") -> None:
    """
    在字型英文名稱後加上後綴（如 'Subset'），以避免與原始字型混淆。
    """
    if "name" not in font:
        return

    name_table = font["name"]
    suffix_clean = suffix.strip()
    suffix_ps = suffix_clean.replace(" ", "")

    # 先取得修改前的名稱快照
    raw_records = [
        (r.nameID, r.platformID, r.platEncID, r.langID, r.toUnicode())
        for r in name_table.names
    ]

    for name_id, plat_id, enc_id, lang_id, val in raw_records:
        if not val:
            continue

        new_val = None
        if name_id == 1:  # Font Family Name: "Instrument Sans" -> "Instrument Sans Subset"
            new_val = f"{val} {suffix_clean}"
        elif name_id == 16:  # Typographic Family Name
            new_val = f"{val} {suffix_clean}"
        elif name_id == 4:  # Full Font Name: "Instrument Sans Regular" -> "Instrument Sans Subset Regular"
            # 找到同一語系的原始 Family Name
            orig_fam = next(
                (v for nid, pid, eid, lid, v in raw_records if nid == 1 and pid == plat_id and eid == enc_id and lid == lang_id),
                ""
            )
            if orig_fam and orig_fam in val:
                new_val = val.replace(orig_fam, f"{orig_fam} {suffix_clean}", 1)
            else:
                new_val = f"{val} {suffix_clean}"
        elif name_id == 6:  # PostScript Name: "InstrumentSans-Regular" -> "InstrumentSansSubset-Regular"
            if "-" in val:
                prefix, style = val.split("-", 1)
                new_val = f"{prefix}{suffix_ps}-{style}"
            else:
                new_val = f"{val}{suffix_ps}"
        elif name_id == 25:  # Variations PostScript Name Prefix
            new_val = f"{val}{suffix_ps}"
        elif name_id == 3:  # Unique identifier: "1.000;NONE;InstrumentSans-Regular"
            orig_ps = next(
                (v for nid, pid, eid, lid, v in raw_records if nid == 6 and pid == plat_id and eid == enc_id and lid == lang_id),
                ""
            )
            if orig_ps and orig_ps in val:
                if "-" in orig_ps:
                    prefix, style = orig_ps.split("-", 1)
                    new_ps = f"{prefix}{suffix_ps}-{style}"
                else:
                    new_ps = f"{orig_ps}{suffix_ps}"
                new_val = val.replace(orig_ps, new_ps, 1)
            else:
                new_val = f"{val}-{suffix_ps}"

        if new_val is not None:
            name_table.setName(new_val, name_id, plat_id, enc_id, lang_id)


def run_subsetter():
    # 檢查輸入檔案是否存在
    if not os.path.exists(input_ttf):
        print(f"錯誤：找不到檔案 '{input_ttf}'，請確認路徑是否正確。")
        return

    # 檢查輸出檔案是否存在且比輸入檔案更新
    if os.path.exists(output_ttf):
        input_mtime = os.path.getmtime(input_ttf)
        output_mtime = os.path.getmtime(output_ttf)
        if output_mtime >= input_mtime:
            print(f"⏩ 輸出檔案 '{output_ttf}' 已存在且較輸入檔案新，略過不處理。")
            return

    # 確保輸出目錄存在
    output_dir = os.path.dirname(output_ttf)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

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

        print("3. 正在更新字型英文名稱（加入 'Subset' 後綴）...")
        update_font_names_with_suffix(font_to_subset, suffix="Subset")

        print(f"4. 正在儲存裁切後的檔案...")

        # 4. 儲存結果
        subset.save_font(font_to_subset, output_ttf, options)

        # 釋放檔案控制權，避免 Windows 鎖定
        font_to_subset.close()

        print(f"\n✅ 成功生成！檔案已存為：{output_ttf}")
        print("（已保留原始字型的 wdth 與 wght 變數軸度，並更新名稱為包含 Subset）")

    except Exception as e:
        print(f"\n❌ 執行失敗：{e}")


if __name__ == "__main__":
    run_subsetter()