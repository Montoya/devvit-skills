# Devvit Skills for Codex

Five reusable skills for building and reviewing Devvit Web apps:

- **devvit-features** — Reddit identity, permissions, leaderboards, sharing, publication, and lifecycle behavior.
- **devvit-games** — authoritative game state, timers, scoring, replays, score visualizations, sharing, and recovery.
- **devvit-performance** — startup latency, caching, pagination, Redis indexes, bundles, and serverless request paths.
- **devvit-testing** — unit and capability testing, concurrency, real Reddit playtests, and launch verification.
- **devvit-ui** — responsive inline and expanded layouts, fixed viewports, safe areas, touch and canvas interaction.

Each folder under `skills/` is an independent skill with its own `SKILL.md` and supporting references.

## Install

### In one project

Copy or symlink the desired skill folders into the project's `.agents/skills/` directory:

```text
your-project/
└── .agents/
    └── skills/
        ├── devvit-features/
        ├── devvit-games/
        ├── devvit-performance/
        ├── devvit-testing/
        └── devvit-ui/
```

### For your user account

Copy or symlink the desired folders into `$HOME/.agents/skills/` to make them available across repositories.

Codex detects skill changes automatically. Restart Codex if a newly added skill does not appear.

You can also ask the built-in `$skill-installer` to install a skill from this GitHub repository after it has been published.

## Use

Codex can select a skill automatically when a request matches its description. You can also invoke one explicitly, for example:

```text
$devvit-ui review this Devvit app for mobile expanded-view layout issues
```

## Repository layout

```text
.
├── LICENSE
├── README.md
└── skills/
    ├── devvit-features/
    ├── devvit-games/
    ├── devvit-performance/
    ├── devvit-testing/
    └── devvit-ui/
```

## License

MIT
