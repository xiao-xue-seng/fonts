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

import os
import sys
import time
from typing import Dict, List

# 確保專案根目錄在 sys.path 中以利載入 tools.utils 模組
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tools.utils.font_transform import transform_font

# ==============================================================================
# 1. 資料夾路徑常數設定
# ==============================================================================
INPUT_DIR = os.path.join(PROJECT_ROOT, "temp", "ttf-raw")  # 來源字型資料夾
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "temp", "ttf-to-next")  # 輸出字型資料夾

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
KAI_SCALE_FACTOR = 1.010  # 縮放比例係數
KAI_DY = 98  # UPM 1024 向上平移量

# ==============================================================================
# 4. 宋體 (TW-Sung) 專用參數設定 (主字集、Ext-B、Plus 共用此組參數)
# ==============================================================================
SUNG_BASE_NAME_EN = "TW-Sung-Aligned"  # 新英文字型家族名稱基礎
SUNG_BASE_NAME_ZH = "全字齊宋"  # 新中文字型家族名稱基礎
SUNG_SCALE_FACTOR = 1.000  # 縮放比例係數
SUNG_DY = 96  # UPM 1024 向上平移量

# ==============================================================================
# 全字庫固定的三個字集擴展結構後綴規則
# ==============================================================================
SUBSET_RULES = [
    {"suffix_file": "-98_1.ttf", "suffix_en": "", "suffix_zh": ""},
    {"suffix_file": "-Ext-B-98_1.ttf", "suffix_en": "-Ext-B", "suffix_zh": " Ext-B"},
    {"suffix_file": "-Plus-98_1.ttf", "suffix_en": "-Plus", "suffix_zh": " Plus"},
]


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
    print(f"來源目錄: {os.path.abspath(INPUT_DIR)}")
    print(f"輸出目錄: {os.path.abspath(OUTPUT_DIR)}")
    print(f"處理楷體: {'啟用' if PROCESS_KAI else '停用'}")
    if PROCESS_KAI:
        print(
            f"  └ 楷體名稱: {KAI_BASE_NAME_EN} / {KAI_BASE_NAME_ZH} | Scale: {KAI_SCALE_FACTOR:.3f} | dy: {KAI_DY}"
        )
    print(f"處理宋體: {'啟用' if PROCESS_SUNG else '停用'}")
    if PROCESS_SUNG:
        print(
            f"  └ 宋體名稱: {SUNG_BASE_NAME_EN} / {SUNG_BASE_NAME_ZH} | Scale: {SUNG_SCALE_FACTOR:.3f} | dy: {SUNG_DY}"
        )
    print(f"待處理字型數: {len(tasks)}")
    print("=" * 70)

    if not tasks:
        print("[提示] 目前楷體與宋體皆未啟用，無任務需執行。")
        return

    # 確保輸出目錄存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 檢查來源檔案完整度
    missing_files = []
    for task in tasks:
        in_path = os.path.join(INPUT_DIR, task["filename"])
        if not os.path.exists(in_path):
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
        scale_factor = task["scale_factor"]
        dy = task["dy"]

        in_path = os.path.join(INPUT_DIR, filename)
        out_filename = f"{name_en}.ttf"
        out_path = os.path.join(OUTPUT_DIR, out_filename)

        print(
            f"\n[{idx}/{len(tasks)}] 正在處理 [{font_type}]：{filename} -> {out_filename}"
        )
        print(f"     名稱：{name_en} / {name_zh}")
        print(f"     參數：scale = {scale_factor:.3f}, dy = {dy:+d}")

        if not os.path.exists(in_path):
            print(f"     ⏩ 來源檔案不存在，跳過此項。")
            skip_count += 1
            continue

        item_start = time.time()
        ok = transform_font(
            input_font_path=in_path,
            output_font_path=out_path,
            font_name_en=name_en,
            font_name_zh=name_zh,
            scale_factor=scale_factor,
            dy=dy,
            decompose=True,
            verbose=True,
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
