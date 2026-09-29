#!/usr/bin/env python3
"""Check generated HTML links and Project Pages base paths without dependencies."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / ".build" / "public"
BASE = "/hyperframes-lab"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src", "poster") and value:
                self.urls.append((tag, name, value))


def target_for(path):
    relative = unquote(path[len(BASE):]).lstrip("/")
    path = PUBLIC / relative
    if path.is_dir() or not path.suffix:
        path /= "index.html"
    return path


def main():
    if not (PUBLIC / "index.html").is_file():
        raise SystemExit("Missing built Home page")
    errors = []
    count = 0
    for html in sorted(PUBLIC.rglob("*.html")):
        parser = Links()
        parser.feed(html.read_text(encoding="utf-8"))
        for tag, attribute, raw in parser.urls:
            parsed = urlsplit(raw)
            if parsed.scheme in ("mailto", "tel", "data") or raw.startswith("#"):
                continue
            if parsed.scheme and parsed.netloc != "greenwakame.github.io":
                continue
            page_url = BASE + "/" + html.relative_to(PUBLIC).as_posix()
            if page_url.endswith("/index.html"):
                page_url = page_url[:-10]
            path = urlsplit(urljoin(page_url, raw)).path
            if parsed.scheme and not path.startswith(BASE + "/") and path != BASE:
                continue  # Main Portfolio or another project
            if not path.startswith(BASE + "/") and path != BASE:
                errors.append(f"{html.relative_to(PUBLIC)}: {tag} {attribute} uses path outside base: {raw}")
                continue
            target = target_for(path)
            if not target.is_relative_to(PUBLIC) or not target.is_file():
                errors.append(f"{html.relative_to(PUBLIC)}: missing {raw}")
            count += 1
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {count} internal URLs across {len(list(PUBLIC.rglob('*.html')))} HTML pages; no missing targets")


if __name__ == "__main__":
    main()
