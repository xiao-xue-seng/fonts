import fs from "node:fs";
import path from "node:path";

export const BUILD_OPTIONS_SCHEMA_VERSION = 1;

export function extractFontFamily(cssContent, fallback = "") {
  if (!cssContent) return fallback;
  const match = cssContent.match(/font-family:\s*["']?([^;"'\r\n]+)["']?/i);
  return match ? match[1].trim() : fallback;
}

export function createResliceTempDir(destDir) {
  const resolvedDestDir = path.resolve(destDir);
  fs.mkdirSync(path.dirname(resolvedDestDir), { recursive: true });
  return fs.mkdtempSync(
    path.join(path.dirname(resolvedDestDir), `.${path.basename(destDir)}.tmp-`),
  );
}

export function replaceOutputDirectory(tempDir, destDir) {
  const resolvedDestDir = path.resolve(destDir);
  const parentDir = path.dirname(resolvedDestDir);
  const baseName = path.basename(resolvedDestDir);
  const backupRoot = fs.mkdtempSync(
    path.join(parentDir, `.${baseName}.backup-`),
  );
  const backupDest = path.join(backupRoot, baseName);
  let hasBackup = false;

  try {
    if (fs.existsSync(resolvedDestDir)) {
      fs.renameSync(resolvedDestDir, backupDest);
      hasBackup = true;
    }
    fs.renameSync(tempDir, resolvedDestDir);
    try {
      fs.rmSync(backupRoot, { recursive: true, force: true });
    } catch (err) {
      console.warn(`  ⚠ 無法清理舊輸出備份: ${backupRoot}`, err.message);
    }
  } catch (err) {
    if (hasBackup && !fs.existsSync(resolvedDestDir)) {
      fs.renameSync(backupDest, resolvedDestDir);
    }
    if (fs.existsSync(backupRoot)) {
      fs.rmSync(backupRoot, { recursive: true, force: true });
    }
    throw err;
  }
}
