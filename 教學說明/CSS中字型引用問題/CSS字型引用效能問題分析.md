(這次問的是 Gemini 3.6 Flash ， 假設它對自家的 Google Fonts 會熟悉一點)

## 🟨Q：

我有一個網站會透過API取得"公用的CSS"，用來統一控制正文內容的樣式。
這份共用的CSS是透過"管理後台"更新其內容，會有一些網站/服務同時引用這份CSS，以便統一所有平台的正文樣式及字型。這份CSS的開頭如下：

```
/*Noto Sans TC (Traditional Chinese) 黑體（思源繁黑體 -）可以設定的 font-weight 字體粗細的變化比較多樣化，從最細到最粗*/
@import url(https://fonts.googleapis.com/earlyaccess/notosanstc.css);
/*font-family: 'Noto Sans TC', sans-serif;*/

/*Noto Sans SC (Simplified Chinese) 黑體（思源簡黑體 -）可以設定的 font-weight 字體粗細的變化比較多樣化，從最細到最粗*/
@import url(https://fonts.googleapis.com/earlyaccess/notosanssc.css);
/*font-family: 'Noto Sans SC', sans-serif;*/

/*cwTeXYen (Chinese Traditional) 圓體字型*/
@import url(https://fonts.googleapis.com/earlyaccess/cwtexyen.css);
/*font-family: 'cwTeXYen', sans-serif;*/

/*cwTeXFangSong (Chinese Traditional) 仿宋體字型*/
@import url(https://fonts.googleapis.com/earlyaccess/cwtexfangsong.css);
/*font-family: 'cwTeXFangSong', serif;*/

/*cwTeXKai (Chinese Traditional) 楷體字型*/
@import url(https://fonts.googleapis.com/earlyaccess/cwtexkai.css);
/*font-family: 'cwTeXKai', serif;*/

/*cwTeXMing (Chinese Traditional) 明體字型*/
@import url(https://fonts.googleapis.com/earlyaccess/cwtexming.css);
/*font-family: 'cwTeXMing', serif;*/

@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@100..900&family=Noto+Serif+SC:wght@200..900&family=LXGW+WenKai+TC:wght@300;400;700&display=swap');

@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@200..900&display=swap');

/*"Noto Serif Tibetan" GOOGLE FONT 藏文字型*/
/* @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+Tibetan:wght@100..900&display=swap'); */
/*font-family: "Noto Serif Tibetan", serif;*/

@font-face {
	font-family: "Monlam Uni OuChan2";
	src: url("https://cdn.amec.amrtf.org/asset/common/fonts/Monlam_Uni_OuChan2.ttf");
}

/* 拉丁字 */
@font-face{
	font-family: 'Noto Sans TC';
	font-weight: 400;
	src: local("Arial");
	unicode-range: U+0000-02FF, U+1D00-1DBF, U+1E00-1EFF, U+2070-218F, U+2C60-2C7F, U+A720-A7FF, U+AB30-AB6F;
}

@font-face{
	font-family: 'Noto Sans TC';
	font-weight: 700;
	src: local("Arial-BoldMT");
	unicode-range: U+0000-02FF, U+1D00-1DBF, U+1E00-1EFF, U+2070-218F, U+2C60-2C7F, U+A720-A7FF, U+AB30-AB6F;
}

/* 破折號、刪節號 */
@font-face{
	font-family: 'cwTeXKai';
	font-weight: 500;
	src: local('標楷體'), local('STKaitiTC-Regular'), local('BiauKaiTC-Regular'), local('Helvetica');
	unicode-range: U+2500, U+2026;
}
@font-face{
	font-family: 'cwTeXFangSong';
	font-weight: 500;
	src: local('標楷體'), local('STKaitiTC-Regular'), local('BiauKaiTC-Regular'), local('Helvetica');
	unicode-range: U+2500, U+2026;
}

/* 單引號、雙引號 */
@font-face{
	font-family: 'cwTeXKai';
	font-weight: 500;
	src: local('標楷體'), local('LiSungLight'), local('Trebuchet MS'), local('Andale Mono'), local('Didot'), local('Georgia'), local('Times New Roman');
	unicode-range: U+201C, U+201D, U+2018, U+2019;
}
@font-face{
	font-family: 'cwTeXFangSong';
	font-weight: 500;
	src: local('標楷體'), local('LiSungLight'), local('Trebuchet MS'), local('Andale Mono'), local('Didot'), local('Georgia'), local('Times New Roman');
	unicode-range: U+201C, U+201D, U+2018, U+2019;
}

.amrtf-amec.zh-hans .ck-content,
.task\.edit.amrtf-amec.zh-hans .ck-content,
body[data-theme=light] .context-root .content .context.amrtf-amec.zh-hans,
body[data-theme=dark] .context-root .content .context.amrtf-amec.zh-hans,
.amrtf-amec.zh-hans{
    font-weight: 400;
    font-family: 'Noto Sans SC', sans-serif;
    font-style: normal;
    font-optical-sizing: auto;
}

.amrtf-amec.bo .ck-content,
.task\.edit.amrtf-amec.bo .ck-content,
body[data-theme=light] .context-root .content .context.amrtf-amec.bo,
body[data-theme=dark] .context-root .content .context.amrtf-amec.bo,
.amrtf-amec.bo{
    bottom:0.18em;
    font-size:100%;
    font-family:'Monlam Uni OuChan2', serif;
    line-height:1.0;
    position:relative;
}
#amrtf-amec{
	width:100%;
}
.amrtf-amec span.seek-to::after,.amrtf-amec seek-to::after{content:attr(data-label)}
.amrtf-amec .image img{width:100%}
.amrtf-amec p{line-height:1.618;text-indent:2em;margin-block-start:1em;text-align:justify;margin-block-end:1em}
.amrtf-amec blockquote p{line-height:1.5;text-indent:0;text-align:justify}
...
```

請先審查這份CSS的內容，我想專注於"字型的引用"部分來探討。

---

## A：

這份 CSS 檔在字型載入與設定上有相當多的歷史包袱與效能隱患。作為跨平台共用的核心 CSS，目前的寫法會嚴重影響引用該 CSS 之網站的**首屏載入速度（LCP）**、**版面跳動（CLS）**，並可能導致**字型樣式覆蓋異常**。

以下為針對「字型引用」部分的重點審查與問題剖析：

### 1. 嚴重警告：使用已棄用的 Google Fonts Early Access API

代碼開頭引用了大量 `/earlyaccess/` 網址：

```css
@import url(https://fonts.googleapis.com/earlyaccess/notosanstc.css);
@import url(https://fonts.googleapis.com/earlyaccess/cwtexyen.css);
/* ... cwTeX 相關字型 ... */
```

- **問題點**：Google 官方早就停止維護 Early Access 管道，且 Early Access 版本的中文 Webfont 未經過良好的切片（CSS Subsetting）優化，**一份完整的字型 CSS 與字型檔會高達 3MB~5MB 以上**。
- **致命影響**：阻擋網頁渲染（Render-Blocking）。每次使用者載入頁面，瀏覽器都會同步下載這 5~6 個巨大的舊版字型 CSS。

### 2. 重複引用與載入衝突（Duplicate Imports）

代碼同時引入了舊版與新版（Google Fonts API v2）的字型：

```css
/* 舊版 Early Access */
@import url(https://fonts.googleapis.com/earlyaccess/notosanstc.css);

/* 新版 Google Fonts API v2 */
@import url("https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@100..900&...&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@200..900&display=swap");
```

- **問題點**：`Noto Sans TC` 與 `Noto Sans SC` 在舊版與新版都被引入了一次。新版 `css2` 支援動態切片（Unicode-range subsetting）與 `font-display: swap`，舊版則無。這導致瀏覽器重複下載相同名稱的字型檔。

### 3. 用 `@font-face` 強制覆蓋區域字元範圍（Unicode-range Hijacking）

代碼中出現了多段類似以下的設定：

```css
/* 拉丁字強制用 Arial 替代 Noto Sans TC */
@font-face {
  font-family: "Noto Sans TC";
  font-weight: 400;
  src: local("Arial");
  unicode-range: U+0000-02FF, ...;
}

/* 破折號、標點符號強制用系統標楷體 */
@font-face {
  font-family: "cwTeXKai";
  font-weight: 500;
  src: local("標楷體"), local("STKaitiTC-Regular"), ...;
  unicode-range: U+2500, U+2026;
}
```

- **問題點**：

1. 將 `font-family: 'Noto Sans TC'` 命名給 `src: local("Arial")`，這是打破 CSS 語意規範的危險做法。當開發者宣告 `font-family: 'Noto Sans TC'` 時，英文會變成 Arial，中文才會是思源黑體，且全形半形字元的基線（Baseline）可能無法對齊，造成排版上下跳動。
2. `cwTeXKai` 本身已經是網路字型（Webfont），但這裡又用本地系統字型（標楷體）註冊了相同的名稱去覆蓋特定的 Unicode 標點符號。如果使用者是 Windows（有標楷體）與 Mac（無標楷體，使用 STKaiti），兩者渲染出來的標點符號寬度與視覺效果會不一致。

### 4. 託管字型檔未優化與潛在跨域問題（CORS）

```css
@font-face {
  font-family: "Monlam Uni OuChan2";
  src: url("https://cdn.amec.amrtf.org/asset/common/fonts/Monlam_Uni_OuChan2.ttf");
}
```

- **問題點**：

1. 直接載入 `.ttf` 原始檔。現代瀏覽器皆支援壓縮率更高的 **`.woff2`** 格式，`.ttf` 檔案通常過大（尤其是藏文字型）。
2. 缺少 `font-display` 屬性（如 `font-display: swap;`），導致字型載入完成前可能出現「不可見文字區塊（FOIT, Flash of Invisible Text）」。
3. 跨網站引用時，若 CDN 未設置 `Access-Control-Allow-Origin: *` HTTP Header，其他引用此 CSS 的服務可能會被瀏覽器擋下字型載入。

### 5. 隱形不可見字元（Non-breaking space 污染）

在選擇器部分：

```css
.amrtf-amec.zh-hans .ck-content,
.task\.edit.amrtf-amec.zh-hans .ck-content,
...

```

- **問題點**：選擇器結尾處（逗號後面）混入了 **`U+00A0` (No-Break Space, 不換行空格)**，而非標準的 `U+0020` 空格。某些嚴格的 CSS 解析器或建置工具會因此判斷 CSS 語法錯誤，導致該段樣式完全失效。

### 審查總結表

| 項目           | 目前狀態                                           | 潛在風險 / 影響                              |
| -------------- | -------------------------------------------------- | -------------------------------------------- |
| **載入效能**   | 引入 6+ 個 Early Access API 與重複的 v2 API        | 嚴重拖慢首屏載入（LCP），阻塞頁面渲染        |
| **字型格式**   | 使用 `.ttf` 且無 `font-display`                    | 造成 FOIT（文字閃爍/暫時隱形），檔案體積過大 |
| **字體排版**   | 強制用 `unicode-range` 將 Arial 注入 Noto 命名空間 | 基線不對齊、字體寬度異常、跨平台顯示不一致   |
| **語法安全性** | 包含不換行空格（`U+00A0`）                         | 部分瀏覽器或打包工具解析失敗                 |

### 建議的優化方向

1. **全面拔除 `@import url(.../earlyaccess/...)**`，改為統一透過 Google Fonts API v2 載入（或者由自己的 CDN 託管拆切後的 `.woff2`）。
2. **停止在 `@font-face` 中對既有字型名稱（如 Noto Sans TC）進行拉丁字或標點符號的補丁式覆蓋**。應改在 CSS 的 fallback chain 中統一處理，例如：

```css
font-family: Arial, "Noto Sans TC", sans-serif;
```

3. **自訂字型補上 `font-display: swap;` 並轉碼為 `.woff2**`。

您希望我們接下來針對這份 CSS 進行**結構重構與代碼清理**，還是進一步討論**如何在跨網站架構下優化中/藏文字型的載入效能**？

---

## 🟨Q：

OK。我想先專注於字型的引用方式來探討，包含您提到的「如何在跨網站架構下優化字型的載入效能」，請提供符合目前主流的做法。
這份CSS中，引入字型的用意應該是希望能透過"管理後台"網頁來控制正文的字型，所以透過 @import url(...) 方式載入字型，這應當沒問題吧？

---

## A：

透過管理後台動態更新 CSS 檔案，並在 CSS 開頭使用 `@import url(...)` 載入字型，在**架構概念**上是合理的，但**在實作細節與現代前端效能標準上，這並非最佳做法**。

在跨網站（Multi-tenant / Cross-domain）架構下，如果直接在 CSS 中寫死 `@import` 外部字型，會遇到嚴重的**效能瓶頸（瀑布流延遲）**與**快取控制問題**。

以下針對「目前主流做法」與「@import 的效能陷阱」進行深入解析與重構建議：

### 1. 為什麼直接使用 `@import` 會造成效能瓶頸？

當其他網站引用這份「公用 CSS」時，瀏覽器的載入流程會變成**多重連鎖請求（Font Waterfall）**：

1. **主網站** HTML 解析到 `<link rel="stylesheet" href=".../common.css">`。
2. 瀏覽器下載並解析 `common.css`。
3. 瀏覽器在 `common.css` 開頭發現 `@import url('[https://fonts.googleapis.com/](https://fonts.googleapis.com/)...')`，暫停渲染，開始下載 Google Fonts CSS。
4. Google Fonts CSS 下載完成並解析後，瀏覽器才知道真正要下載的字型檔 (`.woff2`) 網址。
5. 瀏覽器發起第 3 層請求去下載 `.woff2` 字型檔。
6. **結果**：使用者會遇到長達數秒的文字空白（FOIT）或版面劇烈跳動（CLS），尤其在行動網路環境下更明顯。

### 2. 現代主流優化方案（跨網站架構）

要達到「透過後台動態控制字型」，同時具備「極致載入速度」，目前主流有以下兩種最佳實踐：

#### 方案 A：雙軌分離模式（HTML 預載 + CSS 變數控制）—— 最推薦

將「**字型檔案的下載**」與「**字型的套用（後台控制）**」解耦。

- **第一步：主網站 HTML 負責「預先連線與載入字型」**
  引用公用 CSS 的子網站，在 HTML `<head>` 中加入 `preconnect` 與 Google Fonts CSS 引用（可使用現代的 `css2` API 整合一次載入）：

```html
<!-- 1. 提前建立 TLS 握手連線 -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />

<!-- 2. 一次性打包引入所需字型 (Noto Sans, Noto Serif, Ma Shan Zheng 等) -->
<link
  href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@300;400;700&family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@100..900&family=Noto+Sans+TC:wght@100..900&family=Noto+Serif+SC:wght@200..900&family=Noto+Serif+TC:wght@200..900&display=swap"
  rel="stylesheet"
/>
```

- **第二步：公用 CSS 透過 CSS 變數（CSS Custom Properties）控制**
  公用 CSS 檔案中**完全移除 `@import**`，僅保留字型指定與預設備援（Fallback）：

```css
:root {
  /* 後台可透過動態更新此變數或 class 來切換字型 */
  --main-font-family:
    "Noto Sans TC", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    sans-serif;
}

/* 簡體中文環境 */
.amrtf-amec.zh-hans {
  font-family: var(--main-font-family-hans, "Noto Sans SC", sans-serif);
  font-style: normal;
}

/* 藏文環境 */
.amrtf-amec.bo {
  font-family: "Monlam Uni OuChan2", "Noto Serif Tibetan", serif;
}
```

#### 方案 B：自建 CDN 自託管字型（Self-Hosting）

如果平台需要支援「藏文」或自訂的特殊的 `.ttf` / `.woff2` 字型（例如 `Monlam Uni OuChan2`），強烈建議將字型檔 hosted 在自己的跨國 CDN（如 Cloudflare / AWS CloudFront）上。

1. **格式轉碼**：將 `.ttf` 轉為 **`.woff2`** 格式（體積可減少 30% ~ 50%）。
2. **CORS 設定**：CDN 必須設定 HTTP Header 允許跨域引用：

```http
Access-Control-Allow-Origin: *
Cache-Control: public, max-age=31536000, immutable

```

3. **在公用 CSS 中聲明 `@font-face**`：

```css
@font-face {
  font-family: "Monlam Uni OuChan2";
  src:
    url("https://cdn.amec.amrtf.org/asset/common/fonts/Monlam_Uni_OuChan2.woff2")
      format("woff2"),
    url("https://cdn.amec.amrtf.org/asset/common/fonts/Monlam_Uni_OuChan2.ttf")
      format("truetype");
  font-display: swap; /* 確保字型下載完成前先用系統字型顯示，避免文字隱形 */
}
```

### 3. 優化後的公用 CSS 字型引入範例

若管理後台產出的公用 CSS 必須包含字型載入邏輯，請將舊有的十幾個 `@import` 簡化為**單一 Google Fonts v2 請求**，並補上自訂字型優化：

```css
/* 1. 濃縮為單一 v2 API 請求，並帶上記號 &display=swap */
@import url("https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@400;700&family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@400;700&family=Noto+Sans+TC:wght@400;700&family=Noto+Serif+SC:wght@400;700&family=Noto+Serif+TC:wght@400;700&display=swap");

/* 2. 藏文字型自託管設定 (補上 font-display: swap 與 woff2) */
@font-face {
  font-family: "Monlam Uni OuChan2";
  src: url("https://cdn.amec.amrtf.org/asset/common/fonts/Monlam_Uni_OuChan2.woff2")
    format("woff2");
  font-display: swap;
}

/* 3. 中英文與標點符號 Fallback 鏈設計（取代原有的 unicode-range 強制覆蓋） */
:root {
  --font-tc:
    "Noto Sans TC", Arial, "PingFang TC", "Microsoft JhengHei", sans-serif;
  --font-sc:
    "Noto Sans SC", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
}

/* 4. 樣式套用 */
.amrtf-amec.zh-hans .ck-content,
.amrtf-amec.zh-hans {
  font-weight: 400;
  font-family: var(--font-sc);
  font-style: normal;
}

.amrtf-amec.bo .ck-content,
.amrtf-amec.bo {
  font-size: 100%;
  font-family: "Monlam Uni OuChan2", "Noto Serif Tibetan", serif;
  line-height: 1.5;
}
```

---

## 🟨Q：

關於當前寫法中「@import 會造成效能瓶頸」部分，我想確認一下是每個 @import 都會個別造成延遲，還是整個 common.css 中的所有 @import 合併起來會延遲一次？

---

## A：

簡單來說：**每個外部 `@import` 都是獨立的 HTTP 請求，瀏覽器預設會「串行（Sequence）」下載它們，因此延遲是會「層層疊加」的。**

如果不小心形成多層嵌套，延遲會呈倍數成長；即使寫在同一支 CSS 開頭，也會顯著拉長整體下載時間。

### 1. 同一支 CSS 裡的多個 `@import`：串行下載延遲

當瀏覽器下載並解析您的 `common.css` 時，會從上到下掃描 `@import`：

```css
@import url(https://fonts.googleapis.com/.../notosanstc.css);  /* 請求 1 */
@import url(https://fonts.googleapis.com/.../notosanssc.css);  /* 請求 2 */
@import url(https://fonts.googleapis.com/.../cwtexyen.css);   /* 請求 3 */
...

```

- **瀏覽器的處理方式**：
  雖然現代瀏覽器會試圖同時發起多個 HTTP/2 或 HTTP/3 請求，但 **CSS 的解析順序具有嚴格限制**。在所有 `@import` 的 CSS 檔案完全下載並解析完畢之前，瀏覽器會暫停渲染（Block Rendering）頁面正文。
- **延遲累加機制**：
  如果寫了 8 個 `@import`，瀏覽器就必須建立 8 次連線（或在同一連線發送 8 個 Request）。頁面畫面呈現的等待時間，取決於**這 8 個請求中下載最慢的那一個**，而不是全部打包只算一次連線時間。

### 2. 致命的「多層瀑布流（Font Waterfall）」：層層相扣的連鎖延遲

這是 `@import` 引用 Webfont 最嚴重的問題。以 Google Fonts 為例，連鎖過程如下：

```
[1] 瀏覽器下載 HTML
     ↓ (發現 <link rel="stylesheet" href="common.css">)
[2] 瀏覽器下載 common.css
     ↓ (解析 common.css 開頭，發現 @import url('https://fonts.googleapis...'))
[3] 瀏覽器發起 HTTP 請求下載 Google Fonts CSS
     ↓ (下載完畢，解析內容，裡面包含了字型檔的 @font-face { src: url(...) })
[4] 瀏覽器發起 HTTP 請求下載真正的 .woff2 字型檔
     ↓
[5] 文字終於正常顯示

```

**這意味著**：

- 整個連鎖反應需要 **4 次往返（RTT - Round Trip Time）** 才能拿到字型檔。
- 如果使用者在行動網路環境，單次往返需時 100ms，光是字型呈現的連鎖等待時間就高達 `100ms × 4 = 400ms`。
- 在這 400ms 期間，頁面文字要麼是**隱形的（FOIT）**，要麼會**突然跳動變換字體（CLS）**。

### 3. 如何證明與改進？

您可以透過瀏覽器的 **开发者工具 (F12) -> Network (網路)** 頁籤，觀察 Network Waterfall（網路瀑布流圖表）：

- **使用多個 `@import` 時**：會看到一長串階梯狀的條形圖，後面的請求都在等前面的請求完成。
- **合併為單一 `<link>` 或將 @import 合併為一支時**：
  如果將 8 個 Google Fonts 寫法簡化為單一 API 請求：

```css
/* 8 次請求縮減為 1 次請求 */
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+SC&family=Noto+Sans+TC&family=Noto+Serif+TC&display=swap");
```

這樣瀏覽器只需要發起 **1 次** Google CSS 請求，就能同時取得所有字型的片段資訊，連锁等待層級立即減少。

### 總結

- **不是合併延遲一次**：每個 `@import` 都會發起一個獨立的 HTTP 請求。
- **阻塞渲染時間加長**：@import 越多，瀏覽器鎖定頁面不渲染的時間就越長。
- **最適做法**：將多個字型需求整合為**單一 URL 請求**，並盡可能將連線宣吿（如 `<link rel="preconnect">`）提前至 HTML 中，打破多層連鎖的效能瓶頸。

---

## 🟨Q：

後來我們已經利用 github + jsdelivr 自託管多個免費開源字型，也寫了一個 api\font-loader.js 供各平台呼叫：

```html
<head>
  <meta charset="UTF-8" />
  <!-- 💡 建議放在 <head> 靠前的位置，讓字型連線與下載最早開始發揮效能 -->
  <script
    src="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/api/font-loader-min.js"
    data-site="amec"
    async
  ></script>
  ...
</head>
```

它可以讀取「紀錄網站所需字型的 JSON 檔」，例如 amec.json，然後進行：

- 自動預先連線 (Preconnect)：自動分析字型來源網域，並預先建立網路連線（含跨域安全性設定），縮短下載延遲。若 HTML 本身已經手動寫過連線標籤，SDK 會聰明判斷並跳過，不重複建立。
- 智慧去重載入 (Deduplication)：載入字型前會先檢查頁面上是否已經寫了該字型。連版本號差異（如 `@v1.1.0` 與 `@main`）都會自動忽略並比對，如果網站已有該字型，SDK 會直接保留網站原本的連結，不會產生重複下載的問題。

管理者只要修改 amec.json 就可以控制前端的正文字型。

並且，前端會使用以下方式一次性載入四個 Noto 字型，做為網站的基礎字型。由於內容所需的字重種類較多，所以請求了5種常用字重，而不請求全範圍字重(100..900)。

```html
<link
  id="google-fonts-link"
  href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Noto+Sans+SC:wght@300;400;500;700;900&family=Noto+Serif+TC:wght@300;400;500;700;900&family=Noto+Serif+SC:wght@300;400;500;700;900&display=swap"
  rel="stylesheet"
/>
```

這樣您覺得如何？

---

## A：

這套改進架構相當傑出！整體設計精準地擊中了現代 Web 效能優化的核心：**「利用 CDN 託管拆分資源」、「用 JS SDK 動態去重與預先連線（Preconnect）」**，並且「將 Google Fonts 整合為單一請求並精簡字重」。

這種設計不僅大幅減少了過去 `@import` 帶來的多層瀑布流延遲，也保留了管理者透過 JSON (例如 `amec.json`) 動態控制字型的彈性。

針對您目前的架構，以下進行優點評估以及 3 個細節上的隱患提示：

### 亮點與值得肯定之處

1. **GitHub + jsDelivr 自託管（Self-hosting）**：

- 將自訂或開源字型（如藏文、 cwTeX 等）放到 CDN 上，能顯著降低主伺服器負載，且 jsDelivr 具有優秀的全球 POP 節點與 HTTP/2、HTTP/3 支援。

2. **自動 Preconnect 與動態去重（Deduplication）**：

- JS SDK 能分析網域並自動插入 `<link rel="preconnect">`，消除了 TLS 握手的時間瓶頸。
- 比對版本號並跳過重複載入，避免了跨平台引用的資源浪費。

3. **Google Fonts 整合與精減字重**：

- 將 4 個 Noto 字型縮減為**單一 `<link>` 請求**。
- 指定 `wght@300;400;500;700;900` 而非全範圍 `100..900`，這非常關鍵——Google Fonts API v2 會根據請求的字重組合來決定返回的 CSS 區塊與 Unicode 切片數量，精簡字重能實質減少生成的 CSS 體積與字型檔下載量。
- 補上了 `&display=swap`，確保字型下載期間頁面文字不會隱形（避免 FOIT）。

### 需要特別留意的 3 個隱患與優化建議

#### 1. SDK 的 async 載入與 FOUT (Flash of Unstyled Text)

在 `<head>` 中使用了 `async` 載入 `font-loader-min.js`：

```html
<script src="..." data-site="amec" async></script>
```

- **潛在問題**：`async` 代表該腳本是「非同步」下載與執行的。如果頁面 HTML 與 CSS 渲染得非常快，而 SDK 還在網路傳輸或解析 `amec.json`，使用者會先看到預設系統字型，待 SDK 將字型檔注入後，頁面字型突然轉變（這稱為 FOUT），甚至觸發**版面跳動（CLS, Cumulative Layout Shift）**。
- **建議做法**：
  如果 `amec.json` 裡面控制的是「正文預設字型」，建議去掉 `async`，或者使用 **`CSS Font Loading API`** (`document.fonts`) 來進行無縫切換；如果是次要/特定區塊字型，使用 `async` 則完全沒有問題。

#### 2. jsDelivr 的 CDN 限制與 CORS Header

- **潛在問題**：當您在自己的網站頁面中通過 CSS 載入由 jsDelivr 託管的 `.woff2` 或 `.ttf` 時，瀏覽器會嚴格檢查 **CORS (Cross-Origin Resource Sharing)**。
- **確認事項**：jsDelivr 預設對靜態資源有開啟 `Access-Control-Allow-Origin: *`，但若是透過 GitHub Release 或特定目錄結構動態讀取，請確保跨域載入時不會在 console 出現 CORS blocked 警示（特別是舊版 Safari 或 Safari iOS）。

#### 3. Google Fonts API v2 的切片與載入量

雖然您只請求了 5 個字重，但**同時請求 4 個中文字型（TC 黑/明 + SC 黑/明）**：

- Noto Sans TC (5 weights)
- Noto Sans SC (5 weights)
- Noto Serif TC (5 weights)
- Noto Serif SC (5 weights)
- **說明**：Google Fonts 雖然會做 Unicode Subsetting（動態切片），但在首頁載入時，這 20 個組合（4字型 × 5字重）產生的 `@font-face` CSS 仍有一定體積。
- **優化建議**：
  若管理後台可以區分**語系環境**（例如繁體中文頁面只下載 TC，簡體中文頁面只下載 SC），將請求拆開（繁體頁只請求 TC，簡體頁只請求 SC），首屏要下載的字型 CSS 體積可以**直接砍半**。

### 總結

您目前的解決方案已經具備大型企業級前端架構的水準。只要確保：

1. SDK 執行時間不會造成過度的版面閃爍（CLS）。
2. 未來考慮依語系（TC / SC）拆分 Google Fonts 請求。

這套以 **`font-loader.js + JSON 配置 + jsDelivr CDN`** 為核心的機制非常健全且維護性極高！

---

## 🟨Q：

使用這套字型SDK後，SDK已提供涵蓋網站所需全部字型，假使原來 common.css 中的 @import url(...) 沒有刪除會有什麼影響嗎？會是備援的效果嗎？

---

## A：

**完全不會有備援的效果，反而會對網站效能產生負面打擊，甚至造成字型樣式覆蓋混亂。**

如果您在 SDK 已載入全部字型的狀況下，依然在 `common.css` 中保留舊有的 `@import url(...)`，會帶來以下 4 個具體影響：

### 1. 毫無「備援（Fallback）」作用

CSS 的機制是**只要聲明了 `@import`，瀏覽器就會無條件執行**。

- **原因**：CSS 無法像程式碼一樣判斷「如果 SDK 沒載入成功，才執行 `@import`」。
- **實際狀況**：無論 SDK 有沒有成功載入字型，`common.css` 開頭的每個 `@import` **每次都會被瀏覽器強制發起 HTTP 請求去下載**。它無法作為備份，只會變成基礎的強制負擔。

### 2. 破壞 SDK 的「去重（Deduplication）」機制，造成重複下載

SDK 的去重邏輯通常是檢查 HTML DOM 中是否已存在該字型的 `<link>` 或 `@font-face`。

但 `@import` 是寫在 CSS 檔案內部的：

- 瀏覽器下載 `common.css` 時，會**同步**去請求 `@import` 裡的 Google Early Access 舊版字型。
- 結果就是：使用者同時下載了 **SDK 載入的現代版字型** 以及 **`common.css` 帶入的舊版大檔案字型**。
- 兩種字型會在背景同時佔用頻寬，讓原本 SDK 做的去重優化完全失效。

### 3. 重蹈覆蓋衝突與「字型名稱搶奪」

在原本的 `common.css` 中，含有大量的自訂 `@font-face`（例如把 Arial 覆蓋到 `Noto Sans TC` 上，或者覆蓋標點符號）：

```css
/* 舊 common.css 中的覆蓋設定 */
@font-face{
	font-family: 'Noto Sans TC';
	src: local("Arial");
	...
}

```

- **後果**：當 SDK 載入標準且完整的 `Noto Sans TC` 後，`common.css` 裡的這段舊寫法會再次覆蓋它。這會導致 SDK 辛苦載入的標準字型，在英文字元或標點符號上又被硬生生替換回系統字型，出現字型渲染不一致或基線錯位的情況。

### 4. 重新觸發「渲染阻塞（Render-Blocking）」與瀑布流延遲

這會直接取消 SDK 所帶來的效能提升：

- 瀏覽器下載 `common.css` 後，因為看到開頭有 `@import`，會**暫停渲染頁面**，並開始連線到 Google 的舊伺服器。
- SDK 建立的 Preconnect 優化與雙軌載入優勢，會被 `@import` 的阻塞機制完全拉慢。

### 正確的處理方式

既然 SDK 已經涵蓋了網站所需的所有字型，**必須將 `common.css` 開頭所有的 `@import url(...)` 以及相關的舊版 `@font-face` 補丁徹底刪除**。

- **真正的備援（Fallback）** 應該寫在 CSS 的 `font-family` 屬性中，而不是透過 `@import`：

```css
/* 正確的備援寫法：若 SDK 字型載入失敗，自動降級使用系統字型 */
.amrtf-amec.zh-hans {
  font-family:
    "Noto Sans SC",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    "Microsoft YaHei",
    sans-serif;
}
```

這樣寫才能確保：SDK 載入成功就用 `Noto Sans SC`；若網路有狀況，瀏覽器會自動順暢切換到後方的系統預設字型（如 `Microsoft YaHei`），這才是標準且無效能損耗的備援機制。
