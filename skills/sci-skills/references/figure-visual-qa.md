# Figure Visual QA

Run this after rendering and before final insertion or packaging.

## Source and execution

- Confirm the source file exists and uses the approved route.
- For result figures, confirm real input readers, declared transformations, Python/R execution evidence, and input-to-output traceability.
- Flag embedded result arrays, unreported manual values, simulated data, or image-generation provenance.
- Preserve raw inputs, processing code, seeds, environment notes, and generated-file timestamps or hashes when available.

## Scientific content

- Match axes, units, groups, sample sizes, metrics, and panel claims to the source.
- Define center, spread, intervals, tests, corrections, and significance notation.
- Show paired, repeated, hierarchical, temporal, or censored structure honestly.
- Make missing, excluded, interpolated, normalized, or transformed values explicit.
- Verify that explanatory diagrams do not overstate mechanisms or causal relations.
- Flag outliers without removing them automatically. Require declared smoothing, interpolation, normalization, clustering, axis truncation, and reference thresholds.
- Resolve every blocking or revision finding returned by the scientific-figures expert.

## Visual inspection at final size

- Read every label and panel letter at the intended manuscript dimensions.
- Check clipping, overlap, whitespace, alignment, legend placement, scale bars, and image crops.
- Confirm consistent group, method, and module mappings across panels and figures.
- Test color plus redundant encodings and inspect a grayscale rendering when relevant.
- Confirm that overview and module panels remain distinguishable and that no panel carries excessive explanatory load.

## Export inspection

- Prefer editable SVG/PDF for plots and diagrams.
- Use high-resolution TIFF/PNG for raster images or required submission files.
- Verify dimensions, effective DPI, page size, transparency, and font behavior where the format permits.
- Detect embedded raster content in nominally vector files and Type 3 or unembedded PDF-font risk where inspectable.
- Check CJK glyphs, Unicode minus, grayscale distinction, and redundant group encodings.
- Open the delivered files rather than trusting successful save calls.

Use the independent `sci-skills-scientific-figures` expert and its current local scripts for data profiling, chart recommendation, source validation, layout QA, and export inspection. Treat unavailable optional checks as `DEGRADED`; do not require installation in the mainline. Automated checks are preflight aids, not proof of scientific correctness.

## User review

Use `templates/figure-review-card.md` after QA. Keep final manuscript insertion blocked until the user explicitly approves the rendered figure.
