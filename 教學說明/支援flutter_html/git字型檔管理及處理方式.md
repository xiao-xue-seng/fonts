## 🟨Q： 我有一個 github 公開倉庫配合 jsdelivr 作為 自託管字型庫，除了已切片.woff2 之外，為了配合APP端，也需要提供.ttf檔案，讓APP可以直接取用。其中有些 .ttf 單檔會超過 5M。這在提交時會被警告或拒絕。 您有何建議可以讓我維持提供檔案給 APP端，又維持git的效能？

## A：

將 .ttf 這種較大的二進位檔案直接放進主要 Git 數據庫，隨時間演進確實會導致 .git 目錄劇烈膨脹、clone 與 push 變慢。

特別需要留意的「陷阱」是：**千萬不要用 Git LFS 來搭配 jsDelivr**。因為 jsDelivr 只會抓取 Git 數據庫內的實體檔案；如果開啟 Git LFS，jsDelivr 抓到的會是一份僅有數十 Bytes 的 LFS 指標純文字檔，導致 APP 載入失敗。

要兼顧 APP 端直接存取、維持 Git 效能與 CDN 加速，有以下幾種最佳實踐方案：

## **方案一：使用 GitHub Release Assets（最推薦）**

如果你希望繼續免費利用 GitHub 的基礎設施，最俐落的做法是**將 .ttf 檔案排除在 Git 追蹤外，改為上傳至 GitHub Release 的附件 (Assets)**。

### **做法與優勢：**

> 1. **不佔用 Git 歷史紀錄**：檔案不屬於任何 commit，.git 數據庫保持輕量，Git 效能完全不受影響。
> 2. **APP 直接取用 URL**： \[https://github.com/username/repo/releases/download/v1.0.0/your-font.ttf\](https://github.com/username/repo/releases/download/v1.0.0/your-font.ttf)
> 3. **流量與大小限制寬鬆**：GitHub Release 單一 Asset 上限高達 2GB，且背後有 Fastly CDN 加速（APP 端通常會有本地快取機制，對下載穩定度要求極高）。

## **方案二：字型瘦身與優化（從源頭減輕體積）**

許多原始 .ttf 檔案體積龐大，是因為包含完整的 OpenType 特性數據、針對極舊 Windows 系統的 Hinting（字型微調資訊）、或是很少用到的特殊字元。

你可以利用 Python 的 fonttools 工具對 .ttf 進行減重：

`# 安裝 fonttools`
`pip install fonttools`

`# 剔除無用的微調資訊與過度細緻的數據表`
`pyftsubset your-font.ttf --unicodes="*" --layout-features="*" --glyph-names --no-hinting --output-file=your-font.min.ttf`

**效果**：通常可以將 5MB \~ 10MB 的 .ttf 瘦身 30% \~ 60%，甚至直接縮減至安全範圍內，且完全不影響 APP 端的文字顯示品質。

## **方案三：使用免費物件儲存（Cloudflare R2 \+ Cloudflare CDN）**

如果字型庫規模較大，將靜態大檔案與程式碼（Git）徹底解耦是長遠的最佳架構。

> - **Cloudflare R2**：提供 **10 GB 免費存儲**，且**完全免傳輸流量費（0 Egress Fee）**。
> - **做法**：將 .ttf 放置於 R2，綁定自訂域名，前面再覆蓋 Cloudflare CDN。APP 端存取速度快且極度穩定，完全不受 GitHub 檔案大小政策限制。

## **方案四：獨立的字型倉庫（若堅持必須使用 jsDelivr）**

如果你的 APP 架構已經寫死只走 jsDelivr 的 URL 格式（cdn.jsdelivr.net/gh/user/repo@ver/font.ttf）：

> 1. **獨立 Repository**：建立一個專門放 .ttf 的倉庫（如 font-ttf-assets），將大檔案與你日常開發的主倉庫隔離。主倉庫保持乾淨，只有這個資產庫承載歷史。
> 2. **淺層複製（Shallow Clone）**：未來維護這個資產庫時，使用 git clone \--depth 1 避免下載冗長的歷史紀錄。

## **總結建議**

> - **首選**：採用 **方案一 (GitHub Releases)** 或 **方案三 (Cloudflare R2)**，讓 Git 只負責版本控制與純文字/微型檔（如 .woff2），這是維持 Git 效能的最根本做法。
> - **補充**：在發佈前先用 **方案二 (pyftsubset)** 處理一次，能有效降低 APP 使用者的下載流量負擔。

---

## 🟨Q： 我選用方案1+方案2。對於APP(flutter_html)而言，ttf/otf字型檔中有那些資訊是不需要的呢？

## A：

在 Flutter（包含 flutter_html 插件）的渲染機制中，文字最終是交付給 Flutter 底層的文字引擎（Skia / Impeller 結合 HarfBuzz 與 FreeType）繪製在行動裝置的屏幕上。

由於手機螢幕具備極高的像素密度（High-DPI / Retina），且 APP 不需要支援傳統桌上型電腦（如舊版 Windows 的 ClearType 抗鋸齒）或實體印表機列印，因此 .ttf / .otf 字型檔中有相當多數據是可以**安全剔除**的。

以下是針對 Flutter 行動端完全不需要、且剔除後減重效果顯著的資訊：

## **1\. 完全不需要的 5 大數據類別**

### **① 網格微調資訊 (Hinting Data)**

> - **包含數據表**：fpgm, prep, cvt , gasp
> - **為何不需要**：Hinting 是為了讓字型在 96 DPI 的低解析度舊版 Windows 螢幕上維持清晰而設計的像素對齊指令。現代智慧型手機螢幕 PPI 普遍在 300\~450 以上，Mobile 渲染引擎會直接打散或忽略這些指令。
> - **減重效益**：**極高**（通常可減少 15% \~ 30% 體積）。

### **② 字元/符號名稱 (Glyph Names)**

> - **包含數據表**：post 表中的 PostScript 名稱 (Version 2.0 格式)
> - **為何不需要**：post 表 2.0 存有每一個字元的文字名稱（例如 A, B, cid00012）。APP 在顯示文字時，完全是用 **Unicode → Glyph ID**（透過 cmap 表）進行查找，名稱僅供 PDF 匯出、印刷或字型開發偵錯使用。
> - **做法**：將 post 表轉換為 Version 3.0，直接抹去所有名稱。

### **③ 桌面與 Windows 遺留數據表 (Desktop / Windows Legacy Tables)**

> - **包含數據表**：DSIG, VDMX, LTSH, hdmx, PCLT

- DSIG：數位簽章 (Digital Signature)，行動端載入時不校驗此項。
- VDMX / LTSH / hdmx：舊版 Windows 用於快速計算字型垂直/水平度量的快取表。
- PCLT：Hewlett-Packard 印表機控制語言數據。
  > - **為何不需要**：Flutter 的文字排版引擎會自行計算 Metrics，完全不讀取這些舊式表格。

### **④ 直排度量資訊 (Vertical Metrics)**

> - **包含數據表**：vhea, vmtx
> - **為何不需要**：如果你的 APP / HTML 內容**只有橫排文字**（絕大多數 UI 與網頁的狀況），垂直書寫度量資訊是完全用不到的。

### **⑤ 罕用 OpenType 特性與進階排版 (Unused OpenType Features)**

> - **包含數據表**：GSUB, GPOS 中的非必要 Feature
> - **為何不需要**：預設的字型常包涵許多印刷等級的特性，例如：小型大寫字母 (smcp)、分數寫法 (frac)、舊式數字 (onum)、花體字 (swsh) 等。APP 介面若無特別排版需求，僅需保留基礎的連字 (liga) 與字距調整 (kern) 即可。

## **2\. 針對 Flutter 優化的 pyftsubset 精準減重指令**

結合方案 1 (GitHub Releases) 與方案 2，你可以使用 Python fonttools 執行以下指令。此指令已為 Mobile APP 渲染環境進行過過濾優化：

`pyftsubset your-font.ttf \`
`--unicodes="*" \`
`--no-hinting \`
`--no-glyph-names \`
`--layout-features="kern,liga,clig,calt,locl" \`
`--drop-tables+="DSIG,VDMX,LTSH,hdmx,PCLT,vhea,vmtx,meta" \`
`--output-file=your-font.min.ttf`

### **關鍵參數說明：**

> - \--no-hinting：剔除 TrueType 指令與微調數據。
> - \--no-glyph-names：將 post 表降級為 v3.0，清空所有 PostScript 字元名稱。
> - \--layout-features="..."：僅保留連詞、字距等必備 OpenType 排版特性，刪除多餘的花體/舊式數字特性。
> - \--drop-tables+=...：強制丟棄所有桌面與直排遺留表格。

## **3\. Flutter 載入的安全底線（千萬不可刪除的表格）**

在進行手動瘦身時，請確保**不要**剔除以下基礎表格，否則 Flutter 在載入字型時會直接拋出 Exception 或變為豆腐塊（□）：

> - head / maxp：字型基本標頭與最大值定義。
> - hhea / hmtx：水平度量資訊（決定字高、行距與字寬）。
> - OS/2：字重 (Font Weight)、字型家族與斜體等系統識別資訊。
> - cmap：Unicode 對應表格（APP 找字的核心）。
> - glyf \+ loca (TTF) 或 CFF /CFF2 (OTF)：字型外框輪廓數據。

---

## 🟨Q： 執行這項優化時，如果原來的字型是可變字型，可以維持可變軸效果嗎？

## A：

**可以，完全可以維持可變軸（Variable Axes）效果！**

pyftsubset 在設計上對可變字型（Variable Fonts）非常友善。只要你在執行指令時**不要**主動指定「壓平 (Instantiate)」參數，它就會自動保留可變字型的動態調整能力（例如字重 wght、字寬 wdth、視覺大小 opsz 等）。

## **1\. 為什麼可以維持？pyftsubset 的運作機制**

當輸入檔案是可變字型時：

> - **預設行為**：pyftsubset 會自動保留 fvar（可變軸定義）、gvar / CFF2（字形變形數據）、STAT（樣式屬性表）與 HVAR（水平度量變形）等核心數據表。
> - **剔除效果**：前面建議的減重參數（如抹去微調指令 \--no-hinting、去除 PostScript 名稱 \--no-glyph-names）只會刪除無關的輔助數據，**完全不會破壞控制可變軸的變形向量 (Deltas)**。

## **2\. 執行時必須注意的 2 個「防坑陷阱」**

為了確保瘦身後的字型依然是可變字型，請特別留意：

### **❌ 絕對不要使用 \--instance 參數**

如果你在指令中加入類似 \--instance="wght=400" 或 \--instance="\*" 的參數，pyftsubset 就會將可變字型「壓平 (Flatten)」成單一或數個傳統的靜態 .ttf 檔，導致可變軸效果徹底消失。

### **❌ \--drop-tables 切勿包含可變數據表**

在設定 \--drop-tables 時，請確保**沒有**包含以下表格：

> - fvar：定義有哪些可變軸（如 wght, wdth）與數值範圍。
> - gvar / CFF2：記錄 TrueType / CFF2 字形隨軸變化的座標偏移量。
> - STAT：定義各個軸數值對應的樣式名稱。
> - HVAR / avar / MVAR：控制進階度量與軸彎曲變形的表格。

## **3\. 可變字型專用的瘦身指令**

你可以放心直接使用以下指令，對可變 .ttf 進行減重：

`pyftsubset your-variable-font.ttf \`
`--unicodes="*" \`
`--no-hinting \`
`--no-glyph-names \`
`--layout-features="kern,liga,clig,calt,locl" \`
`--drop-tables+="DSIG,VDMX,LTSH,hdmx,PCLT,vhea,vmtx,meta" \`
`--output-file=your-variable-font.min.ttf`

## **4\. Flutter 端如何調用（驗證效果）**

瘦身完成並上傳至 GitHub Release 後，Flutter（或 flutter_html）即可直接透過 FontVariation 動態控制字型：

`Text(`
`'動態字重測試',`
`style: TextStyle(`
`fontFamily: 'YourVariableFont',`
`// 透過 FontVariation 動態指定可變軸數值（如字重 550）`
`fontVariations: const [`
`FontVariation('wght', 550.0),`
`],`
`),`
`);`

**體積效益評估**：可變字型經過這套優化後，通常能在**保留無段式字重調整**的前提下，將體積壓到原始檔的 30%\~50%，對行動端 APP 的載入速度非常有幫助。

---

## 🟨Q： 另外，使用使用 GitHub Release Assets時，當每次新增一個tag時，就要新增一個Release ，然後要重新上傳一次所有ttf檔案，是嗎？

## A：

**完全不需要！** 這正是使用 GitHub Release 的一大優勢——**資產（Assets）與程式碼 Tag 是可以完全解耦（拆開維護）的，且上傳後的連結是永久穩定的。**

## **1\. 為什麼不用每次重新上傳？**

GitHub Release Assets 的下載連結格式為： \[https://github.com/使用者/倉庫/releases/download/\](https://github.com/使用者/倉庫/releases/download/)\<Tag名稱\>/\<檔案名稱\>

一旦你在某個 Tag（例如 fonts-v1.0.0）上傳了 .ttf 檔案：

> - **連結永不失效**：只要不手動刪除該 Release，這個網址就會一直存在。
> - **不受新 Tag 影響**：即便你的 GitHub 倉庫後續推了 v1.0.1、v2.0.0 等無數個新版本，APP 端繼續讀取 fonts-v1.0.0 的 .ttf 網址完全不受影響。

## **2\. 兩種極簡的維護策略**

為了避免每次發佈新版本程式碼時被字型檔案干擾，建議採用以下兩種策略之一：

### **策略 A：建立「專屬的資產 Release Tag」（最推薦 🌟）**

將「程式碼 Release」與「字型/靜態資源 Release」分開管理：

> 1. 在 GitHub 建立一個專門給字型使用的獨立 Release Tag，例如叫 **v1.0.0-fonts** 或 **assets-latest**。
> 2. 將瘦身後的 .ttf 檔案一次性上傳到這個專屬 Release 下。
> 3. **APP 端寫死這個穩定的 URL**： \[https://github.com/user/repo/releases/download/v1.0.0-fonts/your-font.min.ttf\](https://github.com/user/repo/releases/download/v1.0.0-fonts/your-font.min.ttf)
> 4. **維護方式**：未來只有在「字型本身有更新/替換」時，才需要去建立 v1.1.0-fonts 上傳新檔；平時開發 APP 或更新倉庫程式碼時，完全不用理會字型。

### **策略 B：利用 GitHub Actions 全自動處理（如果希望字型跟著 Tag 自動發佈）**

如果你希望每次推推新的 Git Tag 時，自動把倉庫裡的 .ttf 瘦身並打包上傳到該次 Release，可以用 GitHub Actions 替代人工：

`# .github/workflows/release-fonts.yml`
`name: Auto Subset and Release Fonts`

`on:`
`release:`
`types: [created]`

`jobs:`
`upload-fonts:`
`runs-on: ubuntu-latest`
`steps:`
`- name: Checkout Code`
`uses: actions/checkout@v4`

      `- name: Set up Python`
        `uses: actions/setup-python@v5`
        `with:`
          `python-version: '3.x'`

      `- name: Install fonttools`
        `run: pip install fonttools brotli`

      `- name: Run pyftsubset optimization`
        `run: |`
          `pyftsubset raw_fonts/your-font.ttf \`
            `--unicodes="*" \`
            `--no-hinting \`
            `--no-glyph-names \`
            `--layout-features="kern,liga,clig,calt,locl" \`
            `--drop-tables+="DSIG,VDMX,LTSH,hdmx,PCLT,vhea,vmtx,meta" \`
            `--output-file=your-font.min.ttf`

      `- name: Upload Font to Release`
        `uses: softprops/action-gh-release@v2`
        `with:`
          `files: your-font.min.ttf`
        `env:`
          `GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}`

**效果**：你只需要在本地推 Git Tag，GitHub 就會在背景自動執行 pyftsubset 瘦身，並自動將 .min.ttf 附加到該次 Release 附件中，完全不消耗你本地電腦的操作時間。

## **總結**

最輕鬆的做法是採納 **策略 A**：建立一個名為 fonts-v1 的 Release，將檔案放上去後就可以安心讓 APP 長期存取。未來只有字型檔案變動時，才需要登入 GitHub 進行一次性更換。

---

## 🟨Q： 上傳Release資源時，可以一次上傳多個ttf檔嗎？

## A：

**是的，完全可以！**

GitHub Release 允許你在**同一個 Release 下上傳任意數量的檔案（Assets）**。不論是 5 個、10 個還是數十個 `.ttf` / `.otf` 檔案，都可以一次性打包附加進去。

---

## 關鍵特性

- **獨立網址**：每一個上傳的字型檔都會獲得專屬且穩定的 CDN 下載連結，方便 APP 按需下載特定字型：
  `[https://github.com/](https://github.com/)<使用者>/<倉庫>/releases/download/<tag>/<檔案名稱>.ttf`
- **容量限制極高**：單一檔案上限為 **2 GB**（經由前面 Python 腳本瘦身後的字型通常只有數百 KB 到 1~2 MB，完全不需擔心）。
- **無數量上限**：GitHub 對單一 Release 的附件數量沒有嚴格限制，一次放數十個檔案都沒有問題。

---

## 三種批次上傳方式

你可以根據你的工作習慣選擇以下方式進行批次上傳：

### 1. 網頁介面（最直覺）

在 GitHub 建立或編輯 Release 時，於下方的 **"Attach binaries by dropping them here or selecting them"** 區塊，直接多選或拖拽**多個字型檔案**進行批量上傳。

### 2. 使用 GitHub CLI (`gh`) 指令（適合命令列）

如果你習慣在 Terminal 操作，可以使用官方 CLI 工具搭配萬用字元（`*`）一次性發佈：

```bash
# 建立 Release 並批量上傳 app_fonts 資料夾內的所有檔案
gh release create v1.0.0-fonts ./app_fonts/* --title "APP Font Assets v1.0.0"

# 若是要補充上傳至既有的 Release
gh release upload v1.0.0-fonts ./app_fonts/*

```

### 3. 使用 GitHub Actions（全自動化）

在 CI/CD 自動化流程中，可搭配 `softprops/action-gh-release` 使用 Glob 語法指定資料夾：

```yaml
- name: Upload Fonts to Release
  uses: softprops/action-gh-release@v2
  with:
    files: app_fonts/* # 自動抓取 app_fonts 資料夾下的所有字型檔
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

> 💡 **實用建議**：批量上傳時，建議確保每一個字型檔的檔名**簡短且不含中文或特殊符號**（例如使用 `noto-sans-tc-bold.ttf` 替代 `思源黑體-粗體.ttf`），這樣 Flutter 在透過 URL 請求下載時最不易發生 URL Encode/Decode 的解析錯誤。

---

## 🟨Q： 我有一個字型檔是 .otf ，如果要給 APP 使用，是否轉成 ttf 較好？

## A：

結論是：**不需要**特別轉成 .ttf，大部分情況下**直接保留 .otf 進行瘦身即可**。

在現代行動端開發（包含 Flutter、iOS 與 Android 原生）中，OTF 與 TTF 的支援度與效能幾乎沒有差異，甚至在許多情況下，保留 OTF 對 APP 反而更有優勢。

## **為什麼不用轉成 TTF？**

### **1\. Flutter 與行動端原生完全支援 OTF**

Flutter 底層的繪圖引擎（Skia / Impeller）以及 iOS / Android 系統底層的字型渲染庫（FreeType / HarfBuzz），對 OTF（使用 CFF 向量外框）與 TTF（使用 TrueType 向量外框）都提供 100% 的原生支援，載入與渲染速度在肉眼上完全沒有差別。

### **2\. OTF 在中文字型（CJK）上通常「體積更小」**

OTF 採用的是 PostScript (CFF) 曲線描述技術，它具備非常優秀的「子程式化 (Subroutinization)」能力——可以將字型中重複出現的部件（例如繁體中文相同的偏旁部首）合併壓縮。

> - 若將一個 CFF 格式的 OTF 轉為 TTF，因為 TrueType 的二次貝茲曲線需要更多控制點，**轉換後的 TTF 檔案體積反而常常會變大 10% \~ 20%**。

### **3\. 避免二次轉檔造成精度損失**

從 OTF (CFF 三次貝茲曲線) 強制轉為 TTF (TrueType 二次貝茲曲線) 屬於「有損轉換」。如果轉檔工具參數沒設定好，可能導致字形邊緣曲線出現微小的變形或錨點偏移。

## **什麼時候才需要考慮轉成 TTF？**

只有在以下少數極端狀況下，才需要轉成 TTF：

> 1. **可變字型（Variable Font）工具鏈相容性**：如果你的 OTF 是可變字型（採用 CFF2 表格），而你使用的某些第三方打包工具或舊版開發環境對 CFF2 支援不佳（TTF 的 gvar 相容性較廣）。
> 2. **特定的舊版繪圖套件限制**：APP 內部若使用了某些非常古老的原生繪圖 C/C++ 函式庫，且該函式庫明確聲明不支援 CFF 格式的 OTF。

## **總結與建議**

> - **直接對 .otf 瘦身**：上一步提供的 Python 腳本（optimize_fonts.py）**已經原生支援 .otf 檔案**。
> - **直接執行**：你只要把 .otf 檔案放進來源資料夾，腳本就會呼叫 fonttools 產出最佳化後的 .otf 瘦身檔，可以直接供 Flutter 使用，不需要額外做格式轉換！

---
