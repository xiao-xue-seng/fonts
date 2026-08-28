/*
🟨 WebFont 批次建置引擎 (Build Engine)

使用範例：
# 1. 批次建置 fonts.config.mjs 中的所有字型套件
node tools/build.mjs

# 2. 僅建置特定名稱的套件（單一字型或群組字型皆可）
node tools/build.mjs tw-kai-aligned
node tools/build.mjs chill-kai

# 3. 指定自訂設定檔路徑
node tools/build.mjs --config ./custom-fonts.config.mjs

🟢前置作業：
- 準備文鼎來源：執行 tools\處理文鼎字型\extract_ttcs.py 拆出 TW ttf。
- 準備對齊版：  執行 tools\處理全字庫對齊\batch_transform_tw.py
- 準備標點子集：執行 tools\extract_cjk_punctuation.py 產生標點符號子集。
- 準備拉丁子集：執行 tools\extract_latin_subset_ttf.py

🟡相關流程：
- tools\optimize_ttf_for_app.py
*/

import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { NPM_SCOPE, OUTPUT_BASE, processFont, toKebabCase } from "./split.mjs";

const DEFAULT_KEYWORDS = ["font", "webfont", "chinese-font"];

/**
 * 產生 package.json 的 keywords
 *
 * 未設定自訂 keywords 時沿用預設值；設定後則完全採用輸入值，並一律加入套件名。
 */
export function getPackageKeywords(config, pkgName) {
  const keywords = Array.isArray(config.keywords)
    ? config.keywords
    : DEFAULT_KEYWORDS;

  return [...new Set([...keywords, pkgName])];
}

/**
 * 從 CSS 內容中提取宣告的 font-family 名稱
 */
export function extractFontFamily(cssContent, fallback = "") {
  if (!cssContent) return fallback;
  const match = cssContent.match(/font-family:\s*["']?([^;"'\r\n]+)["']?/i);
  return match ? match[1].trim() : fallback;
}

/**
 * 修正 CSS 中的 url(...) 相對路徑，使其指向子目錄
 * 例如：url("./0.woff2") 或 url("0.woff2") -> url("./base/0.woff2")
 */
export function rewriteCssUrls(cssContent, subDir) {
  return cssContent.replace(
    /url\(\s*(['"]?)([^'")]+)\1\s*\)/g,
    (match, quote, urlPath) => {
      // 忽略絕對路徑、網路 URL 或 Data URI
      if (/^(https?:|\/\/|data:|\/)/i.test(urlPath)) {
        return match;
      }
      // 移除原有的 ./ 前綴後重新組合
      const cleanPath = urlPath.replace(/^\.\//, "");
      const newPath = `./${subDir}/${cleanPath}`;
      const q = quote || '"';
      return `url(${q}${newPath}${q})`;
    },
  );
}

function ensureNpmIgnoreBuildOptions(destDir) {
  const npmIgnorePath = path.join(destDir, ".npmignore");
  const requiredRules = [".build-options.json", "**/.build-options.json"];
  let existingContent = fs.existsSync(npmIgnorePath)
    ? fs.readFileSync(npmIgnorePath, "utf-8")
    : "";
  const existingRules = new Set(
    existingContent.split(/\r?\n/).map((line) => line.trim()),
  );
  const missingRules = requiredRules.filter((rule) => !existingRules.has(rule));

  if (missingRules.length > 0) {
    const separator =
      existingContent && !existingContent.endsWith("\n") ? "\n" : "";
    fs.writeFileSync(
      npmIgnorePath,
      existingContent + separator + missingRules.join("\n") + "\n",
      "utf-8",
    );
  }
}

function needsReslice(
  filePath,
  destDir,
  subsetMode = "split",
  fontFamily = "",
) {
  const resultCssPath = path.join(destDir, "result.css");
  const buildOptionsPath = path.join(destDir, ".build-options.json");
  if (!fs.existsSync(resultCssPath)) return true;

  let hasMatchingFontFamily = true;
  if (fontFamily) {
    const currentCss = fs.readFileSync(resultCssPath, "utf-8");
    hasMatchingFontFamily = extractFontFamily(currentCss) === fontFamily;
  }

  const fontStat = fs.statSync(filePath);
  const cssStat = fs.statSync(resultCssPath);
  let cachedMode = "split";
  if (fs.existsSync(buildOptionsPath)) {
    try {
      cachedMode = JSON.parse(
        fs.readFileSync(buildOptionsPath, "utf-8"),
      ).subsetMode;
    } catch {
      cachedMode = null;
    }
  }
  const woff2Count = fs
    .readdirSync(destDir)
    .filter((entry) => entry.toLowerCase().endsWith(".woff2")).length;
  const hasExpectedOutput = subsetMode !== "single" || woff2Count === 1;

  return (
    !hasMatchingFontFamily ||
    cssStat.mtimeMs < fontStat.mtimeMs ||
    cachedMode !== subsetMode ||
    !hasExpectedOutput
  );
}

function createResliceTempDir(destDir) {
  const parentDir = path.dirname(path.resolve(destDir));
  fs.mkdirSync(parentDir, { recursive: true });
  return fs.mkdtempSync(
    path.join(parentDir, `.${path.basename(destDir)}.tmp-`),
  );
}

function replaceOutputDirectory(tempDir, destDir) {
  const resolvedDestDir = path.resolve(destDir);
  const backupDir = `${resolvedDestDir}.backup-${Date.now()}`;
  let hasBackup = false;

  try {
    if (fs.existsSync(resolvedDestDir)) {
      fs.renameSync(resolvedDestDir, backupDir);
      hasBackup = true;
    }
    fs.renameSync(tempDir, resolvedDestDir);
    if (hasBackup) fs.rmSync(backupDir, { recursive: true, force: true });
  } catch (err) {
    if (hasBackup && !fs.existsSync(resolvedDestDir)) {
      fs.renameSync(backupDir, resolvedDestDir);
    }
    throw err;
  }
}

/**
 * 複製原始授權檔案或目錄至輸出目錄
 */
export function copyLicenseSource(destDir, licenseSource) {
  if (!licenseSource) return;

  const sources = Array.isArray(licenseSource)
    ? licenseSource
    : [licenseSource];

  for (const src of sources) {
    if (!src || typeof src !== "string") continue;
    const resolvedSrc = path.resolve(src);

    if (!fs.existsSync(resolvedSrc)) {
      console.warn(`  ⚠ 找不到指定的授權來源: ${src}`);
      continue;
    }

    const stat = fs.statSync(resolvedSrc);
    const baseName = path.basename(resolvedSrc);
    const targetPath = path.join(destDir, baseName);

    try {
      if (stat.isDirectory()) {
        fs.cpSync(resolvedSrc, targetPath, { recursive: true });
        console.log(
          `  📄 已複製授權資料夾: ${baseName}/ -> ${path.relative(process.cwd(), targetPath)}`,
        );
      } else if (stat.isFile()) {
        fs.copyFileSync(resolvedSrc, targetPath);
        console.log(
          `  📄 已複製授權檔案: ${baseName} -> ${path.relative(process.cwd(), targetPath)}`,
        );
      }
    } catch (err) {
      console.error(`  ✖ 複製授權來源失敗 [${src}]:`, err.message);
    }
  }
}

/**
 * 產出 package.json
 */
function writePackageJson(destDir, config, mainCssFile) {
  const pkgName = toKebabCase(config.name);
  const packageJson = {
    name: `@${NPM_SCOPE}/${pkgName}`,
    version: config.version || "1.0.0",
    description:
      config.description || `Webfont subset for ${config.title || pkgName}`,
    main: mainCssFile,
    style: mainCssFile,
    keywords: getPackageKeywords(config, pkgName),
    license: config.license || "OFL-1.1",
    publishConfig: {
      access: "public",
    },
  };

  fs.writeFileSync(
    path.join(destDir, "package.json"),
    JSON.stringify(packageJson, null, 2),
    "utf-8",
  );
}

/**
 * 產出單一字型的 README.md
 */
function writeSingleReadme(destDir, config, fontFamily) {
  const pkgName = toKebabCase(config.name);
  const genericFamily = config.genericFamily || "sans-serif";
  const detailsSection = config.details ? `\n${config.details.trim()}\n` : "";
  const version = config.version || "latest";

  const content = `# @${NPM_SCOPE}/${pkgName}

${config.description || `Webfont subset for **${config.title || pkgName}**.`}
${detailsSection}
## 引用方式 (jsDelivr CDN)

\`\`\`html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@${NPM_SCOPE}/${pkgName}@${version}/result.css" />
\`\`\`

## CSS 使用範例

\`\`\`css
body {
  font-family: "${fontFamily}", ${genericFamily};
}
\`\`\`
`;
  fs.writeFileSync(path.join(destDir, "README.md"), content, "utf-8");
}

/**
 * 產出群組字型的 README.md
 */
function writeGroupReadme(destDir, config, fontFamily) {
  const pkgName = toKebabCase(config.name);
  const genericFamily = config.genericFamily || "sans-serif";
  const detailsSection = config.details ? `\n${config.details.trim()}\n` : "";
  const version = config.version || "latest";
  const items = config.items || [];

  const subsetListMd = items
    .map(
      (it) =>
        `- **${it.name || it.subDir}**: \`https://cdn.jsdelivr.net/npm/@${NPM_SCOPE}/${pkgName}@${version}/${it.subDir}/result.css\``,
    )
    .join("\n");

  const firstSubDir = items[0]?.subDir || "base";

  const content = `# @${NPM_SCOPE}/${pkgName}

${config.description || `Webfont subset for **${config.title || pkgName}**.`}
${detailsSection}
## 引用方式 (jsDelivr CDN)

### 1. 載入完整字集 (所有子集整合版)

\`\`\`html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@${NPM_SCOPE}/${pkgName}@${version}/index.css" />
\`\`\`

### 2. 按需載入個別子集

${subsetListMd}

\`\`\`html
<!-- 範例：僅載入 ${items[0]?.name || firstSubDir} 子集 -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@${NPM_SCOPE}/${pkgName}@${version}/${firstSubDir}/result.css" />
\`\`\`

## CSS 使用範例

\`\`\`css
body {
  font-family: "${fontFamily}", ${genericFamily};
}
\`\`\`
`;
  fs.writeFileSync(path.join(destDir, "README.md"), content, "utf-8");
}

/**
 * 建置單一字型套件
 */
async function buildSingleFont(config) {
  const pkgName = toKebabCase(config.name);
  const destDir = path.join(OUTPUT_BASE, pkgName);

  if (!fs.existsSync(config.file)) {
    console.error(`✖ 找不到字型檔案: ${config.file}`);
    return { status: "error", name: config.name };
  }

  const subsetMode = config.subsetMode || "split";
  const shouldReslice = needsReslice(
    config.file,
    destDir,
    subsetMode,
    config.fontFamily,
  );
  const processDestDir = shouldReslice
    ? createResliceTempDir(destDir)
    : destDir;

  let result;
  try {
    result = await processFont(config.file, {
      license: config.license,
      version: config.version,
      fontFamily: config.fontFamily,
      subsetMode,
      includeLocal: config.includeLocal !== false,
      outDir: processDestDir,
      pkgFiles: false,
    });

    if (shouldReslice && result.status === "success") {
      replaceOutputDirectory(processDestDir, destDir);
    }
  } finally {
    if (shouldReslice && fs.existsSync(processDestDir)) {
      fs.rmSync(processDestDir, { recursive: true, force: true });
    }
  }

  if (result.status === "error") {
    return { status: "error", name: config.name };
  }

  if (subsetMode === "single") {
    ensureNpmIgnoreBuildOptions(destDir);
  }

  // 從產出的 result.css 中解析 fontFamily，確保所用的值符合實際。
  const resultCssPath = path.join(destDir, "result.css");
  let fontFamily = config.fontFamily || pkgName;
  if (fs.existsSync(resultCssPath)) {
    const cssContent = fs.readFileSync(resultCssPath, "utf-8");
    fontFamily = extractFontFamily(cssContent, fontFamily);
  }

  // 產生根目錄設定與說明檔
  writePackageJson(destDir, config, "result.css");
  writeSingleReadme(destDir, config, fontFamily);

  // 複製授權檔案或資料夾
  if (config.licenseSource) {
    copyLicenseSource(destDir, config.licenseSource);
  }

  return { status: result.status, name: config.name };
}

/**
 * 建置群組字型套件
 */
async function buildFontGroup(config) {
  const pkgName = toKebabCase(config.name);
  const groupDestDir = path.join(OUTPUT_BASE, pkgName);

  if (!fs.existsSync(groupDestDir)) {
    fs.mkdirSync(groupDestDir, { recursive: true });
  }

  if (
    config.subsetMode === "single" ||
    config.items.some((item) => item.subsetMode === "single")
  ) {
    ensureNpmIgnoreBuildOptions(groupDestDir);
  }

  console.log(
    `\n📦 開始處理群組套件: [${config.name}] (包含 ${config.items.length} 個子集)`,
  );

  const mergedCssSections = [];
  let detectedFontFamily = "";
  let hasError = false;
  let allSkipped = true;

  for (const item of config.items) {
    if (!fs.existsSync(item.file)) {
      console.error(`  ✖ 找不到子集檔案: ${item.file}`);
      hasError = true;
      continue;
    }

    const subDirName = item.subDir || toKebabCase(item.name);
    const subDestDir = path.join(groupDestDir, subDirName);
    const subsetMode = item.subsetMode || config.subsetMode || "split";
    const shouldReslice = needsReslice(
      item.file,
      subDestDir,
      subsetMode,
      item.fontFamily,
    );
    const processDestDir = shouldReslice
      ? createResliceTempDir(subDestDir)
      : subDestDir;

    let result;
    try {
      result = await processFont(item.file, {
        license: config.license,
        version: config.version,
        fontFamily: item.fontFamily,
        subsetMode,
        includeLocal: config.includeLocal !== false,
        outDir: processDestDir,
        pkgFiles: false,
      });

      if (shouldReslice && result.status === "success") {
        replaceOutputDirectory(processDestDir, subDestDir);
      }
    } finally {
      if (shouldReslice && fs.existsSync(processDestDir)) {
        fs.rmSync(processDestDir, { recursive: true, force: true });
      }
    }

    if (result.status === "error") {
      hasError = true;
      continue;
    }

    if (subsetMode === "single") {
      ensureNpmIgnoreBuildOptions(subDestDir);
    }

    if (result.status === "success") {
      allSkipped = false;
    }

    // 讀取子集的 result.css 並修正相對路徑
    const resultCssPath = path.join(subDestDir, "result.css");
    if (fs.existsSync(resultCssPath)) {
      const rawCss = fs.readFileSync(resultCssPath, "utf-8");

      // 擷取字型名稱（以第一個成功讀取的子集為主）
      if (!detectedFontFamily) {
        detectedFontFamily = extractFontFamily(rawCss);
      }

      const rewrittenCss = rewriteCssUrls(rawCss, subDirName);

      mergedCssSections.push(
        `/* ==========================================================================\n` +
          `   Subset: ${item.name || subDirName}\n` +
          `   ========================================================================== */\n` +
          rewrittenCss.trim(),
      );
    }
  }

  if (hasError) {
    return { status: "error", name: config.name };
  }

  // ★ 合併生成根目錄 index.css
  const indexCssPath = path.join(groupDestDir, "index.css");
  const finalIndexCss =
    `/**\n` +
    ` * @package @${NPM_SCOPE}/${pkgName}\n` +
    ` * @version ${config.version || "1.0.0"}\n` +
    ` * @license ${config.license || "OFL-1.1"}\n` +
    ` */\n\n` +
    mergedCssSections.join("\n\n") +
    "\n";

  fs.writeFileSync(indexCssPath, finalIndexCss, "utf-8");
  console.log(
    `  ✔ 已自動合成群組入口樣式: ${path.relative(process.cwd(), indexCssPath)}`,
  );

  // 確定最終 fontFamily
  const finalFontFamily = detectedFontFamily || config.title || pkgName;

  // 產生群組根目錄 package.json 與 README.md
  writePackageJson(groupDestDir, config, "index.css");
  writeGroupReadme(groupDestDir, config, finalFontFamily);

  // 複製授權檔案或資料夾
  if (config.licenseSource) {
    copyLicenseSource(groupDestDir, config.licenseSource);
  }

  return { status: allSkipped ? "skipped" : "success", name: config.name };
}

/**
 * 主執行入口
 */
export async function main() {
  const { values, positionals } = parseArgs({
    options: {
      config: { type: "string", short: "c", default: "./fonts.config.mjs" },
      help: { type: "boolean", short: "h" },
    },
    strict: false,
    allowPositionals: true,
  });

  if (values.help) {
    console.log(`使用說明：`);
    console.log(`  批次建置全部字型: node tools/build.mjs`);
    console.log(`  建置指定名稱套件: node tools/build.mjs <packageName>`);
    console.log(`\n選用參數：`);
    console.log(
      `  -c, --config <path>   指定字型設定檔路徑 (預設: ./fonts.config.mjs)`,
    );
    process.exit(0);
  }

  const configPath = path.resolve(values.config || "./fonts.config.mjs");
  if (!fs.existsSync(configPath)) {
    console.error(`✖ 找不到設定檔: ${configPath}`);
    process.exit(1);
  }

  // 動態載入設定檔
  const configModule = await import(pathToFileURL(configPath).href);
  const fontConfigs = configModule.default || [];

  if (!Array.isArray(fontConfigs) || fontConfigs.length === 0) {
    console.warn(`⚠ 設定檔中未包含任何字型項目。`);
    process.exit(0);
  }

  // 若有傳入指定名稱，則過濾出該項目
  const targetName = positionals[0]?.toLowerCase();
  const targetConfigs = targetName
    ? fontConfigs.filter((cfg) => toKebabCase(cfg.name) === targetName)
    : fontConfigs;

  if (targetName && targetConfigs.length === 0) {
    console.error(`✖ 在設定檔中找不到名稱為 "${targetName}" 的字型套件。`);
    process.exit(1);
  }

  console.log(`========================================`);
  console.log(`🚀 開始 WebFont 套件批次建置`);
  console.log(`  設定檔: ${configPath}`);
  console.log(`  待處理套件數: ${targetConfigs.length}`);
  console.log(`========================================`);

  const globalStart = Date.now();
  let successCount = 0;
  let skippedCount = 0;
  let failCount = 0;

  for (const config of targetConfigs) {
    let res;
    if (Array.isArray(config.items) && config.items.length > 0) {
      res = await buildFontGroup(config);
    } else if (config.file) {
      res = await buildSingleFont(config);
    } else {
      console.warn(`⚠ 套件 [${config.name}] 既無 items 也無 file，略過。`);
      continue;
    }

    if (res.status === "success") successCount++;
    else if (res.status === "skipped") skippedCount++;
    else if (res.status === "error") failCount++;
  }

  console.log(`\n========================================`);
  console.log(
    `🎉 建置流程結束！總耗時: ${((Date.now() - globalStart) / 1000).toFixed(2)} 秒`,
  );
  console.log(
    `📊 統計結果: 成功 ${successCount} 個, 略過 ${skippedCount} 個, 失敗 ${failCount} 個 (共 ${targetConfigs.length} 個)`,
  );
  if (skippedCount > 0) {
    console.log("略過者，仍會更新 package.json 與 README.md。");
  }
  console.log(`========================================`);
}

// CLI 執行
if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
  main();
}
