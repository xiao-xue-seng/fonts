(function () {
  // 每個網站/服務可以有自己的字型清單 JSON
  // 自動取得當前執行的 <script> 標籤
  const currentScript =
    document.currentScript ||
    (function () {
      const scripts = document.getElementsByTagName("script");
      return scripts[scripts.length - 1];
    })();

  // 從標籤上的 data-site 讀取網站代碼 (預設值為 'amec')
  const site = currentScript?.getAttribute("data-site") || "amec";

  // 動態拼出對應的 JSON 網址
  const CONFIG_URL = `https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@main/api/${site}.json`;

  let loadedFontsData = [];

  /**
   * 檢測並補上 Preconnect (會檢查網站 HTML 是否已有該域名的 preconnect)
   * @param {string} url - 完整的 CSS 網址 (如 https://cdn.jsdelivr.net/...)
   */
  function ensurePreconnect(url) {
    try {
      // 提取域名 Origin (例如: "https://cdn.jsdelivr.net")
      const targetOrigin = new URL(url).origin;

      // 取得頁面上所有的 <link rel="preconnect">
      const existingPreconnects = Array.from(
        document.querySelectorAll('link[rel="preconnect"]'),
      );

      // 檢查是否已有相同 Origin 的 preconnect (無論 href 結尾是否有斜線)
      const hasPreconnect = existingPreconnects.some((link) => {
        try {
          return new URL(link.href).origin === targetOrigin;
        } catch {
          return false;
        }
      });

      // 如果網站本來的 HTML 裡面沒有，才幫它動態補上
      if (!hasPreconnect) {
        const link = document.createElement("link");
        link.rel = "preconnect";
        link.href = targetOrigin;
        link.crossOrigin = "anonymous"; // 字型跨域預連線的最佳實踐
        document.head.appendChild(link);
      }
    } catch (e) {
      console.warn("[FontLoader] Invalid URL for preconnect:", url);
    }
  }

  /**
   * 移除 URL 中的版本標籤 (例如將 @main, @v1.1.0 抹去，以利純路徑比對)
   * 例：.../fonts@v1.1.0/chill-kai/result.css -> .../fonts/chill-kai/result.css
   * @param {string} url
   * @returns {string}
   */
  function normalizeFontUrl(url) {
    if (!url) return "";
    // 匹配 @ 開頭直到下一個斜線 / 之前的字元並取代為空字串
    return url.replace(/@[^/]+/, "");
  }

  /**
   * 插入字型 CSS (具備去重功能，並忽略 @版本號 的差異)
   * @param {string} cssUrl
   */
  function injectFontCSS(cssUrl) {
    // 1. 將準備插入的目標網址去除版本號 (例如去掉 @main)
    const targetNormalizedUrl = normalizeFontUrl(cssUrl);

    // 2. 取得頁面上所有的 <link rel="stylesheet">
    const existingLinks = Array.from(
      document.querySelectorAll('link[rel="stylesheet"]'),
    );

    // 3. 檢查頁面上是否已經有相同字型路徑的 CSS (不論版本是 @v1.1.0、@master 或 @main)
    const isAlreadyPresent = existingLinks.some((link) => {
      // 瀏覽器存取 link.href 會自動轉為完整的絕對路徑
      const currentLinkNormalizedUrl = normalizeFontUrl(link.href);
      return currentLinkNormalizedUrl === targetNormalizedUrl;
    });

    // 4. 如果網站 HTML 裡面已經有寫了 (不管是什麼版本)，就直接 return 保留原樣
    if (isAlreadyPresent) {
      return;
    }

    // 5. 頁面上真的沒有這個字型，才建立新的 <link> 插入
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = cssUrl;
    document.head.appendChild(link);
  }

  /**
   * 主初始化邏輯
   */
  async function init() {
    try {
      const response = await fetch(CONFIG_URL);
      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);

      const fontList = await response.json();
      loadedFontsData = fontList;

      // 1. 處理 Preconnect (先建立連線)
      fontList.forEach((font) => {
        if (font.cssUrl) ensurePreconnect(font.cssUrl);
      });

      // 2. 載入所有字型 CSS
      fontList.forEach((font) => {
        if (font.cssUrl) injectFontCSS(font.cssUrl);
      });

      // 3. 更新全域狀態並發送 CustomEvent 通知前端 (如 Vue)
      if (window.__FONT_SDK__) {
        window.__FONT_SDK__.isReady = true;
      }

      window.dispatchEvent(
        new CustomEvent("fonts:loaded", { detail: fontList }),
      );
    } catch (err) {
      console.error("[FontLoader] Failed to load fonts configuration:", err);
    }
  }

  // 掛載極簡的全域介面 (提供給 Vue 或其他腳本查詢)
  window.__FONT_SDK__ = {
    getAvailableFonts: () => [...loadedFontsData],
    isReady: false,
  };

  // 確保 DOM 準備就緒後執行
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
