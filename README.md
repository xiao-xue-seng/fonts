# 自託管 WebFont 倉庫

祈請 大寶恩師 加持

本倉庫收錄經過中文子集化（`cn-font-split`）切片之免費可商用 WebFont。

## 📦 字型列表與引入方式

### 1. 寒蝉正楷體 (ChillKai)

- **授權**：SIL Open Font License 1.1
- **CSS 引入網址**：

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/chill-kai/result.css"
  />
  ```

  或使用 tag 方式，如：v1.0.0，cdn 快取會更穩定：(以下各字型皆同，不再重複贅述)

  ```html
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1.0.0/chill-kai/result.css"
  />
  ```

- **CSS 套用**：
  ```css
  font-family: "ChillKai", serif;
  ```

### 2. 全字庫正楷體 Ext-B、全字庫正宋體 Ext-B

- **字型來源說明**：
  本專案字型採集自 中華民國數位發展部 / 國家發展委員會 [中文標準交換碼全字庫 (CNS 11643)]，依據政府資料開放授權條款 (OGDL 1.0) 及 SIL OFL 1.1 進行託管與分發。

- **CSS 引入網址**：

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

- **CSS 套用**：

  ```css
  font-family: "TW-Kai-Ext-B", serif;
  font-family: "TW-Sung-Ext-B", serif;
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
    body {
      font-family: "ChillKai", "TW-Kai-ExtB", serif;
    }
  </style>
  ```
