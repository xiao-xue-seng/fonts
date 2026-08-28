/*
🟨 cn-font-split 切分字型工具

使用範例：

# 1. 預設使用 (license: OFL-1.1, version: 1.0.0, 包含 local(), 輸出至 ./.dist/<font-name>)
node tools/split.mjs -f ./fonts/ChillKai-Merged.ttf

# 2. 自訂輸出目錄與停用 package.json/README.md 生成
node tools/split.mjs -f ./temp/TW-Kai-Aligned.ttf -o ./.dist/tw-kai-aligned/base --no-pkg

# 3. 自訂 license 與 version
node tools/split.mjs -f ./fonts/ChillKai-Merged.ttf -l "Apache-2.0" -v "2.1.0"

# 4. 排除 CSS 中的 local()
node tools/split.mjs -f ./fonts/ChillKai-Merged.ttf --no-local

# 5. 指定資料夾批次處理
node tools/split.mjs -d ./raw-fonts -l "OFL-1.1" -v "1.0.1" --no-local
*/

import { fontSplit } from "cn-font-split";
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

// ---------------------- 設定區域 ----------------------
// 你的 npm 帳號名稱（發布 Scoped Package 時使用，例如 @xiao-xue-seng/chill-kai）
export const NPM_SCOPE = "xiao-xue-seng";
export const OUTPUT_BASE = "./.dist";
// ------------------------------------------------------

// 轉換為小寫連字號 (kebab-case)
export function toKebabCase(str) {
  return str
    .replace(/([a-z0-9])([A-Z])/g, "$1-$2")
    .replace(/[\s_]+/g, "-")
    .replace(/[^a-zA-Z0-9-]/g, "")
    .toLowerCase();
}

function getFontCodepoints(filePath) {
  const buffer = fs.readFileSync(filePath);
  const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);
  const numTables = view.getUint16(4);
  let cmapOffset = 0;
  let cmapLength = 0;

  for (let index = 0; index < numTables; index++) {
    const recordOffset = 12 + index * 16;
    const tag = String.fromCharCode(
      view.getUint8(recordOffset),
      view.getUint8(recordOffset + 1),
      view.getUint8(recordOffset + 2),
      view.getUint8(recordOffset + 3),
    );
    if (tag === "cmap") {
      cmapOffset = view.getUint32(recordOffset + 8);
      cmapLength = view.getUint32(recordOffset + 12);
      break;
    }
  }
  if (!cmapOffset || !cmapLength) throw new Error("字型缺少有效的 cmap 表");

  const cmapEnd = cmapOffset + cmapLength;
  const numSubtables = view.getUint16(cmapOffset + 2);
  let bestSubtable = null;
  for (let index = 0; index < numSubtables; index++) {
    const recordOffset = cmapOffset + 4 + index * 8;
    const platformId = view.getUint16(recordOffset);
    const encodingId = view.getUint16(recordOffset + 2);
    const subtableOffset = cmapOffset + view.getUint32(recordOffset + 4);
    const format = view.getUint16(subtableOffset);
    const priority = format === 12 || format === 13
      ? (platformId === 3 && encodingId === 10 ? 3 : 2)
      : format === 4
        ? (platformId === 3 ? 1 : 0)
        : -1;
    if (subtableOffset < cmapEnd && priority >= 0 && (!bestSubtable || priority > bestSubtable.priority)) {
      bestSubtable = { offset: subtableOffset, format, priority };
    }
  }
  if (!bestSubtable) throw new Error("字型缺少支援的 cmap 格式");

  const codepoints = new Set();
  const offset = bestSubtable.offset;
  if (bestSubtable.format === 12 || bestSubtable.format === 13) {
    const groupCount = view.getUint32(offset + 12);
    for (let index = 0; index < groupCount; index++) {
      const groupOffset = offset + 16 + index * 12;
      const start = view.getUint32(groupOffset);
      const end = view.getUint32(groupOffset + 4);
      for (let codepoint = start; codepoint <= end; codepoint++) codepoints.add(codepoint);
    }
  } else {
    const segmentCount = view.getUint16(offset + 6) / 2;
    const endCodeOffset = offset + 14;
    const startCodeOffset = endCodeOffset + segmentCount * 2 + 2;
    for (let segment = 0; segment < segmentCount; segment++) {
      const start = view.getUint16(startCodeOffset + segment * 2);
      const end = view.getUint16(endCodeOffset + segment * 2);
      for (let codepoint = start; codepoint <= end; codepoint++) {
        if (codepoint !== 0xffff) codepoints.add(codepoint);
      }
    }
  }
  return [...codepoints].sort((left, right) => left - right);
}

// 自動生成 package.json 與 README.md
export function generatePackageFiles(
  destDir,
  pkgName,
  rawFontName,
  { license = "OFL-1.1", version = "1.0.0" } = {},
) {
  const packageJson = {
    name: `@${NPM_SCOPE}/${pkgName}`,
    version: version,
    description: `Webfont subset for ${rawFontName}`,
    main: "result.css",
    style: "result.css",
    keywords: ["font", "webfont", "chinese-font", pkgName],
    license: license,
    publishConfig: {
      access: "public", // Scoped package 必須設定 public 才能免費公開發布
    },
  };

  const readmeContent = `# @${NPM_SCOPE}/${pkgName}

Webfont subset for **${rawFontName}**.

## 引用方式 (jsDelivr CDN)

\`\`\`html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@${NPM_SCOPE}/${pkgName}@latest/result.css" />
\`\`\`

\`\`\`css
body {
  font-family: "${rawFontName}", sans-serif;
}
\`\`\`
`;

  fs.writeFileSync(
    path.join(destDir, "package.json"),
    JSON.stringify(packageJson, null, 2),
    "utf-8",
  );
  fs.writeFileSync(path.join(destDir, "README.md"), readmeContent, "utf-8");
}

// 核心切片函式
export async function processFont(filePath, options = {}) {
  const {
    license = "OFL-1.1",
    version = "1.0.0",
    includeLocal = true,
    outDir = null,
    pkgFiles = true,
    fontFamily = "",
    subsetMode = "split",
  } = options;

  const filename = path.basename(filePath);
  const rawFontName = path.parse(filename).name;
  const kebabName = toKebabCase(rawFontName);
  const destDir = outDir ? path.resolve(outDir) : path.join(OUTPUT_BASE, kebabName);
  const resultCssPath = path.join(destDir, "result.css");
  const buildOptionsPath = path.join(destDir, ".build-options.json");

  // 檢查輸出檔案 (result.css) 是否存在且較新
  if (fs.existsSync(resultCssPath)) {
    const fontStat = fs.statSync(filePath);
    const cssStat = fs.statSync(resultCssPath);
    let cachedMode = "split";
    if (fs.existsSync(buildOptionsPath)) {
      try {
        cachedMode = JSON.parse(fs.readFileSync(buildOptionsPath, "utf-8")).subsetMode;
      } catch {
        cachedMode = null;
      }
    }
    const woff2Count = fs
      .readdirSync(destDir)
      .filter((entry) => entry.toLowerCase().endsWith(".woff2"))
      .length;
    const hasExpectedOutput = subsetMode !== "single" || woff2Count === 1;
    if (
      cssStat.mtimeMs >= fontStat.mtimeMs &&
      cachedMode === subsetMode &&
      hasExpectedOutput
    ) {
      console.log(`\n⏭️  略過 (輸出的 result.css 已是最新): ${filename}`);
      return { status: "skipped", destDir, resultCssPath };
    }
  }

  // 如果 destDir 不存在，則自行建立
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }

  console.log(`\n========================================`);
  console.log(`▶ 開始處理: ${filename}`);
  console.log(`  輸出目標: ${destDir}`);
  console.log(`  套件名稱: @${NPM_SCOPE}/${kebabName}`);
  console.log(`  版本號碼: ${version}`);
  console.log(`  授權條款: ${license}`);
  console.log(`  包含 local(): ${includeLocal ? "是" : "否"}`);
  console.log(`  產生套件檔: ${pkgFiles ? "是" : "否"}`);
  console.log(`========================================`);

  const startTime = Date.now();

  try {
    // 執行切片
    const splitOptions = {
      input: filePath,
      outDir: destDir,
      ...(fontFamily ? { css: { fontFamily } } : {}),
      // ─── 關閉不需要的額外檔案 ───
      testHtml: false, // 關閉生成 index.html (測試頁面)
      testHTML: false, // 兼容不同版本的命名大小寫
      reporter: false, // 關閉生成 reporter.bin 及 index.proto (分析報告)
      previewImage: null, // 確保不額外產生 preview.svg 預覽圖
    };
    if (subsetMode === "single") {
      for (const entry of fs.readdirSync(destDir)) {
        if (entry.toLowerCase().endsWith(".woff2")) {
          fs.unlinkSync(path.join(destDir, entry));
        }
      }
      splitOptions.subsets = [getFontCodepoints(filePath)];
      splitOptions.autoSubset = false;
    }
    await fontSplit(splitOptions);

    // 若設定不包含 local()，自輸出的 result.css 中移除 local(...)
    if (!includeLocal && fs.existsSync(resultCssPath)) {
      const originalCss = fs.readFileSync(resultCssPath, "utf-8");
      const updatedCss = originalCss.replace(/local\([^)]*\)\s*,\s*/g, "");
      fs.writeFileSync(resultCssPath, updatedCss, "utf-8");
    }

    // ─── 自動清理不需要的殘留檔案 ───
    const filesToRemove = [
      "index.proto",
      "reporter.bin",
      "index.html",
      "preview.svg",
    ];
    for (const file of filesToRemove) {
      const target = path.join(destDir, file);
      if (fs.existsSync(target)) {
        fs.unlinkSync(target);
      }
    }

    fs.writeFileSync(
      buildOptionsPath,
      JSON.stringify({ subsetMode }, null, 2),
      "utf-8",
    );

    // 寫入發布所需的設定檔 (若啟用)
    if (pkgFiles) {
      generatePackageFiles(destDir, kebabName, rawFontName, {
        license,
        version,
      });
    }

    console.log(
      `✔ 完成！耗時: ${((Date.now() - startTime) / 1000).toFixed(2)} 秒`,
    );
    return { status: "success", destDir, resultCssPath };
  } catch (err) {
    console.error(`✖ 處理失敗 [${filename}]:`, err);
    return { status: "error", destDir, error: err };
  }
}

export async function main() {
  // 解析命令列參數 (Node 18.3+ 內建支援)
  const { values } = parseArgs({
    options: {
      file: { type: "string", short: "f" },
      dir: { type: "string", short: "d" },
      outDir: { type: "string", short: "o" },
      license: { type: "string", short: "l", default: "OFL-1.1" },
      version: { type: "string", short: "v", default: "1.0.0" },
      local: { type: "boolean", default: true },
      "no-local": { type: "boolean" },
      pkgFiles: { type: "boolean", default: true },
      "no-pkg": { type: "boolean" },
      "no-pkg-files": { type: "boolean" },
    },
    strict: false,
    allowPositionals: true,
  });

  let includeLocal = true;
  if (values["no-local"] === true) {
    includeLocal = false;
  } else if (values.local !== undefined) {
    if (typeof values.local === "boolean") {
      includeLocal = values.local;
    } else if (typeof values.local === "string") {
      includeLocal =
        values.local.toLowerCase() !== "false" && values.local !== "0";
    }
  }

  let pkgFiles = true;
  if (values["no-pkg"] === true || values["no-pkg-files"] === true) {
    pkgFiles = false;
  } else if (values.pkgFiles !== undefined) {
    if (typeof values.pkgFiles === "boolean") {
      pkgFiles = values.pkgFiles;
    } else if (typeof values.pkgFiles === "string") {
      pkgFiles =
        values.pkgFiles.toLowerCase() !== "false" && values.pkgFiles !== "0";
    }
  }

  const license = values.license || "OFL-1.1";
  const version = values.version || "1.0.0";
  const outDir = values.outDir || null;

  const fontFiles = [];

  if (values.file) {
    if (fs.existsSync(values.file)) {
      fontFiles.push(values.file);
    } else {
      console.error(`找不到指定檔案: ${values.file}`);
      process.exit(1);
    }
  } else if (values.dir) {
    if (fs.existsSync(values.dir)) {
      // 僅讀取該層，不遞迴
      const files = fs.readdirSync(values.dir);
      for (const file of files) {
        const fullPath = path.join(values.dir, file);
        if (fs.statSync(fullPath).isFile() && /\.(ttf|otf)$/i.test(file)) {
          fontFiles.push(fullPath);
        }
      }
    } else {
      console.error(`找不到指定資料夾: ${values.dir}`);
      process.exit(1);
    }
  } else {
    console.log(`使用說明：`);
    console.log(
      `  指定單一字型: node split.mjs -f ./fonts/ChillKai-Merged.ttf`,
    );
    console.log(`  指定字型資料夾: node split.mjs -d ./raw-fonts`);
    console.log(`\n選用參數：`);
    console.log(`  -o, --outDir <path>     自訂切片輸出目標目錄 (預設: .dist/<font-name>)`);
    console.log(`  -l, --license <name>    指定授權條款 (預設: OFL-1.1)`);
    console.log(`  -v, --version <semver>  指定套件版本號 (預設: 1.0.0)`);
    console.log(
      `  --local / --no-local    指定 CSS 是否包含 local() 本地字型引用 (預設: 包含)`,
    );
    console.log(
      `  --pkgFiles / --no-pkg   指定是否自動產生 package.json 與 README.md (預設: 產生)`,
    );
    process.exit(0);
  }

  if (fontFiles.length === 0) {
    console.log("沒有找到符合的 .ttf 檔案。");
    return;
  }

  console.log(`共找到 ${fontFiles.length} 個字型檔案待處理...`);
  let successCount = 0;
  let skippedCount = 0;
  let failCount = 0;

  for (const fontPath of fontFiles) {
    const res = await processFont(fontPath, {
      license,
      version,
      includeLocal,
      outDir,
      pkgFiles,
    });
    if (res?.status === "success") successCount++;
    else if (res?.status === "skipped") skippedCount++;
    else if (res?.status === "error") failCount++;
  }

  console.log(`\n========================================`);
  console.log(`🎉 全部字型處理完成！請查看 ${outDir || OUTPUT_BASE} 目錄。`);
  console.log(
    `📊 處理統計: 成功切片 ${successCount} 個, 略過 ${skippedCount} 個, 失敗 ${failCount} 個 (共 ${fontFiles.length} 個)`,
  );
  console.log(`========================================`);
}

// 若直接以 CLI 執行此檔案則啟動 main()
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main();
}
