#!/usr/bin/env python3

import html
import os
import shutil
import sys
from pathlib import Path


def escape_content(value: str) -> str:
    return html.escape(value, quote=True)


def collect_pdfs(artifact_path: Path) -> list[Path]:
    return sorted(artifact_path.rglob("*.pdf"))


def build_links_html(pdfs: list[Path], artifact_path: Path) -> str:
    links: list[str] = []
    for pdf in pdfs:
        rel_path = pdf.relative_to(artifact_path)
        href = f"{artifact_path.as_posix().rstrip('/')}/{rel_path.as_posix()}"
        label = rel_path.as_posix()
        links.append(f'    <li><a href="{escape_content(href)}">{escape_content(label)}</a></li>')

    if not links:
        links.append("    <li>No PDF artifacts were found for this build.</li>")

    return "\n".join(links)


def render_index(
    template_path: Path,
    page_title: str,
    page_description: str,
    links_html: str,
) -> str:
    template = template_path.read_text(encoding="utf-8")
    rendered = template.replace("__PAGE_TITLE__", escape_content(page_title))
    rendered = rendered.replace("__PAGE_DESCRIPTION__", escape_content(page_description))
    rendered = rendered.replace("__PDF_LINKS__", links_html)
    return rendered


def main() -> None:
    artifact_path_value = os.environ.get("ARTIFACT_PATH", "").strip()
    page_title = os.environ.get("PAGE_TITLE", "LaTeX Build Artifacts")
    page_description = os.environ.get("PAGE_DESCRIPTION", "Generated from the latest build.")

    if not artifact_path_value:
        print("ARTIFACT_PATH is required", file=sys.stderr)
        sys.exit(1)

    artifact_path = Path(artifact_path_value)
    if not artifact_path.exists() or not artifact_path.is_dir():
        print(f"Artifact path does not exist or is not a directory: {artifact_path}", file=sys.stderr)
        sys.exit(1)

    action_path = Path(os.environ.get("GITHUB_ACTION_PATH", ""))
    if not action_path:
        print("GITHUB_ACTION_PATH is required", file=sys.stderr)
        sys.exit(1)

    template_path = action_path.parent.parent / "pages" / "index.template.html"
    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    pdfs = collect_pdfs(artifact_path)
    links_html = build_links_html(pdfs, artifact_path)

    site_dir = Path("site")
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True, exist_ok=True)

    index_html = render_index(
        template_path=template_path,
        page_title=page_title,
        page_description=page_description,
        links_html=links_html,
    )
    (site_dir / "index.html").write_text(index_html, encoding="utf-8")

    destination = site_dir / artifact_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(artifact_path, destination, dirs_exist_ok=True)

    print(f"Pages site generated at: {site_dir}")
    print(f"Indexed PDFs: {len(pdfs)}")


if __name__ == "__main__":
    main()