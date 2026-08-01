# 📚 字型動態載入器 (Font Loader SDK) 使用說明文件

這套工具是用來幫您的網站**自動載入專屬字型**的輕量級 SDK。透過簡單的一行程式碼，網站就能自動連線到中央字型庫，載入您需要的字型，並在 Vue 3 前端專案中輕鬆使用。

---

## 🚀 第一步：如何在網站中引入 SDK

請在網站 HTML（通常是 `index.html`）的 **`<head>` 標籤內靠前的位置**，加入以下這行 `<script>` 程式碼：

```html
<head>
  <meta charset="UTF-8" />
  <!-- 💡 建議放在 <head> 靠前的位置，讓字型連線與下載最早開始發揮效能 -->
  <script
    src="https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/api/font-loader-min.js"
    data-site="amec"
    async
  ></script>
  ...
</head>
```

### 關鍵參數說明：

- **`data-site="amec"`**（重要）：
  這個屬性是告訴 SDK：「**請幫我讀取 amec 這個網站專用的字型清單**」。
  SDK 會自動去抓取 `https://.../api/amec.json` 設定檔。未來如果擴充了新網站（例如 `amrtf`），只需新增設定檔後，將此處改成 `data-site="amrtf"` 即可，完全不用改動 JS 內容！

✨ **如果您只是要顯示字型，不需要取得字型清單等進階資訊，那麼到這裡就全部完成了！** ✨

---

## 🛠️ 第二步：全域物件 `window.__FONT_SDK__` 介紹

當 SDK 載入後，它會在瀏覽器的全域環境（`window`）自動掛載一個名為 **`__FONT_SDK__`** 的物件，並發送一個完成事件。

### 1. SDK 提供的方法與屬性

| 名稱                      | 型態       | 說明                                              |
| :------------------------ | :--------- | :------------------------------------------------ |
| **`isReady`**             | `Boolean`  | 標記字型清單是否已載入完畢（`true` 表示已就緒）。 |
| **`getAvailableFonts()`** | `Function` | 呼叫後會回傳目前網站可用的**字型陣列清單**。      |

### 2. 回傳的字型物件結構 (Font Item)

呼叫 `getAvailableFonts()` 時，會拿到像這樣的陣列資料：

```json
[
  {
    "id": "chill-kai",
    "name": "ChillKai",
    "displayName": "寒蟬楷體",
    "cssUrl": "https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/chill-kai/result.css"
  },
  {
    "id": "iansui",
    "name": "Iansui",
    "displayName": "芫荽體",
    "cssUrl": "https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/iansui/result.css"
  }
]
```

---

## 💚 第三步：在 Vue 3 專案中使用 (Composition API + JavaScript)

如果您要在 Vue 3 專案中取得可用的字型清單（例如做成字型選擇下拉選單），請參考以下範例：

### Vue 3 實戰範例程式碼：

```vue
<template>
  <div class="font-selector-demo">
    <h3>字型選擇器範例</h3>

    <!-- 下拉選單：展示所有可用的字型 -->
    <select v-model="selectedFont">
      <option value="">預設系統字型</option>
      <option v-for="font in fontList" :key="font.id" :value="font.name">
        {{ font.displayName }}
      </option>
    </select>

    <!-- 預覽區塊：套用選擇的字型 -->
    <div
      class="text-preview"
      :style="{
        fontFamily: selectedFont
          ? `'${selectedFont}', sans-serif`
          : 'sans-serif',
      }"
    >
      這是一段預覽文字。Hans words Test Text 123.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

// 儲存字型清單
const fontList = ref([]);
// 使用者選擇的字型名稱 (對應 CSS 的 font-family)
const selectedFont = ref("");

// 處理字型設定的邏輯
function setupFonts(fonts) {
  fontList.value = fonts;
  console.log("成功取得可用字型清單：", fonts);
}

onMounted(() => {
  // 情況 1：如果 SDK 已經載入完成 (isReady === true)
  if (window.__FONT_SDK__?.isReady) {
    setupFonts(window.__FONT_SDK__.getAvailableFonts());
  }
  // 情況 2：如果 SDK 還在網路下載中，監聽 'fonts:loaded' 自訂事件
  else {
    window.addEventListener(
      "fonts:loaded",
      (event) => {
        // event.detail 會包含最新的字型陣列
        setupFonts(event.detail);
      },
      { once: true },
    ); // { once: true } 確保事件觸發一次後自動卸載
  }
});
</script>

<style scoped>
.font-selector-demo {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.text-preview {
  margin-top: 15px;
  padding: 15px;
  background-color: #f9f9f9;
  font-size: 20px;
  line-height: 1.6;
}
</style>
```

---

## ❓ 常見問題 (FAQ)

### Q1：`font-loader-min.js` 運作時會自動幫網站做哪些優化？

**答**：SDK 為了確保下載速度與防止重複載入，會在背景自動完成以下兩大任務：

1. **自動預先連線 (Preconnect)**：自動分析字型來源網域，並預先建立網路連線（含跨域安全性設定），縮短下載延遲。若您的 HTML 本身已經手動寫過連線標籤，SDK 會聰明判斷並跳過，不重複建立。
2. **智慧去重載入 (Deduplication)**：載入字型前會先檢查頁面上是否已經寫了該字型。**連版本號差異（如 `@v1.1.0` 與 `@main`）都會自動忽略並比對**，如果網站已有該字型，SDK 會直接保留網站原本的連結，不會產生重複下載的問題。

### Q2：為什麼不能直接呼叫 `window.__FONT_SDK__.getAvailableFonts()`，有時候會拿到空的？

**答**：因為 SDK 是透過網路非同步去抓取 `amec.json` 的。如果您的 Vue 組件掛載（Mounted）時，網路請求還沒完成，`isReady` 就會是 `false`。
因此，**請務必照著範例寫出 `if (isReady) { ... } else { 監聽 fonts:loaded }` 的雙重判斷**，才能確保百分之百抓得到資料！

### Q3：未來如果要增加新的字型，管理員需要改程式碼嗎？

**答**：完全不需要改任何 JS 或 Vue 程式碼！
管理員只需要在 GitHub 倉庫的 `api/amec.json` 裡面新增該字型，SDK 與 Vue 畫面就會自動讀取並顯示新的字型。

### Q4：`font.name` 和 `font.displayName` 有什麼不同？

- **`displayName`**：適合**給人看的名稱**（例如："寒蟬楷體"），用於選單標籤。
- **`name`**：適合**給 CSS 讀取的名稱**（例如："ChillKai"），用於 `font-family: "ChillKai"`。
