#!/usr/bin/env python3
"""Update the README.md status block in-place.

Reads audit files from audits/<project>/*.md, parses grade + date, and
regenerates the `<!-- STATUS:BEGIN -->` ... `<!-- STATUS:END -->` region
with a summary. Idempotent: if only the timestamp changed and nothing
else, strips the timestamp to avoid no-op churn.
"""
from __future__ import annotations

import datetime as dt
import os
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
AUDITS_DIR = ROOT / "audits"
README = ROOT / "README.md"

BEGIN = "<!-- STATUS:BEGIN -->"
END = "<!-- STATUS:END -->"

GRADE_RE = re.compile(r"Grade:\s*\*?\*?\s*([A-F][+\-]?)", re.IGNORECASE)
DATE_RE = re.compile(r"\*?\*?Date:\*?\*?\s*(\d{4}-\d{2}-\d{2})")

# Grade sort order for distribution display.
GRADE_ORDER = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F", "?"]


def parse_audit(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    grade_match = GRADE_RE.search(text)
    date_match = DATE_RE.search(text)
    return {
        "path": path,
        "name": path.name,
        "grade": grade_match.group(1).upper() if grade_match else "?",
        "date": date_match.group(1) if date_match else None,
    }


def sprint_sort_key(name: str) -> tuple:
    """Sort sprint filenames so that e.g. sprint-13.10 > sprint-13.9 > sprint-13.2."""
    nums = re.findall(r"\d+", name)
    return tuple(int(n) for n in nums) if nums else (0,)


def collect_projects() -> dict[str, list[dict]]:
    """Return {project_name: [audit_dict, ...]} sorted newest-first."""
    projects: dict[str, list[dict]] = {}
    if not AUDITS_DIR.is_dir():
        return projects
    for proj_dir in sorted(AUDITS_DIR.iterdir()):
        if not proj_dir.is_dir():
            continue
        audits = [parse_audit(p) for p in proj_dir.glob("*.md")]
        # Sort: by date desc, then by sprint number desc (for multi-audit days).
        audits.sort(
            key=lambda a: (a["date"] or "0000-00-00", sprint_sort_key(a["name"])),
            reverse=True,
        )
        projects[proj_dir.name] = audits
    return projects


def github_link(project: str, filename: str) -> str:
    return f"https://github.com/brott-studio/studio-audits/blob/main/audits/{project}/{filename}"


def days_ago(date_str: str | None, today: dt.date) -> int | None:
    if not date_str:
        return None
    try:
        d = dt.date.fromisoformat(date_str)
    except ValueError:
        return None
    return (today - d).days


def render(projects: dict[str, list[dict]]) -> str:
    today = dt.date.today()
    lines: list[str] = []
    lines.append("## 📊 Status")
    lines.append("")

    total_audits = sum(len(v) for v in projects.values())
    total_projects = len(projects)
    lines.append(
        f"**{total_audits} audits across {total_projects} project"
        f"{'s' if total_projects != 1 else ''}**"
    )
    lines.append("")

    # Per-project section
    for project, audits in projects.items():
        if not audits:
            continue
        lines.append(f"### `{project}` ({len(audits)} audits)")

        # Cadence (last 7 / 30 days)
        d7 = sum(1 for a in audits if (days_ago(a["date"], today) or 10**6) <= 7)
        d30 = sum(1 for a in audits if (days_ago(a["date"], today) or 10**6) <= 30)
        lines.append(f"**Cadence:** {d7} in last 7d · {d30} in last 30d")
        lines.append("")

        # Grade distribution (last 10)
        recent = audits[:10]
        counts = Counter(a["grade"] for a in recent)
        dist_parts = []
        for g in GRADE_ORDER:
            if counts.get(g):
                dist_parts.append(f"{g}×{counts[g]}")
        if dist_parts:
            lines.append(f"**Recent grades (last {len(recent)}):** {' · '.join(dist_parts)}")
            lines.append("")

        # Latest 5 audits
        lines.append("**Latest audits:**")
        for a in audits[:5]:
            label = a["name"].replace(".md", "")
            date = a["date"] or "—"
            link = github_link(project, a["name"])
            lines.append(f"- [{label}]({link}) · {a['grade']} · {date}")
        lines.append("")

    lines.append(
        f"_Last updated: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        f" · [update workflow](../../actions/workflows/readme-status.yml)_"
    )
    return "\n".join(lines)


def strip_timestamp(block: str) -> str:
    """Remove the '_Last updated: ...' line so idempotence checks ignore it."""
    return re.sub(r"_Last updated:.*", "", block)


def splice(readme_text: str, new_block: str) -> str:
    if BEGIN not in readme_text or END not in readme_text:
        # First-time install: append block before any trailing content.
        return f"{readme_text.rstrip()}\n\n{BEGIN}\n{new_block}\n{END}\n"
    pattern = re.compile(
        re.escape(BEGIN) + r".*?" + re.escape(END),
        re.DOTALL,
    )
    return pattern.sub(f"{BEGIN}\n{new_block}\n{END}", readme_text)


def main() -> int:
    projects = collect_projects()
    new_block = render(projects)
    current = README.read_text(encoding="utf-8")
    updated = splice(current, new_block)

    # Idempotence: if only the timestamp differs, keep the original.
    def extract_block(text: str) -> str:
        m = re.search(re.escape(BEGIN) + r"(.*?)" + re.escape(END), text, re.DOTALL)
        return m.group(1) if m else ""

    if strip_timestamp(extract_block(current)) == strip_timestamp(extract_block(updated)):
        print("No semantic change — leaving README.md unchanged.")
        return 0

    README.write_text(updated, encoding="utf-8")
    print("README.md updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
