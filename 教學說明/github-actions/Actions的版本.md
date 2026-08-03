🟨Q：如何知道actions/checkout@vX 的最新版本是什麼？哪裡可以查到？

---

要查詢 GitHub Actions（如 `actions/checkout` 或 `actions/setup-python`）的最新版本，最標準、最準確的方式主要有兩種。另外，我也非常推薦一種「全自動」的懶人方法。

_(順帶一提：為了解決 Node.js 20 淘汰的問題，截至目前的最新版本，官方已經推出了 **`v7`**。所以你可以直接把你的 YAML 改為 `actions/checkout@v7` 與 `actions/setup-python@v7`)_

以下是 3 種查詢與維護版本的最佳途徑：

### 方法 1：直接看該 Action 的官方 GitHub 倉庫 (最推薦)

這類官方 Action 的原始碼本身也是公開在 GitHub 上的，網址通常就是 `https://github.com/` 加上它在 YAML 裡的名稱。

1. **開啟網址：** 例如進入 [https://github.com/actions/checkout](https://github.com/actions/checkout) 或 [https://github.com/actions/setup-python](https://github.com/actions/setup-python)。
2. **查看 Releases：** 網頁右側邊欄有一個 **「Releases」** 區塊。
3. **尋找 Latest：** 最上方會有一個綠色標籤寫著 **「Latest」**，旁邊顯示的版本號（例如 `v7.0.1`）就是當前最新版。

> 💡 **小知識：主版本號原則**
> 在 YAML 檔案中，你不需要寫到最細的 `v7.0.1`，只需要寫主版本號 **`@v7`** 即可。這樣當官方推出安全性小修復（如 `v7.0.2`）時，GitHub 會自動幫你抓取最新的次要版本，兼具穩定與安全。

---

### 方法 2：透過 GitHub Marketplace (市集) 查詢

GitHub 有一個專門的 Actions 市集，裡面會直接提供最新版的複製貼上程式碼。

1. **前往市集：** [https://github.com/marketplace](https://github.com/marketplace)
2. **搜尋套件：** 在搜尋框輸入 `checkout`。
3. **辨識官方：** 點擊由 GitHub 官方發布、帶有藍色勾勾（Verified creator）的套件。
4. **取得代碼：** 在該套件頁面的右上方，點擊 **「Use latest version」**，跳出來的程式碼範例就會直接顯示最新版的寫法（例如 `uses: actions/checkout@v7`）。

---

### 方法 3：終極絕招 — 用 Dependabot 讓它全自動更新！

如果你不想每次都手動去查版本、改程式碼，強烈建議把這個工作交給 GitHub 內建的機器人 **Dependabot**！只要有新版本推出，它會**自動幫你發送 PR (Pull Request) 來更新 YAML 檔**。

**設定方式：**
在你的倉庫中建立一個新檔案：`.github/dependabot.yml`，並貼上以下內容：

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions" # 專門監控 GitHub Actions 的版本
    directory: "/"
    schedule:
      interval: "weekly" # 每週自動檢查一次
```

存檔並推送到 GitHub 後，這隻自動化機器人就會啟動。未來不管是出 `v8` 還是 `v9`，它都會自動跳出來幫你把舊程式碼改成最新版，你只需要按一下同意（Merge）就能完成更新，超級省心！
