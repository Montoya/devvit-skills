#!/usr/bin/env python3
"""Validate the portable structure of every skill in this repository."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None

    value = match.group(1).strip()
    if value[:1] in {"'", '"'}:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return None
        return parsed if isinstance(parsed, str) else None
    return value


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    relative_skill = skill_file.relative_to(ROOT)

    if not skill_file.is_file():
        return [f"{skill_dir.relative_to(ROOT)}: missing SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.DOTALL)
    if not match:
        return [f"{relative_skill}: missing valid YAML frontmatter"]

    frontmatter = match.group(1)
    name = frontmatter_value(frontmatter, "name")
    description = frontmatter_value(frontmatter, "description")

    if not name:
        errors.append(f"{relative_skill}: missing name")
    elif not NAME_PATTERN.fullmatch(name):
        errors.append(f"{relative_skill}: name must use lowercase letters, numbers, and hyphens")
    elif name != skill_dir.name:
        errors.append(f"{relative_skill}: name '{name}' must match directory '{skill_dir.name}'")

    if not description:
        errors.append(f"{relative_skill}: missing description")
    elif len(description) > 200:
        errors.append(f"{relative_skill}: description is {len(description)} characters; maximum is 200")

    for target in LINK_PATTERN.findall(text):
        target = target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "#")):
            continue
        if not (skill_file.parent / target).resolve().is_file():
            errors.append(f"{relative_skill}: broken local link '{target}'")

    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print("skills/: directory not found", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        print("skills/: no skill directories found", file=sys.stderr)
        return 1

    errors = [error for skill_dir in skill_dirs for error in validate_skill(skill_dir)]
    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
