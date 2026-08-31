"""
讀取字型檔的 cmap 映射表，並輸出各個 CJK 區段的覆蓋率
"""

import sys
import unicodedata
from fontTools.ttLib import TTFont


def display_width(text):
    """計算終端機顯示寬度（中文/全形字佔 2 格，半形字佔 1 格）。"""
    return sum(
        2 if unicodedata.east_asian_width(ch) in {"W", "F"} else 1 for ch in str(text)
    )


def pad_display(text, target_width, align="left"):
    """
    根據終端機的實際顯示寬度進行對齊填充。
    解決中英文混排時 Python 原生 format / ljust 跑版的問題。
    """
    text_str = str(text)
    current_w = display_width(text_str)
    padding = max(0, target_width - current_w)

    if align == "left":
        return text_str + " " * padding
    elif align == "right":
        return " " * padding + text_str
    elif align == "center":
        left = padding // 2
        right = padding - left
        return " " * left + text_str + " " * right
    return text_str


def analyze_cjk_coverage(font_path):
    try:
        # 載入字型檔 (支援 .ttf, .otf, .woff, .woff2)
        font = TTFont(font_path)
    except Exception as e:
        print(f"無法讀取字型檔: {e}")
        return

    # 取得字型中所有已編碼的 Unicode 碼位集合
    cmap = font.getBestCmap()
    if not cmap:
        print("未找到有效 cmap 編碼表")
        return
    unicodes = set(cmap.keys())

    # 定義 CJK 核心 Unicode 區間及標準總字數
    cjk_blocks = {
        "CJK 基本區 (BMP, U+4E00..U+9FFF)": (0x4E00, 0x9FFF, 20992),
        "CJK 擴展 A 區 (Ext-A, U+3400..U+4DBF)": (0x3400, 0x4DBF, 6592),
        "CJK 擴展 B 區 (Ext-B, U+20000..U+2A6DF)": (0x20000, 0x2A6DF, 42711),
        "CJK 擴展 C 區 (Ext-C, U+2A700..U+2B73F)": (0x2A700, 0x2B73F, 4149),
        "CJK 相容漢字 (U+F900..U+FAFF)": (0xF900, 0xFAFF, 512),
        "PUA 私用區 (U+E000..U+F8FF)": (0xE000, 0xF8FF, 6400),
    }

    # 基礎各欄寬度設定
    min_name_w = max(
        max(display_width(name) for name in cjk_blocks), display_width("Unicode 區段")
    )
    count_col_w = max(15, display_width("收錄數 / 總數"))
    rate_col_w = max(8, display_width("覆蓋率"))
    gap = "   "  # 欄位間距 (3 格空白)

    # 標題文字
    title = f"分析字型: {font_path}"
    total_count = f"總編碼字碼數 (Unicode count): {len(unicodes)}"

    # 計算基本表格寬度
    base_table_w = min_name_w + len(gap) + count_col_w + len(gap) + rate_col_w

    # 決定整體的統一行寬（若字型路徑很長，表格寬度會自動等寬延展）
    line_width = max(display_width(title), display_width(total_count), base_table_w)

    # 若標題較長，將多出的寬度擴充給第一欄，確保表格線與最外框寬度完全一致
    name_w = min_name_w + (line_width - base_table_w)

    # 輸出表頭
    print("=" * line_width)
    print(pad_display(title, line_width, "left"))
    print(pad_display(total_count, line_width, "left"))
    print("=" * line_width)

    # 輸出欄位名稱
    header_name = pad_display("Unicode 區段", name_w, "left")
    header_count = pad_display("收錄數 / 總數", count_col_w, "center")
    header_rate = pad_display("覆蓋率", rate_col_w, "right")
    print(f"{header_name}{gap}{header_count}{gap}{header_rate}")
    print("-" * line_width)

    # 輸出各區段資料列
    for block_name, (start, end, total) in cjk_blocks.items():
        count = sum(1 for code in unicodes if start <= code <= end)
        rate = (count / total) * 100 if total > 0 else 0

        col_name = pad_display(block_name, name_w, "left")
        count_str = f"{count:>6} / {total:<6}"
        col_count = pad_display(count_str, count_col_w, "center")
        rate_str = f"{rate:>6.2f}%"
        col_rate = pad_display(rate_str, rate_col_w, "right")

        print(f"{col_name}{gap}{col_count}{gap}{col_rate}")

    print("=" * line_width)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_cjk.py <字型檔案路徑>")
    else:
        analyze_cjk_coverage(sys.argv[1])
