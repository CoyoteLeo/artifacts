"""Wrap each pages/<slug>/page.html in the document skeleton and write dist/.

page.html is the exact file published as a claude.ai artifact: a body fragment
(its own <title>, <style>, markup) without <!doctype>/<head>/<body>. The artifact
host adds that skeleton at publish time, so a static host needs it added here,
or the page renders in quirks mode with no viewport meta.
"""

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ROOT / "pages"
DIST = ROOT / "dist"

# Mirrors the artifact host's skeleton so a page renders the same in both places.
SKELETON = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
body{{margin:0;font:14px/1.5 system-ui,-apple-system,sans-serif;background:#fafaf9}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def page_title(fragment: str, fallback: str) -> str:
    match = re.search(r"<title>(.*?)</title>", fragment[:8192], re.S)
    return match.group(1).strip() if match else fallback


def main() -> None:
    shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir()
    entries = []
    for page in sorted(PAGES.glob("*/page.html")):
        slug = page.parent.name
        fragment = page.read_text(encoding="utf-8")
        out_dir = DIST / slug
        # Supporting files (images, data) sit next to page.html and ship as-is.
        shutil.copytree(page.parent, out_dir, ignore=shutil.ignore_patterns("page.html"))
        (out_dir / "index.html").write_text(SKELETON.format(body=fragment), encoding="utf-8")
        entries.append((slug, page_title(fragment, slug)))

    items = "\n".join(
        f'<li><a href="{slug}/">{html.escape(title)}</a></li>' for slug, title in entries
    )
    index = f"<title>Artifacts</title>\n<main style=\"max-width:640px;margin:0 auto;padding:32px 16px\">\n<h1>Artifacts</h1>\n<ul>\n{items}\n</ul>\n</main>"
    (DIST / "index.html").write_text(SKELETON.format(body=index), encoding="utf-8")
    print(f"built {len(entries)} page(s) into {DIST}")


if __name__ == "__main__":
    main()
