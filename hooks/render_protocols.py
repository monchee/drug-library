"""
MkDocs hook to render clinical protocol tables from YAML frontmatter.
Replaces HTML-comment markers with tables generated from the frontmatter:
  <!-- scratch:overview -->        -> Overview table (presentation, diluent)
  <!-- scratch:spt -->             -> SPT table
  <!-- scratch:idt -->             -> IDT dilution-series table
  <!-- scratch:challenge -->       -> Challenge protocol table
  <!-- scratch:review-banner -->   -> Warning admonition when under_review is true

Precedence Rules:
1. Challenge Intervals: Per-step `interval` takes precedence over challenge-level `interval`
   (the challenge-level `interval` serves as the default for steps that omit an interval).
2. SPT Controls: Per-protocol `spt.positive_control` and `spt.negative_control` take precedence
   over directory-level defaults defined in `docs/drugs/.meta.yml` (applied via MkDocs meta plugin).
"""
import re
from typing import Any, Dict, List, Optional


def render_review_banner(protocols: List[Dict[str, Any]]) -> str:
    """Render warning admonition if any protocol is under review."""
    under_review_protocols = [p for p in protocols if p.get("under_review")]
    if not under_review_protocols:
        return ""

    notes = [p.get("review_note") for p in under_review_protocols if p.get("review_note")]
    note_text = " ".join(notes).strip() if notes else "This protocol is currently under clinical review."

    return (
        '!!! warning "Protocol under clinical review"\n'
        f"    {note_text}\n\n"
        "    See [Protocols for Review](../reference/protocols-for-review.md) for details.\n\n"
    )


def render_overview_table(protocol: Dict[str, Any]) -> str:
    """Render presentation/diluent overview table if present."""
    rows = []
    if protocol.get("presentation"):
        rows.append(f"| Presentation | {protocol['presentation']} |")
    if protocol.get("diluent"):
        rows.append(f"| Diluent | {protocol['diluent']} |")

    if not rows:
        return ""

    return "| Field | Detail |\n|---|---|\n" + "\n".join(rows) + "\n"


def render_spt_table(protocol: Dict[str, Any], page_meta: Optional[Dict[str, Any]] = None) -> str:
    """
    Render SPT table matching SCRATCH drug page conventions.

    Controls precedence:
    1. Per-protocol override in frontmatter: protocol.spt.positive_control / negative_control
    2. Directory/page defaults from docs/drugs/.meta.yml (applied to page.meta)
    """
    spt = protocol.get("spt")
    if not spt:
        return ""

    dilution = str(spt.get("dilution", "") or "").strip()
    concentration = str(spt.get("concentration", "") or "").strip()

    if dilution and concentration:
        if concentration in dilution:
            test_solution = dilution
        else:
            test_solution = f"{dilution} ({concentration})"
    elif concentration:
        test_solution = concentration
    elif dilution:
        test_solution = dilution
    else:
        return ""

    page_meta = page_meta or {}
    meta_spt = page_meta.get("spt") if isinstance(page_meta.get("spt"), dict) else {}

    pos_control = (
        spt.get("positive_control")
        or meta_spt.get("positive_control")
        or page_meta.get("positive_control")
        or ""
    )
    neg_control = (
        spt.get("negative_control")
        or meta_spt.get("negative_control")
        or page_meta.get("negative_control")
        or ""
    )

    rows = [
        "| Reagent | Concentration |",
        "|---|---|",
        f"| Test solution | {test_solution} |",
    ]
    if pos_control:
        rows.append(f"| Positive control | {pos_control} |")
    if neg_control:
        rows.append(f"| Negative control | {neg_control} |")

    return "\n".join(rows) + "\n"


def render_idt_table(protocol: Dict[str, Any]) -> str:
    """Render IDT dilution series table."""
    idt = protocol.get("idt")
    if not idt:
        return ""

    lines = [
        "| Step | Dilution | Concentration | Preparation |",
        "|---|---|---|---|",
    ]
    for idx, step in enumerate(idt, start=1):
        dilution = str(step.get("dilution", "") or "")
        concentration = str(step.get("concentration", "") or "")
        prep = str(step.get("preparation", "") or "")
        lines.append(f"| {idx} | {dilution} | {concentration} | {prep} |")

    return "\n".join(lines) + "\n"


def render_challenge_table(protocol: Dict[str, Any]) -> str:
    """
    Render Challenge graded dose protocol table.

    Interval precedence:
    1. Per-step interval: step.interval
    2. Challenge-level default: challenge.interval
    """
    challenge = protocol.get("challenge")
    if not challenge:
        return ""

    steps = challenge.get("steps", [])
    if not steps:
        return ""

    default_interval = challenge.get("interval", "") or ""

    has_volume = any(s.get("volume") for s in steps)
    has_cumulative = any(s.get("cumulative") for s in steps)
    has_interval = any(s.get("interval") or default_interval for s in steps)

    if has_volume and has_cumulative and has_interval:
        headers = ["Step", "Dose", "Volume", "Interval", "Cumulative Dose"]
    elif has_volume and has_cumulative:
        headers = ["Step", "Dose", "Volume", "Cumulative Dose"]
    elif has_volume and has_interval:
        headers = ["Step", "Dose", "Volume", "Interval"]
    elif has_interval:
        headers = ["Step", "Dose", "Interval"]
    elif has_cumulative:
        headers = ["Step", "Dose", "Cumulative Dose"]
    else:
        headers = ["Step", "Dose"]

    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    lines = [header_line, sep_line]

    for idx, step in enumerate(steps, start=1):
        row = [str(idx), str(step.get("dose", ""))]
        if "Volume" in headers:
            row.append(str(step.get("volume", "") or ""))
        if "Interval" in headers:
            row.append(str(step.get("interval") or default_interval or ""))
        if "Cumulative Dose" in headers:
            row.append(str(step.get("cumulative", "") or ""))
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines) + "\n"


def on_page_markdown(markdown: str, page: Any, config: Any, files: Any) -> str:
    """MkDocs hook event for page markdown processing."""
    # Fast path: if no scratch markers in markdown, return markdown untouched
    if "<!-- scratch:" not in markdown:
        return markdown

    meta = getattr(page, "meta", {}) or {}
    protocols = meta.get("protocols") or []

    def get_protocol(proto_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if not protocols:
            return None
        if proto_id:
            for p in protocols:
                if isinstance(p, dict) and p.get("id") == proto_id:
                    return p
            return None
        return protocols[0] if isinstance(protocols[0], dict) else None

    def replace_marker(match: re.Match) -> str:
        marker = match.group(1).strip()
        proto_id = match.group(2) if match.group(2) else None

        if marker == "review-banner":
            return render_review_banner(protocols)

        proto = get_protocol(proto_id)
        if not proto:
            return ""

        if marker == "overview":
            return render_overview_table(proto)
        elif marker == "spt":
            return render_spt_table(proto, meta)
        elif marker == "idt":
            return render_idt_table(proto)
        elif marker == "challenge":
            return render_challenge_table(proto)

        return ""

    pattern = re.compile(r"<!--\s*scratch:([a-z-]+)(?::([a-z0-9_-]+))?\s*-->")
    return pattern.sub(replace_marker, markdown)

