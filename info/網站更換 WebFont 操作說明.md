### 📢 網站更換 WebFont（網路字型）操作說明

> **💡 核心觀念釐清：**
> 更換網頁字型**完全不需要修改 API 或後端資料庫內容**！
> WebFont 屬於單純的「前端外觀呈現（HTML / CSS）」，只需在網頁載入字型 CSS 並指定字型名稱即可。

具體操作只需以下 3 個步驟：

---

#### 1. 修改通用 CSS 樣式表（替換字型名稱）

將後台/全站通用樣式表中原本的字型名稱進行替換：

- **楷書**：字型名稱改為 `"ChillKai"`
- **仿宋**：字型名稱改為 `"Iansui"`

#### 2. 在網頁 `<head>` 中引入字型（建議儘量靠前放置）

在網站的首頁及每個獨立頁面的 `<head>` 標籤中，加入以下兩行代碼：

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/iansui/result.css"
/>
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/chill-kai/result.css"
/>
```

_(小提示：把這兩行放在 `<head>` 越靠前的位置，字型載入越快，可以避免網頁文字閃爍的問題)_

#### 3. 在 CSS 中套用新字型

完成上述兩步後，網頁就會自動顯示新字型了。若需要在特定元件或網頁區塊單獨套用，直接在 CSS 中指定即可：

```css
/* 使用寒蟬正楷體 */
.kai-text {
  font-family: "ChillKai", serif;
}

/* 使用芫荽體（仿宋） */
.fangsong-text {
  font-family: "Iansui", serif;
}
```
