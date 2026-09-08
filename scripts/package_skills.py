#!/usr/bin/env python3
"""Create one upload-ready ZIP archive per skill."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist",
        help="Directory for generated ZIP files (default: dist/)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validation = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_skills.py")],
        check=False,
    )
    if validation.returncode:
        return validation.returncode

    output_dir = args.output.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    for skill_dir in skill_dirs:
        archive_path = output_dir / f"{skill_dir.name}.zip"
        with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
            for path in sorted(skill_dir.rglob("*")):
                if path.is_file() and path.name != ".DS_Store":
                    archive.write(path, path.relative_to(SKILLS_DIR))
        print(f"Created {archive_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
