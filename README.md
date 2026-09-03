# 自託管 WebFont 倉庫

✨祈請 大寶恩師 加持

感恩所有開源字型及工具的創作者們

本倉庫收錄經過中文子集化（`cn-font-split`）切片之免費可商用 WebFont。

## 🟧發行管道異動

切片化字型檔(.woff2)已改由`npm`發行。 github 的切片字型檔將保持相容不刪除，但停止於 v1.2.2 不再更新。
後續此倉庫的版本更新主要都是針對 SDK。

## 🟨SDK 使用方式

請參考 [Font Loader SDK 說明文件](<教學說明/sdk/字型動態載入器%20(Font%20Loader%20SDK)%20使用說明文件.md>)

## 📦 字型列表與引入方式

### 🟩文鼎PL中楷

#### 字型來源說明

本專案採用文鼎科技（Arphic Technology Co., Ltd.）之 AR PL UKai 字型，並配合 Debian / Ubuntu CJK-Unifonts 社群修補後，透過 ARPHIC PUBLIC LICENSE（ARPHICPL）進行自託管與分發。切片與格式轉換後，仍須保留原始版權宣告與授權檔案。

#### 在網頁 `<head>` 中引入字型

##### 1. 載入完整字集 (所有子集整合版)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/ar-pl-ukai@2.0.0/index.css"
/>
```

##### 2. 按需載入個別子集

CN (簡體字集)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/ar-pl-ukai@2.0.0/cn/result.css"
/>
```

TW (繁體字集)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/ar-pl-ukai@2.0.0/tw/result.css"
/>
```

#### CSS 使用範例

CN (簡體字集)

```css
body {
  font-family: "AR PL UKai CN", serif;
}
```

TW (繁體字集)

```css
body {
  font-family: "AR PL UKai TW", serif;
}
```

#### 版權聲明

本字型源自文鼎科技之 ARPHIC PUBLIC LICENSE 授權字型，包含原始版權註明「Copyright (C) 1999 Arphic Technology Co., Ltd.」與相關授權說明；本倉庫已將授權檔案一併收錄於各字型資料夾及 `npm` 套件中，請於散布時一併保留。

#### 備註

- CN 字集的標點原生是"置中式"，若須"靠下式"標點，可用`"Noto Serif SC Punct"`替換標點。

---

### 🟩文鼎PL細上海宋

#### 字型來源說明

本專案採用文鼎科技（Arphic Technology Co., Ltd.）之 AR PL UMing 字型，並配合 Debian / Ubuntu CJK-Unifonts 社群修補後，透過 ARPHIC PUBLIC LICENSE（ARPHICPL）進行自託管與分發。切片與格式轉換後，仍須保留原始版權宣告與授權檔案。

#### 在網頁 `<head>` 中引入字型

##### 1. 載入完整字集 (所有子集整合版)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/ar-pl-uming@2.0.0/index.css"
/>
```

##### 2. 按需載入個別子集

CN (簡體字集)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/ar-pl-uming@2.0.0/cn/result.css"
/>
```

TW (繁體字集)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/ar-pl-uming@2.0.0/tw/result.css"
/>
```

#### CSS 使用範例

CN (簡體字集)

```css
body {
  font-family: "AR PL UMing CN", serif;
}
```

TW (繁體字集)

```css
body {
  font-family: "AR PL UMing TW", serif;
}
```

#### 版權聲明

本字型源自文鼎科技之 ARPHIC PUBLIC LICENSE 授權字型，包含原始版權註明「Copyright (C) 1999 Arphic Technology Co., Ltd.」與相關授權說明；本倉庫已將授權檔案一併收錄於各字型資料夾及 `npm` 套件中，請於散布時一併保留。

#### 備註

- 此字型的標點符號有些是"靠下式"，有些是"置中式，若須符合簡繁慣例，可用`"Noto Serif SC Punct"`、`"Noto Serif TC Punct"`或`"TW-Kai-Aligned Punct"`替換標點。

---

### 🟩寒蟬活仿宋

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/chill-huo-fangsong@1.0.0/result.css"
  />
  ```

- **CSS 使用範例**：
  ```css
  body {
    font-family: "ChillHuoFangSong", serif;
  }
  ```

---

### 🟩寒蟬正楷體 (ChillKai)

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/chill-kai@1.0.0/result.css"
  />
  ```

- **CSS 使用範例**：

  ```css
  body {
    font-family: "ChillKai", serif;
  }
  ```

- 備註：
  - `寒蟬正楷`源自`全字庫`具有：
    - 垂直位置偏低的歷史包袱。
    - 原設計目的是補齊中文字碼，未特別考慮字形之間的協調性等等，較適合用於補缺字，而非長篇排版。
  - 標點符號是簡體左下風格。

---

### 🟩匯文仿宋

- **原字型的聲明**：本字体文件开源且免费商用,禁止第三方在任何平台以任何方式用此字体牟利。如果您用付费方式获得了此字体文件,请找卖家退款。

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/huiwen-fangsong@1.0.0/result.css"
  />
  ```

- **CSS 使用範例**：
  ```css
  body {
    font-family: "Huiwen-Fangsong", serif;
  }
  ```

---

### 🟩芫荽體

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/iansui@1.0.0/result.css"
  />
  ```

- **CSS 使用範例**：
  ```css
  body {
    font-family: "Iansui", serif;
  }
  ```

---

### 🟩Instrument Sans 拉丁字子集

用來取代中文字型的拉丁文字，讓整體排版更美觀。為什麼做成子集？是因為不想取代原 Instrument Sans 所有字碼範圍的字，只想取代部分字碼。

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/instrument-sans-subset@1.0.0/result.css"
  />
  ```

- **CSS 使用範例**：
  ```css
  body {
    font-family: "Instrument Sans Subset", sans-serif;
  }
  ```

---

### 🟩Noto Serif SC 標點符號子集 / Noto Serif TC 標點符號子集

適用場景：將此字型排在 CSS font-family 的最前面，用以強制取代後方字型的標點符號，無須修改 DOM 結構。

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/noto-serif-sc-punct@1.0.0/result.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/noto-serif-tc-punct@1.0.0/result.css"
  />
  ```

- **CSS 使用範例**：

  ```css
  body {
    font-family: "Noto Serif SC Punct", serif;
  }
  body {
    font-family: "Noto Serif TC Punct", serif;
  }
  ```

---

### 🟩全字齊楷

「全字齊楷」針對「全字庫正楷體」進行了垂直位置校正，其中標點符號是採用選擇性調整，排除原已接近置中的字碼。

全字庫傳承自早期 Windows 系統的字型設計規範，其字型內部座標系（EM Square）將字身位置刻意偏下繪製。全字庫常是缺字備援的首選字型，當瀏覽器或排版軟體將不同字型的基線（Baseline）對齊於同條水平線時，全字庫字體會顯得比「文鼎楷體/宋體」等現代標準字型矮上一截，且無法單純透過 CSS 的 @font-face 參數進行垂直平移。

為避免排版時需額外撰寫 CSS (transform) 或標籤進行修正，本套件已於字型內部直接修正字形座標點，將字身垂直置中，確保全字庫在現代網頁與跨平台混排時能具備一致且完美的對齊表現。

#### 字型來源說明：

本專案字型採集自 中華民國數位發展部 / 國家發展委員會 [中文標準交換碼全字庫 (CNS 11643)]，依據 SIL OFL 1.1 進行託管與分發。

#### 在網頁 `<head>` 中引入字型

##### 1. 載入完整字集 (所有子集整合版)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/tw-kai-aligned@1.0.2/index.css"
/>
```

##### 2. 按需載入個別子集

Base (基本字集)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/tw-kai-aligned@1.0.2/base/result.css"
/>
```

Ext-B (擴充 B 字集)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/tw-kai-aligned@1.0.2/ext-b/result.css"
/>
```

Plus (自造字區)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/tw-kai-aligned@1.0.2/plus/result.css"
/>
```

#### CSS 使用範例

Base (基本字集)

```css
body {
  font-family: "TW-Kai-Aligned", serif;
}
```

Ext-B (擴充 B 字集)

```css
body {
  font-family: "TW-Kai-Aligned-Ext-B", serif;
}
```

Plus (自造字區)

```css
body {
  font-family: "TW-Kai-Aligned-Plus", serif;
}
```

---

### 🟩全字齊楷 標點符號子集

繁體慣用的「置中式」標點符號。
適用場景：將此字型排在 CSS font-family 的最前面，用以強制取代後方字型的標點符號，無須修改 DOM 結構。

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/tw-kai-aligned-punct@1.0.2/result.css"
  />
  ```

- **CSS 使用範例**：

  ```css
  body {
    font-family: "TW-Kai-Aligned Punct", serif;
  }
  ```

---

### 🟩全字齊宋

「全字齊宋」針對「全字庫正宋體」進行了垂直位置校正，其中標點符號是採用選擇性調整，排除原已接近置中的字碼。

全字庫傳承自早期 Windows 系統的字型設計規範，其字型內部座標系（EM Square）將字身位置刻意偏下繪製。全字庫常是缺字備援的首選字型，當瀏覽器或排版軟體將不同字型的基線（Baseline）對齊於同條水平線時，全字庫字體會顯得比「文鼎楷體/宋體」等現代標準字型矮上一截，且無法單純透過 CSS 的 @font-face 參數進行垂直平移。

為避免排版時需額外撰寫 CSS (transform) 或標籤進行修正，本套件已於字型內部直接修正字形座標點，將字身垂直置中，確保全字庫在現代網頁與跨平台混排時能具備一致且完美的對齊表現。

#### 字型來源說明：

本專案字型採集自 中華民國數位發展部 / 國家發展委員會 [中文標準交換碼全字庫 (CNS 11643)]，依據 SIL OFL 1.1 進行託管與分發。

#### 在網頁 `<head>` 中引入字型\*

##### 1. 載入完整字集 (所有子集整合版)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/tw-sung-aligned@1.0.2/index.css"
/>
```

##### 2. 按需載入個別子集

Base (基本字集)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/tw-sung-aligned@1.0.2/base/result.css"
/>
```

Ext-B (擴充 B 字集)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/tw-sung-aligned@1.0.2/ext-b/result.css"
/>
```

Plus (自造字區)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/tw-sung-aligned@1.0.2/plus/result.css"
/>
```

#### CSS 使用範例：

Base (基本字集)

```css
body {
  font-family: "TW-Sung-Aligned", serif;
}
```

Ext-B (擴充 B 字集)

```css
body {
  font-family: "TW-Sung-Aligned-Ext-B", serif;
}
```

Plus (自造字區)

```css
body {
  font-family: "TW-Sung-Aligned-Plus", serif;
}
```

---

### 🟩朱雀仿宋

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@xiao-xue-seng/zhuque-fangsong@1.0.0/result.css"
  />
  ```

- **CSS 使用範例**：
  ```css
  .my-text-style {
    font-family: "Zhuque Fangsong (technical preview)", serif;
  }
  ```

---

## 📦 收錄字型與版權聲明 (Credits & Licenses)

本倉庫收錄之字型均為開源、免費可商用字型，各字型版權歸屬於其原始創作者所有：

| 字型名稱                    | 原始作者 / 團隊                              | 原專案連結與授權                                                                |
| :-------------------------- | :------------------------------------------- | :------------------------------------------------------------------------------ |
| **寒蟬正楷體 / 寒蟬活仿宋** | Warren2060                                   | [GitHub](https://github.com/Warren2060) (SIL OFL 1.1)                           |
| **朱雀仿宋**                | 璇璣造字 (TrionesType)                       | [GitHub](https://github.com/TrionesType/zhuque) (SIL OFL 1.1)                   |
| **匯文仿宋**                | 特里王 (Terry Wang)                          | 復刻自 59-4 活字 (作者自訂免費商用)                                             |
| **芫荽體**                  | ButTaiwan                                    | [GitHub](https://github.com/ButTaiwan/iansui) (SIL OFL 1.1)                     |
| **文鼎PL中楷**              | 文鼎科技 / Debian / Ubuntu CJK-Unifonts 社群 | [ARPHICPL](ukai-tw/license/zh_TW.UTF-8/ARPHICPL.TXT)                            |
| **文鼎PL細上海宋**          | 文鼎科技 / Debian / Ubuntu CJK-Unifonts 社群 | [ARPHICPL](uming-tw/license/zh_TW.UTF-8/ARPHICPL.txt)                           |
| **全字庫正楷體、正宋體**    | 數位發展部 / 國家發展委員會                  | [全字庫](https://www.fonts.org.tw/) (SIL OFL 1.1)                               |
| **Instrument Sans**         | Instrument / Rodrigo Fuenzalida              | [Google Fonts](https://fonts.google.com/specimen/Instrument+Sans) (SIL OFL 1.1) |
