#!/usr/bin/env python3
"""Check durable browser-facing structure without matching page copy."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, {key: value or "" for key, value in attrs}))


def has_tag(parser: StructureParser, tag: str, **attrs: str) -> bool:
    return any(
        item_tag == tag and all(item_attrs.get(key) == value for key, value in attrs.items())
        for item_tag, item_attrs in parser.tags
    )


def check_structure(path: Path) -> list[str]:
    parser = StructureParser()
    parser.feed(path.read_text(encoding="utf-8"))
    failures: list[str] = []
    checks = [
        ("main workflow landmark", has_tag(parser, "main", **{"data-testid": "checkout-flow"})),
        ("order form anchor", has_tag(parser, "form", **{"data-testid": "order-form"})),
        ("submit action", has_tag(parser, "button", **{"data-action": "submit-order", "type": "submit"})),
        ("status region", has_tag(parser, "section", role="status", **{"aria-live": "polite"})),
    ]
    for name, passed in checks:
        if not passed:
            failures.append(name)
    return failures


def self_test() -> None:
    assert check_structure(Path("examples/browser_page.html")) == []
    assert check_structure(Path("examples/browser_page_missing_structure.html"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="examples/browser_page.html")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("self-test passed")
        return 0

    failures = check_structure(Path(args.path))
    if not failures:
        print("PASS browser_structure")
        return 0
    print("FAIL browser_structure: missing " + ", ".join(failures))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
