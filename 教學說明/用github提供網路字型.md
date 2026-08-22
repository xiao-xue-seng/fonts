
# ✔️ 使用公開 GitHub + jsDelivr 建立字型 CDN
（寒蟬正楷體子集化案例）

---

## 1. 方案概述
使用公開 GitHub 倉庫存放字型子集化檔案，並透過 jsDelivr 自動提供全球 CDN。
此方法不需伺服器、不需設定、不需申請帳號，是最簡單且可長期維護的字型部署方式。

---

## 2. 為什麼選擇 jsDelivr
- 全球 CDN 加速
- 完全免費
- 不需註冊、不需登入
- 自動快取與版本化
- 直接讀取公開 GitHub repo
- 適合字型、CSS、JS 等靜態資源

---

## 3. jsDelivr 與 GitHub 的關係
- jsDelivr **不是** GitHub 所擁有
- jsDelivr 是獨立的開源 CDN
- 透過 GitHub 的公開 API 讀取檔案
- 只要 repo 是公開的，jsDelivr 就能提供 CDN

---

## 4. 使用流程（最簡單的 3 步驟）

### 步驟 1：建立公開 GitHub 倉庫
放入字型子集化檔案與 CSS：

```
/dist/
  ChillKai.css
  ChillKai-Subset.woff2
```

### 步驟 2：在 CSS 中寫好 @font-face
（示例）

```css
@font-face {
  font-family: 'ChillKai';
  src: url('ChillKai-Subset.woff2') format('woff2');
  font-display: swap;
}
```

### 步驟 3：使用 jsDelivr 作為 CDN
引用方式：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/<user>/<repo>@main/dist/ChillKai.css">
```

網站即可直接使用字型。

---

## 5. 優點總結
- 不需架設伺服器
- 不需設定 CORS
- 不需維護 CDN
- 不需任何帳號或 API key
- 自動版本化（@v1、@v2）
- 全球快取、速度快
- 完全免費
- 適合個人、團隊、企業使用

---

## 6. 授權合法性
寒蟬正楷體：**OFL‑1.1**（允許嵌入、再分發、商用）
你的子集化 repo：**Apache‑2.0**（允許修改、再分發、商用）
→ 完全合法使用與提供 CDN。

---

## 7. 推薦的 Repo 結構

```
/dist/
  ChillKai.css
  ChillKai-Subset.woff2
LICENSE
README.md
```

---

## 8. 適用情境
- 個人網站
- 企業官網
- 部落格
- Web App
- 文件系統
- 任何需要中文字型的前端專案

---
