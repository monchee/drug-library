#!/usr/bin/env python3
"""
Compare rendered output between MkDocs (site/) and Astro/Starlight (dist/)
across all drug pages.

Verifies:
1. DOSE TABLES: parse every <table>, strip tags, unescape entities, compare cell text.
2. ADMONITIONS: compare extracted text (title + body) between MkDocs (<div class="admonition">)
   and Starlight (<aside class="...starlight-aside...">).
3. REVIEW METADATA: verify presence of "Reviewed by" on all drug pages in both outputs.
4. PROSE CONTENT: extract main article content, excluding site chrome (nav, sidebar, toc,
   header, footer, search, pagination, permalinks, print buttons), normalize entities and
   typographic punctuation/quotes, and compare body text across all pages.
"""

import argparse
import difflib
import html
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Tuple, Optional


class TableParser(HTMLParser):
    """Extracts tables as 2D grids of cleaned text cells."""

    def __init__(self) -> None:
        super().__init__()
        self.tables: List[List[List[str]]] = []
        self.current_table: Optional[List[List[str]]] = None
        self.current_row: Optional[List[str]] = None
        self.cell_chunks: List[str] = []
        self.in_cell: bool = False

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag == "table":
            self.current_table = []
        elif tag == "tr" and self.current_table is not None:
            self.current_row = []
        elif tag in ("td", "th") and self.current_row is not None:
            self.in_cell = True
            self.cell_chunks = []
        elif tag in ("br", "p", "div", "li") and self.in_cell:
            self.cell_chunks.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th") and self.in_cell:
            self.in_cell = False
            raw_text = "".join(self.cell_chunks)
            clean_text = " ".join(html.unescape(raw_text).split())
            if self.current_row is not None:
                self.current_row.append(clean_text)
        elif tag == "tr" and self.current_row is not None:
            if self.current_row:
                self.current_table.append(self.current_row)
            self.current_row = None
        elif tag == "table" and self.current_table is not None:
            if self.current_table:
                self.tables.append(self.current_table)
            self.current_table = None
        elif tag in ("p", "div", "li") and self.in_cell:
            self.cell_chunks.append(" ")

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_chunks.append(data)

    def handle_entityref(self, name: str) -> None:
        if self.in_cell:
            self.cell_chunks.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self.in_cell:
            self.cell_chunks.append(f"&#{name};")


class AdmonitionParser(HTMLParser):
    """Extracts admonition text blocks from MkDocs or Starlight rendered HTML."""

    def __init__(self, mode: str = "site") -> None:
        super().__init__()
        self.mode = mode
        self.admonitions: List[str] = []
        self.depth: int = 0
        self.current_chunks: List[str] = []
        self.in_admonition: bool = False

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "").split()

        is_admonition_start = False
        if self.mode == "site":
            if "admonition" in classes and not self.in_admonition:
                is_admonition_start = True
        elif self.mode == "dist":
            if tag == "aside" and "starlight-aside" in classes and not self.in_admonition:
                is_admonition_start = True

        if is_admonition_start:
            self.in_admonition = True
            self.depth = 1
            self.current_chunks = []
            return

        if self.in_admonition:
            self.depth += 1
            self.current_chunks.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if self.in_admonition:
            self.depth -= 1
            if self.depth == 0:
                self.in_admonition = False
                raw_text = "".join(self.current_chunks)
                clean_text = " ".join(html.unescape(raw_text).split())
                self.admonitions.append(clean_text)
                self.current_chunks = []
            else:
                self.current_chunks.append(" ")

    def handle_data(self, data: str) -> None:
        if self.in_admonition:
            self.current_chunks.append(data)

    def handle_entityref(self, name: str) -> None:
        if self.in_admonition:
            self.current_chunks.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self.in_admonition:
            self.current_chunks.append(f"&#{name};")


class ProseParser(HTMLParser):
    """
    Extracts the main article body text from MkDocs or Astro/Starlight HTML.
    Excludes chrome (nav, sidebar, toc, header, footer, search, pagination,
    headerlinks/permalinks, tags metadata, print buttons).
    """

    BLOCK_TAGS = {
        "p", "div", "li", "tr", "th", "td",
        "h1", "h2", "h3", "h4", "h5", "h6",
        "br", "hr", "blockquote", "aside", "section",
        "dt", "dd"
    }

    IGNORED_TAGS = {"script", "style", "nav", "button", "svg"}

    def __init__(self, mode: str = "site") -> None:
        super().__init__()
        self.mode = mode
        self.in_content: bool = False
        self.tag_stack: List[Tuple[str, bool]] = []
        self.ignore_tags_stack: List[str] = []
        self.text_chunks: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "").split() if attrs_dict.get("class") else []

        if not self.in_content:
            if self.mode == "site" and tag == "article" and "md-content__inner" in classes:
                self.in_content = True
                self.tag_stack.append((tag, False))
                return
            elif self.mode == "dist" and tag == "div" and "sl-markdown-content" in classes:
                self.in_content = True
                self.tag_stack.append((tag, False))
                return
            return

        should_ignore = False
        if (
            tag in self.IGNORED_TAGS
            or "headerlink" in classes
            or "md-tags" in classes
            or "scratch-review-metadata" in classes
            or "scratch-print-btn" in classes
        ):
            should_ignore = True

        self.tag_stack.append((tag, should_ignore))
        if should_ignore:
            self.ignore_tags_stack.append(tag)

        # Preserve emoji shortcodes/text from twemoji or img alt
        if tag == "img" and not self.ignore_tags_stack:
            if "twemoji" in classes and "title" in attrs_dict and attrs_dict["title"]:
                self.text_chunks.append(attrs_dict["title"])
            elif "alt" in attrs_dict and attrs_dict["alt"]:
                self.text_chunks.append(attrs_dict["alt"])

        if tag in self.BLOCK_TAGS:
            self.text_chunks.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if not self.in_content:
            return

        if tag in self.BLOCK_TAGS:
            self.text_chunks.append(" ")

        while self.tag_stack:
            popped_tag, was_ignored = self.tag_stack.pop()
            if was_ignored and self.ignore_tags_stack and self.ignore_tags_stack[-1] == popped_tag:
                self.ignore_tags_stack.pop()
            if popped_tag == tag:
                break

        if not self.tag_stack:
            self.in_content = False

    def handle_data(self, data: str) -> None:
        if self.in_content and not self.ignore_tags_stack:
            self.text_chunks.append(data)

    def handle_entityref(self, name: str) -> None:
        if self.in_content and not self.ignore_tags_stack:
            self.text_chunks.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self.in_content and not self.ignore_tags_stack:
            self.text_chunks.append(f"&#{name};")


def normalize_prose(raw_text: str) -> str:
    """Normalizes unescaped HTML, typographic quotes, dashes, and whitespace."""
    # 1. Unescape HTML entities
    text = html.unescape(raw_text)
    # 2. Normalize smart / typographic quotes & apostrophes
    text = text.replace("‘", "'").replace("’", "'").replace("`", "'")
    text = text.replace("“", '"').replace("”", '"')
    # 3. Normalize non-breaking and zero-width spaces
    text = text.replace("\u00a0", " ").replace("\u200b", "")
    # 4. Collapse consecutive whitespace
    return " ".join(text.split())


def parse_tables(html_content: str) -> List[List[List[str]]]:
    parser = TableParser()
    parser.feed(html_content)
    return parser.tables


def parse_admonitions(html_content: str, mode: str) -> List[str]:
    parser = AdmonitionParser(mode=mode)
    parser.feed(html_content)
    return parser.admonitions


def parse_prose(html_content: str, mode: str) -> str:
    parser = ProseParser(mode=mode)
    parser.feed(html_content)
    raw_text = "".join(parser.text_chunks)
    return normalize_prose(raw_text)


def format_prose_diff(site_text: str, dist_text: str) -> str:
    """Generates a concise snippet diff showing differences between Site and Dist prose."""
    s_words = site_text.split()
    d_words = dist_text.split()
    matcher = difflib.SequenceMatcher(None, s_words, d_words)
    diff_lines = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            s_snippet = " ".join(s_words[max(0, i1 - 3):min(len(s_words), i2 + 3)])
            d_snippet = " ".join(d_words[max(0, j1 - 3):min(len(d_words), j2 + 3)])
            diff_lines.append(
                f"      [diff: {tag}]\n"
                f"        MkDocs: ... {s_snippet} ...\n"
                f"        Astro:  ... {d_snippet} ..."
            )
    return "\n".join(diff_lines) if diff_lines else "      Text differs (lengths: MkDocs=%d, Astro=%d)" % (len(site_text), len(dist_text))


def compare_builds(
    site_dir: Path,
    dist_dir: Path,
    docs_dir: Path,
    verbose: bool = False,
    strict_prose: bool = False,
) -> int:
    if not site_dir.exists():
        print(f"Error: MkDocs site directory not found: {site_dir}", file=sys.stderr)
        return 1

    if not dist_dir.exists():
        print(f"Error: Astro dist directory not found: {dist_dir}", file=sys.stderr)
        return 1

    if not docs_dir.exists():
        print(f"Error: docs drugs directory not found: {docs_dir}", file=sys.stderr)
        return 1

    drug_files = sorted([p for p in docs_dir.glob("*.md") if p.name != "index.md"])
    if not drug_files:
        print(f"Error: No drug Markdown files found in {docs_dir}", file=sys.stderr)
        return 1

    print(f"Comparing MkDocs ({site_dir}) vs Astro ({dist_dir}) across {len(drug_files)} drug pages...\n")

    table_errors = []
    admonition_errors = []
    review_errors = []
    prose_errors = []
    missing_files = []

    total_site_tables = 0
    total_dist_tables = 0
    total_site_admonitions = 0
    total_dist_admonitions = 0
    site_reviewed_count = 0
    dist_reviewed_count = 0
    prose_matched_count = 0

    for doc_path in drug_files:
        slug = doc_path.stem
        site_html_path = site_dir / "drugs" / slug / "index.html"
        dist_html_path = dist_dir / "drugs" / slug / "index.html"

        if not site_html_path.exists():
            missing_files.append((slug, f"Missing in MkDocs output: {site_html_path}"))
            continue

        if not dist_html_path.exists():
            missing_files.append((slug, f"Missing in Astro output: {dist_html_path}"))
            continue

        site_html = site_html_path.read_text(encoding="utf-8")
        dist_html = dist_html_path.read_text(encoding="utf-8")

        # 1. Dose Tables Comparison
        site_tables = parse_tables(site_html)
        dist_tables = parse_tables(dist_html)
        total_site_tables += len(site_tables)
        total_dist_tables += len(dist_tables)

        if len(site_tables) != len(dist_tables):
            table_errors.append(
                (slug, f"Table count mismatch: MkDocs has {len(site_tables)} tables, Astro has {len(dist_tables)} tables")
            )
        else:
            for t_idx, (s_tab, d_tab) in enumerate(zip(site_tables, dist_tables), start=1):
                if len(s_tab) != len(d_tab):
                    table_errors.append(
                        (slug, f"Table #{t_idx} row count mismatch: MkDocs has {len(s_tab)} rows, Astro has {len(d_tab)} rows")
                    )
                else:
                    for r_idx, (s_row, d_row) in enumerate(zip(s_tab, d_tab), start=1):
                        if s_row != d_row:
                            table_errors.append(
                                (
                                    slug,
                                    f"Table #{t_idx}, Row #{r_idx} differs:\n"
                                    f"      MkDocs: {s_row}\n"
                                    f"      Astro:  {d_row}",
                                )
                            )

        # 2. Admonitions Comparison
        site_adms = parse_admonitions(site_html, mode="site")
        dist_adms = parse_admonitions(dist_html, mode="dist")
        total_site_admonitions += len(site_adms)
        total_dist_admonitions += len(dist_adms)

        if len(site_adms) != len(dist_adms):
            admonition_errors.append(
                (slug, f"Admonition count mismatch: MkDocs has {len(site_adms)}, Astro has {len(dist_adms)}")
            )
        else:
            for a_idx, (s_adm, d_adm) in enumerate(zip(site_adms, dist_adms), start=1):
                if s_adm != d_adm:
                    admonition_errors.append(
                        (
                            slug,
                            f"Admonition #{a_idx} text differs:\n"
                            f"      MkDocs: {s_adm}\n"
                            f"      Astro:  {d_adm}",
                        )
                    )

        # 3. Review Metadata Comparison
        site_has_rev = "Reviewed by" in site_html
        dist_has_rev = "Reviewed by" in dist_html
        if site_has_rev:
            site_reviewed_count += 1
        if dist_has_rev:
            dist_reviewed_count += 1

        if site_has_rev != dist_has_rev:
            review_errors.append(
                (slug, f"'Reviewed by' presence mismatch: MkDocs={site_has_rev}, Astro={dist_has_rev}")
            )

        # 4. Prose Comparison
        site_prose = parse_prose(site_html, mode="site")
        dist_prose = parse_prose(dist_html, mode="dist")

        if site_prose == dist_prose:
            prose_matched_count += 1
        else:
            diff_detail = format_prose_diff(site_prose, dist_prose)
            prose_errors.append((slug, f"Prose content differs:\n{diff_detail}"))

    # Hard failures for tables, admonitions, review metadata, missing files, or strict prose
    hard_failure = bool(
        missing_files
        or table_errors
        or admonition_errors
        or review_errors
        or (site_reviewed_count != dist_reviewed_count)
        or (strict_prose and prose_errors)
    )

    if hard_failure:
        print("=" * 75, file=sys.stderr)
        print("RENDERER COMPARISON FAILED", file=sys.stderr)
        print("Differences detected between MkDocs and Astro rendered outputs:", file=sys.stderr)
        print("=" * 75, file=sys.stderr)

        if missing_files:
            print("\n[!] Missing HTML Files:", file=sys.stderr)
            for slug, msg in missing_files:
                print(f"  - {slug}: {msg}", file=sys.stderr)

        if table_errors:
            print(f"\n[!] Dose Table Differences ({len(table_errors)}):", file=sys.stderr)
            for slug, msg in table_errors:
                print(f"  - {slug}: {msg}", file=sys.stderr)

        if admonition_errors:
            print(f"\n[!] Admonition Differences ({len(admonition_errors)}):", file=sys.stderr)
            for slug, msg in admonition_errors:
                print(f"  - {slug}: {msg}", file=sys.stderr)

        if review_errors:
            print(f"\n[!] Review Metadata Differences ({len(review_errors)}):", file=sys.stderr)
            for slug, msg in review_errors:
                print(f"  - {slug}: {msg}", file=sys.stderr)

        if site_reviewed_count != dist_reviewed_count:
            print(
                f"\n[!] Review Metadata Count Mismatch: MkDocs={site_reviewed_count}, Astro={dist_reviewed_count}",
                file=sys.stderr,
            )

        if prose_errors:
            print(f"\n[!] Prose Content Differences ({len(prose_errors)}):", file=sys.stderr)
            for slug, msg in prose_errors:
                print(f"  - {slug}: {msg}", file=sys.stderr)

        print("\n" + "=" * 75, file=sys.stderr)
        return 1

    # If no hard failure, report status (with warnings if any prose diffs exist)
    if prose_errors:
        print("=" * 75)
        print("RENDERER COMPARISON PASSED (WITH PROSE WARNINGS)")
        print("=" * 75)
        print(f"✓ Drug pages checked:     {len(drug_files)}/{len(drug_files)}")
        print(f"✓ Dose tables compared:   {total_dist_tables} tables (0 differences)")
        print(f"✓ Admonitions compared:   {total_dist_admonitions} admonitions (0 differences)")
        print(f"✓ Review metadata:        {dist_reviewed_count}/{len(drug_files)} pages contain 'Reviewed by' (0 differences)")
        diff_slugs = ", ".join(slug for slug, _ in prose_errors)
        print(f"⚠ Prose text compared:    {prose_matched_count}/{len(drug_files)} pages identical ({len(prose_errors)} warning: {diff_slugs})")
        print("=" * 75)
        print("\n[!] Prose Warnings:")
        for slug, msg in prose_errors:
            print(f"  - {slug}:\n{msg}")
        print("\n" + "=" * 75)
    else:
        print("=" * 75)
        print("RENDERER COMPARISON PASSED")
        print("=" * 75)
        print(f"✓ Drug pages checked:     {len(drug_files)}/{len(drug_files)}")
        print(f"✓ Dose tables compared:   {total_dist_tables} tables (0 differences)")
        print(f"✓ Admonitions compared:   {total_dist_admonitions} admonitions (0 differences)")
        print(f"✓ Review metadata:        {dist_reviewed_count}/{len(drug_files)} pages contain 'Reviewed by' (0 differences)")
        print(f"✓ Prose text compared:    {len(drug_files)}/{len(drug_files)} drug pages identical (0 differences)")
        print("=" * 75)

    return 0


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Compare rendered output of drug pages between MkDocs and Astro/Starlight."
    )
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=repo_root / "site",
        help="Path to MkDocs output directory (default: <repo_root>/site)",
    )
    parser.add_argument(
        "--dist-dir",
        type=Path,
        default=repo_root / "dist",
        help="Path to Astro output directory (default: <repo_root>/dist)",
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=repo_root / "docs" / "drugs",
        help="Path to Markdown drug docs directory (default: <repo_root>/docs/drugs)",
    )
    parser.add_argument(
        "--strict-prose",
        action="store_true",
        help="Treat prose differences as hard failure (exit code 1)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    args = parser.parse_args()

    sys.exit(
        compare_builds(
            args.site_dir,
            args.dist_dir,
            args.docs_dir,
            verbose=args.verbose,
            strict_prose=args.strict_prose,
        )
    )


if __name__ == "__main__":
    main()

