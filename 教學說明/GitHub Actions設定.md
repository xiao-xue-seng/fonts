完全不需要任何特殊工具或產生程序！GitHub 內建了自動偵測機制。

只要您在儲存庫（Repository）的根目錄建立對應的資料夾與檔案，**將 YAML 文字直接貼進去並 Commit Push 上去**，GitHub 就會自動啟用它！

以下是完整的設定步驟教學：

---

### 第一步：建立資料夾與檔案

在您的專案根目錄下，建立如下的路徑與檔案（**請注意 `.github` 前面有一個點**）：

```text
專案根目錄/
└── .github/
    └── workflows/
        └── generate-fonts-json.yml  <-- 建立這個檔案
```

---

### 第二步：將以下內容貼入 `generate-fonts-json.yml`

這裡為您加上了 `permissions: contents: write`（讓 GitHub 機器人有權限寫入並 Push 檔案）以及 `[skip ci]`（避免機器人 Commit 觸發無限迴圈）： (詳見 .github\workflows\generate-fonts-json.yml)

---

### 第三步：Commit 並 Push 到 GitHub

開啟您的終端機（Terminal）或 Git 軟體，執行：

```bash
git add .github/workflows/generate-fonts-json.yml
git commit -m "ci: add font list auto-generation workflow"
git push origin main
```

---

### 第四步：檢查 GitHub Actions 是否成功運作

1. 打開您的 GitHub 儲存庫網頁。
2. 點選上方的 **「Actions」** 分頁。
3. 您會看到一個名為 **「Generate Font List JSON」** 的工作正在執行或已顯示綠色勾勾（Success）！

![GitHub Actions 示意圖](https://docs.github.com/assets/cb-19036/images/help/repository/actions-tab.png)

---

### 💡 唯一的注意事項：GitHub Repo 權限確認

有些 GitHub 帳號預設關閉了 Actions 機器人推動程式碼的權限。為了確保萬無一失：

1. 到 GitHub 儲存庫的 **Settings**（設定）。
2. 左側選單找到 **Actions** -> **General**。
3. 往下拉到 **Workflow permissions** 區塊。
4. 選擇 **「Read and write permissions」**（讀取與寫入權限）。
5. 點擊 **Save**。

之後，只要您上傳新字型資料夾並更新 `result.css`，GitHub 就會自動幫您跑 Python 腳本並更新 `api/fonts.json` 了！
