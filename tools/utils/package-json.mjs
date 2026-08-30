import fs from "node:fs";
import path from "node:path";
import { BUILD_OPTIONS_SCHEMA_VERSION } from "./font-output.mjs";

const DEFAULT_LICENSE = "OFL-1.1";
const DEFAULT_VERSION = "1.0.0";

/**
 * 讀取輸出目錄中的 package.json。
 *
 * 回傳 null 表示檔案不存在或內容不是有效的 JSON 物件；這讓呼叫端可以
 * 將它視為「沒有可用的快取 metadata」。
 */
export function readPackageJson(destDir) {
  const packageJsonPath = path.join(destDir, "package.json");
  if (!fs.existsSync(packageJsonPath)) return null;

  try {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf-8"));
    return packageJson && typeof packageJson === "object" && !Array.isArray(packageJson)
      ? packageJson
      : null;
  } catch {
    return null;
  }
}

export function readPackageBuildOptions(destDir) {
  const packageJson = readPackageJson(destDir);
  const buildOptions = packageJson?.buildOptions;
  return buildOptions && typeof buildOptions === "object" && !Array.isArray(buildOptions)
    ? buildOptions
    : null;
}

/**
 * 將切片快取所需欄位標準化。這些欄位只應包含會影響切片輸出的選項。
 */
export function normalizeBuildOptions(buildOptions = {}) {
  return {
    schemaVersion: BUILD_OPTIONS_SCHEMA_VERSION,
    ...buildOptions,
  };
}

/**
 * 建立標準 npm package.json 物件。
 *
 * 呼叫端只負責提供流程特有的 metadata；package.json 的共同結構由此處
 * 統一維護。fontMetadata 是非切片資訊，不會被放入 buildOptions。
 */
export function createPackageJson({
  scope,
  pkgName,
  rawFontName = pkgName,
  version = DEFAULT_VERSION,
  description = `Webfont subset for ${rawFontName}`,
  main = "result.css",
  keywords = ["font", "webfont", "chinese-font", pkgName],
  license = DEFAULT_LICENSE,
  buildOptions = null,
  fontMetadata = null,
} = {}) {
  const packageJson = {
    name: `@${scope}/${pkgName}`,
    version,
    description,
    main,
    style: main,
    keywords: [...new Set(keywords)],
    license,
    publishConfig: {
      access: "public",
    },
  };

  if (buildOptions) {
    packageJson.buildOptions = normalizeBuildOptions(buildOptions);
  }
  if (fontMetadata) {
    packageJson.fontMetadata = fontMetadata;
  }

  return packageJson;
}

export function writePackageJson(destDir, packageJson) {
  fs.writeFileSync(
    path.join(destDir, "package.json"),
    JSON.stringify(packageJson, null, 2) + "\n",
    "utf-8",
  );
}

export function writePackageBuildOptions(destDir, buildOptions) {
  const packageJson = readPackageJson(destDir) || {};
  packageJson.buildOptions = normalizeBuildOptions(buildOptions);
  writePackageJson(destDir, packageJson);
}
