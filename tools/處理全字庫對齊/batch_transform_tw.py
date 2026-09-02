#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
程式名稱：全字庫字型專用批次座標對齊、縮放與自動更名處理程式 (batch_transform_tw.py)
說明：
    專為全字庫正楷體 (TW-Kai) 與正宋體 (TW-Sung) 量身打造。

    先利用 tw-align-tuner.html 分別調整出 楷體與宋體的參數，填入此工具的常數中。

    在 VS Code 等 IDE 中可直接點擊「執行 (Run)」一鍵批次處理。
===============================================================================
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List

from fontTools.ttLib import TTFont, TTLibError

# 確保專案根目錄在 sys.path 中以利載入 tools.utils 模組
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.utils.font_transform import transform_font

# ==============================================================================
# 1. 資料夾路徑常數設定
# ==============================================================================
INPUT_DIR = PROJECT_ROOT / "temp" / "ttf-raw"  # 來源字型資料夾
OUTPUT_DIR = PROJECT_ROOT / "temp" / "ttf-to-next"  # 輸出字型資料夾

# ==============================================================================
# 2. 處理開關常數設定 (True: 處理 / False: 跳過)
# ==============================================================================
PROCESS_KAI = True  # 是否處理 全字庫楷體 (TW-Kai)
PROCESS_SUNG = True  # 是否處理 全字庫宋體 (TW-Sung)

# ==============================================================================
# 3. 楷體 (TW-Kai) 專用參數設定 (主字集、Ext-B、Plus 共用此組參數)
# ==============================================================================
KAI_BASE_NAME_EN = "TW-Kai-Aligned"  # 新英文字型家族名稱基礎
KAI_BASE_NAME_ZH = "全字齊楷"  # 新中文字型家族名稱基礎
# 版號更動原則
#   變更來源檔案：更新主版號
#   調整整體參數：更新次版號
#   調整排除字元：更新修訂版號
# git tag 與 傳統 OpenType 規範的 fontRevision 欄位的對映：
#   v1.0.0 → Version 1.000 (修訂版號用兩碼)
#   v1.1.0 → Version 1.100
#   v1.1.1 → Version 1.101
KAI_VERSION = "1.002"  # 楷體衍生字型版本號
KAI_SCALE_FACTOR = 1.006  # 縮放比例係數
KAI_DY = 90  # UPM 1024 向上平移量

# ==============================================================================
# 4. 宋體 (TW-Sung) 專用參數設定 (主字集、Ext-B、Plus 共用此組參數)
# ==============================================================================
SUNG_BASE_NAME_EN = "TW-Sung-Aligned"  # 新英文字型家族名稱基礎
SUNG_BASE_NAME_ZH = "全字齊宋"  # 新中文字型家族名稱基礎
SUNG_VERSION = "1.002"  # 宋體衍生字型版本號
SUNG_SCALE_FACTOR = 1.000  # 縮放比例係數
SUNG_DY = 90  # UPM 1024 向上平移量

# ==============================================================================
# 全字庫固定的三個字集擴展結構後綴規則
# ==============================================================================
SUBSET_RULES = [
    {"suffix_file": "-98_1.ttf", "suffix_en": "", "suffix_zh": ""},
    {"suffix_file": "-Ext-B-98_1.ttf", "suffix_en": "-Ext-B", "suffix_zh": " Ext-B"},
    {"suffix_file": "-Plus-98_1.ttf", "suffix_en": "-Plus", "suffix_zh": " Plus"},
]

# 這些標點原本就已置中或接近置中，不需要再調整。
EXCLUDE_UNICODE_RANGES = "2022-2031,203C,2042,2044,2047-2049,204E,3000-3003,FE52,FE54-FE57,FF01,FF0C,FF0E,FF1A,FF1B,FF1F"

# 2000-206F,  # 通用標點（“ ” ‘ ’ — … 等）
# 3000-303F,  # CJK 符號和標點（、 。 《 》 「 」 【 】 等）
# FE10-FE1F,  # 直排形式
# FE30-FE4F,  # CJK 相容形式（直排引號、專名線等）
# FE50-FE6F,  # 小型變體形式（繁體/Big5 相容標點如 ﹐ ﹑ ﹖ 等）
# FF00-FFEF,  # 全形 ASCII 標點（！ ？ ， ： ； 等）


def has_matching_transform_metadata(
    input_font_path: str | Path,
    output_font_path: str | Path,
    scale_factor: float,
    dy: int,
    decompose: bool,
    version: str,
    unicode_ranges: object,
    exclude_unicode_ranges: object,
) -> bool:
    """判斷輸出字型是否已使用相同的變形參數。"""
    input_font_path = Path(input_font_path)
    output_font_path = Path(output_font_path)

    if not output_font_path.exists():
        return False

    try:
        with TTFont(str(input_font_path), lazy=True) as input_font:
            upm = input_font["head"].unitsPerEm

        with TTFont(str(output_font_path), lazy=True) as output_font:
            meta_table = output_font.get("meta")
            if meta_table is None or "xfrm" not in meta_table.data:
                return False
            metadata = json.loads(meta_table.data["xfrm"].decode("utf-8"))
    except (
        OSError,
        KeyError,
        TypeError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        TTLibError,
    ):
        return False

    expected = {
        "scale_factor": scale_factor,
        "dy": dy,
        "upm": upm,
        "decompose": decompose,
        "version": version,
        "unicode_ranges": unicode_ranges,
        "exclude_unicode_ranges": exclude_unicode_ranges,
    }
    return all(metadata.get(key) == value for key, value in expected.items())


def generate_tasks() -> List[Dict]:
    """
    根據常數開關與基礎名稱，自動合成待執行的 FONT_TASKS 清單
    """
    tasks = []

    # 產生楷體任務
    if PROCESS_KAI:
        for rule in SUBSET_RULES:
            tasks.append(
                {
                    "font_type": "楷體 (Kai)",
                    "filename": f"TW-Kai{rule['suffix_file']}",
                    "name_en": f"{KAI_BASE_NAME_EN}{rule['suffix_en']}",
                    "name_zh": f"{KAI_BASE_NAME_ZH}{rule['suffix_zh']}",
                    "version": KAI_VERSION,
                    "scale_factor": KAI_SCALE_FACTOR,
                    "dy": KAI_DY,
                }
            )

    # 產生宋體任務
    if PROCESS_SUNG:
        for rule in SUBSET_RULES:
            tasks.append(
                {
                    "font_type": "宋體 (Sung)",
                    "filename": f"TW-Sung{rule['suffix_file']}",
                    "name_en": f"{SUNG_BASE_NAME_EN}{rule['suffix_en']}",
                    "name_zh": f"{SUNG_BASE_NAME_ZH}{rule['suffix_zh']}",
                    "version": SUNG_VERSION,
                    "scale_factor": SUNG_SCALE_FACTOR,
                    "dy": SUNG_DY,
                }
            )

    return tasks


def run_batch():
    tasks = generate_tasks()

    print("=" * 70)
    print(" 全字庫字型批次座標對齊、縮放與自動更名處理作業")
    print("=" * 70)
    print(f"來源目錄: {INPUT_DIR.resolve()}")
    print(f"輸出目錄: {OUTPUT_DIR.resolve()}")
    print(f"處理楷體: {'啟用' if PROCESS_KAI else '停用'}")
    if PROCESS_KAI:
        print(
            f"  └ 楷體名稱: {KAI_BASE_NAME_EN} / {KAI_BASE_NAME_ZH} | Version: {KAI_VERSION} | Scale: {KAI_SCALE_FACTOR:.3f} | dy: {KAI_DY}"
        )
    print(f"處理宋體: {'啟用' if PROCESS_SUNG else '停用'}")
    if PROCESS_SUNG:
        print(
            f"  └ 宋體名稱: {SUNG_BASE_NAME_EN} / {SUNG_BASE_NAME_ZH} | Version: {SUNG_VERSION} | Scale: {SUNG_SCALE_FACTOR:.3f} | dy: {SUNG_DY}"
        )
    print(f"待處理字型數: {len(tasks)}")
    print("=" * 70)

    if not tasks:
        print("[提示] 目前楷體與宋體皆未啟用，無任務需執行。")
        return

    # 確保輸出目錄存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 檢查來源檔案完整度
    missing_files = []
    for task in tasks:
        in_path = INPUT_DIR / task["filename"]
        if not in_path.exists():
            missing_files.append(in_path)

    if missing_files:
        print("[警告] 以下來源字型檔案不存在：")
        for mf in missing_files:
            print(f"  ❌ {mf}")
        print("-" * 70)

    batch_start_time = time.time()
    success_count = 0
    fail_count = 0
    skip_count = 0

    for idx, task in enumerate(tasks, start=1):
        filename = task["filename"]
        name_en = task["name_en"]
        name_zh = task["name_zh"]
        font_type = task["font_type"]
        version = task["version"]
        scale_factor = task["scale_factor"]
        dy = task["dy"]

        in_path = INPUT_DIR / filename
        out_filename = f"{name_en}.ttf"
        out_path = OUTPUT_DIR / out_filename

        print(
            f"\n[{idx}/{len(tasks)}] 正在處理 [{font_type}]：{filename} -> {out_filename}"
        )
        print(f"     名稱：{name_en} / {name_zh}")
        print(f"     版本：{version} | 參數：scale = {scale_factor:.3f}, dy = {dy:+d}")

        if not in_path.exists():
            print(f"     ⏩ 來源檔案不存在，跳過此項。")
            skip_count += 1
            continue

        if has_matching_transform_metadata(
            input_font_path=in_path,
            output_font_path=out_path,
            scale_factor=scale_factor,
            dy=dy,
            decompose=True,
            version=version,
            unicode_ranges=None,
            exclude_unicode_ranges=EXCLUDE_UNICODE_RANGES,
        ):
            print("     ⏩ 輸出檔案已存在且變形參數相同，跳過此項。")
            skip_count += 1
            continue

        item_start = time.time()
        ok = transform_font(
            input_font_path=str(in_path),
            output_font_path=str(out_path),
            font_name_en=name_en,
            font_name_zh=name_zh,
            scale_factor=scale_factor,
            dy=dy,
            decompose=True,
            verbose=True,
            # unicode_ranges="",
            exclude_unicode_ranges=EXCLUDE_UNICODE_RANGES,
            version=version,
        )

        item_elapsed = time.time() - item_start
        if ok:
            success_count += 1
            print(f"     ✅ 完成！耗時: {item_elapsed:.1f} 秒")
        else:
            fail_count += 1
            print(f"     ❌ 失敗！耗時: {item_elapsed:.1f} 秒")

    batch_total_time = time.time() - batch_start_time
    print("\n" + "=" * 70)
    print(" 批次作業摘要統計")
    print("=" * 70)
    print(f"總任務數     : {len(tasks)}")
    print(f"成功完成     : {success_count}")
    print(f"失敗         : {fail_count}")
    print(f"略過 (無檔案): {skip_count}")
    print(f"總耗時       : {batch_total_time:.1f} 秒")
    print("=" * 70)


if __name__ == "__main__":
    run_batch()
