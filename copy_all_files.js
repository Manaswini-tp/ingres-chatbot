const fs = require("fs");
const path = require("path");

const ROOT_DIR = __dirname;
const OUTPUT_FILE = path.join(ROOT_DIR, "all_code.txt");

// ✅ Include only real source code files
const ALLOWED_EXTENSIONS = [".js", ".jsx", ".py", ".html", ".css", ".env",".csv",".java",".mini",".g4",".xml",".yml","txt"];

// 🚫 Skip these folders completely
const SKIP_FOLDERS = [
  "node_modules",
  ".git",
  "venv",
  "__pycache__",
  "dist",
  "build",
  ".next",
  ".vite",
  "ml/venv",
  "output",
  "target"
];

// 🚫 Skip these specific files or patterns
const SKIP_FILES = [
  "package-lock.json",
  "yarn.lock",
  "pnpm-lock.yaml",
  "all_code.txt",
  ".DS_Store",
  "commands.txt",
  "copy_all_files.js"
];

// ✅ Skip large files (>1 MB)
const MAX_SIZE_BYTES = 1 * 1024 * 1024;

function shouldSkip(fullPath, stat) {
  if (stat.isDirectory()) {
    return SKIP_FOLDERS.some(folder => fullPath.includes(folder));
  }
  const fileName = path.basename(fullPath);
  const ext = path.extname(fullPath).toLowerCase();

  return (
    !ALLOWED_EXTENSIONS.includes(ext) ||
    SKIP_FILES.includes(fileName) ||
    stat.size > MAX_SIZE_BYTES
  );
}

function collectFiles(dir) {
  let content = "";
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (shouldSkip(fullPath, stat)) continue;

    if (stat.isDirectory()) {
      content += collectFiles(fullPath);
    } else {
      content += `\n\n// ======= ${fullPath} =======\n\n`;
      try {
        const fileText = fs.readFileSync(fullPath, "utf8");
        content += fileText;
      } catch {
        content += "// (Skipped unreadable file)\n";
      }
    }
  }

  return content;
}

// 🚀 Run
console.log("Collecting project code, please wait...");
const allCode = collectFiles(ROOT_DIR);
fs.writeFileSync(OUTPUT_FILE, allCode);
console.log(`✅ Clean project code saved to: ${OUTPUT_FILE}`);
