依據 npm 官方文件規範，發布套件至 npm Registry 需要完成帳號雙重驗證、設定 `package.json` 檔案清單與執行發布指令。

## 發布流程 Step-by-Step

### 設定 package.json 核心欄位

- `name`：套件名稱（必須全小寫、不含空格與 URL 非安全字元，且未在 Registry 被使用）。
- `version`：遵守語意化版本規範（SemVer，如 `1.0.0`）。
- `main` / `exports`：指定套件的程式進入點（如 `dist/index.js`）。
- `files`：指定要包含在發布檔中的資料夾或檔案白名單（例如 `["dist", "README.md"]`）。

### 登入與身分驗證

- 在終端機執行 `npm login` 完成帳號登入與 2FA 雙重驗證。
- 執行 `npm whoami` 可確認當前登入身分。

### 預覽打包內容

- 執行 `npm pack --dry-run` 檢查實際上會打包（`.tgz`）進去的所有檔案與預估容量，確保未誤傳敏感或不必要的檔案。

### 執行發布

- **一般公開套件**：執行 `npm publish`。
- **作用域套件（Scoped Package，如 `@username/pkg`）**：預設為私有，欲免費公開發布需加上參數 `npm publish --access public`。

#### 直接發布指定資料夾

只要將目標資料夾的路徑作為參數傳遞給 `npm publish` 指令即可，無需先手動切換目錄。
在專案根目錄下執行：

```bash
npm publish .dist/tw-kai-aligned

```

若套件帶有作用域（Scoped Package，例如 `@scope/instrument-sans-subset`），且要免費公開發布，需補上 `--access public`：

```bash
npm publish .dist/tw-kai-aligned --access public

```

#### 推薦的發布與預覽步驟

1. **預覽打包內容**
   在實際發布前，可先檢查該資料夾最終會被上傳哪些檔案：

```bash
npm pack --dry-run .dist/tw-kai-aligned

```

2. **切換目錄發布（備選方式）**
   若習慣在該資料夾環境下執行，也可以先切換目錄再發布：

```bash
cd .dist/tw-kai-aligned
npm publish

```

---

**容量與規格限制**

| 限制項目                      | 官方限制規格         | 說明與建議                                                                      |
| ----------------------------- | -------------------- | ------------------------------------------------------------------------------- |
| **單一 Tarball (.tgz) 容量**  | **500 MB**           | 建議控制在 **10 MB 以內**。過大容易導致 CLI 記憶體溢位或上傳超時。              |
| **`package.json` 檔案大小**   | **384 KB**           | 不得放置過長註解、大量內嵌數據或過長描述。                                      |
| **套件名稱長度**              | **<= 214 字元**      | 包含 Scope 名稱，開頭不可含大寫字母，僅能使用 URL 安全字元。                    |
| **取消發布 (Unpublish) 時限** | **發布後 72 小時內** | 僅限無其他 Registry 套件依賴時；超過 72 小時僅能改用 `npm deprecate` 標記廢棄。 |

---

**注意事項與最佳實踐**

- **強制啟用 2FA 雙重驗證**：npm 已全面要求發布套件的帳號必須開啟 2FA（支援 Authenticator App 或 Security Key）。
- **發布檔案精簡化**：
- 優先使用 `package.json` 中的 `files` 白名單。
- 若使用 `.npmignore`，務必排除 `.env`、測試檔案、原始碼（若有編譯步驟）、CI 配置檔，防止敏感資訊洩漏。

- **版本號不可覆蓋 (SemVer)**：
- 發布過的版本號無法重新寫入，任何代碼更動皆需透過命令提升版本：
- 修復 Bug：`npm version patch`（`1.0.0` → `1.0.1`）
- 新增向下相容功能：`npm version minor`（`1.0.0` → `1.1.0`）
- 破壞性變更：`npm version major`（`1.0.0` → `2.0.0`）

- **自動化 CI/CD 安全發布**：若搭配 GitHub Actions 發布，建議建立 **Granular Access Token** 並啟用 npm Provenance，以提高軟體供應鏈安全認證。
