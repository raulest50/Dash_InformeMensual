const fs = require("node:fs");
const path = require("node:path");
const sharp = require("C:/Users/hardp/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");
const { PNG } = require("C:/Users/hardp/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pngjs");

const here = __dirname;
const sourcePng = path.resolve(here, "..", "logoComce.png");

async function loadPixelmatch() {
  const modulePath = "file:///C:/Users/hardp/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pixelmatch/index.js";
  const mod = await import(modulePath);
  return mod.default;
}

function readPng(file) {
  return PNG.sync.read(fs.readFileSync(file));
}

async function renderSvg(name, options = {}) {
  const input = path.join(here, name);
  const suffix = options.suffix || "review";
  const output = path.join(here, name.replace(/\.svg$/i, `.${suffix}.png`));
  let image = sharp(input, { density: 192 });

  if (options.width || options.height) {
    image = image.resize({
      width: options.width,
      height: options.height,
      fit: options.fit || "contain",
      background: options.background || { r: 255, g: 255, b: 255, alpha: 0 },
    });
  }

  if (options.flatten) {
    image = image.flatten({ background: options.flatten });
  }

  await image.png().toFile(output);
  return output;
}

async function main() {
  const pixelmatch = await loadPixelmatch();

  const rendered = [];
  rendered.push(await renderSvg("logoComce.svg", { width: 1231, height: 480, flatten: "#FFFFFF" }));
  rendered.push(await renderSvg("logoComce-mono.svg", { width: 1231, height: 480, flatten: "#FFFFFF" }));
  rendered.push(await renderSvg("logoComce-white.svg", { width: 1231, height: 480, flatten: "#1E252B" }));
  rendered.push(await renderSvg("logoComce-compact.svg", { width: 1140, height: 225, flatten: "#FFFFFF" }));
  rendered.push(await renderSvg("logoComce.svg", { width: 420, height: 164, flatten: "#FFFFFF", suffix: "web-review" }));
  rendered.push(await renderSvg("logoComce.svg", { width: 2462, height: 960, flatten: "#FFFFFF", suffix: "print-review" }));

  const actual = readPng(rendered[0]);
  const expected = readPng(sourcePng);
  const diff = new PNG({ width: expected.width, height: expected.height });
  const mismatched = pixelmatch(expected.data, actual.data, diff.data, expected.width, expected.height, {
    threshold: 0.16,
    includeAA: false,
  });
  const diffPath = path.join(here, "logoComce.diff.png");
  fs.writeFileSync(diffPath, PNG.sync.write(diff));

  const metrics = {
    source: path.relative(here, sourcePng).replaceAll("\\", "/"),
    rendered: path.basename(rendered[0]),
    diff: path.basename(diffPath),
    width: expected.width,
    height: expected.height,
    mismatchedPixels: mismatched,
    mismatchPercent: Number(((mismatched / (expected.width * expected.height)) * 100).toFixed(3)),
    reviewFiles: rendered.map((file) => path.basename(file)),
  };

  fs.writeFileSync(path.join(here, "review-metrics.json"), JSON.stringify(metrics, null, 2));
  console.log(JSON.stringify(metrics, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
