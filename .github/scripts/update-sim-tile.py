#!/usr/bin/env python3
"""
update-sim-tile.py — Update the SIM-REPORT block in studio-audits/README.md.

Usage:
    python3 update-sim-tile.py --report sim-reports/battlebrotts-v2/2026-04-27.md
                               --project battlebrotts-v2

Inserts or replaces the <!-- SIM-REPORT:BEGIN -->...<!-- SIM-REPORT:END --> block.
Idempotent.
"""

import argparse
import re
import sys
from pathlib import Path

BEGIN_MARKER = "<!-- SIM-REPORT:BEGIN -->"
END_MARKER = "<!-- SIM-REPORT:END -->"


def extract_summary(report_path: Path, project: str) -> str:
    """Extract runs count and flag count from a sim report Markdown file."""
    try:
        text = report_path.read_text()
    except OSError:
        return f"- [{report_path.name}]({report_path}) — could not read report"

    date = report_path.stem  # YYYY-MM-DD

    # Extract runs collected
    runs = "?"
    m = re.search(r"\*\*Runs collected:\*\* (\d+)", text)
    if m:
        runs = m.group(1)

    # Count ⚠️ flags in balance section
    flag_count = 0
    if "## ⚠️ Balance flags" in text:
        flags_section = text.split("## ⚠️ Balance flags")[1].split("## Failures")[0]
        flag_count = flags_section.count("**") // 2  # each flag has one **name** pair

    flag_str = f"⚠️ {flag_count} balance flag{'s' if flag_count != 1 else ''}" if flag_count > 0 else "✅ no flags"

    return f"- **[{date}](sim-reports/{project}/{date}.md)** · {runs} runs · {flag_str}"


def update_readme(readme_path: Path, block_content: str) -> bool:
    """Replace or insert the SIM-REPORT block. Returns True if changed."""
    text = readme_path.read_text()
    new_block = f"{BEGIN_MARKER}\n{block_content}\n{END_MARKER}"

    if BEGIN_MARKER in text and END_MARKER in text:
        new_text = re.sub(
            re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER),
            new_block,
            text,
            flags=re.DOTALL,
        )
    else:
        new_text = text.rstrip() + "\n\n" + new_block + "\n"

    if new_text == text:
        return False
    readme_path.write_text(new_text)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    readme_path = Path("README.md")
    if not readme_path.exists():
        print("README.md not found", file=sys.stderr)
        sys.exit(1)

    summary_line = extract_summary(args.report, args.project)
    block_content = f"""## 🎮 Latest Sim Reports

### `{args.project}`
{summary_line}

_Auto-updated by `{args.project}/.github/workflows/sim.yml`_"""

    changed = update_readme(readme_path, block_content)
    if changed:
        print(f"README.md updated with sim report for {args.project}")
    else:
        print("README.md unchanged (already up to date)")


if __name__ == "__main__":
    main()
