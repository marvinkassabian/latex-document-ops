#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


def build_pdf_name_set(source_dir: Path, pattern: str) -> set[str]:
    if not source_dir.exists():
        return set()
    return {f"{tex_file.stem}.pdf" for tex_file in source_dir.glob(pattern)}


def download_release_pdfs(
    release_tag: str,
    repository: str = "",
    sections_dir: str = "src/sections",
    frontmatter_dir: str = "src/frontmatter",
) -> None:
    if not repository:
        repository = os.environ.get("GITHUB_REPOSITORY", "")

    if not repository:
        print("Error: repository not provided and GITHUB_REPOSITORY not set", file=sys.stderr)
        sys.exit(1)

    build_dir = Path("build")
    sections_out_dir = build_dir / "sections"
    frontmatter_out_dir = build_dir / "frontmatter"
    build_dir.mkdir(exist_ok=True)
    sections_out_dir.mkdir(exist_ok=True)
    frontmatter_out_dir.mkdir(exist_ok=True)

    frontmatter_pdf_names = build_pdf_name_set(Path(frontmatter_dir), "*.tex")
    section_pdf_names = build_pdf_name_set(Path(sections_dir), "*.tex")

    ambiguous = frontmatter_pdf_names & section_pdf_names
    if ambiguous:
        for name in sorted(ambiguous):
            print(
                f"Ambiguous PDF basename appears in both {frontmatter_dir} and {sections_dir}: {name}",
                file=sys.stderr,
            )
        sys.exit(1)

    result = subprocess.run(
        [
            "gh",
            "release",
            "download",
            release_tag,
            "--repo",
            repository,
            "--pattern",
            "*.pdf",
            "--dir",
            str(build_dir),
        ],
        check=False,
    )
    if result.returncode != 0:
        sys.exit(result.returncode)

    for pdf in build_dir.glob("*.pdf"):
        if pdf.name in frontmatter_pdf_names:
            pdf.rename(frontmatter_out_dir / pdf.name)
        elif pdf.name in section_pdf_names:
            pdf.rename(sections_out_dir / pdf.name)


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        print(
            "Usage: download_release_pdfs.py <release_tag> [repository] [sections_dir] [frontmatter_dir]",
            file=sys.stderr,
        )
        sys.exit(1)

    release_tag = sys.argv[1]
    repository = sys.argv[2] if len(sys.argv) > 2 else ""
    sections_dir = sys.argv[3] if len(sys.argv) > 3 else "src/sections"
    frontmatter_dir = sys.argv[4] if len(sys.argv) > 4 else "src/frontmatter"
    download_release_pdfs(release_tag, repository, sections_dir, frontmatter_dir)


if __name__ == "__main__":
    main()
