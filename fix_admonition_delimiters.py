#!/usr/bin/env python3
"""
fix_admonition_delimiters — Wrap shorthand AsciiDoc admonitions in ==== delimiters.

Finds the single-paragraph admonition shorthand:

    [TIP]
    Some content.

and rewrites it as the explicit delimited form:

    [TIP]
    ====
    Some content.
    ====

Supported admonition labels: NOTE, TIP, IMPORTANT, WARNING, CAUTION.

What is ignored:

- Admonitions already delimited with ``====``, including ones that carry
  a block anchor (``[[id]]``) and/or a block title (``.Title``) between
  the type line and the ``====`` opener.
- The inline paragraph-prefix form (``TIP: message on one line``).
- Content inside listing (``----``), literal (``....``), passthrough (``++++``),
  or comment (``////``) delimited blocks.
- A ``[TIP]`` line followed immediately by a blank line, a heading, another
  block attribute line (``[source,java]``), or any structural delimiter —
  the block is malformed or non-standard; leave it untouched.

What is normalized:

- Open-block-delimited admonitions (``[NOTE]`` followed by ``--`` ... ``--``)
  have their ``--`` delimiters replaced with ``====`` so the doc tree uses
  one consistent admonition delimiter.
- A block title (``.Title``) and/or anchor (``[[id]]``) carried between the
  ``[TIP]`` line and the wrapped paragraph is kept *above* the new ``====``
  opener — placing it inside ``====`` would change rendering and break the
  block.

USAGE

    # Dry-run on a single file (default — no writes)
    python3 fix_admonition_delimiters.py path/to/file.adoc

    # Dry-run over a directory tree
    python3 fix_admonition_delimiters.py path/to/asciidoc/

    # Apply the fix
    python3 fix_admonition_delimiters.py --apply path/to/asciidoc/

    # Scan multiple repos at once
    python3 fix_admonition_delimiters.py --apply \\
        ~/gitlab/quarkus/asciidoc/ \\
        ~/quarkus-mcp-server/docs/modules/ROOT/pages/ \\
        ~/quarkus-langchain4j/docs/modules/ROOT/pages/

Exit code: 0 on success, 1 if any file could not be read or written.
"""

import argparse
import re
import sys
from pathlib import Path

ADMONITIONS = ("NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION")
ADMONITION_LINE = re.compile(r"^\[(" + "|".join(ADMONITIONS) + r")\]\s*$")

# Delimited-block fences. Processing is suppressed inside these.
FENCES = {"----", "....", "++++", "////"}

# Lines that terminate an un-delimited admonition paragraph: blanks,
# headings, other block attribute lines, and any structural block delimiter.
TERMINATOR = re.compile(
    r"^(?:"
    r"\s*$"                                          # blank line
    r"|={1,6}\s+\S"                                  # section heading
    r"|\[[^\]]+\]\s*$"                               # another [attr] line
    r"|----|\.\.\.\.|\+\+\+\+|////|====|\*\*\*\*|____|\|==="
    r")"
)


def fix_text(text: str) -> tuple[str, int]:
    """Return (new_text, block_count) with shorthand admonitions delimited."""
    lines = text.splitlines(keepends=False)
    out: list[str] = []
    i = 0
    n = len(lines)
    changed = 0
    fence: str | None = None

    while i < n:
        line = lines[i]
        stripped = line.rstrip()

        # Track fenced blocks: copy through, skip all admonition logic inside.
        if fence is None:
            if stripped in FENCES:
                fence = stripped
                out.append(line)
                i += 1
                continue
        else:
            out.append(line)
            if stripped == fence:
                fence = None
            i += 1
            continue

        # Outside any fence — look for shorthand admonition.
        if not ADMONITION_LINE.match(line):
            out.append(line)
            i += 1
            continue

        # Found "[TYPE]" on its own line. Peek ahead.
        out.append(line)
        j = i + 1

        # An AsciiDoc block can carry a block anchor ("[[id]]"), a block
        # title (".Title"), and/or additional attribute lines ("[...]")
        # between the admonition type and the opening delimiter. Collect
        # them before deciding whether the block is already delimited.
        meta_start = j
        while j < n and (
            (lines[j].startswith(".") and not lines[j].startswith(".."))
            or re.match(r"^\[\[[^\]]+\]\]\s*$", lines[j])
            or re.match(r"^\[[^\]]+\]\s*$", lines[j])
        ):
            j += 1

        # Already delimited with ====: emit metadata + ==== and hand off.
        if j < n and lines[j].rstrip() == "====":
            out.extend(lines[meta_start:j + 1])
            i = j + 1
            continue

        # Open-block-delimited admonition ([NOTE] ... -- ... --).
        # Convert the -- delimiters to ==== for consistency. If the body
        # already contains nested example-block delimiters (===={4,+}),
        # bump the wrapper to one more = so Asciidoctor can disambiguate.
        if j < n and lines[j].rstrip() == "--":
            open_idx = j
            close_idx = open_idx + 1
            while close_idx < n and lines[close_idx].rstrip() != "--":
                close_idx += 1
            if close_idx < n:
                body = lines[open_idx + 1:close_idx]
                max_inner = 0
                for body_line in body:
                    m = re.match(r"^(=+)\s*$", body_line)
                    if m and len(m.group(1)) >= 4:
                        max_inner = max(max_inner, len(m.group(1)))
                wrapper = "=" * max(4, max_inner + 1)
                out.extend(lines[meta_start:open_idx])
                out.append(wrapper)
                out.extend(body)
                out.append(wrapper)
                changed += 1
                i = close_idx + 1
                continue
            # Unterminated open block → fall through to safe path below.

        # Nothing usable after the metadata → leave the shorthand alone
        # (but keep any metadata lines we consumed).
        if j >= n or TERMINATOR.match(lines[j]):
            out.extend(lines[meta_start:j])
            i = j
            continue

        # Bare shorthand with no delimiter: keep metadata above the new
        # ==== opener (placing it inside ==== would change rendering),
        # then wrap the paragraph.
        start = j
        while j < n and not TERMINATOR.match(lines[j]):
            j += 1
        out.extend(lines[meta_start:start])   # title/anchor/attrs
        out.append("====")
        out.extend(lines[start:j])            # paragraph content
        out.append("====")
        changed += 1
        i = j

    new_text = "\n".join(out)
    # Preserve the exact trailing-newline run from the original file.
    orig_tail = len(text) - len(text.rstrip("\n"))
    new_tail = len(new_text) - len(new_text.rstrip("\n"))
    if new_tail < orig_tail:
        new_text += "\n" * (orig_tail - new_tail)
    elif new_tail > orig_tail:
        new_text = new_text.rstrip("\n") + "\n" * orig_tail
    return new_text, changed


def iter_adoc_files(paths):
    for p in paths:
        path = Path(p).expanduser()
        if path.is_file():
            if path.suffix == ".adoc":
                yield path
        elif path.is_dir():
            yield from sorted(path.rglob("*.adoc"))
        else:
            print(f"skip: {p} (not a file or directory)", file=sys.stderr)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Wrap shorthand AsciiDoc admonitions in ==== delimiters.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help=".adoc files or directories to scan",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write fixes in place (default is dry-run)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="suppress per-file output",
    )
    args = parser.parse_args(argv)

    total_blocks = 0
    total_files = 0
    errors = 0

    for path in iter_adoc_files(args.paths):
        try:
            original = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"error reading {path}: {e}", file=sys.stderr)
            errors += 1
            continue
        new_text, changed = fix_text(original)
        if not changed:
            continue
        total_blocks += changed
        total_files += 1
        if args.apply:
            try:
                path.write_text(new_text, encoding="utf-8")
            except OSError as e:
                print(f"error writing {path}: {e}", file=sys.stderr)
                errors += 1
                continue
            verb = "fixed"
        else:
            verb = "would fix"
        if not args.quiet:
            print(f"{verb} {changed} block(s): {path}")

    verb = "Fixed" if args.apply else "Would fix"
    print(f"{verb} {total_blocks} admonition block(s) across {total_files} file(s).")
    if not args.apply and total_blocks:
        print("Rerun with --apply to write changes.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
