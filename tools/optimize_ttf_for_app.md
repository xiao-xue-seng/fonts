這是一個為您量身打造的 Python 腳本（optimize_fonts.py），它能自動掃描指定資料夾中的所有 .ttf 與 .otf 檔案，針對 Mobile APP（如 Flutter）進行精準瘦身，並且**完整保留可變字型（Variable Fonts）的可變軸屬性**。

### **💡 腳本特色與優化項目**

1. **APP 專用極致瘦身**：

- **剔除 Hinting 指令** (--no-hinting)：移除針對舊電腦螢幕的像素對齊數據。
- **剔除字元名稱表** (--no-glyph-names)：將 post 表轉為 v3.0，清理無用名稱。
- **丟棄桌面/印表機遺留數據表** (--drop-tables+=...)：自動移除 DSIG (簽章)、VDMX / LTSH / hdmx (Windows度量)、PCLT (印表機數據)、vhea/vmtx (直排數據) 與 meta 表。
- **保留關鍵 OpenType 特性**：保留字距調整與基礎連詞（kern,liga,clig,calt,locl）。

2. **完整支援可變字型**：

- 未使用任何壓平（Flatten/Instance）參數，自動保留 fvar, gvar, CFF2, STAT 等可變軸定義與動態變形數據。

3. **優良的 CLI 互動與統計**：

- 支援指定**來源資料夾**、**輸出資料夾**與**遞迴搜尋**。
- 自動計算並顯示每一個檔案的瘦身前後體積差異與總計節省的流量比例。

### **📦 前置準備**

執行腳本前，請確保系統已安裝 fonttools 及相關依賴：

`pip install fonttools brotli`

### **🚀 使用說明**

#### **1\. 基本用法 (指定來源與輸出資料夾)**

`python optimize_fonts.py -i ./raw_fonts -o ./app_fonts`

#### **2\. 遞迴搜尋子資料夾 (-r 或 \--recursive)**

如果你的字型散落在子資料夾中，加入 \-r 參數會自動維持原有的目錄結構並輸出到目標資料夾：

`python optimize_fonts.py -i ./my_font_library -o ./optimized_output -r`
