# artifacts

Pages first published as claude.ai artifacts, kept here as the source of truth and deployed to GitHub Pages.

## Layout

- `pages/<slug>/page.html` — the exact file published as the artifact: a body fragment with its own `<title>` and `<style>`, no `<!doctype>`/`<head>`/`<body>`. Supporting files (images, data) go next to it.
- `build.py` — wraps each fragment in the same document skeleton the artifact host adds, writes `dist/<slug>/index.html` plus a `dist/index.html` listing every page.
- `.github/workflows/pages.yml` — builds on every push and PR, deploys `dist/` to Pages from `main`.

## Add or update a page

1. Edit `pages/<slug>/page.html` here, not in the artifact.
2. `python3 build.py`, then open `dist/<slug>/index.html` to check it.
3. Merge to `main`; Pages deploys it at `https://coyoteleo.github.io/artifacts/<slug>/`.
4. To keep the artifact in sync, republish the same `page.html` to its artifact URL.

Only static pages work here. An artifact that uses the host's runtime (`window.claude`, shared database, uploads) won't run on Pages.

This repo and its Pages site are public: keep personal details (home address, phone numbers) out of `page.html`.

## Pages

- `taichung-trip` — 台中深度三日 · artifact: https://claude.ai/artifact/TYb1adFWGLGuiT2RyzGsdk
- `nye-2027` — 跨年海景四日 · artifact: https://claude.ai/artifact/XQjMv53GnFC9aB15DRijVc
