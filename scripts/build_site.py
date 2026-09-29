#!/usr/bin/env python3
"""Build a small Jekyll source tree from the repository's original content."""

import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / ".build" / "site-src"
CASE_ROOT = ROOT / "case-studies"
DOC_ROOT = ROOT / "docs"
EXAMPLE_ROOT = ROOT / "examples"
REQUIRED = {
    "slug", "title", "summary", "category", "tags", "featured", "duration",
    "resolution", "fps", "poster", "video", "poster_alt", "status",
}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)|!\[([^\]]*)\]\(([^)]+)\)")
GITHUB = "https://github.com/greenwakame/hyperframes-lab/blob/main"
KNOWLEDGE_ORDER = [
    "environment", "getting-started", "workflow", "animation-design",
    "validation-and-render", "troubleshooting", "github-delivery",
]


def fail(message):
    raise ValueError(message)


def json_front_matter(values):
    return "---\n" + json.dumps(values, ensure_ascii=False) + "\n---\n\n"


def write_page(relative, values, body):
    destination = OUTPUT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json_front_matter(values) + body, encoding="utf-8")


def checked_asset(case_dir, raw, name):
    if not isinstance(raw, str) or not raw.startswith("./"):
        fail(f"{case_dir.name}: {name} must be a ./ relative path")
    path = (case_dir / raw).resolve()
    if not path.is_relative_to(case_dir.resolve()):
        fail(f"{case_dir.name}: {name} escapes the case directory")
    if not path.is_file():
        fail(f"{case_dir.name}: missing {name}: {raw}")
    return path


def webp_size(path):
    data = path.read_bytes()[:40]
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        fail(f"{path.relative_to(ROOT)}: expected a WebP image")
    kind = data[12:16]
    if kind == b"VP8 " and data[23:26] == b"\x9d\x01\x2a":
        return (int.from_bytes(data[26:28], "little") & 0x3FFF,
                int.from_bytes(data[28:30], "little") & 0x3FFF)
    if kind == b"VP8X":
        return (1 + int.from_bytes(data[24:27], "little"),
                1 + int.from_bytes(data[27:30], "little"))
    if kind == b"VP8L" and data[20] == 0x2F:
        b1, b2, b3, b4 = data[21:25]
        return (1 + b1 + ((b2 & 0x3F) << 8),
                1 + (b2 >> 6) + (b3 << 2) + ((b4 & 0x0F) << 10))
    fail(f"{path.relative_to(ROOT)}: unsupported WebP encoding")


def validate_cases():
    cases = []
    seen = set()
    for case_dir in sorted(CASE_ROOT.iterdir()):
        if not case_dir.is_dir():
            continue
        metadata_path = case_dir / "case.json"
        if not metadata_path.is_file():
            fail(f"{case_dir.name}: missing case.json")
        try:
            case = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            fail(f"{metadata_path}: invalid JSON: {error}")
        missing = sorted(REQUIRED - case.keys())
        if missing:
            fail(f"{case_dir.name}: missing fields: {', '.join(missing)}")
        slug = case["slug"]
        if not isinstance(slug, str) or not SLUG.fullmatch(slug):
            fail(f"{case_dir.name}: invalid slug")
        if slug != case_dir.name:
            fail(f"{case_dir.name}: directory name differs from slug {slug}")
        if slug in seen:
            fail(f"duplicate slug: {slug}")
        seen.add(slug)
        for field in ("title", "summary", "category", "poster_alt", "status", "resolution"):
            if not isinstance(case[field], str) or not case[field].strip():
                fail(f"{slug}: {field} must be a nonempty string")
        if not isinstance(case["tags"], list) or not all(isinstance(tag, str) and tag for tag in case["tags"]):
            fail(f"{slug}: tags must be a list of strings")
        if type(case["featured"]) is not bool:
            fail(f"{slug}: featured must be boolean")
        if type(case["duration"]) not in (int, float) or case["duration"] <= 0:
            fail(f"{slug}: duration must be positive number")
        if type(case["fps"]) not in (int, float) or case["fps"] <= 0:
            fail(f"{slug}: fps must be positive number")
        if "date" in case:
            try:
                dt.date.fromisoformat(case["date"])
            except (TypeError, ValueError):
                fail(f"{slug}: date must be YYYY-MM-DD")
        for field in ("poster", "video"):
            checked_asset(case_dir, case[field], field)
        case["poster_width"], case["poster_height"] = webp_size(checked_asset(case_dir, case["poster"], "poster"))
        if not (case_dir / "README.md").is_file():
            fail(f"{slug}: missing README.md")
        case["url"] = f"/cases/{slug}/"
        case["poster_url"] = f"/assets/cases/{slug}/{case['poster'][2:]}"
        case["video_url"] = f"/assets/cases/{slug}/{case['video'][2:]}"
        case["source_url"] = f"{GITHUB}/case-studies/{slug}/README.md"
        cases.append(case)
    if not cases:
        fail("no cases found")
    cases.sort(key=lambda case: case["slug"])
    cases.sort(key=lambda case: case.get("date", ""), reverse=True)
    return cases


def site_path(target):
    relative = target.relative_to(ROOT).as_posix()
    if relative == "RIGHTS-AND-CREDITS.md":
        return "/rights/"
    if relative in ("LICENSE-CODE", "LICENSE-DOCS"):
        return f"{GITHUB}/{relative}"
    if relative == "docs/README.md":
        return "/knowledge/"
    if relative.startswith("docs/") and relative.endswith(".md"):
        return f"/knowledge/{target.stem}/"
    if relative == "case-studies/README.md":
        return "/cases/"
    parts = target.relative_to(ROOT).parts
    if len(parts) >= 3 and parts[0] == "case-studies":
        slug = parts[1]
        if len(parts) == 3 and parts[2] == "README.md":
            return f"/cases/{slug}/"
        if len(parts) == 3 and parts[2] in ("DESIGN.md", "ITERATIONS.md"):
            return f"/cases/{slug}/{parts[2][:-3].lower()}/"
        if parts[2] in ("assets", "media"):
            return f"/assets/cases/{slug}/{'/'.join(parts[2:])}"
    if relative == "examples/README.md":
        return "/examples/"
    if len(parts) >= 3 and parts[0] == "examples":
        slug = parts[1]
        if len(parts) == 3 and parts[2] == "README.md":
            return f"/examples/{slug}/"
        if len(parts) == 3 and parts[2] == "index.html":
            return f"/examples/{slug}/demo/"
    fail(f"unmapped local link target: {relative}")


def rewrite_links(markdown, source_path):
    def replace(match):
        label = match.group(1) if match.group(1) is not None else match.group(3)
        raw = match.group(2) if match.group(2) is not None else match.group(4)
        image = match.group(3) is not None
        parsed = urlsplit(raw)
        if parsed.scheme or raw.startswith("//") or raw.startswith("#"):
            return match.group(0)
        target = (source_path.parent / parsed.path).resolve()
        if not target.is_relative_to(ROOT) or not target.exists():
            fail(f"{source_path.relative_to(ROOT)}: broken link: {raw}")
        mapped = site_path(target)
        suffix = ("?" + parsed.query if parsed.query else "") + ("#" + parsed.fragment if parsed.fragment else "")
        url = "{{ '" + mapped + "' | relative_url }}" + suffix if mapped.startswith("/") else mapped + suffix
        if image and target.suffix.lower() == ".webp":
            width, height = webp_size(target)
            return (f'<img src="{url}" alt="{html.escape(label, quote=True)}" '
                    f'width="{width}" height="{height}" loading="lazy" decoding="async">')
        return f"{'!' if image else ''}[{label}]({url})"
    return MARKDOWN_LINK.sub(replace, markdown)


def source_body(path, remove_heading=True):
    body = path.read_text(encoding="utf-8")
    if remove_heading:
        body = re.sub(r"\A# [^\n]+\n", "", body, count=1)
    return rewrite_links(body.lstrip(), path)


def title_of(path):
    match = re.search(r"^# (.+)$", path.read_text(encoding="utf-8"), re.M)
    if not match:
        fail(f"{path.relative_to(ROOT)}: missing H1")
    return match.group(1)


def excerpt_of(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        if line and not line.startswith(("#", "-", "|", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "![", "[")):
            clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
            clean = clean.replace("**", "").replace("`", "")
            return clean[:180]
    return title_of(path)


def build_cases(cases):
    for case in cases:
        slug = case["slug"]
        case_dir = CASE_ROOT / slug
        body = (case_dir / "README.md").read_text(encoding="utf-8")
        body = re.sub(r"\A# [^\n]+\n", "", body, count=1)
        # The case layout owns the hero poster, player and direct MP4 link.
        body = "\n".join(line for line in body.splitlines()
                         if not (case["poster"][2:] in line and case["video"][2:] in line)
                         and not (case["video"][2:] in line and line.lstrip().startswith("[")))
        body = rewrite_links(body.lstrip(), case_dir / "README.md")
        fields = dict(case, layout="case", permalink=case["url"], description=case["summary"],
                      og_image=case["poster_url"], source_path=f"case-studies/{slug}/README.md")
        fields["published_date"] = case.get("date")
        fields["has_design"] = (case_dir / "DESIGN.md").is_file()
        fields["has_iterations"] = (case_dir / "ITERATIONS.md").is_file()
        write_page(f"_cases/{slug}.md", fields, body)
        for name in ("DESIGN", "ITERATIONS"):
            path = case_dir / f"{name}.md"
            if path.is_file():
                write_page(f"cases/{slug}/{name.lower()}.md", {
                    "layout": "article", "title": title_of(path),
                    "description": case["summary"],
                    "permalink": f"/cases/{slug}/{name.lower()}/",
                    "source_path": path.relative_to(ROOT).as_posix(),
                    "parent_url": case["url"], "parent_title": case["title"],
                    "lang": "ja",
                }, source_body(path))
        for asset in (case_dir / "assets").rglob("*"):
            if asset.is_file():
                destination = OUTPUT / "assets" / "cases" / slug / asset.relative_to(case_dir)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(asset, destination)
        video = checked_asset(case_dir, case["video"], "video")
        destination = OUTPUT / case["video_url"].lstrip("/")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video, destination)


def build_knowledge():
    pages = []
    for path in sorted(DOC_ROOT.glob("*.md")):
        if path.name == "README.md":
            continue
        slug = path.stem
        fields = {
            "layout": "article", "title": title_of(path), "description": excerpt_of(path),
            "permalink": f"/knowledge/{slug}/", "source_path": path.relative_to(ROOT).as_posix(),
            "parent_url": "/knowledge/", "parent_title": "Knowledge", "lang": "ja",
        }
        write_page(f"knowledge/{slug}.md", fields, source_body(path))
        pages.append({"slug": slug, "title": fields["title"], "description": fields["description"],
                      "url": fields["permalink"]})
    order = {slug: index for index, slug in enumerate(KNOWLEDGE_ORDER)}
    pages.sort(key=lambda page: (order.get(page["slug"], len(order)), page["slug"]))
    return pages


def build_examples():
    pages = []
    for directory in sorted(EXAMPLE_ROOT.iterdir()):
        if not directory.is_dir():
            continue
        readme = directory / "README.md"
        if not readme.is_file():
            continue
        slug = directory.name
        if not SLUG.fullmatch(slug):
            fail(f"invalid example slug: {slug}")
        original = directory / "index.html"
        demo_supported = original.is_file() and slug == "stable-sprite-ui-reaction"
        fields = {
            "layout": "example", "title": title_of(readme), "description": excerpt_of(readme),
            "permalink": f"/examples/{slug}/", "source_path": readme.relative_to(ROOT).as_posix(),
            "lang": "ja", "example_slug": slug,
            "demo_url": f"/examples/{slug}/demo/" if demo_supported else None,
        }
        write_page(f"examples/{slug}.md", fields, source_body(readme))
        pages.append({"slug": slug, "title": fields["title"], "description": fields["description"],
                      "url": fields["permalink"], "demo_url": fields["demo_url"]})
        if demo_supported:
            html = original.read_text(encoding="utf-8")
            if "window.__timelines['stable-sprite-demo']" in html:
                html = html.replace(
                    "<head>",
                    '<head>\n  <link rel="icon" type="image/svg+xml" href="../../../assets/favicon.svg">\n'
                    '  <script>window.__timelines = {};</script>',
                    1,
                )
                adapter = """<script>
window.addEventListener('message', event => {
  if (event.origin !== location.origin || !event.data || event.data.type !== 'demo-control') return;
  const timeline = window.__timelines['stable-sprite-demo'];
  if (!timeline) return;
  if (event.data.action === 'play') timeline.play();
  if (event.data.action === 'pause') timeline.pause();
  if (event.data.action === 'replay') timeline.restart();
});
</script>"""
                html = html.replace("</body>", adapter + "\n</body>", 1)
                demo = OUTPUT / "examples" / slug / "demo" / "index.html"
                demo.parent.mkdir(parents=True, exist_ok=True)
                demo.write_text(html, encoding="utf-8")
    return pages


def main():
    cases = validate_cases()
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    build_cases(cases)
    knowledge = build_knowledge()
    examples = build_examples()
    data = OUTPUT / "_data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "cases.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (data / "knowledge.json").write_text(json.dumps(knowledge, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (data / "examples.json").write_text(json.dumps(examples, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rights = ROOT / "RIGHTS-AND-CREDITS.md"
    write_page("rights.md", {
        "layout": "article", "title": title_of(rights),
        "description": "Documentation, example code, project media and third-party rights.",
        "permalink": "/rights/", "source_path": rights.name, "lang": "ja",
    }, source_body(rights))
    print(f"Generated Jekyll source: {OUTPUT} ({len(cases)} cases, {len(knowledge)} knowledge pages, {len(examples)} examples)")


if __name__ == "__main__":
    main()
