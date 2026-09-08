# Contributing

Contributions that make these Devvit skills more accurate, focused, and useful are welcome.

## Add or update a skill

Every skill lives in `skills/<skill-name>/` and must contain a `SKILL.md` file.

```text
skills/example-skill/
├── SKILL.md
├── references/  # Optional detailed guidance
├── scripts/     # Optional deterministic helpers
└── assets/      # Optional files used in generated output
```

The `SKILL.md` file must begin with YAML frontmatter containing:

```yaml
---
name: example-skill
description: Explain what the skill does and when an agent should use it.
---
```

Keep the directory name and frontmatter `name` identical. Use lowercase letters, numbers, and hyphens, and keep the description at or below 200 characters for broad client compatibility.

Keep the main file focused on routing and essential constraints. Put substantial topic-specific detail in `references/` and link to it from `SKILL.md`. Add scripts or assets only when the skill actually uses them.

## Validate

Run the same checks used in CI:

```bash
python3 scripts/validate_skills.py
python3 scripts/package_skills.py --output /tmp/devvit-skill-packages
```

The validator checks required frontmatter, naming, description length, and local Markdown links. The packaging command confirms every skill can be turned into a desktop-uploadable ZIP.

## Pull requests

Keep pull requests scoped to one concern. Explain the Devvit behavior being captured or corrected, and identify which claims were verified against installed types, official documentation, automated tests, or a real Reddit playtest.
