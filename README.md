# 自託管 WebFont 倉庫

祈請 大寶恩師 加持

本倉庫收錄經過中文子集化（`cn-font-split`）切片之免費可商用 WebFont。

## 📦 字型列表與引入方式

### 🟩寒蝉正楷體 (ChillKai)

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/chill-kai/result.css"
  />
  ```

  或使用 tag 方式，如：`v1.0.0`，cdn 快取會更穩定：(以下各字型皆同，不再重複贅述)

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1.0.0/chill-kai/result.css"
  />
  ```

- **CSS 中使用**：
  ```css
  .my-text-style {
    font-family: "ChillKai", serif;
  }
  ```

---

### 🟩全字庫正楷體 Ext-B、全字庫正宋體 Ext-B

- **字型來源說明**：
  本專案字型採集自 中華民國數位發展部 / 國家發展委員會 [中文標準交換碼全字庫 (CNS 11643)]，依據政府資料開放授權條款 (OGDL 1.0) 及 SIL OFL 1.1 進行託管與分發。

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/tw-kai-extb/result.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/tw-sung-extb/result.css"
  />
  ```

- **CSS 中使用**：

  ```css
  .my-text-style {
    font-family: "TW-Kai-Ext-B", serif;
    font-family: "TW-Sung-Ext-B", serif;
  }
  ```

- 使用 全字庫 作為 寒蟬正楷體 的罕用字備援：

  ```html
  <!-- 1. 引入主要字型 (寒蝉正楷體) -->
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/chill-kai/result.css"
  />

  <!-- 2. 引入備援字型 (全字庫 Ext-B) -->
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/tw-kai-extb/result.css"
  />

  <style>
    .my-text-style {
      font-family: "ChillKai", "TW-Kai-ExtB", serif;
    }
  </style>
  ```

---

### 🟩朱雀仿宋

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/zhuque-fangsong/result.css"
  />
  ```

- **CSS 中使用**：
  ```css
  .my-text-style {
    font-family: "Zhuque Fangsong (technical preview)", serif;
  }
  ```

---

### 🟩寒蝉活仿宋

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/chill-huo-fangsong/result.css"
  />
  ```

- **CSS 中使用**：
  ```css
  .my-text-style {
    font-family: "ChillHuoFangSong", serif;
  }
  ```

---

### 🟩汇文仿宋

- **原字型的聲明**：本字体文件开源且免费商用,禁止第三方在任何平台以任何方式用此字体牟利。如果您用付费方式获得了此字体文件,请找卖家退款。

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/huiwen-fangsong/result.css"
  />
  ```

- **CSS 中使用**：
  ```css
  .my-text-style {
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
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/iansui/result.css"
  />
  ```

- **CSS 中使用**：
  ```css
  .my-text-style {
    font-family: "Iansui", serif;
  }
  ```

---

### 🟩全字庫正楷體標點符號子集、全字庫正宋體標點符號子集

用來取代簡體字型的標點符號，以符合繁中的置中標點習慣。

- **字型來源說明**：
  本專案字型採集自 中華民國數位發展部 / 國家發展委員會 [中文標準交換碼全字庫 (CNS 11643)]，依據政府資料開放授權條款 (OGDL 1.0) 及 SIL OFL 1.1 進行託管與分發。

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/tw-kai-punct/result.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/tw-sung-punct/result.css"
  />
  ```

- **CSS 中使用**：

  放在簡體字之前，利用備援(fallback)特性取代標點符號。

  ```css
  .my-text-style {
    font-family: "TW-Kai-Punct", "ChillKai", serif;
    font-family: "TW-Sung-Punct", "ChillHuoFangSong", serif;
  }
  ```

---

### 🟩Instrument Sans 拉丁字子集

用來取代中文字型中的拉丁文字，讓整體排版更美觀。為什麼做成子集？是因為不想要取代原 Instrument Sans 所有字碼範圍的字，只想取代部分字碼。

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/instrument-sans/result.css"
  />
  ```

- **CSS 中使用**：
  ```css
  .my-text-style {
    font-family: "InstrumentSansLatinSubset", "Noto Sans TC", sans-serif;
  }
  ```

---

## 📦 收錄字型與版權聲明 (Credits & Licenses)

本倉庫收錄之字型均為開源、免費可商用字型，各字型版權歸屬於其原始創作者所有：

| 字型名稱                    | 原始作者 / 團隊                 | 原專案連結與授權                                                                |
| :-------------------------- | :------------------------------ | :------------------------------------------------------------------------------ |
| **寒蝉正楷體 / 寒蟬活仿宋** | Warren2060                      | [GitHub](https://github.com/Warren2060) (SIL OFL 1.1)                           |
| **朱雀仿宋**                | 璇璣造字 (TrionesType)          | [GitHub](https://github.com/TrionesType/zhuque) (SIL OFL 1.1)                   |
| **匯文仿宋**                | 特里王 (Terry Wang)             | 復刻自 59-4 活字 (SIL OFL 1.1)                                                  |
| **芫荽體**                  | ButTaiwan                       | [GitHub](https://github.com/ButTaiwan/iansui) (SIL OFL 1.1)                     |
| **全字庫正楷體、正宋體**    | 數位發展部 / 國家發展委員會     | [全字庫](https://www.fonts.org.tw/) (OGDL 1.0 / OFL 1.1)                        |
| **Instrument Sans**         | Instrument / Rodrigo Fuenzalida | [Google Fonts](https://fonts.google.com/specimen/Instrument+Sans) (SIL OFL 1.1) |
