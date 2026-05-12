# COMCE Fendipetroleo SVG Assets

Generated vector package based on `../logoComce.png`.

## Files

- `logoComce.svg`: main color reconstruction, `viewBox="0 0 1231 480"`.
- `logoComce-mono.svg`: monochrome version for light backgrounds.
- `logoComce-white.svg`: white version for dark backgrounds.
- `logoComce-compact.svg`: compact top-row variant.
- `*.review.png`: rendered review PNGs generated from the SVG files.
- `logoComce.diff.png`: pixel-level comparison against the source PNG.
- `review-metrics.json`: render and comparison metrics.

## Regeneration

Run from the repository root:

```powershell
& "Dash_InformeMensual\assets\brand_svg\generate_brand_svg.ps1"
& "C:\Users\hardp\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" "Dash_InformeMensual\assets\brand_svg\render_review.cjs"
```

The final SVGs contain outlined paths only. They do not embed raster images or depend on runtime fonts.
