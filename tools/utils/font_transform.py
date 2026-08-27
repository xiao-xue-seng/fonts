#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
模組名稱：通用字型座標轉換、縮放、輪廓攤平與元資料更名工具 (font_transform.py)
功能：
    1. 單一字型轉換處理：讀取指定字型檔 (.ttf)。
    2. 自動/自訂 UPM 平移量 (dy) 與等比例縮放 (scale_factor)。
    3. 自動水平置中補償 (dx)，確保縮放後字符仍在字寬中心。
    4. 可選強制「攤平 (Decompose)」所有複合字，避免破圖或相依遺失。
    5. 自動更名字型家族名稱與字型樣式名稱（支援英文與中文）。
    6. 輸出為全新的標準字型檔 (TTF)。
    7. 可指定要調整及要排除的 Unicode 範圍（排除範圍優先）。
===============================================================================
"""

import argparse
import os
import re
import sys
import time
from typing import Dict, Iterable, Optional, Tuple, Union
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

# 確保專案根目錄在 sys.path 中
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from tools.utils.font_metadata import update_font_metadata
except ImportError:
    from font_metadata import update_font_metadata

# ==========================================
# 預設常數設定
# ==========================================
DEFAULT_SCALE_FACTOR = 1.0
DEFAULT_STYLE_EN = "Regular"
DEFAULT_STYLE_ZH = "標準"

# 常見 UPM 對應的向上平移量參考預設值 (若未特別傳入則 dy = 0)
COMMON_DY_PRESETS: Dict[int, int] = {
    1024: 112,
    1000: 109,
    2048: 224,
}

# 自訂/未列出 UPM 時的相對 em 位移量參考值 (位移 px / 64px)
COMMON_FALLBACK_EM_SHIFT = 0.1094

# Unicode 範圍可使用 U+ 前綴（可省略），例如：U+4E00-9FFF,U+3001-303F
UnicodeRange = Tuple[int, int]


def parse_unicode_ranges(
    ranges: Optional[Union[str, Iterable[str]]],
) -> Tuple[UnicodeRange, ...]:
    """將 Unicode 範圍文字解析成包含端點的整數區間。

    支援以逗號或空白分隔的單點及區間，例如 ``U+4E00-9FFF, 3001``。
    空值代表未指定任何範圍。
    """
    if ranges is None:
        return ()

    if isinstance(ranges, str):
        values = [ranges]
    else:
        values = list(ranges)

    result = []
    for value in values:
        # 先移除區間連字號兩側的空白，讓「U+4E00 - U+9FFF」也能使用。
        normalized_value = re.sub(
            r"(?i)([0-9a-f])\s*-\s*(?=(?:U\+)?[0-9a-f])", r"\1-", value.strip()
        )
        for item in re.split(r"[\s,]+", normalized_value):
            if not item:
                continue
            match = re.fullmatch(
                r"(?:U\+)?([0-9A-Fa-f]+)(?:\s*-\s*(?:U\+)?([0-9A-Fa-f]+))?",
                item,
            )
            if not match:
                raise ValueError(
                    f"無效的 Unicode 範圍「{item}」，格式應為 U+4E00-9FFF 或 U+3001"
                )

            start = int(match.group(1), 16)
            end = int(match.group(2) or match.group(1), 16)
            if start > end or end > 0x10FFFF:
                raise ValueError(f"無效的 Unicode 範圍「{item}」")
            result.append((start, end))

    return tuple(result)


def _codepoint_in_ranges(codepoint: int, ranges: Tuple[UnicodeRange, ...]) -> bool:
    return any(start <= codepoint <= end for start, end in ranges)


# ==========================================
# 核心攤平筆刷
# ==========================================
class DecomposingTTGlyphPen(TTGlyphPen):
    """
    繼承自 TTGlyphPen，攔截所有「組合元件 (Component)」。
    遇到複合字時，強制遞迴展開成獨立的點與線，完全消滅元件相依性。
    """

    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.glyphSet = glyphSet

    def addComponent(self, glyphName, transformation):
        # 過濾無效或空指標的元件
        if not glyphName or str(glyphName) == "0":
            return

        try:
            comp_glyph = self.glyphSet[glyphName]
        except KeyError:
            return

        # 套用變換矩陣後，將子元件直接畫成普通點線
        tpen = TransformPen(self, transformation)
        comp_glyph.draw(tpen)


# ==========================================
# 輔助計算函數
# ==========================================
def get_optimal_dy(
    upm: int,
    dy: Optional[int] = None,
    dy_presets: Optional[Union[Dict[int, int], int]] = None,
    fallback_em_shift: Optional[float] = None,
    verbose: bool = True,
) -> int:
    """
    計算最適垂直平移量 dy。
    優先順序：直接指定 dy > dy_presets 字典查詢 > fallback_em_shift 計算 > 預設 0
    """
    # 1. 直接指定固定 dy
    if dy is not None:
        return dy

    # 2. dy_presets 傳入單一整數
    if isinstance(dy_presets, int):
        return dy_presets

    # 3. dy_presets 字典對應
    if isinstance(dy_presets, dict):
        if upm in dy_presets:
            return dy_presets[upm]
        if fallback_em_shift is not None:
            calculated_dy = round(upm * fallback_em_shift)
            if verbose:
                print(
                    f"[資訊] 偵測到非預設 UPM ({upm})，依比例自動計算 dy = {calculated_dy}"
                )
            return calculated_dy

    # 4. 僅提供 fallback_em_shift
    if fallback_em_shift is not None and fallback_em_shift != 0.0:
        calculated_dy = round(upm * fallback_em_shift)
        if verbose:
            print(f"[資訊] 依 em 位移比例計算 dy = {calculated_dy} (UPM: {upm})")
        return calculated_dy

    return 0


# ==========================================
# 核心轉換函數
# ==========================================
def transform_font(
    input_font_path: str,
    output_font_path: str,
    font_name_en: str,
    font_name_zh: str,
    font_style_en: str = DEFAULT_STYLE_EN,
    font_style_zh: str = DEFAULT_STYLE_ZH,
    scale_factor: float = DEFAULT_SCALE_FACTOR,
    dy: Optional[int] = None,
    dy_presets: Optional[Union[Dict[int, int], int]] = None,
    fallback_em_shift: Optional[float] = None,
    decompose: bool = True,
    unicode_ranges: Optional[Union[str, Iterable[str]]] = None,
    exclude_unicode_ranges: Optional[Union[str, Iterable[str]]] = None,
    verbose: bool = True,
) -> bool:
    """
    執行單一字型檔案之座標變換、縮放、輪廓攤平與內部名稱更新。

    :param input_font_path: 來源字型路徑 (.ttf)
    :param output_font_path: 輸出字型路徑 (.ttf)
    :param font_name_en: 新英文字型家族名稱 (例如: "TW-Kai-Aligned")
    :param font_name_zh: 新中文字型家族名稱 (例如: "全字齊楷")
    :param font_style_en: 新英文字型樣式名稱 (預設: "Regular")
    :param font_style_zh: 新中文字型樣式名稱 (預設: "標準")
    :param scale_factor: 尺寸縮放比例係數 (預設: 1.0)
    :param dy: 直接指定垂直平移量 (優先權最高)
    :param dy_presets: UPM 平移量對應物件/字典 (例: {1024: 112, 1000: 109, 2048: 224})
    :param fallback_em_shift: 未匹配 UPM 時的相對 em 位移比例
    :param decompose: 是否強制攤平所有複合字元 (預設: True)
    :param unicode_ranges: 要調整的 Unicode 範圍；空值表示不限制
    :param exclude_unicode_ranges: 要排除的 Unicode 範圍，優先於 unicode_ranges
    :param verbose: 是否輸出詳細處理進度 (預設: True)
    :return: 轉換成功回傳 True，失敗回傳 False
    """
    if not os.path.exists(input_font_path):
        print(f"[錯誤] 找不到字型檔案：{input_font_path}", file=sys.stderr)
        return False

    # 確保輸出目錄存在
    output_dir = os.path.dirname(os.path.abspath(output_font_path))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    if verbose:
        print("=" * 65)
        print(f"正在載入來源字型：{input_font_path} ...")

    start_time = time.time()
    try:
        font = TTFont(input_font_path)
    except Exception as e:
        print(f"[錯誤] 無法讀取字型檔案 {input_font_path}: {e}", file=sys.stderr)
        return False

    upm = font["head"].unitsPerEm
    try:
        included_ranges = parse_unicode_ranges(unicode_ranges)
        excluded_ranges = parse_unicode_ranges(exclude_unicode_ranges)
    except ValueError as e:
        print(f"[錯誤] {e}", file=sys.stderr)
        return False

    actual_dy = get_optimal_dy(
        upm=upm,
        dy=dy,
        dy_presets=dy_presets,
        fallback_em_shift=fallback_em_shift,
        verbose=verbose,
    )

    if verbose:
        print(f"字型 UPM       : {upm}")
        print(f"新字型英文名稱 : {font_name_en} ({font_style_en})")
        print(f"新字型中文名稱 : {font_name_zh} ({font_style_zh})")
        print(f"套用縮放比例   : {scale_factor:.3f} ({scale_factor * 100:.1f}%)")
        print(f"套用垂直平移   : dy = {actual_dy:+d}")
        print(f"強制攤平複合字 : {'是' if decompose else '否'}")
        print("=" * 65)

    glyf_table = font["glyf"]
    hmtx_table = font["hmtx"]
    glyph_set = font.getGlyphSet()
    glyph_order = font.getGlyphOrder()
    total_glyphs = len(glyph_order)

    # 以 cmap 建立需要調整的 glyph 集合。排除範圍先套用，確保優先權最高。
    best_cmap = font.getBestCmap() or {}
    excluded_glyphs = {
        glyph_name
        for codepoint, glyph_name in best_cmap.items()
        if _codepoint_in_ranges(codepoint, excluded_ranges)
    }
    if included_ranges:
        selected_glyphs = {
            glyph_name
            for codepoint, glyph_name in best_cmap.items()
            if _codepoint_in_ranges(codepoint, included_ranges)
        }
    else:
        selected_glyphs = set(glyph_order)
    glyphs_to_transform = selected_glyphs - excluded_glyphs

    if verbose:
        print(
            f"字型內共有 {total_glyphs:,} 個字符 (Glyphs)，開始進行座標轉換與輪廓處理..."
        )
        if included_ranges or excluded_ranges:
            print(
                f"符合調整範圍的 Glyphs: {len(glyphs_to_transform):,}，"
                f"排除 Glyphs: {len(excluded_glyphs):,}"
            )

    new_glyphs = {}
    new_metrics = {}
    success_count = 0
    empty_count = 0
    skipped_count = 0

    # 逐一轉換所有字形
    for idx, glyph_name in enumerate(glyph_order, start=1):
        try:
            if glyph_name not in glyphs_to_transform:
                new_glyphs[glyph_name] = glyf_table[glyph_name]
                new_metrics[glyph_name] = hmtx_table.metrics.get(glyph_name, (upm, 0))
                skipped_count += 1
                if verbose and (idx % 5000 == 0 or idx == total_glyphs):
                    percent = (idx / total_glyphs) * 100
                    elapsed = time.time() - start_time
                    print(
                        f"轉換進度: {idx:>6,}/{total_glyphs:,} ({percent:5.1f}%) | 耗時: {elapsed:.1f}s"
                    )
                continue

            # 讀取原始字寬
            orig_metrics = hmtx_table.metrics.get(glyph_name, (upm, 0))
            orig_width = orig_metrics[0]

            # 計算水平置中補償 (dx)
            dx = (orig_width - (orig_width * scale_factor)) / 2.0
            matrix = (scale_factor, 0, 0, scale_factor, dx, actual_dy)

            # 選擇使用的鋼筆（攤平或一般鋼筆）
            pen = (
                DecomposingTTGlyphPen(glyph_set) if decompose else TTGlyphPen(glyph_set)
            )
            t_pen = TransformPen(pen, matrix)
            glyph_set[glyph_name].draw(t_pen)
            transformed_glyph = pen.glyph()

            # 重新計算邊界與 LSB
            if transformed_glyph.numberOfContours == 0:
                lsb = 0
                empty_count += 1
            else:
                transformed_glyph.recalcBounds(glyf_table)
                lsb = getattr(transformed_glyph, "xMin", 0)

            new_glyphs[glyph_name] = transformed_glyph
            new_metrics[glyph_name] = (orig_width, lsb)
            success_count += 1

        except Exception as e:
            if verbose:
                print(f"[警告] 處理字符 {glyph_name} 時發生異常: {e}")
            new_glyphs[glyph_name] = glyf_table[glyph_name]
            new_metrics[glyph_name] = hmtx_table.metrics.get(glyph_name, (upm, 0))

        # 進度回報
        if verbose and (idx % 5000 == 0 or idx == total_glyphs):
            percent = (idx / total_glyphs) * 100
            elapsed = time.time() - start_time
            print(
                f"轉換進度: {idx:>6,}/{total_glyphs:,} ({percent:5.1f}%) | 耗時: {elapsed:.1f}s"
            )

    # 套用向量表更新
    if verbose:
        print("\n正在套用向量轉換結果...")
    glyf_table.glyphs = new_glyphs
    hmtx_table.metrics = new_metrics

    # 更新字型內部名稱
    if verbose:
        print(
            f"正在更新字型內部名稱為「{font_name_en} {font_style_en}」/「{font_name_zh} {font_style_zh}」..."
        )
    update_font_metadata(
        font=font,
        en_name=font_name_en,
        en_style=font_style_en,
        zh_name=font_name_zh,
        zh_style=font_style_zh,
    )

    # 儲存新字型
    if verbose:
        print("=" * 65)
        print(f"正在寫入輸出檔案：{output_font_path} ...")
    font.save(output_font_path)

    total_time = time.time() - start_time
    output_size_mb = os.path.getsize(output_font_path) / (1024 * 1024)

    if verbose:
        print("✨ 轉換完成！")
        print(
            f"成功轉換字符數 : {success_count:,} (實體字: {success_count - empty_count:,}, 空白/控制符: {empty_count:,})"
        )
        if skipped_count:
            print(f"略過未符合 Unicode 範圍的字符數 : {skipped_count:,}")
        print(f"輸出檔案大小   : {output_size_mb:.2f} MB")
        print(f"總耗時         : {total_time:.1f} 秒")
        print("=" * 65)

    return True


# ==========================================
# CLI 命令列入口
# ==========================================
def main():
    parser = argparse.ArgumentParser(
        description="通用字型座標轉換、縮放、輪廓攤平與元資料更名工具",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-i", "--input", required=True, help="來源字型檔案路徑 (.ttf)")
    parser.add_argument("-o", "--output", required=True, help="輸出字型檔案路徑 (.ttf)")
    parser.add_argument(
        "--name-en", required=True, help="新英文字型家族名稱 (例如 TW-Kai-Aligned)"
    )
    parser.add_argument(
        "--name-zh", required=True, help="新中文字型家族名稱 (例如 全字齊楷)"
    )
    parser.add_argument(
        "--style-en", default=DEFAULT_STYLE_EN, help="新英文字型樣式名稱"
    )
    parser.add_argument(
        "--style-zh", default=DEFAULT_STYLE_ZH, help="新中文字型樣式名稱"
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=DEFAULT_SCALE_FACTOR,
        help="尺寸縮放比例係數",
    )
    parser.add_argument(
        "--dy",
        type=int,
        default=None,
        help="固定垂直平移量 (若指定則優先套用此值)",
    )
    parser.add_argument(
        "--dy-1024",
        type=int,
        default=None,
        help="UPM 1024 的向上平移量 (dy)",
    )
    parser.add_argument(
        "--dy-1000",
        type=int,
        default=None,
        help="UPM 1000 的向上平移量 (dy)",
    )
    parser.add_argument(
        "--dy-2048",
        type=int,
        default=None,
        help="UPM 2048 的向上平移量 (dy)",
    )
    parser.add_argument(
        "--fallback-shift",
        type=float,
        default=None,
        help="未指定 UPM 時的相對 em 位移量 (例如 0.1094)",
    )
    parser.add_argument(
        "--no-decompose",
        action="store_true",
        help="停用複合字元強制攤平",
    )
    parser.add_argument(
        "--unicode-range",
        "--include-unicode",
        dest="unicode_ranges",
        action="append",
        default=None,
        help="要調整的 Unicode 範圍，可重複指定；格式如 U+4E00-9FFF,U+3001",
    )
    parser.add_argument(
        "--exclude-unicode-range",
        "--exclude-unicode",
        dest="exclude_unicode_ranges",
        action="append",
        default=None,
        help="要排除的 Unicode 範圍，可重複指定；優先於 --unicode-range",
    )

    args = parser.parse_args()

    # 提前驗證範圍，讓 CLI 以標準 argparse 錯誤格式結束。
    try:
        parse_unicode_ranges(args.unicode_ranges)
        parse_unicode_ranges(args.exclude_unicode_ranges)
    except ValueError as e:
        parser.error(str(e))

    # 組裝 dy_presets
    dy_presets = {}
    if args.dy_1024 is not None:
        dy_presets[1024] = args.dy_1024
    if args.dy_1000 is not None:
        dy_presets[1000] = args.dy_1000
    if args.dy_2048 is not None:
        dy_presets[2048] = args.dy_2048

    success = transform_font(
        input_font_path=args.input,
        output_font_path=args.output,
        font_name_en=args.name_en,
        font_name_zh=args.name_zh,
        font_style_en=args.style_en,
        font_style_zh=args.style_zh,
        scale_factor=args.scale,
        dy=args.dy,
        dy_presets=dy_presets if dy_presets else None,
        fallback_em_shift=args.fallback_shift,
        decompose=not args.no_decompose,
        unicode_ranges=args.unicode_ranges,
        exclude_unicode_ranges=args.exclude_unicode_ranges,
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
