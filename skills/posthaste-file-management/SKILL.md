---
name: posthaste-file-management
description: >
  Manage PostHaste project templates and file structures. Use this skill whenever
  the user mentions PostHaste, wants to create a new project folder, browse or
  apply a PostHaste template, list existing PostHaste projects, design a new
  template, or organize project assets. Also trigger when user says things like
  "set up a project", "create project folders", "apply my template", "list my
  templates", "new PostHaste project", "where are my projects", or "organize my
  files with PostHaste". This skill reads directly from PostHaste's local template
  storage and can create folder structures on disk — no need for PostHaste to be
  running.
---

# PostHaste File Management Skill

PostHaste (by Digital Rebellion) is a local desktop app that creates project folder
structures from customizable templates. It has no API — this skill works directly
with PostHaste's files on disk.

---

## Key Locations

### Mac
- **Templates dir**: `~/Library/Application Support/Digital Rebellion/Post Haste/Templates/`
- **Prefs/config**: `~/Library/Preferences/com.digitalrebellion.PostHaste.plist`
- **Default project root**: Ask user or detect from their prefs

### Windows
- **Templates dir**: `%APPDATA%\Digital Rebellion\Post Haste\Templates\`
- **Prefs**: Registry or `%APPDATA%\Digital Rebellion\Post Haste\`

> **First step**: Always detect the OS and check whether the templates directory
> exists before proceeding. If it doesn't exist, tell the user and ask them to
> confirm their PostHaste install location.

---

## Template File Format

PostHaste templates are stored as **XML `.phtemplate` files** (or as directory
bundles containing an `info.plist` and file stubs on older versions).

Typical structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<template>
  <name>Feature Film</name>
  <items>
    <item type="folder" name="[project]">
      <item type="folder" name="01_Footage">
        <item type="folder" name="[date]_Shoot_01"/>
      </item>
      <item type="folder" name="02_Audio"/>
      <item type="folder" name="03_Graphics"/>
      <item type="folder" name="04_Exports"/>
      <item type="file" name="[project].prproj" src="blank_premiere.prproj"/>
    </item>
  </items>
</template>
```

Variables use `[square_bracket]` syntax:
- `[project]` — project name
- `[client]` — client name
- `[date]` — current date (formatted per prefs)
- `[user]` — logged-in username
- `[template]` — auto-renamed to full project name
- Any custom parameter name in square brackets

---

## Core Tasks

### 1. List Templates

```python
import os, glob, xml.etree.ElementTree as ET

templates_dir = os.path.expanduser(
    "~/Library/Application Support/Digital Rebellion/Post Haste/Templates/"
)
templates = glob.glob(os.path.join(templates_dir, "*.phtemplate"))
for t in templates:
    tree = ET.parse(t)
    root = tree.getroot()
    name = root.findtext("name") or os.path.basename(t)
    print(f"  • {name}  ({os.path.basename(t)})")
```

### 2. Read & Display a Template

Parse the XML and render its folder tree. Use `scripts/read_template.py` for this.

Show the user:
- Template name
- Folder hierarchy with indentation
- Which items use variables (highlight `[...]`)
- Any bundled file stubs

### 3. Create a Project from a Template

Steps:
1. Ask user: which template? (show list)
2. Ask for each required parameter (project name, client, date override, etc.)
3. Resolve all `[variable]` names in folder/file names
4. Create the folder tree at the chosen destination
5. Copy any bundled file stubs into place
6. Open the resulting folder in Finder/Explorer

Use `scripts/create_project.py` for the actual creation logic.

### 4. Design / Edit a Template

When a user wants to create or modify a template:
1. Collect the folder structure they want (ask conversationally)
2. Identify which parts should be variable (project name, date, client, etc.)
3. Generate the XML
4. Write it to the templates directory
5. Confirm PostHaste will see it immediately (no restart needed)

### 5. List Recent Projects

PostHaste tracks recent projects in its prefs plist. Read:
```python
import plistlib
prefs_path = os.path.expanduser(
    "~/Library/Preferences/com.digitalrebellion.PostHaste.plist"
)
with open(prefs_path, "rb") as f:
    prefs = plistlib.load(f)
recent = prefs.get("recentProjects", [])
```

---

## Variable Resolution Rules

When creating a project, resolve variables in this order:
1. Replace `[project]` with the project name parameter
2. Replace `[client]` with client name (if provided, else skip the item if it's
   the entire filename)
3. Replace `[date]` with today's date in the user's preferred format (default: YYYY-MM-DD)
4. Replace `[user]` with `os.getlogin()`
5. Replace any other `[param]` with the value provided
6. If a parameter is blank AND it makes up the **entire** filename, skip creating
   that file/folder entirely
7. Any file/folder named literally `[template]` → rename to the full project name

---

## Separator & Naming

PostHaste uses a configurable separator between parameters (default `_`). When
building a project folder name from multiple params, join with `_` unless the
user's prefs say otherwise.

Example: Project=`Wildlife`, Client=`NatGeo`, Date=`2026-04-02`
→ `NatGeo_Wildlife_2026-04-02`

---

## Reference Files

- `references/template-format.md` — Detailed XML schema for `.phtemplate` files
- `references/variables.md` — Full variable list and edge cases
- `scripts/read_template.py` — Parse and display a template
- `scripts/create_project.py` — Create folder structure from template + params
- `scripts/list_projects.py` — Read recent projects from prefs
- `scripts/new_template.py` — Generate a new `.phtemplate` XML file

---

## Error Handling

| Situation | Response |
|---|---|
| Templates dir not found | Ask user to confirm PostHaste install path |
| Template XML malformed | Show raw file, ask user how to fix it |
| Project folder already exists | Warn user, ask if they want to overwrite |
| Missing required parameter | Prompt the user before creating |
| No PostHaste templates at all | Offer to create a starter template from scratch |

---

## Conversation Style

Keep it practical and short. When listing templates or parameters, use clean
lists. When creating a project, confirm the full folder name + destination before
creating. After creation, confirm success and show the top-level folder path.
