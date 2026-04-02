# PostHaste File Management Skill

A [CoWork](https://www.anthropic.com/products/claude) skill that brings [Post Haste](https://www.digitalrebellion.com/posthaste/) project template management into your AI assistant — without needing the app open.

> **Post Haste** by [Digital Rebellion](https://www.digitalrebellion.com/) is a free Mac/Windows desktop app for creating consistent project folder structures from customizable templates. This skill reads and works with Post Haste's files directly on disk.

---

## What It Does

| Capability | Description |
|---|---|
| **List templates** | Read your Post Haste templates dir and display each template's folder tree and variables |
| **Create a project** | Build a full folder structure on disk from a template + your parameters (project name, client, date, etc.) |
| **Design a template** | Describe a folder structure in plain language and generate the `.phtemplate` XML file |
| **List recent projects** | Read Post Haste's preferences to show and navigate recently created projects |

---

## Requirements

- **Post Haste** installed on Mac or Windows: [Download free](https://www.digitalrebellion.com/posthaste/)
- **CoWork** desktop app (Anthropic)
- Python 3.8+ (included with macOS / available on Windows)

---

## Installation

1. Download `posthaste-skill.skill` from [Releases](../../releases)
2. Open CoWork
3. Go to **Settings → Skills → Install from file**
4. Select `posthaste-skill.skill`

That's it — no configuration needed. The skill auto-detects your Post Haste templates directory.

---

## Usage Examples

Once installed, just talk to CoWork naturally:

### List your templates
```
"Show me my Post Haste templates"
"What templates do I have?"
"List my PostHaste templates"
```

### Create a new project
```
"Create a new project from my Video Production template, project name Wildlife Doc, client NatGeo"
"Set up project folders for a new commercial shoot"
"New PostHaste project"
```

### Design a new template
```
"Create a new Post Haste template for podcast episodes"
"I want a template with folders: Raw Audio, Edited, Show Notes, Artwork, Published"
```

### Browse recent projects
```
"Show my recent PostHaste projects"
"Where are my projects?"
"Open project #3 in Finder"
```

---

## File Structure

```
posthaste-skill/
├── SKILL.md                        # Skill definition and instructions
├── references/
│   └── template-format.md          # PostHaste .phtemplate XML schema reference
└── scripts/
    ├── read_template.py            # Parse and display a template
    ├── create_project.py           # Create folder structure from template + params
    ├── new_template.py             # Generate a new .phtemplate XML file
    └── list_projects.py            # List recent projects from prefs plist
```

---

## Post Haste Template Locations

| OS | Templates directory |
|---|---|
| **macOS** | `~/Library/Application Support/Digital Rebellion/Post Haste/Templates/` |
| **Windows** | `%APPDATA%\Digital Rebellion\Post Haste\Templates\` |

The skill reads from (and writes to) this directory automatically. Any template you create through CoWork will appear immediately in the Post Haste app — no restart needed.

---

## Template Variable Reference

Post Haste uses `[square_bracket]` variables in folder and file names:

| Variable | Value |
|---|---|
| `[project]` | Project name |
| `[client]` | Client name |
| `[date]` | Current date (formatted per your Post Haste prefs) |
| `[user]` | Logged-in OS username |
| `[template]` | Auto-replaced with the full project folder name |

Any custom parameter you define in Post Haste preferences can also be used.

---

## Scripts (standalone use)

The scripts can also be run directly from the terminal:

```bash
# List all templates
python3 scripts/read_template.py --list

# Display a specific template's tree
python3 scripts/read_template.py ~/...Templates/VideoProduction.phtemplate

# Create a project (dry run first)
python3 scripts/create_project.py ~/...Templates/VideoProduction.phtemplate \
    ~/Projects project="Wildlife Doc" client="NatGeo" --dry-run

# Create for real
python3 scripts/create_project.py ~/...Templates/VideoProduction.phtemplate \
    ~/Projects project="Wildlife Doc" client="NatGeo"

# List recent projects
python3 scripts/list_projects.py

# Open project #2 in Finder
python3 scripts/list_projects.py --open 2

# Create a new template from a JSON spec
python3 scripts/new_template.py my_spec.json
```

---

## Contributing

Pull requests welcome. If you build templates or improvements, please share them!

1. Fork this repo
2. Create a branch: `git checkout -b my-improvement`
3. Commit your changes: `git commit -m 'Add thing'`
4. Push and open a PR

---

## License

MIT

---

## Links

- [Post Haste by Digital Rebellion](https://www.digitalrebellion.com/posthaste/) — the app this skill works with
- [Post Haste User Manual (PDF)](https://www.digitalrebellion.com/docs/Post%20Haste%20User%20Manual.pdf)
- [CoWork by Anthropic](https://www.anthropic.com/) — the desktop tool that runs this skill
