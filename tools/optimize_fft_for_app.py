import sys
import argparse
import subprocess
import time
from pathlib import Path

DEFAULT_INPUT_DIR = "tools/ttf-raw"
DEFAULT_OUTPUT_DIR = "tools/ttf-optimized"

def check_fonttools_installed():
    try:
        import fontTools
        return True
    except ImportError:
        return False

def human_readable_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def optimize_font(input_path: Path, output_path: Path) -> tuple[bool, str]:
    """
    使用 fontTools.subset 模組對單一 TTF/OTF 字型進行瘦身最佳化。
    保留可變字型軸 (Variable Font Axes)，剔除行動端 (APP) 不需要的情境數據表。
    """
    cmd = [
        sys.executable, "-m", "fontTools.subset",
        str(input_path),
        "--unicodes=*",
        "--no-hinting",
        "--no-glyph-names",
        "--layout-features=kern,liga,clig,calt,locl",
        "--drop-tables+=DSIG,VDMX,LTSH,hdmx,PCLT,vhea,vmtx,meta",
        f"--output-file={output_path}"
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0 and output_path.exists():
            return True, ""
        else:
            return False, result.stderr or result.stdout
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(
        description="針對 Mobile APP (Flutter 等) 自動進行 TTF/OTF 字型批量瘦身與最佳化工具"
    )
    parser.add_argument(
        "-i", "--input", default=DEFAULT_INPUT_DIR, type=str,
        help=f"來源資料夾路徑 (預設: {DEFAULT_INPUT_DIR}；搜尋其中的 .ttf 與 .otf 檔案)"
    )
    parser.add_argument(
        "-o", "--output", default=DEFAULT_OUTPUT_DIR, type=str,
        help=f"瘦身後字型的輸出資料夾路徑 (預設: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true",
        help="是否遞迴搜尋子資料夾中的字型檔案"
    )

    args = parser.parse_args()

    if not check_fonttools_installed():
        print("❌ 錯誤：未找到 fonttools 套件。")
        print("請先執行以下指令安裝依賴：")
        print("   pip install fonttools brotli")
        sys.exit(1)

    input_dir = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"❌ 來源資料夾不存在或不是有效目錄：{input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    pattern = "**/*" if args.recursive else "*"
    font_files = [
        p for p in input_dir.glob(pattern)
        if p.is_file() and p.suffix.lower() in [".ttf", ".otf"]
    ]

    if not font_files:
        print(f"⚠️ 在 '{input_dir}' 中找不到任何 .ttf 或 .otf 檔案。")
        sys.exit(0)

    print("=" * 65)
    print("🚀 開始進行字型瘦身最佳化")
    print(f"📂 來源資料夾: {input_dir}")
    print(f"📂 輸出資料夾: {output_dir}")
    print(f"🎯 找到字型檔數量: {len(font_files)} 個")
    print("=" * 65)

    total_orig_size = 0
    total_opt_size = 0
    success_count = 0

    start_time = time.time()

    for idx, font_path in enumerate(font_files, 1):
        rel_path = font_path.relative_to(input_dir)
        out_font_path = output_dir / rel_path
        out_font_path.parent.mkdir(parents=True, exist_ok=True)

        orig_size = font_path.stat().st_size
        total_orig_size += orig_size

        print(f"[{idx}/{len(font_files)}] 處理中: {rel_path} ({human_readable_size(orig_size)})...", end="", flush=True)

        success, err_msg = optimize_font(font_path, out_font_path)

        if success:
            opt_size = out_font_path.stat().st_size
            total_opt_size += opt_size
            reduction = (1 - (opt_size / orig_size)) * 100 if orig_size > 0 else 0
            print(f" ✅ 完成! ({human_readable_size(opt_size)}, 減少 {reduction:.1f}%)")
            success_count += 1
        else:
            print(" ❌ 失敗!")
            print(f"   詳細錯誤訊息: {err_msg.strip()}")

    elapsed = time.time() - start_time
    print("=" * 65)
    print("🎉 全部處理完成！")
    print(f"⏱️ 耗時: {elapsed:.2f} 秒")
    print(f"📊 成功率: {success_count}/{len(font_files)}")
    if total_orig_size > 0 and success_count > 0:
        total_reduction = (1 - (total_opt_size / total_orig_size)) * 100
        saved_bytes = total_orig_size - total_opt_size
        print(f"📦 總體積變化: {human_readable_size(total_orig_size)} -> {human_readable_size(total_opt_size)}")
        print(f"📉 總共節省了: {human_readable_size(saved_bytes)} ({total_reduction:.1f}%)")
    print("=" * 65)

if __name__ == "__main__":
    main()
