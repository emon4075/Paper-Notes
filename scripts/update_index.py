#!/usr/bin/env python3
"""Rebuild the paper index in README.md from the frontmatter of notes/*.md.

Standard library only -- the frontmatter parser below is deliberately hand-rolled
so the repo has no dependencies. Notes with missing or malformed frontmatter are
reported on stderr and skipped; they never abort the run.

Usage:  python scripts/update_index.py
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "notes"
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- INDEX:START -->"
END_MARKER = "<!-- INDEX:END -->"

REQUIRED_FIELDS = ("title", "date_read")
VALID_DEPTHS = ("deep", "skim")
RECENT_DAYS = 30
MISSING = "—"
UNFILED = "unfiled"


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)


def _clean(value: str) -> str:
    """Strip whitespace, surrounding quotes, and trailing ` # comment` from a value."""
    value = value.strip()
    if value[:1] in ('"', "'"):
        quote_char = value[0]
        closing = value.find(quote_char, 1)
        if closing != -1:
            return value[1:closing]
        return value[1:].strip()
    comment = value.find(" #")
    if comment != -1:
        value = value[:comment]
    return value.strip()


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    """Return (fields, None) on success or (None, reason) if the block is unusable."""
    lines = text.splitlines()
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1

    if index >= len(lines) or lines[index].strip() != "---":
        return None, "no YAML frontmatter (file must start with '---')"

    fields: dict[str, str] = {}
    last_key: str | None = None
    closed = False

    for line in lines[index + 1:]:
        stripped = line.strip()
        if stripped == "---":
            closed = True
            break
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            # Block list item: fold it into the key it belongs to, so
            # `authors:` works written either as a list or as one line.
            if last_key:
                item = _clean(stripped[2:])
                existing = fields[last_key]
                fields[last_key] = f"{existing}, {item}" if existing else item
            continue

        key, separator, value = stripped.partition(":")
        key = key.strip()
        if not separator or not key:
            continue
        fields[key] = _clean(value)
        last_key = key

    if not closed:
        return None, "frontmatter block is not closed (missing second '---')"
    if not fields:
        return None, "frontmatter block has no 'key: value' fields"
    return fields, None


def load_notes() -> list[dict[str, object]]:
    """Read every note, skipping (with a warning) any the index can't render."""
    if not NOTES_DIR.is_dir():
        warn(f"no notes directory at {NOTES_DIR}")
        return []

    notes: list[dict[str, object]] = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as exc:
            warn(f"{path.name}: could not read file ({exc})")
            continue

        fields, reason = parse_frontmatter(text)
        if fields is None:
            warn(f"{path.name}: {reason} -- skipped")
            continue

        empty = [name for name in REQUIRED_FIELDS if not fields.get(name)]
        if empty:
            warn(f"{path.name}: missing {', '.join(empty)} -- skipped")
            continue

        try:
            date_read = date.fromisoformat(fields["date_read"])
        except ValueError:
            warn(
                f"{path.name}: date_read {fields['date_read']!r} is not YYYY-MM-DD -- skipped"
            )
            continue

        depth = fields.get("depth", "")
        if depth and depth not in VALID_DEPTHS:
            warn(f"{path.name}: depth {depth!r} is not one of {'/'.join(VALID_DEPTHS)}")

        notes.append(
            {
                "path": path,
                "title": fields["title"],
                "date_read": date_read,
                "venue": fields.get("venue", ""),
                "year": fields.get("year", ""),
                "area": fields.get("area", ""),
                "depth": depth,
            }
        )

    # Stable sort: newest first, ties broken alphabetically by title.
    notes.sort(key=lambda note: str(note["title"]).lower())
    notes.sort(key=lambda note: note["date_read"], reverse=True)  # type: ignore[return-value,arg-type]
    return notes


def cell(value: str) -> str:
    """Make a value safe to drop into a markdown table cell."""
    text = " ".join(str(value).split()).replace("|", "\\|")
    return text or MISSING


def venue_year(note: dict[str, object]) -> str:
    venue = str(note["venue"]).strip()
    year = str(note["year"]).strip()
    if venue and year:
        return f"{venue} {year}"
    return venue or year


def render_table(notes: list[dict[str, object]]) -> str:
    rows = [
        "| Date Read | Paper | Venue/Year | Area | Depth |",
        "| --- | --- | --- | --- | --- |",
    ]
    for note in notes:
        path: Path = note["path"]  # type: ignore[assignment]
        link = f"[{cell(str(note['title']))}](notes/{quote(path.name)})"
        rows.append(
            "| {date} | {paper} | {venue} | {area} | {depth} |".format(
                date=note["date_read"],
                paper=link,
                venue=cell(venue_year(note)),
                area=cell(str(note["area"])),
                depth=cell(str(note["depth"])),
            )
        )
    return "\n".join(rows)


def summarize(notes: list[dict[str, object]]) -> str:
    if not notes:
        return "No papers indexed yet."

    total = len(notes)
    counts = Counter(str(note["area"]).strip() or UNFILED for note in notes)
    by_size = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    areas = ", ".join(f"{area} ({count})" for area, count in by_size)

    cutoff = date.today() - timedelta(days=RECENT_DAYS)
    recent = sum(1 for note in notes if note["date_read"] >= cutoff)  # type: ignore[operator]

    return (
        f"{total} {'paper' if total == 1 else 'papers'} · {areas} · "
        f"{recent} read in the last {RECENT_DAYS} days"
    )


def rewrite_readme(block: str) -> bool | None:
    """Replace the marked region of README.md. Returns True if the file changed."""
    if not README.is_file():
        fail(f"no README.md at {README}")
        return None

    text = README.read_text(encoding="utf-8-sig")
    start = text.find(START_MARKER)
    end = text.find(END_MARKER)
    if start == -1 or end == -1:
        fail(f"README.md is missing the {START_MARKER} / {END_MARKER} markers")
        return None
    if end < start:
        fail(f"README.md has {END_MARKER} before {START_MARKER}")
        return None

    updated = f"{text[:start + len(START_MARKER)]}\n\n{block}\n\n{text[end:]}"
    if updated == text:
        return False

    README.write_text(updated, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    notes = load_notes()
    summary = summarize(notes)

    block = f"_{summary}_" if not notes else f"_{summary}_\n\n{render_table(notes)}"
    changed = rewrite_readme(block)
    if changed is None:
        return 1

    print(summary)
    print(f"{'Updated' if changed else 'No change to'} {README.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
