# 自託管 WebFont 倉庫

祈請 大寶恩師 加持

感恩所有開源字型的創作者們

本倉庫收錄經過中文子集化（`cn-font-split`）切片之免費可商用 WebFont。

## 📦 字型列表與引入方式

### 🟩寒蝉正楷體 (ChillKai)

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/chill-kai/result.css"
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
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/tw-kai-extb/result.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/tw-sung-extb/result.css"
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
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/chill-kai/result.css"
  />

  <!-- 2. 引入備援字型 (全字庫 Ext-B) -->
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/tw-kai-extb/result.css"
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
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/zhuque-fangsong/result.css"
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
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/chill-huo-fangsong/result.css"
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
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/huiwen-fangsong/result.css"
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
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/iansui/result.css"
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
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/tw-kai-punct/result.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/tw-sung-punct/result.css"
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

### 🟩文鼎楷體 / 明體（台灣版與大陸版）

- **字型來源說明**：
  本專案採用文鼎科技（Arphic Technology Co., Ltd.）之 AR PL UKai / AR PL UMing 字型，並配合 Debian / Ubuntu CJK-Unifonts 社群修補後，透過 ARPHIC PUBLIC LICENSE（ARPHICPL）進行自託管與分發。切片與格式轉換後，仍須保留原始版權宣告與授權檔案。

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/ukai-tw/result.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/ukai-cn/result.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/uming-tw/result.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/uming-cn/result.css"
  />
  ```

- **CSS 中使用**：

  ```css
  .my-text-style {
    font-family: "AR PL UKai TW", serif;
  }
  .my-text-style {
    font-family: "AR PL UKai CN", serif;
  }
  .my-text-style {
    font-family: "AR PL UMing TW", serif;
  }
  .my-text-style {
    font-family: "AR PL UMing CN", serif;
  }
  ```

- **版權聲明**：
  本字型源自文鼎科技之 ARPHIC PUBLIC LICENSE 授權字型，包含原始版權註明「Copyright (C) 1999 Arphic Technology Co., Ltd.」與相關授權說明；本倉庫已將授權檔案一併收錄於各字型資料夾中，請於散布時一併保留。

---

### 🟩Instrument Sans 拉丁字子集

用來取代中文字型中的拉丁文字，讓整體排版更美觀。為什麼做成子集？是因為不想要取代原 Instrument Sans 所有字碼範圍的字，只想取代部分字碼。

- **授權**：SIL Open Font License 1.1

- **在網頁 `<head>` 中引入字型**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/instrument-sans/result.css"
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

| 字型名稱                        | 原始作者 / 團隊                              | 原專案連結與授權                                                                                                         |
| :------------------------------ | :------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **寒蝉正楷體 / 寒蟬活仿宋**     | Warren2060                                   | [GitHub](https://github.com/Warren2060) (SIL OFL 1.1)                                                                    |
| **朱雀仿宋**                    | 璇璣造字 (TrionesType)                       | [GitHub](https://github.com/TrionesType/zhuque) (SIL OFL 1.1)                                                            |
| **匯文仿宋**                    | 特里王 (Terry Wang)                          | 復刻自 59-4 活字 (SIL OFL 1.1)                                                                                           |
| **芫荽體**                      | ButTaiwan                                    | [GitHub](https://github.com/ButTaiwan/iansui) (SIL OFL 1.1)                                                              |
| **文鼎楷體（台灣版 / 大陸版）** | 文鼎科技 / Debian / Ubuntu CJK-Unifonts 社群 | [ARPHICPL](ukai-tw/license/zh_TW.UTF-8/ARPHICPL.TXT) / [ARPHICPL](ukai-cn/license/zh_CN.UTF-8/ARPHICPL.TXT) (ARPHICPL)   |
| **文鼎明體（台灣版 / 大陸版）** | 文鼎科技 / Debian / Ubuntu CJK-Unifonts 社群 | [ARPHICPL](uming-tw/license/zh_TW.UTF-8/ARPHICPL.txt) / [ARPHICPL](uming-cn/license/zh_CN.utf-8/ARPHICPL.txt) (ARPHICPL) |
| **全字庫正楷體、正宋體**        | 數位發展部 / 國家發展委員會                  | [全字庫](https://www.fonts.org.tw/) (OGDL 1.0 / OFL 1.1)                                                                 |
| **Instrument Sans**             | Instrument / Rodrigo Fuenzalida              | [Google Fonts](https://fonts.google.com/specimen/Instrument+Sans) (SIL OFL 1.1)                                          |
