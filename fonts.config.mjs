/**
 * 🟨 WebFont 字型套件清單設定檔
 *
 * 設定欄位說明：
 * - name: 套件名稱 (發布為 @xiao-xue-seng/<name>)
 * - title: 顯示標題
 * - version: 版本號 (預設: 1.0.0)
 * - license: 授權條款 (預設: OFL-1.1) 必須符合 SPDX（Software Package Data Exchange）識別碼標準。
 * - licenseSource: (選填) 原始授權檔案或資料夾路徑 (支援字串或陣列，建置時會自動複製到輸出目錄)
 * - genericFamily: 通用字型家族 ("sans-serif" | "serif"，預設: "sans-serif")
 * - includeLocal: 是否在 CSS 中包含 local() 本地字型引用 (預設: true)
 * - description: 簡短描述 (用於 package.json 與 README 標頭)
 * - keywords: (選填) package.json 關鍵字陣列；未設定時使用建置工具的預設值
 * - details: README 詳細說明 (支援 Markdown，插入於 description 之後)
 * - file: 單一字型檔案路徑 (單一字型套件使用)
 * - items: 子集檔案清單陣列 (群組字型套件使用)
 */

const TW_ALIGNED_COMMON_DETAILS = `全字庫傳承自早期 Windows 系統的字型設計規範，其字型內部座標系（EM Square）將字身位置刻意偏下繪製。全字庫常是缺字備援的首選字型，當瀏覽器或排版軟體將不同字型的基線（Baseline）對齊於同條水平線時，全字庫字體會顯得比「文鼎楷體/宋體」等現代標準字型矮上一截，且無法單純透過 CSS 的 @font-face 參數進行垂直平移。

為避免排版時需額外撰寫 CSS (transform) 或標籤進行修正，本套件已於字型內部直接修正字形座標點，將字身垂直置中，確保全字庫在現代網頁與跨平台混排時能具備一致且完美的對齊表現。`;

function getBasicDetails(name) {
  return `## 字型介紹
本專案收錄由 ${name} 經 cn-font-split@7.4.3 切片化(Font Slicing)後之 WebFont。`;
}

export default [
  // ─── 🔵 範例 1：群組字型套件 ───
  {
    name: "tw-kai-aligned",
    title: "TW-Kai Aligned (全字齊楷)",
    version: "1.0.0",
    license: "OFL-1.1",
    includeLocal: true,
    genericFamily: "serif",
    description: "全字齊楷：全字庫正楷體經垂直對齊調整後之切片化 WebFont",
    details: `## 字型介紹
本專案收錄由 全字庫正楷體 (TW-Kai) 經垂直對齊調整後之切片化 WebFont，包含常用字 (Base)、擴充 B 字集 (Ext-B) 與自造字區 (Plus)。

「全字齊楷」針對「全字庫正楷體」進行了垂直位置校正。

${TW_ALIGNED_COMMON_DETAILS}
`,
    items: [
      {
        name: "Base (基本字集)",
        file: "./temp/ttf-to-next/TW-Kai-Aligned.ttf",
        subDir: "base",
      },
      {
        name: "Ext-B (擴充 B 字集)",
        file: "./temp/ttf-to-next/TW-Kai-Aligned-Ext-B.ttf",
        subDir: "ext-b",
      },
      {
        name: "Plus (自造字區)",
        file: "./temp/ttf-to-next/TW-Kai-Aligned-Plus.ttf",
        subDir: "plus",
      },
    ],
  },
  {
    name: "tw-sung-aligned",
    title: "TW-Sung Aligned (全字齊宋)",
    version: "1.0.0",
    license: "OFL-1.1",
    includeLocal: true,
    genericFamily: "serif",
    description: "全字齊宋：全字庫正宋體經垂直對齊調整後之切片化 WebFont",
    details: `## 字型介紹
本專案收錄由 全字庫正宋體 (TW-Sung) 經垂直對齊調整後之切片化 WebFont，包含常用字 (Base)、擴充 B 字集 (Ext-B) 與自造字區 (Plus)。

「全字齊宋」針對「全字庫正宋體」進行了垂直位置校正。

${TW_ALIGNED_COMMON_DETAILS}
`,
    items: [
      {
        name: "Base (基本字集)",
        file: "./temp/ttf-to-next/TW-Sung-Aligned.ttf",
        subDir: "base",
      },
      {
        name: "Ext-B (擴充 B 字集)",
        file: "./temp/ttf-to-next/TW-Sung-Aligned-Ext-B.ttf",
        subDir: "ext-b",
      },
      {
        name: "Plus (自造字區)",
        file: "./temp/ttf-to-next/TW-Sung-Aligned-Plus.ttf",
        subDir: "plus",
      },
    ],
  },

  // ─── 🟢 範例 2：單一字型套件 ───
  {
    name: "tw-kai-aligned-punct",
    title: "TW-Kai Aligned Punct (全字齊楷-標點)",
    version: "1.0.0",
    license: "OFL-1.1",
    includeLocal: true,
    genericFamily: "serif",
    description:
      "全字齊楷-標點：全字庫正楷體經垂直對齊調整後之切片化 WebFont (僅包含標點符號)",
    details: `## 字型介紹
本專案收錄由 全字庫正楷體 (TW-Kai) 經垂直對齊調整後之切片化 WebFont，僅包含標點符號。

適用場景：將此字型排在 CSS font-family 的最前面，用以強制取代後方字型的標點符號，無須修改 DOM 結構。

「全字齊楷」針對「全字庫正楷體」進行了垂直位置校正。

${TW_ALIGNED_COMMON_DETAILS}`,
    file: "./temp/ttf-to-next/TW-Kai-Aligned-Punct.ttf",
  },
  // 全字庫的標點應該都是一樣的，所以不需要另外製作宋體標點。

  {
    name: "chill-huo-fangsong",
    title: "ChillHuoFangSong (寒蟬活仿宋)",
    version: "1.0.0",
    license: "OFL-1.1",
    includeLocal: true,
    genericFamily: "serif",
    description: "寒蟬活仿宋 之切片化 WebFont",
    details: getBasicDetails("寒蟬活仿宋"),
    file: "./temp/ttf-to-next/ChillHuoFangSong_Regular.otf",
  },

  {
    name: "chill-kai",
    title: "ChillKai (寒蟬正楷體)",
    version: "1.0.0",
    license: "OFL-1.1",
    includeLocal: true,
    genericFamily: "serif",
    description: "寒蟬正楷體 之切片化 WebFont",
    details: getBasicDetails("寒蟬正楷體"),
    file: "./temp/ttf-to-next/ChillKai.ttf",
  },

  {
    name: "huiwen-fangsong",
    title: "Huiwen-Fangsong (匯文仿宋)",
    version: "1.0.0",
    license: "SEE LICENSE IN LICENSE",
    licenseSource: "temp/licenseSource/huiwen-fangsong/LICENSE",
    includeLocal: true,
    genericFamily: "serif",
    description: "匯文仿宋 之切片化 WebFont",
    details: getBasicDetails("匯文仿宋"),
    file: "./temp/ttf-to-next/huiwen-fangsong.ttf",
  },

  {
    name: "iansui",
    title: "Iansui (芫荽體)",
    version: "1.0.0",
    license: "OFL-1.1",
    includeLocal: true,
    genericFamily: "serif",
    description: "芫荽體 之切片化 WebFont",
    details: getBasicDetails("芫荽體"),
    file: "./temp/ttf-to-next/Iansui-Regular.ttf",
  },

  {
    name: "instrument-sans-subset",
    title: "InstrumentSans-Subset (Instrument Sans 拉丁子集)",
    version: "1.0.0",
    license: "OFL-1.1",
    includeLocal: true,
    genericFamily: "sans-serif",
    description: "Instrument Sans 自訂拉丁子集 之切片化 WebFont",
    details: `${getBasicDetails("Instrument Sans 自訂拉丁子集")}

適合用於替換 Noto Sans TC 的拉丁字元，增加排版的多樣性、美觀性。
`,
    keywords: ["font", "webfont"],
    file: "./temp/ttf-to-next/InstrumentSans-Subset.ttf",
  },

  {
    name: "ar-pl-ukai",
    title: "AR PL UKai (文鼎PL中楷)",
    version: "1.0.0",
    license: "SEE LICENSE IN LICENSE",
    licenseSource: "temp/licenseSource/ar-pl-ukai/license",
    includeLocal: true,
    genericFamily: "serif",
    description: "文鼎PL中楷 之切片化 WebFont",
    details: `${getBasicDetails("文鼎PL中楷")}

此專案從 ukai.ttc (0.1.20080216) 中擷取出 ukai-tw.ttf 再經切片化處理。並未修改字形內容。
`,
    file: "./temp/ttf-to-next/ukai-tw.ttf",
  },

  {
    name: "ar-pl-uming",
    title: "AR PL UMing (文鼎PL細上海宋)",
    version: "1.0.0",
    license: "SEE LICENSE IN LICENSE",
    licenseSource: "temp/licenseSource/ar-pl-uming/license",
    includeLocal: true,
    genericFamily: "serif",
    description: "文鼎PL細上海宋 之切片化 WebFont",
    details: `${getBasicDetails("文鼎PL細上海宋")}

此專案從 uming.ttc (0.1.20080216) 中擷取出 uming-tw.ttf 再經切片化處理。並未修改字形內容。

註：此字體原本的「，：；！？」就是靠左下小型。若有需要，可用「全字齊楷 標點 (TW-Kai-Aligned-Punct)」於 CSS font-family 中，前置替換為置中標點。
`,
    file: "./temp/ttf-to-next/uming-tw.ttf",
  },

  {
    name: "zhuque-fangsong",
    title: "ZhuqueFangsong (朱雀仿宋)",
    version: "1.0.0",
    license: "OFL-1.1",
    includeLocal: true,
    genericFamily: "serif",
    description: "朱雀仿宋 之切片化 WebFont",
    details: getBasicDetails("朱雀仿宋(v.0.212)"),
    file: "./temp/ttf-to-next/ZhuqueFangsong-Regular.ttf",
  },
];
