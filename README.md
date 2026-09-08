# Devvit Skills

Reusable agent skills for building polished, production-ready [Devvit Web](https://developers.reddit.com/) apps.

[![skills.sh](https://skills.sh/b/Montoya/devvit-skills)](https://skills.sh/Montoya/devvit-skills)

These skills capture practical guidance for Reddit-native product behavior, games, performance, testing, and responsive UI. Each skill is self-contained and follows the open [Agent Skills specification](https://agentskills.io/).

## Install

Install from this repository with one command:

```bash
npx skills@latest add Montoya/devvit-skills
```

The installer lets you choose which skills to install and which supported coding agents should receive them. The current CLI requires Node.js 22.20 or newer.

Useful variations:

```bash
# Preview the available skills
npx skills@latest add Montoya/devvit-skills --list

# Install one skill
npx skills@latest add Montoya/devvit-skills --skill devvit-ui

# Install globally for Codex and Claude Code
npx skills@latest add Montoya/devvit-skills --skill '*' --agent codex --agent claude-code --global
```

The `skills` CLI supports Codex, Claude Code, Cursor, GitHub Copilot, and many other coding agents. See the [CLI documentation](https://www.skills.sh/docs/cli) for the complete agent list and installation options.

## Skills

| Skill | Use it for |
| --- | --- |
| [devvit-features](skills/devvit-features/SKILL.md) | Identity, permissions, leaderboards, sharing, user content, publication, subscriptions, and lifecycle behavior. |
| [devvit-games](skills/devvit-games/SKILL.md) | Server-authoritative rounds, timers, scoring, rankings, replays, recovery, and accessible feedback. |
| [devvit-performance](skills/devvit-performance/SKILL.md) | Startup latency, caching, pagination, Redis indexes, bundles, and serverless request paths. |
| [devvit-testing](skills/devvit-testing/SKILL.md) | Unit and capability tests, concurrency, webviews, real Reddit playtests, and launch readiness. |
| [devvit-ui](skills/devvit-ui/SKILL.md) | Responsive inline and expanded layouts, fixed viewports, safe areas, touch, canvas, and accessibility. |

## Use

Installed skills can be selected automatically when a request matches their description. You can also invoke one explicitly:

```text
$devvit-ui review this Devvit app for mobile expanded-view layout issues
```

## ChatGPT and Claude desktop apps

Desktop chat apps use uploaded skill packages rather than the `npx skills` coding-agent install path. Clone or download this repository, then build one ZIP per skill:

```bash
python3 scripts/package_skills.py
```

Upload the desired file from `dist/`:

- In ChatGPT, open **Plugins → Skills → Create → Upload from your computer**. Availability depends on your plan and workspace settings. See [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).
- In Claude, open **Customize → Skills**, choose **Create skill**, then **Upload a skill**. See [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Repository layout

```text
.
├── .github/workflows/validate.yml
├── scripts/
│   ├── package_skills.py
│   └── validate_skills.py
└── skills/
    ├── devvit-features/
    ├── devvit-games/
    ├── devvit-performance/
    ├── devvit-testing/
    └── devvit-ui/
```

Each skill keeps its entry point in `SKILL.md` and loads detailed guidance from `references/` only when needed.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), then run:

```bash
python3 scripts/validate_skills.py
```

## License

[MIT](LICENSE)
